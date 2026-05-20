import request from '../utils/request';

// 评估相关API
const assessmentApi = {
  // 提交评估数据
  createAssessment: (payload) => {
    // return request.post('/api/assessments', payload);
    return request.post('/api/assessments', payload);
  },
  // 获取患者信息列表（无参数GET请求）
  getPatientList: () => {
    // 发送GET请求到后端接口，无需传递参数
    return request.get('/api/assessments/list');
  }
};


export default assessmentApi;
