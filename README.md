---
title: Menanam AI
emoji: 🌱
colorFrom: green
colorTo: blue
sdk: docker
pinned: false
---

# Menanam AI

AI-powered agricultural assistant built with FastAPI, RAG, and Streamlit.

🌾 Menanam AI

An Intelligent AI-Powered Decision Support System for Indonesian Agriculture

Menanam AI is an end-to-end agricultural AI platform that combines Machine Learning, Retrieval-Augmented Generation (RAG), and Large Language Models (LLMs) to assist farmers, researchers, and agricultural practitioners in making data-driven farming decisions.

The application provides:

🌾 Crop productivity prediction
🤖 AI agricultural assistant
🌦 Historical weather integration
📍 Location-based prediction
📚 Knowledge retrieval from agricultural documents
🌐 Internet search fallback for up-to-date information
✨ Features
🌾 Crop Productivity Prediction

Predict crop productivity using historical weather conditions and machine learning.

Features:

Location-based prediction
Interactive map
Automatic coordinates
Historical weather lookup
Manual weather input
Estimated harvest calculation

🤖 AI Knowledge Assistant
An AI chatbot powered by Hybrid RAG.

Capabilities:
Agricultural consultation
Disease identification guidance
Cultivation practices
Fertilizer recommendations
Pest management
Internet fallback for current information

📍 Historical Weather Integration
Automatically retrieves historical weather based on selected district.

Weather variables include:
Temperature
Maximum Temperature
Minimum Temperature
Rainfall
Humidity
Wind Speed
Solar Radiation

⚡ FastAPI Backend
REST API for:
Productivity Prediction
AI Assistant
Health Check

🏗 System Architecture
                User

                  │

      Streamlit Frontend

      ┌─────────┴─────────┐

Prediction            AI Assistant

      │                     │

Historical Weather     Hybrid RAG

      │                     │

Machine Learning      Chroma Vector DB

      │                     │

XGBoost Model      Gemini + Internet Search

      └─────────┬──────────┘

            FastAPI Backend

🛠 Tech Stack
## Frontend
Streamlit

## Backend
FastAPI
Uvicorn

## Machine Learning
XGBoost
Scikit-Learn
Pandas
NumPy

## LLM
Google Gemini

## Embedding
intfloat/multilingual-e5-base

## Vector Database
ChromaDB

## Visualization
Folium
Streamlit-Folium

## Deployment
Streamlit Community Cloud

🚀 Installation
git clone https://github.com/USERNAME/menanam-ai.git
cd menanam-ai

Create virtual environment
python -m venv venv
Windows
venv\Scripts\activate

Install dependencies
pip install -r requirements.txt

⚙ Environment Variables
Create .env

GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY

FASTAPI_URL=http://localhost:8000
▶ Run Backend
uvicorn app.main:app --reload
Swagger

http://localhost:8000/docs
▶ Run Frontend
cd frontend
streamlit run Home.py
🤖 Machine Learning Pipeline

The productivity prediction model was trained using historical agricultural and weather datasets.

Input Features
Crop Type
Temperature
Maximum Temperature
Minimum Temperature
Rainfall
Humidity
Wind Speed
Solar Radiation
Model

XGBoost Regressor

Output
Productivity (quintal/hectare)
Estimated Harvest (ton)


📚 RAG Pipeline
Question

↓

Embedding

↓

ChromaDB Retrieval

↓

Similarity Check

↓

Knowledge Base

or

Internet Search

↓

Gemini

↓

Answer


📊 Dataset
The project utilizes multiple agricultural datasets including:

Historical Weather Dataset
Crop Productivity Dataset
Agricultural Knowledge Base
Geographic Coordinates Dataset

📸 Demo
Home
Prediction
AI Assistant
About

🚀 Future Work
Crop Recommendation
NASA POWER API Integration
Sentinel-2 Satellite Monitoring
NDVI Analysis
Prediction History
Farmer Dashboard
Mobile Application
Fertilizer Recommendation System

## Future Deployment
Docker (Frontend)
Render (Backend)

👨‍💻 Author
Hilmi Aji
Bachelor of Agricultural Engineering
Bandung Institute of Technology (ITB)
