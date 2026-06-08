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
        session.run("""
            // ==================== 第一层：患者（节点名 = 真实伤员ID） ====================
            CREATE (p:Patient { name: $name })

            // ==================== 第二层：分类父节点 ====================
            CREATE (info:PatientInfo { name: "PatientInfo" })
            CREATE (vitals:VitalSigns { name: "VitalSigns" })
            CREATE (gcs:GCS { name: "GCSScore" })
            CREATE (scores:TriageScores { name: "TriageScores" })
            CREATE (wound:WoundedArea { name: "WoundedArea" })
            CREATE (img:MedicalImage { name: "MedicalImage" })
            CREATE (desc:InjuryDescription { name: "InjuryDescription" })
            CREATE (sug:MedicalAdvice { name: "MedicalAdvice" })

            // ==================== 第三层：全部是【真实取值节点】（无拼接名！） ====================
            // 患者信息
            CREATE (loc:Location { name: $location })
            CREATE (dt:DateTime { name: $datatime })
            CREATE (gender:Gender { name: $gender })
            CREATE (age:Age { name: $age })
            CREATE (bt:BloodType { name: $bloodtype })

            // 生命体征
            CREATE (hr:HR { name: $hr })
            CREATE (pulse:Pulse { name: $pulse })
            CREATE (resp:Resp { name: $resp })
            CREATE (sbp:SBP { name: $sbp })
            CREATE (dbp:DBP { name: $dbp })
            CREATE (temp:Temp { name: $temp })

            // GCS
            CREATE (gcs_motor:GCS_Motor { name: $gcs_motor })
            CREATE (gcs_verbal:GCS_Verbal { name: $gcs_verbal })
            CREATE (gcs_eye:GCS_Eye { name: $gcs_eye })
            CREATE (gcs_total:GCS_Total { name: $GCS_res })

            // 分诊评分
            CREATE (rts:RTS { name: $RTS_res })
            CREATE (phi:PHI { name: $PHI_res })
            CREATE (crams:CRAMS { name: $CRAM_res })
            CREATE (ml:ML { name: $ML_res })

            // 受伤部位
            CREATE (chest:ChestAbdomen { name: $chest_and_abdomen })
            CREATE (areas:WoundedAreas { name: $wounded_areas })

            // 影像、描述、建议
            CREATE (photos:CapturedPhotos { name: $captured_photos })
            CREATE (injuryDesc:InjuryContent { name: $description })
            CREATE (medicalSug:AdviceContent { name: $suggestion })

            // ==================== 关系：第一层 → 第二层 ====================
            CREATE (p)-[:HAS_PATIENT_INFO]->(info)
            CREATE (p)-[:HAS_VITALS]->(vitals)
            CREATE (p)-[:HAS_GCS]->(gcs)
            CREATE (p)-[:HAS_TRIAGE_SCORES]->(scores)
            CREATE (p)-[:HAS_WOUNDED_AREA]->(wound)
            CREATE (p)-[:HAS_MEDICAL_IMAGE]->(img)
            CREATE (p)-[:HAS_INJURY_DESCRIPTION]->(desc)
            CREATE (p)-[:HAS_MEDICAL_ADVICE]->(sug)

            // ==================== 关系：第二层 → 第三层（真实值） ====================
            CREATE (info)-[:HAS_LOCATION]->(loc)
            CREATE (info)-[:HAS_DATETIME]->(dt)
            CREATE (info)-[:HAS_GENDER]->(gender)
            CREATE (info)-[:HAS_AGE]->(age)
            CREATE (info)-[:HAS_BLOOD_TYPE]->(bt)

            CREATE (vitals)-[:HAS_HR]->(hr)
            CREATE (vitals)-[:HAS_PULSE]->(pulse)
            CREATE (vitals)-[:HAS_RESP]->(resp)
            CREATE (vitals)-[:HAS_SBP]->(sbp)
            CREATE (vitals)-[:HAS_DBP]->(dbp)
            CREATE (vitals)-[:HAS_TEMP]->(temp)

            CREATE (gcs)-[:HAS_MOTOR]->(gcs_motor)
            CREATE (gcs)-[:HAS_VERBAL]->(gcs_verbal)
            CREATE (gcs)-[:HAS_EYE]->(gcs_eye)

            CREATE (scores)-[:HAS_RTS]->(rts)
            CREATE (scores)-[:HAS_PHI]->(phi)
            CREATE (scores)-[:HAS_CRAMS]->(crams)
            CREATE (scores)-[:HAS_ML]->(ml)
            CREATE (scores)-[:HAS_TOTAL]->(gcs_total)

            CREATE (wound)-[:HAS_CHEST_ABDOMEN]->(chest)
            CREATE (wound)-[:HAS_WOUNDED_AREAS]->(areas)

            CREATE (img)-[:HAS_PHOTOS]->(photos)
            CREATE (desc)-[:HAS_CONTENT]->(injuryDesc)
            CREATE (sug)-[:HAS_CONTENT]->(medicalSug)
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
    # with driver.session() as session:
    #     # 执行Cypher语句
    #     session.run("""
    #             CREATE (p:Patient {
    #                 name: $name,
    #                 location: $location,
    #                 datatime: $datatime,
    #                 gender: $gender,
    #                 age: $age,
    #                 bloodtype: $bloodtype
    #             })

    #             CREATE (v:VitalSigns {
    #                 name: "VitalSigns-" + $name,
    #                 hr: $hr,
    #                 pulse: $pulse,
    #                 resp: $resp,
    #                 sbp: $sbp,
    #                 dbp: $dbp,
    #                 temp: $temp
    #             })

    #             CREATE (gcs:GCS {
    #                 name: "GCS-" + $name,
    #                 motor: $gcs_motor,
    #                 verbal: $gcs_verbal,
    #                 eye: $gcs_eye,
    #                 total: $GCS_res
    #             })

    #             CREATE (score:TriageScore {
    #                 name: "TriageScore-" + $name,
    #                 RTS: $RTS_res,
    #                 PHI: $PHI_res,
    #                 CRAMS: $CRAM_res,
    #                 ML: $ML_res
    #             })

    #             CREATE (wound:WoundedArea {
    #                 name: "WoundedArea-" + $name,
    #                 chest_and_abdomen: $chest_and_abdomen,
    #                 areas: $wounded_areas
    #             })

    #             CREATE (img:MedicalImage {
    #                 name: "MedicalImage-" + $name,
    #                 captured_photos: $captured_photos
    #             })

    #             CREATE (desc:InjuryDescription {
    #                 name: "InjuryDescription-" + $name,
    #                 content: $description
    #             })

    #             CREATE (sug:MedicalAdvice {
    #                 name: "MedicalAdvice-" + $name,
    #                 content: $suggestion
    #             })

    #             CREATE (p)-[:HAS_VITALS]->(v)
    #             CREATE (p)-[:HAS_GCS]->(gcs)
    #             CREATE (p)-[:HAS_TRIAGE_SCORE]->(score)
    #             CREATE (p)-[:HAS_WOUNDED_AREA]->(wound)
    #             CREATE (p)-[:HAS_MEDICAL_IMAGE]->(img)
    #             CREATE (p)-[:HAS_INJURY_DESCRIPTION]->(desc)
    #             CREATE (p)-[:HAS_MEDICAL_ADVICE]->(sug)
    #         """,
    #             name=data['wounded_id'],
    #             location=data['location'],
    #             datatime=data['DateTime'],
    #             gender=data['gender'],
    #             age=data['age'],
    #             bloodtype=data['blood_type'],
    #             hr=data['hr'],
    #             pulse=data['pulse'],
    #             resp=data['breath'],
    #             sbp=data['sysbp'],
    #             dbp=data['dbp'],
    #             temp=data['temp'],
    #             gcs_motor=data['gcs_motor'],
    #             gcs_verbal=data['gcs_verbal'],
    #             gcs_eye=data['gcs_eye'],
    #             chest_and_abdomen=data['chest_and_abdomen'],
    #             RTS_res=data['RTS_res'],
    #             PHI_res=data['PHI_res'],
    #             CRAM_res=data['CRAMS_res'],
    #             GCS_res=data['GCS_res'],
    #             ML_res=data['ML_res'],
    #             wounded_areas=data['wounded_areas'],
    #             captured_photos=data['captured_photos'],
    #             description=data['description'],
    #             suggestion=data['suggestion']
    #         )
    # 关闭连接
    driver.close()
    return JsonResponse({'code': 200, 'status': 'success'})
