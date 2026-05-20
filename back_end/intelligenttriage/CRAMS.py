
def getCRAMSResult(sysbp, breath, chest, gcs_motor, gcs_verbal):
    # 通过CRAMS法获取伤伤结果 https://nursing.medsci.cn/article/show_article.do?id=98a684e496ea
    sysbp_score = 2 if sysbp >= 100 else 1 if sysbp >= 85 and sysbp <= 99 else 0
    breath_score = 2 if breath >= 12 and breath <= 20 else 0 if breath == 0 else 1
    chest_score = chest
    motor_score = 2 if gcs_motor == 6 else 1 if gcs_motor >= 2 and gcs_motor <= 5 else 0
    verbal_score = 2 if gcs_verbal == 5 else 1 if gcs_verbal >= 3 and gcs_verbal <= 4 else 0
    CRAMS_score = sysbp_score + breath_score + chest_score + motor_score + verbal_score
    if CRAMS_score >= 9:
        return 'minor injury'
    elif CRAMS_score > 6 and CRAMS_score <= 8:
        return "severe injury"
    else:
        return "extremely severe injury"