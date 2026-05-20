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
    # 将数据保存到neo4j数据库
    with driver.session() as session:
        # 执行Cypher语句
        session.run("""
                CREATE (p:Patient {
                    name: $name,
                    location: $location,
                    datatime: $datatime,
                    gender: $gender,
                    age: $age,
                    bloodtype: $bloodtype
                })

                CREATE (v:VitalSigns {
                    name: "VitalSigns-" + $name,
                    hr: $hr,
                    pulse: $pulse,
                    resp: $resp,
                    sbp: $sbp,
                    dbp: $dbp,
                    temp: $temp
                })

                CREATE (gcs:GCS {
                    name: "GCS-" + $name,
                    motor: $gcs_motor,
                    verbal: $gcs_verbal,
                    eye: $gcs_eye,
                    total: $GCS_res
                })

                CREATE (score:TriageScore {
                    name: "TriageScore-" + $name,
                    RTS: $RTS_res,
                    PHI: $PHI_res,
                    CRAMS: $CRAM_res,
                    ML: $ML_res
                })

                CREATE (wound:WoundedArea {
                    name: "WoundedArea-" + $name,
                    chest_and_abdomen: $chest_and_abdomen,
                    areas: $wounded_areas
                })

                CREATE (img:MedicalImage {
                    name: "MedicalImage-" + $name,
                    captured_photos: $captured_photos
                })

                CREATE (desc:InjuryDescription {
                    name: "InjuryDescription-" + $name,
                    content: $description
                })

                CREATE (sug:MedicalAdvice {
                    name: "MedicalAdvice-" + $name,
                    content: $suggestion
                })

                CREATE (p)-[:HAS_VITALS]->(v)
                CREATE (p)-[:HAS_GCS]->(gcs)
                CREATE (p)-[:HAS_TRIAGE_SCORE]->(score)
                CREATE (p)-[:HAS_WOUNDED_AREA]->(wound)
                CREATE (p)-[:HAS_MEDICAL_IMAGE]->(img)
                CREATE (p)-[:HAS_INJURY_DESCRIPTION]->(desc)
                CREATE (p)-[:HAS_MEDICAL_ADVICE]->(sug)
            """,
                name=data['wounded_id'],
                location=data['location'],
                datatime=data['DateTime'],
                gender=data['gender'],
                age=data['age'],
                bloodtype=data['blood_type'],
                hr=data['hr'],
                pulse=data['pulse'],
                resp=data['breath'],
                sbp=data['sysbp'],
                dbp=data['dbp'],
                temp=data['temp'],
                gcs_motor=data['gcs_motor'],
                gcs_verbal=data['gcs_verbal'],
                gcs_eye=data['gcs_eye'],
                chest_and_abdomen=data['chest_and_abdomen'],
                RTS_res=data['RTS_res'],
                PHI_res=data['PHI_res'],
                CRAM_res=data['CRAMS_res'],
                GCS_res=data['GCS_res'],
                ML_res=data['ML_res'],
                wounded_areas=data['wounded_areas'],
                captured_photos=data['captured_photos'],
                description=data['description'],
                suggestion=data['suggestion']
            )
    # 关闭连接
    driver.close()
    return JsonResponse({'code': 200, 'status': 'success'})
