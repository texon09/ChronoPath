# Local Setup & Installation Guide

Welcome to ChronoPath AI! This guide will help you set up the project locally for development.

## Prerequisites
- Node.js (v18+)
- Python (3.10+)
- PostgreSQL (v14+) running locally or via Docker
- A Firebase Project with Authentication enabled
- A Google Cloud Project with the Maps and Gemini APIs enabled

## 1. Clone the Repository
```bash
git clone https://github.com/texon09/ChronoPath.git
cd ChronoPath
```

## 2. Backend Setup (FastAPI)
ChronoPath AI uses Python and FastAPI for the agentic backend.

### Virtual Environment
```bash
python -m venv .venv
# Windows:
.\.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Backend Environment Variables
Create a `.env` file in the root `ChronoPath` directory:
```env
# API Keys
GOOGLE_API_KEY="your_gemini_api_key_here"
GOOGLE_MAPS_API_KEY="your_google_maps_api_key_here"

# Database
DATABASE_URL="postgresql+asyncpg://postgres:password@localhost:5432/chronopath"

# Firebase (ensure firebase-admin.json is downloaded from your Firebase console)
GOOGLE_APPLICATION_CREDENTIALS="firebase-admin.json"
```
Place your `firebase-admin.json` service account file in the root directory.

### Start the Backend
```bash
uvicorn api.main:app --port 8000 --reload
```

## 3. Frontend Setup (Next.js)
Navigate into the `frontend` directory.

### Install Dependencies
```bash
cd frontend
npm install
```

### Frontend Environment Variables
Create a `.env.local` file inside the `frontend/` directory:
```env
NEXT_PUBLIC_API_URL="http://localhost:8000"

# Firebase Config (from your Firebase Console)
NEXT_PUBLIC_FIREBASE_API_KEY="your_api_key"
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN="your_project_id.firebaseapp.com"
NEXT_PUBLIC_FIREBASE_PROJECT_ID="your_project_id"
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET="your_project_id.appspot.com"
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID="your_sender_id"
NEXT_PUBLIC_FIREBASE_APP_ID="your_app_id"
```

### Start the Frontend
```bash
npm run dev
```
The app will be available at `http://localhost:3000`.
