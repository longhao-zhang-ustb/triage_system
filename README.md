# DP-PTE 一种用于院前检伤急救的数字医生软件
> 本软件提供了一种面向自然灾害等伤亡现场的快速检伤救援平台，实现了快速伤情感知、智能化检伤分类和紧急医疗建议的生成等核心功能

[![版本](https://img.shields.io/badge/Version-1.0.0-blue)](https://github.com/longhao-zhang-ustb/triage_system)
[![构建状态](https://img.shields.io/badge/Build-Passing-brightgreen)](https://img.shields.io/badge/Build-Passing-brightgreen))
[![许可证](https://img.shields.io/badge/License-Apache--2.0-green))](LICENSE)

![软件主界面](front_end/src/assets/Intelligent_Triage_and_Emergency_Care_System.png)

## 📑 目录
- [项目介绍](#-项目介绍)
- [核心功能](#-核心功能)
- [运行环境与依赖](#-运行环境与依赖)
- [配置说明](#-配置说明)
- [开源许可](#-开源许可)
- [联系方式](#-联系方式)

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

