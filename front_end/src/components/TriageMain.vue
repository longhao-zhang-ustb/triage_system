<template>
  <div class="triage-system-main">
    <section class="wounded-info-header">
      <!-- Intelligent Triage and Emergency Care System: prehospital -->
      <div class="header-left">
        <h1 class="header-title">DP-PTE</h1>
        <!-- Time + Location -->
        <div class="time-location">
          <span id="current-time">DateTime: {{ currentTime }}</span>
          <span> | </span>
          <span id="location">{{locationText}}</span>
        </div>
      </div>
      <div class="button-container">
        <!-- 蓝牙状态指示灯 -->
        <div class="bluetooth-status">
          <div
            class="status-light"
            :class="{ gray: btStatus === 'disconnected', orange: btStatus === 'searching', green: btStatus === 'connected' }"
          >
          </div>
        </div>
        <div class="fun-button" @click="searchDevice">Connect</div>
        <span class="button-separator"> | </span>
        <div class="fun-button" @click="switchWounded">Disconnect</div>
        <span class="button-separator"> | </span>
        <div class="fun-button" @click="saveWoundedInfo">Save</div>
        <div id="uploadTip" style="margin-left:10px;color:#666;display:none;font-weight:bold;"></div>
      </div>
    </section>
    <!-- 主要核心功能：检伤分类区 & 紧急救治区 -->
    <main class="main-content">
      <!-- 检伤分类区 -->
      <section class="triage-classification">
        <h2 class="ia-section-title">Injury Assessment</h2>
        <div class="box-item">
          <div class="h3-wrap">
            <h3>Patient Demographics</h3>
            <span class="help-icon" @click="openDemoHelpModal">?</span>
          </div>
          <div class="grid-form">
            <div class="form-item">
              <label>Patient ID:</label>
              <input type="text" id="patient-id" placeholder="---" onfocus="this.placeholder=''" onblur="if(this.value === '') this.placeholder = '---'">
            </div>
            <div class="form-item">
              <label>Gender:</label>
                <select id="gender" class="default-option" required>
                  <option value="" disabled selected hidden>---</option>
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                </select>
            </div>
            <div class="form-item">
              <label>Age:</label>
              <input type="text" id="age" placeholder="---" onfocus="this.placeholder=''" onblur="if(this.value === '') this.placeholder = '---'">
            </div>
            <div class="form-item">
              <label>Blood Type:</label>
              <select id="blood-type" class="default-option" required>
                <option value="" disabled selected hidden>---</option>
                <option value="A">A</option>
                <option value="B">B</option>
                <option value="AB">AB</option>
                <option value="O">O</option>
              </select>
            </div>
          </div>
        </div>
        <div class="box-item">
          <div class="h3-wrap">
            <h3>Vital Signs</h3>
            <span class="help-icon" @click="openVitalHelpModal">?</span>
          </div>
          <!-- 生命体征信息 -->
          <div class="grid-form-vital">
            <div class="vital-form-item">
              <label>HR:</label>
              <input type="text" id="heart-rate" :value="heartRate" placeholder="--">
            </div>
            <div class="vital-form-item">
              <label>PUL:</label>
              <input type="text" id="pulse" :value="pulse" placeholder="--">
            </div>
            <div class="vital-form-item">
              <label>RR:</label>
              <input type="text" id="respiratory-rate" :value="respiratoryRate" placeholder="--">
            </div>
            <div class="vital-form-item">
              <label>SBP:</label>
              <input type="text" id="systolic-blood-pressure" :value="systolicBP" placeholder="--">
            </div>
            <div class="vital-form-item">
              <label>DBP:</label>
              <input type="text" id="diastolic-blood-pressure" :value="diastolicBP" placeholder="--">
            </div>
            <div class="vital-form-item">
              <label>TEM:</label>
              <input type="text" id="temperature" :value="temperature" placeholder="--">
            </div>
          </div>
        </div>
        <div class="box-item">
          <div class="h3-wrap">
            <h3>Neurological Signs (Glasgow Coma Scale)</h3>
            <span class="help-icon" @click="openGCSHelpModal">?</span>  
          </div>
          <div class="grid-form-ns">
            <div class="ns-form-item">
              <label>Eye Opening</label>
                <select id="eye-opening-score" class="default-option" required>
                  <option value="" disabled selected hidden>---</option>
                  <option value="4">4-Spontaneous</option>
                  <option value="3">3-To Sound</option>
                  <option value="2">2-To Pressure</option>
                  <option value="1">1-None</option>
                </select>
            </div>
            <div class="ns-form-item">
              <label>Motor Response</label>
              <select id="motor-response-score" class="default-option" required>
                  <option value="" disabled selected hidden>---</option>
                  <option value="6">6-Obey Commands</option>
                  <option value="5">5-Localising</option>
                  <option value="4">4-Normal Flexion</option>
                  <option value="3">3-Abnormal Flexion</option>
                  <option value="2">2-Extension</option>
                  <option value="1">1-None</option>
                </select>
            </div>
            <div class="ns-form-item">
              <label>Verbal Response</label>
              <select id="verbal-response-score" class="default-option" required>
                  <option value="" disabled selected hidden>---</option>
                  <option value="5">5-Orientated</option>
                  <option value="4">4-Confused</option>
                  <option value="3">3-Words</option>
                  <option value="2">2-Sounds</option>
                  <option value="1">1-None</option>
                </select>
            </div>
          </div>
        </div>
        <div class="box-item">
          <div class="h3-wrap">
            <h3>Other Information</h3>
            <!-- <span class="help-icon">?</span>   -->
          </div>
          <div class="form-item-other">
            <label>Chest and Abdomen:</label>
            <select id="supplement" class="default-option" required>
              <option value="" disabled selected hidden>---</option>
              <option value="2">2-No Tenderness Present</option>
              <option value="1">1-Tenderness Present in the Chest or Abdomen</option>
              <option value="0">0-Flail Chest, Plate-like Abdomen, or Penetrating Wound</option>
            </select>
          </div>
        </div>
        <div class="box-item">
          <div class="h3-wrap">
            <h3>Intelligent Triage Results</h3>
            <!-- <div class="evaluate-btn-wrap"> -->
              <!-- <button type="button" class="evaluate-btn" @click="startAssessment" style="font-weight:bold;">Start</button> -->
            <!-- </div> -->
          </div>
          <!-- 智能分类结果 -->
          <div class="triage-table">
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; width: 100%;">
              <div style="display: flex; flex-direction: column; gap: 20px;">
                <div style="padding: 16px; border-radius: 8px; border:2px solid rgb(134, 21, 21); background: #fff; box-shadow: 0 2px 6px rgba(0,0,0,0.06); min-height: 120px;">
                  <div style="font-weight: 600; margin-bottom: 6px;">RTS</div>
                  <div style="color: black; font-weight: bold; font-size: 16px;">{{ RTS_res }}</div>
                </div>
                <div style="padding: 16px; border-radius: 8px; border:2px solid rgb(134, 21, 21); background: #fff; box-shadow: 0 2px 6px rgba(0,0,0,0.06); min-height: 120px;">
                  <div style="font-weight: 600; margin-bottom: 6px;">PHI</div>
                  <div style="color: black; font-weight: bold; font-size: 16px;">{{ PHI_res }}</div>
                </div>
              </div>
              <div style="display: flex; flex-direction: column; gap: 20px;">
                <div style="padding: 16px; border-radius: 8px; border:2px solid rgb(134, 21, 21); background: #fff; box-shadow: 0 2px 6px rgba(0,0,0,0.06); min-height: 120px;">
                  <div style="font-weight: 600; margin-bottom: 6px;">CRAMS</div>
                  <div style="color: black; font-weight: bold; font-size: 16px;">{{ CRAMS_res }}</div>
                </div>
                <div style="padding: 16px; border-radius: 8px; border:2px solid rgb(134, 21, 21); background: #fff; box-shadow: 0 2px 6px rgba(0,0,0,0.06); min-height: 120px;">
                  <div style="font-weight: 600; margin-bottom: 6px;">GCS</div>
                  <div style="color: black; font-weight: bold; font-size: 16px;">{{ GCS_res }}</div>
                </div>
              </div>
              <div style="display: flex; flex-direction: column; gap: 12px;">
                <div style="padding: 16px; border-radius: 8px; border:2px solid rgb(134, 21, 21); background: #fff; box-shadow: 0 2px 6px rgba(0,0,0,0.06); min-height: 260px;">
                  <div style="font-weight: 600; margin-bottom: 6px; text-align: center;">Intelligent Model</div>
                  <div style="display: flex; flex-direction: column; gap: 18px; padding: 12px 15px; background: #fef2f2; border-radius: 6px; margin-top: 15%;">
                    <div style="text-align: center;">
                      <span style="font-size: 14px; color: #333; display: block; margin-bottom: 6px;">Mortality Rate</span>
                      <span style="font-size: 16px; font-weight: bold; color: #861515; display: block; text-align: center;">{{ ML_res.split('_')[0] }}</span>
                    </div>
                    <div style="text-align: center;">
                      <span style="font-size: 14px; color: #333; display: block; margin-bottom: 6px;">Probability</span>  
                      <span style="font-size: 16px; font-weight: bold; color: #861515;">{{ ML_res.split('_')[1] }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div id="analysisModal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.4); z-index: 9999; align-items: center; justify-content: center;">
            <div style="background: rgb(134, 21, 21); padding: 30px 50px; border-radius: 8px; font-size: 25px; color: white; font-weight: bold">
                An analysis is in progress, please wait...
            </div>
          </div>
        </div>
      </section>
      <section class="emergency-care">
        <h2 class="ia-section-title">Emergency Care</h2>
        <div class="care-layout">
          <!-- 左侧：再分为2个区域 -->
          <div class="care-left">
            <!-- 左侧上部分 -->
            <div class="care-box">
              <h3>Injured Area</h3>
              <div class="injury-area">
                <label class="radio-item"><input type="checkbox" value="Head" v-model="selectedAreas">Head</label>
                <label class="radio-item"><input type="checkbox" value="Neck" v-model="selectedAreas">Neck</label>
                <label class="radio-item"><input type="checkbox" value="Face" v-model="selectedAreas">Face</label>
                <label class="radio-item"><input type="checkbox" value="Chest" v-model="selectedAreas">Chest</label>
                <label class="radio-item"><input type="checkbox" value="Abdomen and Pelvis" v-model="selectedAreas">Abdomen and Pelvis</label>
                <label class="radio-item"><input type="checkbox" value="Upper Limbs" v-model="selectedAreas"> Upper Limbs</label>
                <label class="radio-item"><input type="checkbox" value="Lower Limbs" v-model="selectedAreas"> Lower Limbs</label>
                <label class="radio-item"><input type="checkbox" value="Body Surface" v-model="selectedAreas"> Body Surface</label>
                <label class="radio-item"><input type="checkbox" value="Spine" v-model="selectedAreas"> Spine</label>
              </div>
            </div>
            <!-- 左侧中部分 -->
            <div class="care-box">
              <!-- 标题+按钮 同行布局 -->
              <div class="box-header">
                <h3>Image Data Acquisition</h3>
                <div class="btn-group">
                  <button class="img-btn">Open Camera</button>
                  <button class="img-btn">Take Photos</button>
                </div>
              </div>
              <div class="image-preview-layout">
                <!-- 左侧：视频画面 -->
                <div class="video-area">
                  <video id="cameraVideo" autoplay playsinline></video>
                  <div class="placeholder">Camera Preview</div>
                </div>
                <!-- 右侧：2行2列 4张拍照结果 -->
                <div class="photo-grid">
                  <div class="photo-item" id="injuryPhoto1"><img ref="img1" src="" alt="Photo 1"></div>
                  <div class="photo-item" id="injuryPhoto2"><img ref="img2" src="" alt="Photo 2"></div>
                  <div class="photo-item" id="injuryPhoto3"><img ref="img3" src="" alt="Photo 3"></div>
                  <div class="photo-item" id="injuryPhoto4"><img ref="img4" src="" alt="Photo 4"></div>
                </div>
              </div>
            </div>
            <!-- 左侧下部分 -->
            <div class="care-box">
              <!-- 标题 + 语音按钮（同行右对齐） -->
              <div class="supp-header">
                <h3>Supplementary Information</h3>
                <button id="voiceBtn" class="voice-btn">🎤 Voice Input</button>
              </div>
              <!-- 底部可编辑文字区域 -->
              <div 
                class="show-text" 
                id="showText" 
                contenteditable="true"
              >
                Additional information about the injury...
              </div>
            </div>
          </div> 
          <!-- 右侧为1个聊天框 -->
          <div class="care-chat">
            <div class="top-content">
              <div class="ai-doctor-box">
                <div class="ai-doctor-icon" id="aiIcon">
                  <img src="../assets/digital_doctor.png" alt="AI Doctor Icon">
                </div>
                <div class="loading-tip" id="loadingTip" v-if="isLoading">The Answer is on its way...</div>
                <div id="adviceContainer" class="advice-container" v-if="showResult">
                  <p>{{ adviceText }}</p>
                </div>
              </div>
              
            </div>
            <div class="btn-bottom">
              <button 
                class="breath-btn" 
                @click="getAdvice"
                :disabled="isLoading"
              >
                {{ isLoading ? 'Getting advice...' : 'Click Here for Advice from a Digital Doctor' }}
              </button>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
<!-- 人口统计学弹窗设计 -->
<div v-if="DemoHelpModal" class="modal-overlay" @click.self="closeDemoHelpModal">
  <div class="modal-card">
    <div class="modal-header">
      <h4>Help Information</h4>
      <button class="close-btn" @click="closeDemoHelpModal">×</button>
    </div>
    <div class="modal-body">
      <p>Patient Demographics includes the patient's basic information:</p>
      <ul>
        <li>Patient ID (Unique identifier)</li>
        <li>Gender</li>
        <li>Age</li>
        <li>Blood Type</li>
      </ul>
      <p class="tip">Please fill in truthfully and accurately for patient demographics.</p>
    </div>
  </div>
</div>
<!-- 生命体征弹窗设计 -->
<div v-if="VitalHelpModal" class="modal-overlay" @click.self="closeVitalHelpModal">
  <div class="modal-card">
    <div class="modal-header">
      <h4>Help Information</h4>
      <button class="close-btn" @click="closeVitalHelpModal">×</button>
    </div>
    <div class="modal-body">
      <p>Vital Signs Description:</p>
      <ul>
        <li>Heart Rate (HR)</li>
        <li>Pulse (PUL)</li>
        <li>Respiratory Rate (RR)</li>
        <li>Systolic Blood Pressure (SBP)</li>
        <li>Diastolic Blood Pressure (DBP)</li>
        <li>Temperature (TEM)</li>
      </ul>
      <div class="modal-body-wrapper">
        <div class="video-section">
          <p class="video-title"> Vital Signs Operation Demonstration</p>
          <div class="video-container">
            <video 
              class="demo-video" 
              controls 
              preload="metadata"
            >
              <source 
                src="http://localhost:8000/media/wounded/video/SensEcho.mp4" 
                type="video/mp4" 
              />
              Your browser does not support video playback.
            </video>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
<!-- 格拉斯哥操作方法弹窗设计 -->
<div v-if="GCSHelpModal" class="modal-overlay" @click.self="closeGCSHelpModal">
  <div class="modal-card">
    <div class="modal-header">
      <h4>Help Information</h4>
      <button class="close-btn" @click="closeGCSHelpModal">×</button>
    </div>
    <div class="modal-body">
      <div class="modal-body-wrapper">
        <div class="video-section">
          <p class="video-title"> Glasgow Coma Scale Operation Demonstration</p>
          <div class="video-container">
            <video 
              class="demo-video" 
              controls 
              preload="metadata"
            >
              <source 
                src="http://localhost:8000/media/wounded/video/GCS.mp4" 
                type="video/mp4" 
              />
              Your browser does not support video playback.
            </video>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script setup>
import { ref, onMounted, customRef, reactive } from 'vue';
//---------------获取当前时间的代码-----------------//
// 响应式时间变量
const currentTime = ref('');
// 更新时间
function updateTime() {
  const now = new Date();
  currentTime.value = now.toLocaleString('zh-CN');
}

//---------------获取当前位置的代码-----------------//
const locationText = ref('Location...');
function getLocation() {
  if (!navigator.geolocation) {
    locationText.value = 'Your browser does not support geolocation.';
    return;
  }
  navigator.geolocation.getCurrentPosition(
    (position) => {
      const lat = position.coords.latitude.toFixed(4);
      const lng = position.coords.longitude.toFixed(4);
      locationText.value = `Current Location: (${lat}, ${lng})`;
    },
    () => {
      locationText.value = 'Location permission denied.';
    }
  )
}

//------------------------帮助信息弹窗---------------------//
// 控制弹窗的显示与隐藏
let DemoHelpModal = ref(false)
let VitalHelpModal = ref(false)
let GCSHelpModal = ref(false)
// 打开人口统计学弹窗
const openDemoHelpModal = () => {
  DemoHelpModal.value = true
}
// 关闭人口统计学弹窗
const closeDemoHelpModal = () => {
  DemoHelpModal.value = false
}
// 打开生命体征弹窗
const openVitalHelpModal = () => {
  VitalHelpModal.value = true
}
// 关闭生命体征弹窗
const closeVitalHelpModal = () => {
  VitalHelpModal.value = false
}

// 打开格拉斯哥弹方法弹窗
const openGCSHelpModal = () => {
  GCSHelpModal.value = true
}
// 关闭格拉斯哥弹方法弹窗
const closeGCSHelpModal = () => {
  GCSHelpModal.value = false
}

////----------------- 生命体征检测及智能检伤模块 -------------------------
// 蓝牙状态：disconnected（未连接，灰） / searching（搜索中，橙） / connected（已连接，绿）
const btStatus = ref('disconnected')
// 响应式数据
// 定义响应式数据
const heartRate = ref('--')
const pulse = ref('--')
const respiratoryRate = ref('--')
const systolicBP = ref('--')
const diastolicBP = ref('--')
const temperature = ref('--')
let dataInterval = null
// 更新数据的函数
const updateUI = (data) => {
  heartRate.value = data.heartRate || '--'
  pulse.value = data.pulse || '--'
  respiratoryRate.value = data.respiratoryRate || '--'
  systolicBP.value = data.systolicPressure || '--'
  diastolicBP.value = data.diastolicPressure || '--'
  temperature.value = data.temperature || '--'
}

const RTS_res = ref('--')
const PHI_res = ref('--')
const CRAMS_res = ref('--')
const GCS_res = ref('--')
const ML_res = ref('--_--')

// 更新检伤结果数据
const updateTriageResult = (data) => {
  RTS_res.value = data.RTS || '--'
  PHI_res.value = data.PHI || '--'
  CRAMS_res.value = data.CRAMS || '--'
  GCS_res.value = data.GCS || '--'
  ML_res.value = data.ML || '--_--'
}

// 获取数据的函数
const fetchVitalData = async () => {
  try {
    const res = await fetch('http://localhost:8000/api/vitalsign/getvitalData/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    const result = await res.json()
    updateUI(result.data)
    // 判断此时的检伤条目是否完整
    let breath = document.getElementById('respiratory-rate').value.trim();
    if (!breath || breath === '---') {
      breath = -1
    }
    breath=Number(breath)
    let sysbp = document.getElementById('systolic-blood-pressure').value.trim();
    if (!sysbp || sysbp === '---') {
      sysbp = -1
    }
    sysbp=Number(sysbp)
    let gcs_motor = document.getElementById('motor-response-score').value.trim();
    if (!gcs_motor || gcs_motor === '---') {
      gcs_motor = -1
    }
    gcs_motor=Number(gcs_motor)
    let gcs_eye = document.getElementById('eye-opening-score').value.trim();
    if (!gcs_eye || gcs_eye === '---') {
      gcs_eye = -1
    }
    gcs_eye=Number(gcs_eye)
    let gcs_verbal = document.getElementById('verbal-response-score').value.trim();
    if (!gcs_verbal || gcs_verbal === '---') {
      gcs_verbal = -1
    }
    gcs_verbal=Number(gcs_verbal)
    let gcs = -1
    if (gcs_motor !== -1 && gcs_eye !== -1 && gcs_verbal !== -1) {
      gcs = parseInt(gcs_motor) + parseInt(gcs_eye) + parseInt(gcs_verbal);
    }
    gcs=Number(gcs)
    let pulse = document.getElementById('pulse').value.trim();
    if (!pulse || pulse === '--') {
      pulse = -1
    }
    pulse=Number(pulse)
    let chest = document.getElementById('supplement').value.trim();
    if (!chest || chest === '--') {
      chest = -1
    }
    chest=Number(chest)
    let age = document.getElementById('age').value.trim();
    if (!age || age === '---') {
      age = -1
    }
    age = Number(age)
    let hr = document.getElementById('heart-rate').value.trim();
    if (!hr || hr === '--') {
      hr = -1
    }
    hr=Number(hr)
    let temp = document.getElementById('temperature').value.trim();
    if (!temp || temp === '--') {
      temp = -1
    }
    temp=Number(temp)
    // 发送请求给后端
    const params = {breath, chest, gcs_motor, gcs_verbal, gcs, age, hr, sysbp, temp, pulse}
    console.log(params)
    // 请求后端接口
    const response = await fetch('http://localhost:8000/api/intelligenttriage/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(params)
    });
    const triage_result = await response.json();
    console.log('triage_result:', triage_result)
    updateTriageResult(triage_result.triage_result)
  } catch (error) {
    console.error('获取数据失败:', error)
    // 如果获取数据失败，可以选择停止轮询
    stopDataPolling()
  }
}
// 开始轮询数据
const startDataPolling = () => {
  // 清除已有的定时器，避免重复
  if (dataInterval) {
    clearInterval(dataInterval)
  }
  fetchVitalData()
  // 每隔1秒获取一次
  dataInterval = setInterval(fetchVitalData, 1000)
}
// 停止轮询数据
const stopDataPolling = () => {
  if (dataInterval) {
    clearInterval(dataInterval)
    dataInterval = null
  }
}

// 点击搜索设备
async function searchDevice() {
  // 先变成橙色（搜索中）
  btStatus.value = 'searching'
  try {
    // 发送请求给后端，真正连接蓝牙
    const res = await fetch('http://localhost:8000/api/vitalsign/connect/', {
      method: 'POST',
      body: JSON.stringify({
        dev: '2887'
      })
    })
    const result = await res.json()
    console.log(result)
    // 根据后端返回结果判断
    if (result.code === 200 || result.connect_status === 'success') {
      // 连接成功 → 绿色呼吸灯
      btStatus.value = 'connected'
      // 触发函数，每隔1秒更新一次请求一次后端的数据
      startDataPolling()
    } else {
      // 连接失败
      btStatus.value = 'disconnected'
      alert('Failed to connect to the device. Please check the device and try again.');
    }
  } catch (e) {
    // 失败 → 变回灰色
    alert('Failed to connect to the device. Please check your device and try again.');
    btStatus.value = 'disconnected'
  }
  // 组件卸载或断开连接时停止轮询
  const disconnectBluetooth = () => {
    stopDataPolling()
    btStatus.value = 'disconnected'
    // 也可以调用后端的断开接口
  }
}

// 切换下一名伤员时，关闭蓝牙连接并刷新页面
async function switchWounded() {
  // 如果灯不是绿色，则提示用户尚未连接，不能关闭
  if(btStatus.value !== 'connected') {
    alert('Please connect to the device first.');
    return;
  }
  else {
    console.log('Switching to next wounded patient...')
    const res = await fetch('http://localhost:8000/api/vitalsign/disconnect/', {
        method: 'POST',
        body: JSON.stringify({
          dev: '2887'
        })
    })
    const result = await res.json()
    if(result.connect_status === 'success') {
      stopDataPolling()
      btStatus.value = 'disconnected'
      // 等待逻辑结束 → 刷新页面
      setTimeout(() => {
        // 发送后端关闭蓝牙连接
        location.reload();
      }, 500);
    }
  }
}

// 伤部选择
const selectedAreas = ref([])

// 拍照
const img1 = ref(null)
const img2 = ref(null)
const img3 = ref(null)
const img4 = ref(null)
const imgRefs = [img1, img2, img3, img4]

function hasPhoto(imgRef) {
  const src = imgRef.value?.src || ''
  // 只有 base64 才算真正拍照
  return src.startsWith('data:image/')
}

function getCapturedPhotos() {
  const images = [img1, img2, img3, img4]
  return images
    .map(img => img.value?.src)
    .filter(src => src?.startsWith('data:image/')) // 只保留有效照片
}

// 保存伤员信息
async function saveWoundedInfo() {
  // 显示弹窗，正在上传
  const tipDom = document.getElementById('uploadTip')
  tipDom.style.display = 'inline'
  tipDom.innerText = 'Uploading...'
  tipDom.style.color = '#999'
  try {
    const woundinfo = {}
    // 获取伤员ID，如果没有，则提示用户，并中断保存
    woundinfo['wounded_id'] = document.getElementById('patient-id').value.trim();
    if (!woundinfo['wounded_id'] || woundinfo['wounded_id'] === '---') { alert('Please enter the patient ID.'); return;}
    // 获取位置坐标
    woundinfo['location'] = locationText.value;
    // 获取当前时间
    woundinfo['DateTime'] = currentTime.value;
    // 获取伤员性别
    woundinfo['gender'] = document.getElementById('gender').value.trim();
    // 获取伤员年龄
    woundinfo['age'] = document.getElementById('age').value.trim();
    // 获取伤员血型
    woundinfo['blood_type'] = document.getElementById('blood-type').value.trim();
    // 获取生理参数
    woundinfo['hr'] = document.getElementById('heart-rate').value.trim();
    woundinfo['pulse'] = document.getElementById('pulse').value.trim();
    woundinfo['breath'] = document.getElementById('respiratory-rate').value.trim();
    woundinfo['sysbp'] = document.getElementById('systolic-blood-pressure').value.trim();
    woundinfo['dbp'] = document.getElementById('diastolic-blood-pressure').value.trim();
    woundinfo['temp'] = document.getElementById('temperature').value.trim();
    // 获取神经体征 
    woundinfo['gcs_motor'] = document.getElementById('motor-response-score').value.trim();
    woundinfo['gcs_eye'] = document.getElementById('eye-opening-score').value.trim();
    woundinfo['gcs_verbal'] = document.getElementById('verbal-response-score').value.trim();
    // 获取其他信息
    woundinfo['chest_and_abdomen'] = document.getElementById('supplement').value.trim();
    console.log(woundinfo['chest_and_abdomen'])
    if (Number(woundinfo['chest_and_abdomen']) == 2 && woundinfo['chest_and_abdomen'] !== '') {
      woundinfo['chest_and_abdomen'] = 'No Tenderness Present'
    } else if (Number(woundinfo['chest_and_abdomen']) == 1 && woundinfo['chest_and_abdomen'] !== '') {
      woundinfo['chest_and_abdomen'] = 'Tenderness Present in the Chest or Abdomen'
    } else if (Number(woundinfo['chest_and_abdomen']) == 0 && woundinfo['chest_and_abdomen'] !== '') {
      woundinfo['chest_and_abdomen'] = 'Flail Chest, Plate-like Abdomen, or Penetrating Wound'
    }
    // 获取伤情评估结果
    woundinfo['RTS_res'] = RTS_res.value
    woundinfo['PHI_res'] = PHI_res.value
    woundinfo['CRAMS_res'] = CRAMS_res.value
    woundinfo['GCS_res'] = GCS_res.value
    woundinfo['ML_res'] = ML_res.value
    // 获取伤部信息
    woundinfo['wounded_areas'] = selectedAreas.value.join(',')
    // 获取拍照信息
    woundinfo['captured_photos'] = getCapturedPhotos()
    // 获取伤情描述
    // 语音输入信息
    woundinfo['description'] = document.getElementById('showText').innerText.trim()
    // 获取智能助手的建议
    woundinfo['suggestion'] = adviceText.value.trim()
    // 上传后端
    const res = await fetch('http://localhost:8000/api/saveInfo/', {
      method: 'POST',
      body: JSON.stringify(woundinfo)
    });
    // 等待响应
    const result = await res.json();
    if (result.status === 'success') {
      tipDom.innerText = 'Success'
      tipDom.style.color = '#00b42a'
  }} catch (err) {
    tipDom.innerText = 'Failed'
    tipDom.style.color = 'yellow'
  } finally {
    // 3秒后自动隐藏提示
    setTimeout(() => {
      tipDom.style.display = 'none'
    }, 3000)
  }
}

// 组件挂载时更新时间、获取当前位置
onMounted(() => {
  updateTime();
  getLocation();
  setInterval(updateTime, 1000);

  //----------------- 拍照摄像功能模块 -------------------------
  const video = document.getElementById('cameraVideo');
  const openCameraBtn = document.querySelector('.img-btn:nth-child(1)');
  const takePhotoBtn = document.querySelector('.img-btn:nth-child(2)');
  const photoImgs = document.querySelectorAll('.photo-item img');
  let photoIndex = 0;

  // 打开摄像头
  openCameraBtn.addEventListener('click', async () => {
    try {
      // 调用浏览器摄像头权限
      const stream = await navigator.mediaDevices.getUserMedia({
        video: true //开启视频
      });
      video.srcObject = stream;
      console.log('Camera opened successfully');
    } catch (error) {
      console.error('Error opening camera:', error);
      alert('Failed to open camera. Please check your permissions!');
    }
  })
  // 拍照功能模块
  takePhotoBtn.addEventListener('click', async () => {
    if(!video.srcObject) {
      alert('Please open the camera first.');
      return;
    }
    if(photoIndex >= 4) {
      // 询问是否重新拍照
      const confirmReset = confirm( "You have taken 4 photos already. \n Do you want to take new photos again?");
      // 如果确认重置
      if (confirmReset) {
        //清空4张图片
        photoImgs.forEach((img) => {
          img.src = '';
        });
        photoIndex = 0; //计数归零
      }
      return;
    }
    requestAnimationFrame(() => {
      const canvas = document.createElement("canvas");
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext("2d");
      // 画视频
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      // 生成正确图片地址
      const dataURL = canvas.toDataURL("image/png");
      // 赋值
      const imgList = document.querySelectorAll(".photo-item img");
      if (imgList[photoIndex]) {
        imgList[photoIndex].src = dataURL;
      }
      // 赋值给imgRefs
      imgRefs[photoIndex].value.src = dataURL
      photoIndex++;
    });
  })
  //----------------语音识别功能模块-----------------
  const voiceBtn = document.getElementById('voiceBtn');
  const showText = document.getElementById('showText');
  let mediaRecorder = null;
  let audioChunks = [];
  let isRecording = false;
  let startTime = 0; // 录音开始时间
  // 防止重复上传
  let isUploading = false;
  // 按住按钮：开始录音
  voiceBtn.addEventListener('mousedown', async () => {
    // 如果
    if (isRecording || isUploading) {
      // 停止录音
      try {
        if (mediaRecorder) {
          if (mediaRecorder.state !== 'inactive') {
            mediaRecorder.stop();
          }
        }
      } catch (error) {
        console.error('Error stopping recording:', error);
      }
      showText.innerText = 'Additionally information about the injury...';
    }
    try {
      // 1. 获取麦克风权限
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      // 2. 创建录音实例
      mediaRecorder = new MediaRecorder(stream);
      audioChunks = [];
      // 3.监听录音数据
      mediaRecorder.addEventListener('dataavailable', (e) => {
        audioChunks.push(e.data);
      });
      // 4.开始录音
      mediaRecorder.start();
      showText.innerText = 'Recording...';
      startTime = Date.now(); // 记录开始时间
      isRecording = true;
    } catch (error) {
      console.error('Error starting recording:', error);
      alert('Failed to start recording. Please check your permissions!');
    }
  });

  function stopRecordingAndUpload() {
    const duration = (Date.now() - startTime) / 1000; // 计算录音时长（秒）
    // 5. 停止录音
    try {
      if (mediaRecorder) {
        if (mediaRecorder.state !== 'inactive') {
          mediaRecorder.stop();
        }
      }
    } catch (error) {
      console.error('Error stopping recording:', error);
    }
    isRecording = false;
    // 上锁
    isUploading = true;
    if (duration < 1) {
      alert('Too short to record! Please try again.');
      mediaRecorder.addEventListener('stop', async() => {
        mediaRecorder.stream.getTracks().forEach(track => track.stop());
      }, { once: true })
      showText.innerText = 'Additionally information about the injury...';
      return;
    }
    else {
      // 6. 录音停止后，生成文件，上传后端
      mediaRecorder.addEventListener('stop', async () => {
        try {
          showText.innerText = 'Recording stopped. Uploading audio...';
          // 1.生成音频Blob
          const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
          // 2. 构建FormData上传文件
          const formData = new FormData();
          formData.append('audioFile', audioBlob, 'recording.webm');
          // 3.发送到后端
          const res = await fetch('http://localhost:8000/api/speechrecognition/', {
            method: 'POST',
            body: formData
          });
          // 4. 解析响应
          const result = await res.json();
          if (result.content == '') {
            showText.innerText = 'No recognizable speech detected. Please try again.';
            return;
          }
          console.log(result);
          showText.innerText = result.content;
        } catch (error) {
          console.error('Error uploading audio:', error);
          alert('Failed to upload audio. Please try again.');
        } finally {
          if (mediaRecorder?.stream) {
            // 7.关闭麦克风轨道
            mediaRecorder.stream.getTracks().forEach(track => track.stop());
          }
          mediaRecorder = null;
          isUploading = false; // 解锁
        }
      }, { once: true }); // 只执行一次，防止重复监听
    }
  }
  // 松开按钮停止
  voiceBtn.addEventListener("mouseup", () => {
    // 增加判断，只有正在录音的时候才执行
    if (isRecording && mediaRecorder) {
      stopRecordingAndUpload();
    }
  });
  // 鼠标移出按钮也停止
  voiceBtn.addEventListener("mouseleave", () => {
    if (isRecording && mediaRecorder) {
      // 停止录音
      try {
        if (mediaRecorder) {
          if (mediaRecorder.state !== 'inactive') {
            mediaRecorder.stop();
          }
        }
      } catch (error) {
        console.error('Error stopping recording:', error);
      }
      // 修改状态
      isRecording = false;
      // 关闭麦克风音频轨道
      mediaRecorder.stream.getTracks().forEach(track => track.stop());
      // 清空录音数据
      audioChunks = [];
      // 销毁实例
      mediaRecorder = null;
      // 提示用户
      alert('Recording cancelled, audio will not be sent');
      // 恢复默认文本
      showText.innerText = 'Additional information about the injury...';
    }
  });
  // ----------------- AI医生建议按钮 -------------------------
});
const isLoading = ref(false);
const showResult = ref(false);
const adviceText = ref(''); // 建议文字
// 打字机效果（逐字输出 + 自动滚动）
function typeText(text, speed = 50) {
  adviceText.value = '';
  let i = 0;
  const write = () => {
    if (i < text.length) {
      adviceText.value += text[i];
      i++;
      setTimeout(write, speed);
    }
  }
  write();
}

// 点击获取建议
async function getAdvice() {
  //图片屏蔽
  document.getElementById('aiIcon').style.display = 'none';
  isLoading.value = true
  showResult.value = false
  try {
    // 获取界面输入的内容
    // 伤部信息
    let description = '请根据我提供的伤员伤情，给出500字以内的英文院前紧急救治建议。伤员的基本信息为：'
    // 性别
    const gender = document.getElementById('gender').value
    // 如果值不为空，添加到描述中
    if (gender) {
      description += `性别：${gender},`
    }
    // 年龄
    const age = document.getElementById('age').value
    // 如果值不为空，添加到描述中
    if (age) {
      description += `年龄：${age},`
    }
    // 血型
    const bloodType = document.getElementById('blood-type').value
    if (bloodType) {
      description += `血型：${bloodType},`
    }
    // 生命体征信息
    // 心率
    const heartRate = document.getElementById('heart-rate').value
    if (heartRate != '--') {
      description += `心率：${heartRate},`
    }
    // 脉搏
    const pulse = document.getElementById('pulse').value
    if (pulse != '--') {
      description += `脉搏：${pulse},`
    }
    // 呼吸频率
    const respiratoryRate = document.getElementById('respiratory-rate').value
    if (respiratoryRate != '--') {
      description += `呼吸频率：${respiratoryRate},`
    }
    // 收缩压
    const systolicPressure = document.getElementById('systolic-blood-pressure').value
    if (systolicPressure != '--') {
      description += `收缩压：${systolicPressure},`
    }
    // 舒张压
    const diastolicPressure = document.getElementById('diastolic-blood-pressure').value
      if (diastolicPressure != '--') {
        description += `舒张压：${diastolicPressure},`
    }
    // 体温
    const temperature = document.getElementById('temperature').value
    if (temperature != '--') {
      description += `体温：${temperature},`
    }
    // 神经体征
    // eye-opening-score
    const eyeOpeningScore = document.getElementById('eye-opening-score').value
    if (eyeOpeningScore) {
      description += `睁眼反应评分：${eyeOpeningScore},`
    }
    // motor-response-score
    const motorResponseScore = document.getElementById('motor-response-score').value
    if (motorResponseScore) {
      description += `运动反应评分：${motorResponseScore},`
    }
    // verbal-response-score
    const verbalResponseScore = document.getElementById('verbal-response-score').value
    if (verbalResponseScore) {
      description += `语言反应评分：${verbalResponseScore},`
    }
    // other-information
    const otherInformation = document.getElementById('supplement').value
    if (otherInformation) {
      if (Number(otherInformation) == 2 && otherInformation !== '') {
        description += `胸腹部信息：No Tenderness Present,`
      } else if (Number(otherInformation) == 1 && otherInformation !== '') {
        description += `胸腹部信息：Tenderness Present in the chest or abdomen,`
      } else if (Number(otherInformation) == 0 && otherInformation !== '') {
        description += `胸腹部信息：Flail Chest, Plate-like Abdomen or Penetrating Wound,`
      }
    }
    // RTS评分
    const rtsScore = RTS_res.value
    if (rtsScore != '--') {
      description += `RTS评分：${rtsScore},`
    }
    // PHI评分
    const phiScore = PHI_res.value
    if (phiScore != '--') {
      description += `PHI评分：${phiScore},`
    }
    // CRAMS评分
    const cramsScore = CRAMS_res.value
    if (cramsScore != '--') {
      description += `CRAMS评分：${cramsScore},`
    }
    // GCS评分
    const gcsScore = GCS_res.value
    if (gcsScore != '--') {
      description += `GCS评分：${gcsScore},`
    }
    // ML评分
    const mlScore = ML_res.value
    if (mlScore != '--_--') {
      description += `机器学习模型评估的死亡率风险为：${mlScore.split('_')[0]},`
    }
    // 伤部信息,如果selectedArea不为空,添加到描述中
    const selectedArea = selectedAreas.value
    if (selectedArea != '') {
      description += `伤部：${selectedArea}。\n`
    }
    // 判断图片是否为拍照后的图片
    const photos = getCapturedPhotos()
    // 语音输入信息
    const injuryarea = document.getElementById('showText').innerText.trim()
    // 如果值不为空，添加到描述中
    if (injuryarea != 'Additional information about the injury...' && injuryarea != '') {
      description += `伤部：${injuryarea}。\n`
    }
    console.log(description)
    if (description != '' && description != '请根据我提供的伤员伤情，给出500字以内的院前紧急救治建议。伤员的基本信息为：')  {
      description += '综合以上所有的信息给出建议（如果有图片也要结合图片进行描述）。不要写多少字以内这种AI提示词'
      const res = await fetch('http://localhost:8000/api/digitaldoctor/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          question: description,
          photos: photos
        })
      })
      const result = await res.json()
      // 显示结果
      showResult.value = true
      typeText(result.content)
    } else {
      alert('Please supplement detailed wounded information...')
    }
  } catch (err) {
    console.error(err)
    adviceText.value = '获取建议失败，请重试'
    showResult.value = true
  } finally {
    isLoading.value = false
    
  }
}

</script>

<style scoped>

/* 弹窗遮罩 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  animation: fadeIn 0.25s ease;
}

/* 卡片弹窗（高级质感） */
.modal-card {
  width: 420px;
  max-width: 80vh;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  /* overflow: hidden; */
  animation: zoomIn 0.3s ease;
  display: flex;
  flex-direction: column;
}

.modal-body-wrapper {
  flex: 1;
  overflow-y: auto; /* 内容多了自动滚动 */
  padding: 0;
}

/* 头部 */
.modal-header {
  padding: 20px 24px;
  border-bottom: 1px solid #f1f5f9;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.modal-header h4 {
  margin: 0;
  font-size: 18px;
  color: #1e293b;
  font-weight: 600;
}

/* 关闭按钮 */
.close-btn {
  background: transparent;
  border: none;
  font-size: 20px;
  color: #64748b;
  cursor: pointer;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: 0.2s;
}
.close-btn:hover {
  background: #f1f5f9;
  color: #000;
}

/* 内容区 */
.modal-body {
  padding: 24px;
  color: #334155;
  line-height: 1.6;
  font-size: 15px;
}
.modal-body p {
  margin: 0 0 12px 0;
}
.modal-body ul {
  padding-left: 20px;
  margin: 10px 0;
}
.modal-body li {
  margin-bottom: 6px;
}

/* 提示小字 */
.tip {
  color: #4361ee;
  font-weight: 500;
  margin-top: 16px !important;
  font-size: 14px;
}

/* 动画 */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
@keyframes zoomIn {
  from { opacity: 0; transform: scale(0.9); }
  to { opacity: 1; transform: scale(1); }
}

/* 视频区域样式 */
.video-section {
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid #f1f5f9;
}
.video-title {
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 12px !important;
}
.video-container {
  width: 100%;
  height: 220px; /* 固定视频高度*/
  border-radius: 10px;
  overflow: hidden;
  background: #000;
}
.demo-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.triage-system-main {
  height: 100vh;
  background-color:rgb(224, 224, 224);
  font-family: 'Microsoft YaHei', Arial, sans-serif;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

.wounded-info-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex: 0 0 auto;
  background-color:rgb(134, 21, 21);
}

.header-title {
  width: 130px;
  font-size: 2rem;
  font-weight: bold;
  color: #f5f2f2;
  text-align: left;
  margin-left: 10px;
}

.header-left {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.button-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-right: 10px;
}
/* 蓝牙状态指示灯相关样式代码 */
/* 指示灯外层 */
.bluetooth-status {
  display: flex;
  align-items: center;
}

/* 指示灯圆点 */
.status-light {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  transition: all 0.3s ease;
}

/* 未连接：灰色 */
.status-light.gray {
  background: #acacac;
  background-color: #acacac;
  box-shadow: 0 0 6px #acacac;
}

/* 搜索中：橙色呼吸灯 */
.status-light.orange {
  background-color: #ed8936;
  animation: breathOrange 1.6s infinite ease-in-out;
}

/* 已连接：绿色呼吸灯 */
.status-light.green {
  background-color: #1bf049;
  animation: breathGreen 1.6s infinite ease-in-out;
}

/* 橙色呼吸 */
@keyframes breathOrange {
  0% { box-shadow: 0 0 15px #ed8936; opacity: 1; }
  50% { box-shadow: 0 0 5px #ed8936; opacity: 0.3; }
  100% { box-shadow: 0 0 15px #ed8936; opacity: 1; }
}

/* 绿色呼吸 */
@keyframes breathGreen {
  0% { box-shadow: 0 0 15px #38a169; opacity: 1; }
  50% { box-shadow: 0 0 10px #38a169; opacity: 0.8; }
  100% { box-shadow: 0 0 15px #38a169; opacity: 1; }
}

.fun-button {
  display: inline-block;
  margin: 0 5px;
  font-weight: bold;
  cursor: pointer;
  color: white;
}

.fun-button:hover {
  color: orange !important;
}

.button-separator {
  margin: 0 10px;
}

/* 设置位于右侧 */
.time-location {
  font-weight: bold;
  margin-right: 10px;
  color: white;
}

.main-content {
  flex: 1;
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 2fr);
  gap: 1.0rem;
  padding: 0.5rem;
  position: relative;
  z-index: 5;
  min-height: 0;
  overflow: hidden;
  color: rgb(134, 21, 21);
}

.triage-classification {
  border: 1px solid rgb(134, 21, 21);
  padding: 12px 15px;
  border-radius: 10px;
}

.emergency-care {
  border: 1px solid rgb(134, 21, 21);
  border-radius: 10px;
  padding: 12px 15px;
}

.ia-section-title {
  text-align: center;
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  background-color: rgb(134, 21, 21);
  color: white;
}

.care-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.0rem;
  height: 93%;
}

/* 左侧分为2个部分 */
.care-left {
  display: flex;
  flex-direction: column;
  gap: 1rem;

}

.care-box {
  flex: 1;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1rem;
  background: #fafafa;
  padding-top: 0.5rem;
}

/* 帮助图标样式 */
.evaluate-btn-wrap {
  width: 15%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.h3-wrap {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.help-icon {
  width: 18px;
  height: 18px;
  line-height: 18px;
  text-align: center;
  background: #991b1b;
  color: #fff;
  border-radius: 50%;
  font-size: 14px;
  cursor: pointer;
  flex-shrink: 0;
}
/* 人口统计学信息 */
.grid-form {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px 8px;
  margin-top: 8px;
  margin-bottom: 10px;
}
.form-item {
  display: flex;
  align-items: center;
  gap: 6px;
}
.form-item label {
  width: 85px;
  color: black;
  font-size: 14px;
}
.default-option {
  color: #808080;
}
.default-option:valid {
  color: #070707 !important;
}
.form-item input {
  flex: 0.9;
  padding: 4px 8px;
  background-color: #ffffff;
  border: 1px solid rgb(134, 21, 21);
  border-radius: 4px;
  outline: none;
  color: black;
}
.form-item select {
  flex: 0.9;
  padding: 4px 8px;
  background-color: #ffffff;
  border: 1px solid rgb(134, 21, 21);
  border-radius: 4px;
  outline: none;
  color: black;
}
.form-item-other {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 8px;
  margin-bottom: 20px;
}
.form-item-other label {
  width: 25%;
  color: black;
  font-size: 14px;
}
.form-item-other select {
  flex: 0.8;
  padding: 4px 8px;
  background-color: #ffffff;
  border: 1px solid rgb(134, 21, 21);
  border-radius: 4px;
  outline: none;
  color: black;
}
.default-option {
  color: #808080;
}
.default-option:valid {
  color: #070707 !important;
}

/* 生命体征信息 */
.grid-form-vital {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px 8px;
  margin-top: 8px;
  margin-bottom: 10px;
}
.vital-form-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.vital-form-item label {
  width: 40px;
  color: black;
  font-size: 14px;
  white-space: nowrap;
}

.vital-form-item input {
  width: 120px;
  padding: 4px 8px;
  background-color: #fff;
  border: 1px solid rgb(134, 21, 21);
  border-radius: 4px;
  outline: none;
  text-align: center;
  color: black;
}

/* 神经学征信息 */
.grid-form-ns {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px 8px;
  margin-top: 8px;
  margin-bottom: 20px;
}

.ns-form-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.ns-form-item label {
  color: black;
  font-size: 14px;
  white-space: nowrap;
}

.ns-form-item select {
  width: 90%;
  padding: 3px 6px;
  background-color: #fff;
  border: 1px solid rgb(134, 21, 21);
  border-radius: 4px;
  outline: none;
}
/* 智能检伤分类表格 */
.evaluate-btn {
  padding: 6px 14px;
  background: rgb(134, 21, 21) !important;
  background-color: rgb(134, 21, 21) !important;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}
.triage-table {
  margin-top: 15px;
  width: 100%;
  min-height: 310px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  padding: 1rem;
  position: relative;
  overflow: hidden;
  background: #fff;
  border: 3px dashed rgb(134, 21, 21);
}

/* 聊天框样式设计 */
/* 右侧聊天框 */
.care-chat {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1rem;
  background: white;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 10%;
}
.top-content {
  width: 100%;
  height: 80%;
  background-color: white;
  display: flex;
  justify-content: center;
  align-items: center;
}

.ai-doctor-box {
  width: 90%;
  height: 90%;
  display: flex;
  align-items: center;;
  margin-bottom: 10px;
}
.ai-doctor-icon {
  display: flex;
  justify-content: center;
  align-items: center;
}
.ai-doctor-icon img {
  width: 70%;
  height: 50%;
  opacity: 0.3;
}
.loading-tip {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: bold;
  animation: textColorWave 1.8s infinite ease-in-out;
}
@keyframes textColorWave {
  0% { color: #a9b318; }
  50% { color: #e63939; }
  100% { color: #18b33f; }
}
/* 建议区域 上侧展示 超出自滚动 */
.advice-container {
  margin-top: 5%;
  padding: 12px;
  width: 100%;
  max-height: 60vh; 
  overflow-y: auto;
  border-radius: 6px;
  line-height: 1.6;
}
/* 滚动条滑块（红色） */
.advice-container::-webkit-scrollbar-thumb {
  background-color: #861515; /* 深红色，和你的按钮颜色一致 */
  border-radius: 10px;
}
/* 滚动条hover效果 */
.advice-container::-webkit-scrollbar-thumb:hover {
  background-color: #a51a1a;
}
/* 按钮单独放最底部 */
.btn-bottom-wrap {
  width: 100%;
  display: flex;
  justify-content: center;
}
.breath-btn {
  padding: 14px 28px;
  font-size: 16px;
  font-weight: 600;
  color: #fff;
  background: rgb(134, 21, 21) !important;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  animation: breathGlow 2.2s infinite ease-in-out;
}

@keyframes breathGlow {
  0% { box-shadow: 0 0 8px rgba(200,28,28,0.4); background-color: #b31818; }
  50% { box-shadow: 0 0 22px rgba(175, 20, 20, 0.75); background-color: #c81c1c; }
  100% { box-shadow: 0 0 8px rgba(200,28,28,0.4); background-color: #b31818; }
}

.injury-area {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  justify-content: flex-start;
  gap: 12px 10px;
  margin-top: 2%;
  margin-left: 8%;
}

.radio-item {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  font-size: 14px;
  color: #333;
}

.radio-item input[type="radio"] {
  accent-color: rgb(134, 21, 21);
  width: 16px;
  height: 16px;
}

.injury-area input[type="checkbox"]:checked {
  accent-color: rgb(134, 21, 21);
}

/* 图像数据采集按钮组 */
.box-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.btn-group {
  display: flex;
  gap: 8px; /* 按钮之间间距 */
}

.img-btn {
  background: rgb(134, 21, 21) !important;
  background-color: rgb(134, 21, 21) !important;
  background-image: none !important;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  white-space: nowrap;
}

.img-btn:hover {
  opacity: 0.9;
}

/* 视频区域内容调整 */
.image-preview-layout {
  display: grid;
  grid-template-columns: 3fr 2fr; /* 3/5 和 2/5 分配 */
  gap: 12px;
  width: 100%;
  min-height: 260px;
}

.video-area {
  position: relative;
  width: 100%;
  height: 100%;
  background: #000;
  border: 2px solid rgb(134, 21, 21);
  border-radius: 6px;
  overflow: hidden;
  display: flex;
  align-items: top;
  justify-content: center;
}

.video-area video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.video-area .placeholder {
  position: absolute;
  color: #fff;
  font-size: 16px;
  opacity: 0.8;
}

/* 右侧 2行2列 图片网格 */
.photo-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 8px;
  height: 100%;
}

.photo-item {
  position: relative;
  background: #f8f8f8;
  border: 2px solid rgb(134, 21, 21);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.photo-item img[src=""] {
  width: 100%;
  height: 100%;
  object-fit: cover;
  content: url("../assets/empty.png"); 
}

.photo-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* 语音识别区域 */
/* 标题行：左边标题 右边按钮 */
.supp-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

/* 语音按钮 */
.voice-btn {
  padding: 6px 12px;
  background: rgb(134, 21, 21) !important;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

/* 底部可编辑文字区域 */
.show-text {
  min-height: 150px;
  padding: 12px 14px;
  border: 1px solid rgb(134, 21, 21);
  border-radius: 6px;
  background: #fdf5f5;
  font-size: 14px;
  line-height: 1.6;
  outline: none;
  white-space: pre-wrap;
  text-align: left;
}

/* 点击编辑时的样式 */
.show-text:focus {
  background: #fff;
  border-color: rgb(134, 21, 21);
}

</style>
