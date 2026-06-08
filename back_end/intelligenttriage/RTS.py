
def getRTSResult(breath, sbp, gcs):
    # 计算修正创伤计分(Revised Trauma Score, RTS)
    # https://wenku.baidu.com/view/e94ea20abd23482fb4daa58da0116c175f0e1eb7.html?_wkts_=1779176781522&bdQuery=%E7%AE%80%E6%98%93%E6%88%98%E4%BC%A4%E8%AE%A1%E5%88%86%E6%B3%95&chatType=chat
    # https://cals.medlive.cn/calc/show/2?id=calc-66
    breath_score = 4 if float(breath) >= 10 and float(breath) <= 29 else 3 if float(breath) > 29 else 2 if float(breath) >= 6 and float(breath) <= 9 else 1 if float(breath) >= 1 and float(breath) <= 5 else 0
    sbp_score = 4 if float(sbp) > 89 else 3 if float(sbp) <= 89 and float(sbp) >= 76 else 2 if float(sbp) >= 75 and float(sbp) <= 50 else 1 if float(sbp) >= 1 and float(sbp) <= 49 else 0
    gcs_score = 4 if float(gcs) >= 13 and float(gcs) <= 15 else 3 if float(gcs) >= 9 and float(gcs) <= 12 else 2 if float(gcs) >= 6 and float(gcs) <= 8 else 1 if float(gcs) >= 4 and float(gcs) <= 5 else 0
    RTS_level = breath_score + sbp_score + gcs_score
    if RTS_level <= 12 and RTS_level >= 10:
        return "normal"
    elif RTS_level <= 9 and RTS_level >= 7:
        return "minor injury"
    elif RTS_level <= 6 and RTS_level >= 4:
        return "severe injury"
    elif RTS_level <= 3 and RTS_level >= 0:
        return "extremely severe injury"
    return 'unknown'
