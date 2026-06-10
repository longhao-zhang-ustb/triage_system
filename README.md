# DP-PTE---Digital Physician Software for Pre-Hospital Triage and Emergency Care
> This software provides a rapid triage and rescue platform designed for disaster sites and other scenes of mass casualty incidents, offering core functionalities such as rapid casualty detection, intelligent triage classification, and the generation of emergency medical recommendations.

[![Version](https://img.shields.io/badge/Version-1.0.0-blue)](https://github.com/longhao-zhang-ustb/triage_system)
[![Build](https://img.shields.io/badge/Build-Passing-brightgreen)](https://img.shields.io/badge/Build-Passing-brightgreen))
[![License](https://img.shields.io/badge/License-Apache--2.0-green))](LICENSE)

![Main Interface](front_end/src/assets/Intelligent_Triage_and_Emergency_Care_System.png)

## 📑 Table of Contents
- [Introduction](#Introduction)
- [Features](#Features)
- [Dependencies](#Dependencies)
- [Configuration](#Configuration)
- [License](#License)
- [Contact](#Contact)

## 📖 Introduction
This software is a web application designed specifically for pre-hospital emergency medical personnel. It supports wireless communication with wearable vital signs monitoring devices and requires no complex coding—it’s ready to use right out of the box.

## ✨ Features
- Feature 1: Provides a wireless communication interface for wearable devices, supporting the dynamic acquisition of multi-dimensional vital signs, including heart rate, respiratory rate, pulse, blood pressure, and body temperature
- Feature 2: Supports quick recording of various types of injury data, provides an injury image capture function, and offers a voice recognition interface
- Feature 3: Supports intelligent calculation of traditional medical scales such as RTS, CRAMS, PHI, and GCS, as well as mortality rate calculation based on the XGBOOST model
- Feature 4: Supports the generation of emergency response strategies based on large language models
- Feature 5: Supports the storage of on-site injury data and other content, and provides Neo4j graph database storage functionality

## 🧰 Dependencies
- We recommend using the Chrome browser
- Includes numpy=2.2.6, openai=2.37.0, pandas=2.3.3, requests=2.33.1, scikit-learn=1.7.2, scipy=1.15.3, xgboost=3.2.0, websocket=0.2.1
- Programming language tools and others include HTML, CSS, JavaScript, Python, Visual Studio Code, Vue, Django, and Neo4j

## 🤖 Configuration
- To install dependencies for the web frontend, use `npm install package_name`; for the backend, use `pip install module_name`. Use these commands to configure the relevant dependencies.
- The command to run the frontend is `npm run dev`.
- The command to run the backend is `python manage.py runserver`.
- The command to start the database is `neo4j.bat console`.

## 📕 License
This project is open-source under the **Apache License 2.0**.

## 📞 Contact
If you have any questions, please feel free to contact us at any time.
