import pandas as pd
from sklearn.model_selection import train_test_split
import joblib

if __name__ == '__main__':
    # 简化急性生理学评分：Le Gall JR, Lemeshow S, Saulnier F. A new Simplified Acute Physiology Score (SAPS II) based on a European/North American multicenter study. JAMA. 1993;270(24):2957-63. PMID 8254858
    # https://clincalc.com/icumortality/sapsii.aspx
    # 读取伤员数据
    df = pd.read_csv(r"intelligenttriage\database\triage_database.csv")
    # 去掉hadm_id和stay_id列
    df = df.drop(columns=["hadm_id", "stay_id"])
    # 将sapsii根据分数区间划分为不同等级，死亡风险低于1%，死亡风险在1%到10%，死亡风险高于10%
    df["sapsii_level"] = df["sapsii"].apply(lambda x: 0 if x <= 11 else 1 if 12 <= x <= 29 else 2)
    # 根据subject_id划分训练集和测试集
    unique_ids = df["subject_id"].unique()
    train_ids, test_ids = train_test_split(unique_ids, test_size=0.2, random_state=42)
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
    print(classification_report(y_test, y_pred))
    # 保存模型
    joblib.dump(model, r"intelligenttriage\\ML_model\\xgb_model.pkl")
    