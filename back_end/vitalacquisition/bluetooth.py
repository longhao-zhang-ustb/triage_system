import asyncio
from typing import List, Optional, Dict, Tuple
from dataclasses import dataclass
from bleak import BleakClient, BleakScanner
from vitalacquisition.RespCalc import RespRateCalculator
from vitalacquisition.HrCalc import ECGHeartRateCalculator
from collections import defaultdict
import time

ECG_MAC = "F7:AA:3F:04:9A:BE"  # 心电仪2887
BP_MAC = "FD:62:58:05:83:32" # 血压计2887
BP_FALLBACK_MODE = "force" # force就是电脑直连血压计，否则由心电仪转发血压数据（如果心电仪支持的话，不支持就只能force）
# 调试开关
DEBUG_GATT_DUMP = False
DEBUG_GENERAL_SUB = False
DEBUG_RAW_TEMP = True
DEBUG_BP_PAYLOAD = False

# // 心电仪协议
FT_REGISTER_REQ = 0x01
FT_REGISTER_RSP = 0x02
FT_GENERAL = 0x03
FT_SET_RTC = 0x09
FT_STATUS_SWITCH = 0x0B
FT_PERIPHERAL_CTRL = 0x0D
FT_PAIRING_ENABLE = 0x10
FT_BP_MEASURE_CMD = 0x21
FT_BP_RESULT = 0x22
BP_MEASURE_INTERVAL = 5 * 60 # 血压不直连时的自动启动间隔
STATUS_KEEPALIVE_INTERVAL = 60 # 设备状态查询间隔

@dataclass
class DeviceParams:
    # heart_rate_a：来自ECG通用包里“和血氧一起的那个”（doc byte176）
    heart_rate_a: str = "0"
    # 脉搏：来自血压计（FDFDFC/2A35/2A37里的HR/PUL）
    pulse_a: str = "0"
    sbp_a: str = "0"
    dbp_a: str = "0"
    hr_a: str = "0"
    temp_a: str = "0"
    os_a: str = "0"

@dataclass
class ECGState:
    device_id: Optional[List[int]] = None
    notify_uuid: Optional[str] = None
    write_uuid: Optional[str] = None
    write_with_response: bool = False
    ecg_lead_off: bool = False
    spo2_probe_off: bool = False
    thermo_disconnected_alarm: bool = True
    spo2_disconnected_alarm: bool = True
    bp_disconnected_alarm: bool = True
    flow_disconnected_alarm: bool = True
    last_bp_trigger_ts: float = 0.0
    last_bp_result_ts: float = 0.0
    last_sub2_ts: float = 0.0

def has_prop(char, prop: str) -> bool:
    props = getattr(char, "properties", None)
    if props is None:
        return False
    if isinstance(props, (list, tuple, set)):
        return prop in props
    return bool(getattr(props, prop, False))

def try_extract_one_frame(buffer: bytearray) -> Optional[bytes]:
    while True:
        if len(buffer) < 4:
            return None
        if buffer[0] == 0x55 and buffer[1] == 0xAA:
            break
        buffer.pop(0)

    length = (buffer[2] << 8) | buffer[3]
    total = 2 + length
    if len(buffer) < total:
        return None
    frame = bytes(buffer[:total])
    del buffer[:total]
    return frame

def checksum_sum(data: bytes) -> int:
    return sum(data) & 0xFF

def verify_frame(frame: bytes) -> bool:
    if len(frame) < 2 + 2 + 4 + 1 + 1:
        return False
    if not (frame[0] == 0x55 and frame[1] == 0xAA):
        return False
    length = (frame[2] << 8) | frame[3]
    if len(frame) != 2 + length:
        return False
    return frame[-1] == checksum_sum(frame[:-1])

def extract_device_id(frame: bytes) -> List[int]:
    return [frame[4], frame[5], frame[6], frame[7]]

def build_packet(device_id4: List[int], frame_type: int, payload: bytes) -> bytes:
    length = 8 + len(payload)
    pkt = bytearray()
    pkt += b"\x55\xAA"
    pkt += length.to_bytes(2, "big")
    pkt += bytes(device_id4)
    pkt += bytes([frame_type])
    pkt += payload
    pkt += bytes([checksum_sum(pkt)])
    return bytes(pkt)

def cmd_register_rsp(device_id4: List[int]) -> bytes:
    payload = bytes([0xFF]) + int(time.time()).to_bytes(4, "big")
    return build_packet(device_id4, FT_REGISTER_RSP, payload)

def _doc_byte_to_payload_index(doc_byte: int) -> int:
    return doc_byte - 9

def _pick_temp_scale(raw9: int) -> Tuple[str, float]:
    t05 = raw9 / 2.0
    t01 = raw9 / 10.0
    ok05 = 20.0 <= t05 <= 50.0
    ok01 = 20.0 <= t01 <= 50.0
    if ok01 and not ok05:
        return "0.1C", t01
    if ok05 and not ok01:
        return "0.5C", t05
    if ok01 and ok05:
        return "0.1C", t01
    return "0.1C", t01

def parse_general_packet(frame: bytes, params: DeviceParams, state: ECGState,
                         rr_calc: "RespRateCalculator",
                         hr_calc: "ECGHeartRateCalculator",
                         sub_stats: Dict[int, int]):
    payload = frame[9:-1]
    if len(payload) < 6:
        return
    sub = payload[4]
    sub_stats[sub] += 1
    if sub == 2:
        state.last_sub2_ts = time.time()
        idx_status = _doc_byte_to_payload_index(170)
        if idx_status < len(payload):
            bs = payload[idx_status]
            state.ecg_lead_off = (bs & 0x01) != 0
            state.spo2_probe_off = (bs & 0x02) != 0
            state.thermo_disconnected_alarm = (bs & 0x04) != 0
            state.spo2_disconnected_alarm = (bs & 0x08) != 0
            state.bp_disconnected_alarm = (bs & 0x10) != 0
            state.flow_disconnected_alarm = (bs & 0x20) != 0
        idx_temp_lo = _doc_byte_to_payload_index(168)
        idx_temp_hi = _doc_byte_to_payload_index(164)
        if idx_temp_lo < len(payload) and idx_temp_hi < len(payload):
            lo = payload[idx_temp_lo]
            hi_flag = (payload[idx_temp_hi] >> 2) & 0x01
            raw9 = (hi_flag << 8) | lo
            if DEBUG_RAW_TEMP:
                t05 = raw9 / 2.0
                t01 = raw9 / 10.0
                print(f"temp_raw9={raw9} (hi={hi_flag}, lo=0x{lo:02X}) => /2={t05:.1f}C  /10={t01:.1f}C | thermo断开={state.thermo_disconnected_alarm}")
            if state.thermo_disconnected_alarm:
                params.temp_a = "0"
            else:
                scale_name, t = _pick_temp_scale(raw9)
                if 20.0 <= t <= 50.0:
                    params.temp_a = f"{t:.1f}"
                else:
                    params.temp_a = f"0"
        idx_spo2 = _doc_byte_to_payload_index(169)
        if idx_spo2 < len(payload):
            spo2 = payload[idx_spo2]
            if state.spo2_probe_off or state.spo2_disconnected_alarm:
                params.os_a = "0"
            else:
                if 0 < spo2 <= 100:
                    params.os_a = f"{spo2}"
        idx_hr = _doc_byte_to_payload_index(176)
        if idx_hr < len(payload):
            device_hr = payload[idx_hr]
            if not state.ecg_lead_off and 25 <= device_hr <= 240:
                hr_calc.update_device_hr(device_hr)
    elif sub == 0:
        rr_calc.try_feed_resp_wave(payload, sub_packet=0)
        hr_calc.try_feed_ecg_from_general(payload, sub_packet=0)
    elif sub == 1:
        rr_calc.try_feed_resp_wave(payload, sub_packet=1)
        hr_calc.try_feed_ecg_from_general(payload, sub_packet=1)
    rr = rr_calc.get_rr_bpm()
    if rr is not None:
        params.hr_a = f"{rr:.0f}"
    if False:
        params.heart_rate_a = "0"
    else:
        hr = hr_calc.get_hr_bpm()
        if hr is not None:
            params.heart_rate_a = f"{hr:.0f}"
            
def hex_bytes(data: bytes) -> str:
    return " ".join(f"{b:02X}" for b in data)

def parse_bp_result(frame: bytes, params: DeviceParams, state: ECGState):
    payload = frame[9:-1]
    if DEBUG_BP_PAYLOAD:
        print(f"🩺 0x22 payload({len(payload)}B): {hex_bytes(payload)}")
    if len(payload) < 4:
        return
    state.last_bp_result_ts = time.time()
    status = payload[0]
    if status != 0x01:
        params.sbp_a = "测量失败"
        params.dbp_a = "测量失败"
        params.pulse_a = f"失败(status=0x{status:02X})"
        return
    sys_v = payload[1]
    dia_v = payload[2]
    pul_v = payload[3]

    if 40 <= sys_v <= 260 and 20 <= dia_v <= 180:
        params.sbp_a = f"{sys_v}"
        params.dbp_a = f"{dia_v}"
    if 0 < pul_v <= 220:
        params.pulse_a = f"{pul_v}"
        
def cmd_set_rtc(device_id4: List[int]) -> bytes:
    payload = int(time.time()).to_bytes(4, "big")
    return build_packet(device_id4, FT_SET_RTC, payload)

def mac_to_6bytes(mac: str) -> bytes:
    parts = mac.split(":")
    if len(parts) != 6:
        raise ValueError(f"Bad MAC: {mac}")
    return bytes(int(p, 16) for p in parts)

def cmd_peripheral_mac(device_id4: List[int], dev_type: int, mac: str, op: int = 0x01) -> bytes:
    payload = bytes([op & 0xFF, dev_type & 0xFF]) + mac_to_6bytes(mac)
    return build_packet(device_id4, FT_PERIPHERAL_CTRL, payload)

def cmd_pairing_enable(device_id4: List[int]) -> bytes:
    payload = b"\x00\x00\x00\x00"
    return build_packet(device_id4, FT_PAIRING_ENABLE, payload)

def cmd_status_switch(device_id4: List[int], thermo_on: bool, spo2_on: bool, bp_on: bool, flow_on: bool = False) -> bytes:
    b = 0
    b |= (1 if flow_on else 0) << 7
    b |= (1 if bp_on else 0) << 6
    b |= (1 if spo2_on else 0) << 5
    b |= (1 if thermo_on else 0) << 4
    payload = bytes([b, 0x00, 0x00, 0x00])
    return build_packet(device_id4, FT_STATUS_SWITCH, payload)

def cmd_bp_measure(device_id4: List[int], model: int = 0x00, dev_id: int = 0x00) -> bytes:
    payload = bytes([model & 0xFF, dev_id & 0xFF, 0x00, 0x00])
    return build_packet(device_id4, FT_BP_MEASURE_CMD, payload)

def try_parse_hr_2a37(data: bytes) -> Optional[int]:
    if len(data) < 2:
        return None
    flags = data[0]
    hr_16 = (flags & 0x01) != 0
    if not hr_16:
        hr = data[1]
        return hr if 0 < hr <= 220 else None
    if len(data) < 3:
        return None
    hr = int.from_bytes(data[1:3], "little")
    return hr if 0 < hr <= 220 else None

def try_parse_fdfdfc_anywhere(data: bytes) -> Optional[Tuple[int, int, int]]:
    sig = b"\xFD\xFD\xFC"
    i = data.find(sig)
    if i < 0 or len(data) < i + 6:
        return None
    sys_v = data[i + 3]
    dia_v = data[i + 4]
    pul_v = data[i + 5]
    if 40 <= sys_v <= 260 and 20 <= dia_v <= 180 and 30 <= pul_v <= 220:
        return sys_v, dia_v, pul_v
    return None

def sfloat_to_float(raw: int) -> float:
    mantissa = raw & 0x0FFF
    exponent = (raw >> 12) & 0x000F
    if mantissa >= 0x0800:
        mantissa -= 0x1000
    if exponent >= 0x0008:
        exponent -= 0x0010
    return mantissa * (10 ** exponent)

def try_parse_standard_bp_measurement(data: bytes) -> Optional[Tuple[int, int, Optional[int]]]:
    if len(data) < 7:
        return None

    flags = data[0]
    unit_kpa = (flags & 0x01) != 0

    sys_raw = int.from_bytes(data[1:3], "little")
    dia_raw = int.from_bytes(data[3:5], "little")
    _map_raw = int.from_bytes(data[5:7], "little")

    sys_v = sfloat_to_float(sys_raw)
    dia_v = sfloat_to_float(dia_raw)

    if unit_kpa:
        sys_v *= 7.50062
        dia_v *= 7.50062

    idx = 7
    if flags & 0x02:
        idx += 7
    if flags & 0x08:
        idx += 1

    pulse_v = None
    if flags & 0x04:
        if len(data) >= idx + 2:
            pul_raw = int.from_bytes(data[idx:idx + 2], "little")
            pulse_v = int(round(sfloat_to_float(pul_raw)))

    if 40 <= sys_v <= 260 and 20 <= dia_v <= 180:
        return int(round(sys_v)), int(round(dia_v)), pulse_v
    return None

async def connect_by_mac(mac: str, timeout: float = 30.0, max_retries: int = 3) -> BleakClient:
    for attempt in range(1, max_retries + 1):
        try:
            print(f"尝试连接 {mac} (第 {attempt} 次)...")
            # 先扫描发现设备
            device = await BleakScanner.find_device_by_address(mac, timeout=timeout)
            if device is None:
                # 如果没找到，再全量扫描一次试试
                devices = await BleakScanner.discover(timeout=timeout)
                for d in devices:
                    if d.address.upper() == mac.upper():
                        device = d
                        break
                if device is None:
                    raise RuntimeError(f"未发现设备: {mac}")
            # 连接设备
            client = BleakClient(device)
            await client.connect(timeout=timeout)  # 明确设置连接超时
            print(f"成功连接到 {mac}")
            return client
        except Exception as e:
            print(f"连接尝试 {attempt} 失败: {e}")
            if attempt == max_retries:
                print(f"已达到最大重试次数，放弃连接 {mac}")
                raise  # 重新抛出最后的异常
            else:
                # 指数退避：等待时间随重试次数增加，避免频繁重试
                wait_time = 2 ** attempt
                print(f"等待 {wait_time} 秒后重试...")
                await asyncio.sleep(wait_time)
    # 让函数签名正确
    raise RuntimeError(f"无法连接到设备: {mac}")

async def dump_gatt(client: BleakClient):
    try:
        services = await client.get_services()
    except Exception:
        services = client.services
    print("\n GATT特征一览：")
    for s in services:
        for c in getattr(s, "characteristics", []):
            props = getattr(c, "properties", [])
            ps = list(props) if isinstance(props, (list, tuple, set)) else props
            print(f"  - {str(c.uuid)}  props={ps}")
    print("-" * 60)
    
async def discover_rw_uuids_and_write_mode(client: BleakClient) -> Tuple[Optional[str], Optional[str], bool]:
    try:
        services = await client.get_services()
    except Exception:
        services = client.services

    prefer_notify = [
        "0000fff1-0000-1000-8000-00805f9b34fb",
        "6e400003-b5a3-f393-e0a9-e50e24dcca9e",
    ]
    prefer_write = [
        "0000fff2-0000-1000-8000-00805f9b34fb",
        "6e400002-b5a3-f393-e0a9-e50e24dcca9e",
    ]
    notify_chars: List[str] = []
    write_chars: List[Tuple[str, object]] = []

    for s in services:
        for c in getattr(s, "characteristics", []):
            u = str(c.uuid).lower()
            if has_prop(c, "notify") or has_prop(c, "indicate"):
                notify_chars.append(u)
            if has_prop(c, "write") or has_prop(c, "write-without-response"):
                write_chars.append((u, getattr(c, "properties", [])))

    found_notify = next((u for u in prefer_notify if u in notify_chars), None)
    found_write = next((u for u in prefer_write if any(u == x for x, _ in write_chars)), None)

    if not found_notify and notify_chars:
        found_notify = notify_chars[0]
    if not found_write and write_chars:
        found_write = write_chars[0][0]

    write_with_response = False
    for u, props in write_chars:
        if u == found_write:
            ps = list(props) if isinstance(props, (list, tuple, set)) else props
            if isinstance(ps, list):
                if "write" in ps and "write-without-response" not in ps:
                    write_with_response = True
                else:
                    write_with_response = False
            break

    return found_notify, found_write, write_with_response

class ECGHub:
    def __init__(self, mac: str, params: DeviceParams):
        self.mac = mac
        self.client: Optional[BleakClient] = None
        self.params = params
        self.state = ECGState()
        self._rx_buffer = bytearray()
        self.rr_calc = RespRateCalculator()
        self.hr_calc = ECGHeartRateCalculator()
        self.sub_stats: Dict[int, int] = defaultdict(int)

        self._task_status_keepalive: Optional[asyncio.Task] = None
        self._task_bp_periodic: Optional[asyncio.Task] = None
        self._task_sub_stats: Optional[asyncio.Task] = None

        self.ecg_bp_on = (BP_FALLBACK_MODE != "force")

    async def connect_and_run_forever(self):
        while True:
            try:
                await self._connect_once()
                await asyncio.sleep(999999)
            except asyncio.CancelledError:
                raise
            except Exception:
                try:
                    await self.disconnect()
                except Exception:
                    pass
                await asyncio.sleep(2)

    async def _connect_once(self):
        self.client = await connect_by_mac(self.mac, timeout=300.0, max_retries=3)

        if DEBUG_GATT_DUMP:
            await dump_gatt(self.client)

        notify_uuid, write_uuid, wr_resp = await discover_rw_uuids_and_write_mode(self.client)
        self.state.notify_uuid = notify_uuid
        self.state.write_uuid = write_uuid
        self.state.write_with_response = wr_resp

        if not notify_uuid or not write_uuid:
            raise RuntimeError(f"无法发现notify/write UUID：notify={notify_uuid}, write={write_uuid}")

        await self.client.start_notify(notify_uuid, self._on_notify)

        t0 = time.time()
        while self.state.device_id is None and time.time() - t0 < 5:
            await asyncio.sleep(0.05)

        await self.protocol_init_and_enable_peripherals()

    async def disconnect(self):
        for t in [self._task_status_keepalive, self._task_bp_periodic, self._task_sub_stats]:
            if t:
                t.cancel()

        if self.client and self.client.is_connected:
            try:
                if self.state.notify_uuid:
                    await self.client.stop_notify(self.state.notify_uuid)
            except Exception:
                pass
            await self.client.disconnect()

    async def write(self, pkt: bytes):
        if not self.client or not self.client.is_connected:
            raise RuntimeError("心电仪未连接")
        await self.client.write_gatt_char(self.state.write_uuid, pkt, response=self.state.write_with_response)

    def _on_notify(self, _sender: int, data: bytes):
        self._rx_buffer.extend(data)
        while True:
            frame = try_extract_one_frame(self._rx_buffer)
            if frame is None:
                break
            if not verify_frame(frame):
                continue
            self._handle_frame(frame)

    def _handle_frame(self, frame: bytes):
        ft = frame[8]
        if self.state.device_id is None:
            self.state.device_id = extract_device_id(frame)
        if ft == FT_REGISTER_REQ:
            asyncio.create_task(self.write(cmd_register_rsp(self.state.device_id)))
            return
        if ft == FT_GENERAL:
            parse_general_packet(frame, self.params, self.state, self.rr_calc, self.hr_calc, self.sub_stats)
        elif ft == FT_BP_RESULT:
            parse_bp_result(frame, self.params, self.state)

    async def protocol_init_and_enable_peripherals(self):
        did = self.state.device_id or [0, 0, 0, 0]

        await self.write(cmd_set_rtc(did))
        # // await self.write(cmd_peripheral_mac(did, dev_type=0x00, mac=THERMO_MAC, op=0x01))

        if self.ecg_bp_on:
            await self.write(cmd_peripheral_mac(did, dev_type=0x02, mac=BP_MAC, op=0x01))

        await self.write(cmd_pairing_enable(did))
        await self.write(cmd_status_switch(did, thermo_on=True, spo2_on=True, bp_on=self.ecg_bp_on, flow_on=False))

        self._task_status_keepalive = asyncio.create_task(self._status_keepalive_loop())
        self._task_sub_stats = asyncio.create_task(self._sub_stats_loop())

        if self.ecg_bp_on:
            self._task_bp_periodic = asyncio.create_task(self._bp_periodic_loop())

    async def _status_keepalive_loop(self):
        while True:
            await asyncio.sleep(STATUS_KEEPALIVE_INTERVAL)
            if not self.client or not self.client.is_connected:
                continue
            did = self.state.device_id or [0, 0, 0, 0]
            await self.write(cmd_status_switch(did, thermo_on=True, spo2_on=True, bp_on=self.ecg_bp_on, flow_on=False))

    async def _sub_stats_loop(self):
        while True:
            await asyncio.sleep(10)
            if DEBUG_GENERAL_SUB:
                s0 = self.sub_stats.get(0, 0)
                s1 = self.sub_stats.get(1, 0)
                s2 = self.sub_stats.get(2, 0)
                print(f"📊 GENERAL sub统计：sub0={s0}, sub1={s1}, sub2={s2}")

    async def _bp_periodic_loop(self):
        while True:
            await asyncio.sleep(1)
            if not self.client or not self.client.is_connected:
                continue
            now = time.time()
            if now - self.state.last_bp_trigger_ts < BP_MEASURE_INTERVAL:
                continue
            did = self.state.device_id or [0, 0, 0, 0]
            await self.write(cmd_bp_measure(did, model=0x00, dev_id=0x00))
            self.state.last_bp_trigger_ts = now

class BPDirectFallback:
    BP_MEAS_2A35 = "00002a35-0000-1000-8000-00805f9b34fb"
    HR_MEAS_2A37 = "00002a37-0000-1000-8000-00805f9b34fb"

    def __init__(self, mac: str, shared_params: DeviceParams):
        self.mac = mac
        self.client: Optional[BleakClient] = None
        self.params = shared_params
        self._notify_uuids: List[str] = []
        self._running = True

    def stop(self):
        self._running = False

    def _set_bp_pulse(self, pulse: int):
        self.params.pulse_a = f"{pulse}"

    async def _subscribe_all_needed(self):
        if not self.client:
            return
        if DEBUG_GATT_DUMP:
            await dump_gatt(self.client)
        try:
            services = await self.client.get_services()
        except Exception:
            services = self.client.services
        notify_list = []
        for s in services:
            for c in getattr(s, "characteristics", []):
                if has_prop(c, "notify") or has_prop(c, "indicate"):
                    notify_list.append(str(c.uuid))
        self._notify_uuids = notify_list
        lower = [u.lower() for u in self._notify_uuids]
        if self.BP_MEAS_2A35 in lower:
            u = self._notify_uuids[lower.index(self.BP_MEAS_2A35)]
            await self.client.start_notify(u, self._on_notify)
        if self.HR_MEAS_2A37 in lower:
            u = self._notify_uuids[lower.index(self.HR_MEAS_2A37)]
            await self.client.start_notify(u, self._on_notify)
        extra = [u for u in self._notify_uuids if u.lower() not in (self.BP_MEAS_2A35, self.HR_MEAS_2A37)]
        for u in extra[:10]:
            try:
                await self.client.start_notify(u, self._on_notify)
            except Exception:
                pass

    async def _disconnect_internal(self):
        if self.client and self.client.is_connected:
            try:
                for u in self._notify_uuids:
                    try:
                        await self.client.stop_notify(u)
                    except Exception:
                        pass
            except Exception:
                pass
            try:
                await self.client.disconnect()
            except Exception:
                pass
        self.client = None
        self._notify_uuids = []

    async def run_forever(self):
        while self._running:
            try:
                if not self.client or not self.client.is_connected:
                    self.client = await connect_by_mac(self.mac, timeout=6.0)
                    await self._subscribe_all_needed()
                await asyncio.sleep(1.0)
            except Exception:
                await self._disconnect_internal()
                await asyncio.sleep(2.0)
        await self._disconnect_internal()

    def _on_notify(self, _sender: int, data: bytes):
        fdf = try_parse_fdfdfc_anywhere(data)
        if fdf:
            sys_v, dia_v, pul_v = fdf
            self.params.sbp_a = f"{sys_v}"
            self.params.dbp_a = f"{dia_v}"
            self._set_bp_pulse(pul_v)
            return
        parsed = try_parse_standard_bp_measurement(data)
        if parsed:
            sys_v, dia_v, pul_v = parsed
            self.params.sbp_a = f"{sys_v}"
            self.params.dbp_a = f"{dia_v}"
            if pul_v is not None and 0 < pul_v <= 220:
                self._set_bp_pulse(pul_v)
            return
        hr = try_parse_hr_2a37(data)
        if hr is not None:
            self._set_bp_pulse(hr)
            return

class VitalsMonitor:
    def __init__(self, ecg_mac: str = ECG_MAC, bp_mac: str = BP_MAC):
        self.params = DeviceParams()
        self.ecg = ECGHub(ecg_mac, self.params)
        self.bp = BPDirectFallback(bp_mac, self.params) if BP_FALLBACK_MODE == "force" else None
        self._tasks: List[asyncio.Task] = []
    
    async def start(self):
        # // ECG 常驻（自动重连）
        self._tasks.append(asyncio.create_task(self.ecg.connect_and_run_forever()))
        # // BP 常驻（force模式下自动重连）
        if self.bp:
            self._tasks.append(asyncio.create_task(self.bp.run_forever()))
    
    async def stop(self):
        for t in self._tasks:
            t.cancel()
        if self.bp:
            self.bp.stop()
        try:
            await self.ecg.disconnect()
        except Exception:
            pass
        
    def get_vitals(self) -> Dict[str, str]:
        return {
            'heartRate': self.params.heart_rate_a,
            'pulse': self.params.pulse_a,
            'systolicPressure': self.params.sbp_a,
            'diastolicPressure': self.params.dbp_a,
            'respiratoryRate': self.params.hr_a,
            'temperature': self.params.temp_a,
            'oxygenSaturation': self.params.os_a,
        }