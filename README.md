# AIRGUARD - AQI Prediction & Health Advisory System

AirGuard is a production-ready AI system that predicts Air Quality Index (AQI) using XGBoost and provides personalized health advice through a modern web interface and chatbot.

## Features
- **AQI Prediction**: XGBoost ML model trained on synthetic historical data (extensible to real data).
- **Health Engine**: Rule-based health advice for different demographics.
- **Chatbot**: Interactive assistant for AQI queries.
- **Modern UI**: Glassmorphism design using React + Vite.
- **Robust Backend**: FastAPI with production-ready structure.

## Folder Structure
```
AirGuard/
├── backend/            # FastAPI Application
├── frontend/           # React + Vite Frontend
├── ml_engine/          # Machine Learning scripts
├── deploy/             # Dockerfiles
├── docker-compose.yml  # Container Orchestration
└── requirements.txt    # Python Dependencies
```

## Setup Instructions

### Prerequisites
- Python 3.9+
- Node.js 18+
- Docker (optional)

### Quick Start (Local)

1. **Backend Setup**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or .\venv\Scripts\activate on Windows
   pip install -r requirements.txt
   
   # Train Model
   python ml_engine/train_model.py
   
   # Run Server
   uvicorn backend.main:app --reload
   ```

2. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Docker Deployment**:
   ```bash
   docker-compose up --build
   ```

## APIs
- `POST /api/predict-aqi`: Get AQI prediction.
- `POST /api/chatbot`: Chat with assistant.
- `GET /api/health-advice`: Get advice rules.

## Tech Stack
- **ML**: XGBoost, Scikit-learn, Pandas
- **Backend**: FastAPI, Python
- **Frontend**: React, Vite, Lucide, Recharts
- **DevOps**: Docker, Nginx

---
Built by [Your Name]
