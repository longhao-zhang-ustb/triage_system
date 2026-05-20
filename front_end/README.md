# 智能分检终端系统

## 数据结构

文件名：{患者ID}.json

- uid (string): 患者 ID
- name (string): 患者姓名
- sex (int): 性别（0：未知，1：男，2：女）
- age (int): 年龄
- blood (string): 血型（A、B、AB、O）
- injury_data: 伤情数据（JSON 格式）
- score_data: 评分数据（JSON 格式）
- vital_data: 生命体征数据（JSON 格式）
- suggestion (int): 转归后送选择（0：位置，1：收容，2：转归）

### injury_data 详细子结构
```json
{
  "injuries": [
    // 多个 string 代表部位名称
  ],
  "is_battle_injury": "boolean", // 是否为战伤
}
```

### score_data 详细子结构
```json
{
  "glasgow": "int", // 格拉斯哥评分
  "phi": "int", // 生理指数评分
  "start": "int", // START 颜色
}
```

### vital_data 详细子结构
```json
{
  "heart_rate": "int", // 心率（bpm）
  "blood_pressure": {
    "systolic": "int", // 收缩压（mmHg）
    "diastolic": "int" // 舒张压（mmHg）
  },
  "respiratory_rate": "int", // 呼吸频率（次/分钟）
  "oxygen_saturation": "int", // 血氧饱和度（%）
  "temperature": "float", // 体温（℃）
  "timestamp": "string" // 测量时间戳（ISO 格式）
}
```
