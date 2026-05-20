import joblib

def getMLResult(age, hr, sysbp, temp, gcs):
    # 通过机器学习模型评估伤员死亡率风险: Simplified Acute Physiology Score (SAPS) II
    model = joblib.load(r"intelligenttriage\\ML_model\\xgb_model.pkl")
    triage_res = ''
    # 将原始生理参数转换为模型输入的格式
    age_score = 0 if age < 40 else 7 if age >= 40 and age <= 59 else 12 if age >= 60 and age <= 69 else 15 if age >= 70 and age <= 74 else 16 if age >= 75 and age <= 79 else 18
    hr_score = 0 if hr > 70 and hr <= 119 else 2 if hr >= 40 and hr <= 69 else 4 if hr >= 120 and hr <= 159 else 7 if hr >= 160 else 11
    sysbp_score = 0 if sysbp >= 100 and sysbp <= 199 else 2 if sysbp >= 200 else 5 if sysbp >= 70 and sysbp <= 99 else 13
    temp_score = 0 if temp < 39 else 3
    gcs_score = 0 if gcs >= 14 and gcs <= 15 else 5 if gcs >= 11 and gcs <= 13 else 7 if gcs >= 9 and gcs <= 10 else 13 if gcs >= 6 and gcs <= 8 else 26
    # 模型预测
    y_pred = model.predict([[age_score, hr_score, sysbp_score, temp_score, gcs_score]])
    y_pred_proba = model.predict_proba([[age_score, hr_score, sysbp_score, temp_score, gcs_score]])
    # 解析预测结果
    if y_pred[0] == 0:
        triage_res = f"<= 1%_{y_pred_proba[0][0]:.2f}"
    elif y_pred[0] == 1:
        triage_res = f"1% ~ 10%_{y_pred_proba[0][1]:.2f}" 
    elif y_pred[0] == 2:
        triage_res = f"> 10%_{y_pred_proba[0][2]:.2f}"
    return triage_res