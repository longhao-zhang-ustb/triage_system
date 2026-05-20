from django.shortcuts import render
from django.http import JsonResponse
import json
from neo4j import GraphDatabase

# Create your views here.
def save2Neo4j(request):
    # 提示错误信息
    if request.method != 'POST':
        return JsonResponse({'code': 405, 'msg': '只允许POST请求'})
    # 连接neo4j数据库
    uri = "bolt://localhost:7687"
    username = "neo4j"
    password = "neo4j123"
    # 创建连接
    driver = GraphDatabase.driver(uri, auth=(username, password))
    # 保存伤员信息
    data = request.body.decode("utf-8")
    data = json.loads(data)
    print(data)
    # 将数据保存到neo4j数据库
    with driver.session() as session:
        # 执行Cypher语句
        session.run("CREATE (p:Patient {name: $name, location: $location, datatime: $datatime, gender: $gender, age: $age, bloodtype: $bloodtype, hr: $hr, pulse: $pulse, resp: $resp, sbp: $sbp, dbp: $dbp, temp: $temp, gcs_motor: $gcs_motor, gcs_verbal: $gcs_verbal, gcs_eye: $gcs_eye, chest_and_abdomen: $chest_and_abdomen, RTS_res: $RTS_res, PHI_res: $PHI_res, CRAM_res: $CRAM_res, GCS_res: $GCS_res, ML_res: $ML_res, wounded_areas: $wounded_areas, captured_photos: $captured_photos, description: $description, suggestion: $suggestion})",
                    name=data['wounded_id'],
                    location=data['location'],
                    datatime=data['DateTime'],
                    gender=data['gender'],
                    age=data['age'],
                    bloodtype=data['blood_type'],
                    # 心率
                    hr=data['hr'],
                    # 脉搏
                    pulse=data['pulse'],
                    # 呼吸率
                    resp=data['breath'],
                    # 收缩压
                    sbp=data['sysbp'],
                    # 舒张压
                    dbp=data['dbp'],
                    # 体温
                    temp=data['temp'],
                    # gcs_motor
                    gcs_motor=data['gcs_motor'],
                    # gcs_verbal
                    gcs_verbal=data['gcs_verbal'],
                    # gcs_eye
                    gcs_eye=data['gcs_eye'],
                    # chest_and_abdomen
                    chest_and_abdomen=data['chest_and_abdomen'],
                    # RTS_res
                    RTS_res=data['RTS_res'],
                    # PHI_res
                    PHI_res=data['PHI_res'],
                    # CRAM_res
                    CRAM_res=data['CRAMS_res'],
                    # GCS_res
                    GCS_res=data['GCS_res'],
                    # ML_res
                    ML_res=data['ML_res'],
                    # wounded_areas
                    wounded_areas=data['wounded_areas'],
                    # captured_photos
                    captured_photos=data['captured_photos'],
                    # description
                    description=data['description'],
                    # suggestion
                    suggestion=data['suggestion'])
    # 关闭连接
    driver.close()
    return JsonResponse({'code': 200, 'status': 'success'})
