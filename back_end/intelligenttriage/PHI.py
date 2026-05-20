
def getPHIResult(gcs, gcs_verbal, sysbp, pulse, breath, chest):
    # 计算院前指数评估(prehospital index, PHI):https://nursing.medsci.cn/article/show_article.do?id=98a684e496ea
    gcs_score = 0 if gcs == 15 else 5 if gcs_verbal <= 2 else 3
    sysbp_score = 0 if sysbp > 100 else 1 if sysbp >= 86 and sysbp <= 100 else 2 if sysbp >= 75 and sysbp <= 85 else 5
    pulse_score = 0 if pulse >= 51 and pulse <= 119 else 3 if pulse >= 120 else 5
    breath_score = 0 if breath >= 12 and breath <= 20 else 5 if breath < 10 else 3
    phi_score = gcs_score + sysbp_score + pulse_score + breath_score
    if chest == 0:
        phi_score += 4
    if phi_score <= 3:
        return 'minor injury'
    else:
        return 'severe injury'