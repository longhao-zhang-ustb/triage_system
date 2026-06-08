import pandas as pd
from sklearn.model_selection import train_test_split
import joblib
import shap
import matplotlib.pyplot as plt

# 绘图字体设置
plt.rcParams['font.sans-serif'] = ['Times New Roman']  # 设置字体为Times New Roman

if __name__ == '__main__':
    # 简化急性生理学评分：Le Gall JR, Lemeshow S, Saulnier F. A new Simplified Acute Physiology Score (SAPS II) based on a European/North American multicenter study. JAMA. 1993;270(24):2957-63. PMID 8254858
    # https://clincalc.com/icumortality/sapsii.aspx
    # 读取伤员数据
    df = pd.read_csv(r"intelligenttriage\database\triage_database.csv")
    # 去掉hadm_id和stay_id列
    df = df.drop(columns=["hadm_id", "stay_id"])
    # seed和test_size
    seeds = [42, 230, 799, 1345, 5899]
    test_size = [0.4, 0.3, 0.2, 0.1]
    seed = seeds[0]
    test_size = test_size[2]
    # 将sapsii根据分数区间划分为不同等级，死亡风险低于1%，死亡风险在1%到10%，死亡风险高于10%
    df["sapsii_level"] = df["sapsii"].apply(lambda x: 0 if x <= 29 else 1)
    # 根据subject_id划分训练集和测试集
    unique_ids = df["subject_id"].unique()
    train_ids, test_ids = train_test_split(unique_ids, test_size=test_size, random_state=seed)
    train_df = df[df["subject_id"].isin(train_ids)].copy()
    test_df = df[df["subject_id"].isin(test_ids)].copy()
    # 打印训练集和测试集的样本数
    print(f"训练集样本数: {len(train_df)}")
    print(f"测试集样本数: {len(test_df)}")
    # 获取训练集和测试集
    X_train = train_df.drop(columns=["subject_id", "sapsii", "sapsii_level"])
    y_train = train_df["sapsii_level"]
    X_test = test_df.drop(columns=["subject_id", "sapsii", "sapsii_level"])
    y_test = test_df["sapsii_level"]
    print(X_train)
    # 标准化
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    # 保存scaler
    joblib.dump(scaler, r"intelligenttriage\\ML_model\\standard_scaler.pkl")  
    # 构造XGBoost模型
    from xgboost import XGBClassifier
    model = XGBClassifier(n_estimators=150, random_state=42)
    # 训练模型
    model.fit(X_train, y_train)
    # 评估模型
    y_pred = model.predict(X_test)
    # 根据classification_report评估模型
    from sklearn.metrics import classification_report
    print(classification_report(y_test, y_pred, digits=4))
    # 计算MCC
    from sklearn.metrics import matthews_corrcoef
    mcc = matthews_corrcoef(y_test, y_pred)
    print(f"MCC: {mcc:.4f}")
    # 保存模型
    joblib.dump(model, r"intelligenttriage\\ML_model\\xgb_model.pkl")
    # 执行SHAP分析
    feature_names = ["age_score", "hr_score", "sysbp_score", "temp_score", "gcs_score",]
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)
    shap.summary_plot(shap_values, 
                      X_test,
                      cmap="Spectral_r",
                      feature_names=feature_names,
                      show=False
    )
    # plt.show()
    plt.tight_layout()
    plt.savefig(r"intelligenttriage\shap_summary.tif", dpi=300)
"""
########################## seed=42, test_size=0.4 ##########################
              precision    recall  f1-score   support

           0     0.7623    0.7154    0.7381     13431
           1     0.8402    0.8702    0.8549     23089

    accuracy                         0.8133     36520
   macro avg     0.8013    0.7928    0.7965     36520
weighted avg     0.8115    0.8133    0.8120     36520

MCC: 0.5940
########################## seed=230, test_size=0.4 ##########################
              precision    recall  f1-score   support

           0     0.7656    0.7209    0.7426     13478
           1     0.8420    0.8708    0.8561     23017

    accuracy                         0.8154     36495
   macro avg     0.8038    0.7958    0.7994     36495
weighted avg     0.8138    0.8154    0.8142     36495

MCC: 0.5996
########################## seed=799, test_size=0.4 ##########################
            precision    recall  f1-score   support

           0     0.7626    0.7232    0.7424     13343
           1     0.8455    0.8706    0.8579     23214

    accuracy                         0.8168     36557
   macro avg     0.8041    0.7969    0.8001     36557
weighted avg     0.8152    0.8168    0.8157     36557

MCC: 0.6009
########################## seed=1345, test_size=0.4 ##########################
              precision    recall  f1-score   support

           0     0.7725    0.7178    0.7441     13524
           1     0.8409    0.8759    0.8581     23033

    accuracy                         0.8174     36557
   macro avg     0.8067    0.7968    0.8011     36557
weighted avg     0.8156    0.8174    0.8159     36557

MCC: 0.6035
########################## seed=5899, test_size=0.4 ##########################
              precision    recall  f1-score   support

           0     0.7663    0.7238    0.7444     13259
           1     0.8459    0.8729    0.8591     23022

    accuracy                         0.8184     36281
   macro avg     0.8061    0.7983    0.8018     36281
weighted avg     0.8168    0.8184    0.8172     36281

MCC: 0.6044


########################## seed=42, test_size=0.3 ##########################
              precision    recall  f1-score   support

           0     0.7670    0.7104    0.7376     10091
           1     0.8378    0.8739    0.8555     17273

    accuracy                         0.8136     27364
   macro avg     0.8024    0.7922    0.7966     27364
weighted avg     0.8117    0.8136    0.8120     27364

MCC: 0.5945
########################## seed=230, test_size=0.3 ##########################
              precision    recall  f1-score   support

           0     0.7658    0.7235    0.7441     10110
           1     0.8433    0.8705    0.8567     17280

    accuracy                         0.8163     27390
   macro avg     0.8046    0.7970    0.8004     27390
weighted avg     0.8147    0.8163    0.8151     27390

MCC: 0.6016
########################## seed=799, test_size=0.3 ##########################
              precision    recall  f1-score   support

           0     0.7608    0.7231    0.7415      9953
           1     0.8454    0.8694    0.8572     17329

    accuracy                         0.8160     27282
   macro avg     0.8031    0.7963    0.7993     27282
weighted avg     0.8145    0.8160    0.8150     27282

MCC: 0.5993
########################## seed=1345, test_size=0.3 ##########################
              precision    recall  f1-score   support

           0     0.7717    0.7171    0.7434     10105
           1     0.8408    0.8756    0.8578     17239

    accuracy                         0.8170     27344
   macro avg     0.8062    0.7964    0.8006     27344
weighted avg     0.8152    0.8170    0.8155     27344

MCC: 0.6025
########################## seed=5899, test_size=0.3 ##########################
              precision    recall  f1-score   support

           0     0.7706    0.7267    0.7480     10052
           1     0.8456    0.8737    0.8594     17217

    accuracy                         0.8195     27269
   macro avg     0.8081    0.8002    0.8037     27269
weighted avg     0.8179    0.8195    0.8183     27269

MCC: 0.6082
########################## seed=42, test_size=0.2 ##########################
              precision    recall  f1-score   support

           0     0.7704    0.7143    0.7413      6676
           1     0.8417    0.8771    0.8590     11562

    accuracy                         0.8175     18238
   macro avg     0.8061    0.7957    0.8002     18238
weighted avg     0.8156    0.8175    0.8160     18238

MCC: 0.6017
########################## seed=230, test_size=0.2 ##########################
              precision    recall  f1-score   support

           0     0.7678    0.7166    0.7413      6697
           1     0.8406    0.8734    0.8567     11462

    accuracy                         0.8156     18159
   macro avg     0.8042    0.7950    0.7990     18159
weighted avg     0.8138    0.8156    0.8142     18159

MCC: 0.5992
########################## seed=799, test_size=0.2 ##########################
              precision    recall  f1-score   support

           0     0.7614    0.7250    0.7427      6588
           1     0.8479    0.8709    0.8593     11600

    accuracy                         0.8181     18188
   macro avg     0.8046    0.7980    0.8010     18188
weighted avg     0.8166    0.8181    0.8171     18188

MCC: 0.6026
########################## seed=1345, test_size=0.2 ##########################
              precision    recall  f1-score   support

           0     0.7697    0.7224    0.7453      6654
           1     0.8441    0.8743    0.8589     11436

    accuracy                         0.8184     18090
   macro avg     0.8069    0.7983    0.8021     18090
weighted avg     0.8167    0.8184    0.8171     18090

MCC: 0.6052
########################## seed=5899, test_size=0.2 ##########################
              precision    recall  f1-score   support

           0     0.7789    0.7287    0.7530      6712
           1     0.8472    0.8791    0.8629     11485

    accuracy                         0.8237     18197
   macro avg     0.8131    0.8039    0.8079     18197
weighted avg     0.8220    0.8237    0.8223     18197

MCC: 0.6169
########################## seed=42, test_size=0.1 ##########################
              precision    recall  f1-score   support

           0     0.7720    0.7229    0.7467      3396
           1     0.8418    0.8736    0.8574      5734

    accuracy                         0.8175      9130
   macro avg     0.8069    0.7982    0.8020      9130
weighted avg     0.8159    0.8175    0.8162      9130

MCC: 0.6051
########################## seed=230, test_size=0.1 ##########################
              precision    recall  f1-score   support

           0     0.7641    0.7095    0.7358      3287
           1     0.8426    0.8765    0.8592      5831

    accuracy                         0.8163      9118
   macro avg     0.8033    0.7930    0.7975      9118
weighted avg     0.8143    0.8163    0.8147      9118

MCC: 0.5962
########################## seed=799, test_size=0.1 ##########################
              precision    recall  f1-score   support

           0     0.7601    0.7310    0.7453      3260
           1     0.8538    0.8720    0.8628      5875

    accuracy                         0.8217      9135
   macro avg     0.8070    0.8015    0.8040      9135
weighted avg     0.8204    0.8217    0.8209      9135

MCC: 0.6084
########################## seed=1345, test_size=0.1 ##########################
              precision    recall  f1-score   support

           0     0.7656    0.7279    0.7462      3307
           1     0.8462    0.8705    0.8582      5690

    accuracy                         0.8181      8997
   macro avg     0.8059    0.7992    0.8022      8997
weighted avg     0.8166    0.8181    0.8170      8997

MCC: 0.6050
########################## seed=5899, test_size=0.1 ##########################
              precision    recall  f1-score   support

           0     0.7743    0.7269    0.7499      3314
           1     0.8483    0.8781    0.8629      5761

    accuracy                         0.8229      9075
   macro avg     0.8113    0.8025    0.8064      9075
weighted avg     0.8213    0.8229    0.8217      9075

MCC: 0.6138
"""   
