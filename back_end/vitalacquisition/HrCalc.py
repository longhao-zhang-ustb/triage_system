import time
from typing import Deque, Optional, List
from collections import deque

def _doc_byte_to_payload_index(doc_byte: int) -> int:
    return doc_byte - 9
def _extract_ecg_segment_50(payload: bytes, hi_doc_start: int, lo_doc_start: int) -> Optional[List[int]]:
    hi_base = _doc_byte_to_payload_index(hi_doc_start)
    lo_base = _doc_byte_to_payload_index(lo_doc_start)
    if hi_base < 0 or lo_base < 0:
        return None
    if lo_base + 50 > len(payload):
        return None
    if hi_base + 13 > len(payload):
        return None
    out: List[int] = []
    for i in range(50):
        hb = payload[hi_base + (i // 4)]
        sh = (i % 4) * 2
        hi2 = (hb >> sh) & 0x03
        lo8 = payload[lo_base + i]
        out.append((hi2 << 8) | lo8)
    return out

class ECGHeartRateCalculator:
    FS = 200
    WINDOW_SEC = 8
    DIRECT_HR_TTL_SEC = 4.0

    def __init__(self):
        self.samples: Deque[int] = deque(maxlen=self.FS * self.WINDOW_SEC)
        self.last_hr: Optional[float] = None
        self.last_update_ts = 0.0
        self.device_hr: Optional[float] = None
        self.device_hr_ts = 0.0

    def update_device_hr(self, hr: int):
        if 25 <= hr <= 240:
            self.device_hr = float(hr)
            self.device_hr_ts = time.time()

    def try_feed_ecg_from_general(self, payload: bytes, sub_packet: int):
        segs: List[List[int]] = []
        if sub_packet == 0:
            s1 = _extract_ecg_segment_50(payload, 70, 83)
            s2 = _extract_ecg_segment_50(payload, 133, 146)
            if s1 and s2:
                segs = [s1, s2]
        elif sub_packet == 1:
            s3 = _extract_ecg_segment_50(payload, 14, 27)
            s4 = _extract_ecg_segment_50(payload, 77, 90)
            if s3 and s4:
                segs = [s3, s4]
        else:
            return

        added = False
        for seg in segs:
            if all(v == 0 for v in seg) or all(v == 0x3FF for v in seg):
                continue
            if max(seg) - min(seg) < 8:
                continue
            for v in seg:
                self.samples.append(v)
            added = True

        if not added:
            return

        now = time.time()
        if now - self.last_update_ts >= 1.0:
            self.last_update_ts = now
            self.last_hr = self._compute_hr()

    def _compute_hr(self) -> Optional[float]:
        if len(self.samples) < self.FS * 3:
            return None
        import numpy as np
        x = np.array(self.samples, dtype=np.float64)
        x = x - np.mean(x)
        k_base = max(3, int(self.FS * 0.6))
        kernel_base = np.ones(k_base) / k_base
        base = np.convolve(x, kernel_base, mode="same")
        hp = x - base
        d = np.diff(hp, prepend=hp[0])
        sq = d * d
        k_int = max(3, int(self.FS * 0.15))
        kernel_int = np.ones(k_int) / k_int
        y = np.convolve(sq, kernel_int, mode="same")

        min_dist = int(self.FS * 0.25)

        peaks = []
        for i in range(1, len(y) - 1):
            if y[i] > y[i - 1] and y[i] > y[i + 1]:
                peaks.append(i)
        if len(peaks) < 3:
            return None

        pv = y[peaks]
        thr = np.percentile(pv, 80)
        peaks = [p for p in peaks if y[p] >= thr]
        if len(peaks) < 3:
            return None

        chosen = []
        last = -10**9
        for p in peaks:
            if p - last >= min_dist:
                chosen.append(p)
                last = p
        if len(chosen) < 3:
            return None

        rr = np.diff(chosen) / self.FS
        rr = rr[(rr >= 0.25) & (rr <= 1.5)]
        if len(rr) < 2:
            return None

        period = float(np.median(rr))
        hr = 60.0 / period
        if 15 <= hr <= 300:
            return hr
        return None

    def get_hr_bpm(self) -> Optional[float]:
        if self.device_hr is not None and (time.time() - self.device_hr_ts) <= self.DIRECT_HR_TTL_SEC:
            return self.device_hr
        return self.last_hr