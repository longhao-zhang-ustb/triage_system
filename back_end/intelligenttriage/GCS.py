
def getGCSResult(gcs):
    # 计算GCS法: https://mp.weixin.qq.com/s?__biz=MzkyODE4NTczMw==&mid=2247501912&idx=1&sn=b1590cbb0a0e8d9ad5a28c1fdb7d75b6&chksm=c21e24b2f569ada419d1eaad687c3cf0a6db102dcd5a6e00f7dab39b09d1678f9a4ba13a9632&scene=27
    if gcs == 15:
        return "normal"
    elif gcs >= 13 and gcs <= 14:
        return "mild"
    elif gcs >= 9 and gcs <= 12:
        return "moderate"
    elif gcs >= 3 and gcs <= 8:
        return "severe"