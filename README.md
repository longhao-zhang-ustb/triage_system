# DP-PTE---Digital Physician Software for Pre-Hospital Triage and Emergency Care
> This software provides a rapid triage and rescue platform designed for disaster sites and other scenes of mass casualty incidents, offering core functionalities such as rapid casualty detection, intelligent triage classification, and the generation of emergency medical recommendations.

[![Version](https://img.shields.io/badge/Version-1.0.0-blue)](https://github.com/longhao-zhang-ustb/triage_system)
[![Build](https://img.shields.io/badge/Build-Passing-brightgreen)](https://img.shields.io/badge/Build-Passing-brightgreen))
[![License](https://img.shields.io/badge/License-Apache--2.0-green))](LICENSE)

![Main Interface](front_end/src/assets/Intelligent_Triage_and_Emergency_Care_System.png)

## 📑 Content
- [Project Overview](#-Project Overview)
- [Core Features](#-Core Features)
- [Runtime Environment and Dependencies](#-Runtime Environment and Dependencies)
- [Configuration Guide](#-Configuration Guide)
- [Open Source License](#-Open Source License)
- [Contact Information](#-Contact Information)

## 📖 项目介绍
本软件是一款WEB应用程序，专为院前紧急医疗服务人员设计，支持与可穿戴体征检测装置的无线通信，无需复杂代码，开箱即用。

## ✨ 核心功能
- 功能1：提供可穿戴设备无线通信接口，支持多维生命体征的动态获取，包括心率、呼吸率、脉搏、血压、体温等
- 功能2：支持多类别伤情数据的快捷记录，提供伤情图像拍摄功能，提供语音识别接口
- 功能3：支持包括RTS，CRAMS，PHI, GCS等传统医学量表的智能化计算和基于XGBOOST模型的死亡率计算
- 功能4：支持基于大模型生成紧急救援策略
- 功能5：支持现场伤情数据等内容的存储，提供Neo4j图数据库存储功能

## 🧰 运行环境与依赖
- 推荐使用Chrome浏览器

### 软件依赖
- 包括numpy=2.2.6, openai=2.37.0, pandas=2.3.3, requests=2.33.1, scikit-learn=1.7.2, scipy=1.15.3, xgboost=3.2.0, websocket=0.2.1
- 编程语言工具等包括HTML, CSS, JavaScript, Python, Visual Studio Code, Vue, Django, Neo4j

## 配置说明
- Web端依赖的安装`npm install package_name`, 服务端为`pip install module_name`, 通过上述指令完成相关依赖的配置
- 前端运行指令为`npm run dev`
- 服务端运行指令为`python manage.py runserver`
- 数据库启动指令`neo4j.bat console`

## 开源许可
本项目基于 **Apache License 2.0** 开源。

## 联系方式
如有任何问题，随时欢迎与我们联系
