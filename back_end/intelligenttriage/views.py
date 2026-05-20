from django.shortcuts import render
from django.http import JsonResponse
from intelligenttriage.RTS import getRTSResult
from intelligenttriage.PHI import getPHIResult
from intelligenttriage.GCS import getGCSResult
from intelligenttriage.ML import getMLResult
from intelligenttriage.CRAMS import getCRAMSResult
import json

# Create your views here.
def getTriageResult(request):
    if request.method != "POST":
        return JsonResponse({"code": 405, "msg": "仅支持POST"})
    # 解析POST中body中的参数
    #-----------------------------------------------
    data = request.body.decode("utf-8")
    data = json.loads(data)
    breath = data.get("breath")
    sysbp = data.get("sysbp")
    gcs = data.get("gcs")
    chest = data.get("chest")
    gcs_motor = data.get("gcs_motor")
    gcs_verbal = data.get("gcs_verbal")
    age = data.get("age")
    hr = data.get("hr")
    temp = data.get("temp")
    pulse = data.get("pulse")
    #-----------------------------------------------
    # 通过修正创伤计分(Revised Trauma Score, RTS)获取检伤结果
    RTS_res = getRTSResult(breath, sysbp, gcs)
    # 通过院前指数评估(prehospital index, PHI)获取检伤结果
    PHI_res = getPHIResult(gcs, gcs_verbal, sysbp, pulse, breath, chest)
    # 通过CRAMS法获取检伤结果
    CRAMS_res = getCRAMSResult(sysbp, breath, chest, gcs_motor, gcs_verbal)
    # 通过GCS法获取伤员的意识状态
    GCS_res = getGCSResult(gcs)
    # 通过机器学习模型评估伤员死亡率风险: age, hr, sysbp, temp, gcs
    ML_res = getMLResult(age, hr, sysbp, temp, gcs)
    
    return JsonResponse({"code": 200, "msg": "获取成功", "triage_result": {"RTS": RTS_res, "PHI": PHI_res, "CRAMS": CRAMS_res, "GCS": GCS_res, "ML": ML_res}})
