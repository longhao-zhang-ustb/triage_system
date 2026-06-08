from collections import deque, defaultdict
from typing import Optional, Deque
import time

def _doc_byte_to_payload_index(doc_byte: int) -> int:
    return doc_byte - 9

class RespRateCalculator:
    FS = 25
    WINDOW_SEC = 30
    RR_MIN_BPM = 4
    RR_MAX_BPM = 60

    def __init__(self):
        self.samples: Deque[int] = deque(maxlen=self.FS * self.WINDOW_SEC)
        self.last_rr: Optional[float] = None
        self.last_update_ts = 0.0

    def try_feed_resp_wave(self, payload: bytes, sub_packet: int):
        if sub_packet == 0:
            base_doc = 20
        elif sub_packet == 1:
            base_doc = 140
        else:
            return
        base = _doc_byte_to_payload_index(base_doc)
        need = base + 50
        if base < 0 or len(payload) < need:
            return

        pts = []
        for i in range(25):
            msb = payload[base + 2*i]
            lsb = payload[base + 2*i + 1]
            v = (msb << 8) | lsb
            pts.append(v)

        if all(p == 0 for p in pts) or all(p == 0xFFFF for p in pts):
            return
        fill = sum(1 for p in pts if p in (0xAAAA, 0x5555))
        if fill >= 20:
            return

        for v in pts:
            self.samples.append(v)

        now = time.time()
        if now - self.last_update_ts >= 1.0:
            self.last_update_ts = now
            self.last_rr = self._compute_rr()

    def _compute_rr(self) -> Optional[float]:
        if len(self.samples) < self.FS * 15:
            return None
        import numpy as np
        x = np.array(self.samples, dtype=np.float64)
        x = x - np.mean(x)
        k = int(self.FS * 0.4)
        if k < 3:
            k = 3
        kernel = np.ones(k) / k
        xs = np.convolve(x, kernel, mode="same")
        # // 允许最高到 60 次/分，对应最短周期约 1 秒
        min_dist = max(2, int(self.FS * 0.9))
        peaks = []
        for i in range(1, len(xs)-1):
            if xs[i] > xs[i-1] and xs[i] > xs[i+1]:
                peaks.append(i)

        if len(peaks) < 3:
            return None

        peak_vals = xs[peaks]
        thr = np.percentile(peak_vals, 65)
        peaks = [p for p in peaks if xs[p] >= thr]

        peaks2 = []
        last = -10**9
        for p in peaks:
            if p - last >= min_dist:
                peaks2.append(p)
                last = p

        if len(peaks2) < 3:
            return None

        intervals = np.diff(peaks2) / self.FS
        min_interval = 60.0 / self.RR_MAX_BPM
        max_interval = 60.0 / self.RR_MIN_BPM
        intervals = intervals[(intervals >= min_interval) & (intervals <= max_interval)]
        if len(intervals) < 2:
            return None

        # 再做一次一致性过滤，减少高频噪声导致的乱填
        median_interval = float(np.median(intervals))
        tolerance = max(0.18, median_interval * 0.35)
        stable_intervals = intervals[np.abs(intervals - median_interval) <= tolerance]
        if len(stable_intervals) >= 2:
            intervals = stable_intervals

        period = float(np.median(intervals))
        rr = 60.0 / period
        if self.RR_MIN_BPM <= rr <= self.RR_MAX_BPM:
            return rr
        return None

    def get_rr_bpm(self) -> Optional[float]:
        return self.last_rr
