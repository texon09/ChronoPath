# Nomad Notes - Deployment Guide

This guide details the **100% Free Monorepo Deployment** using Vercel. 

Both the Next.js Frontend and the FastAPI Backend will be deployed on Vercel together. Vercel recently upgraded their free "Hobby" tier timeout limit to 5 minutes, which means it can comfortably handle our AI agents without crashing!

## 1. Architecture Overview
- **Frontend (Next.js):** Deployed to Vercel (Edge network).
- **Backend (FastAPI):** Deployed to Vercel as a Serverless Python Function.
- **Caching & Rate Limiting:** Upstash Redis.
- **Database:** Supabase PostgreSQL.

*(Total Cost: $0, No Credit Card Required)*

## 2. Setting Up Upstash Redis
1. Go to [Upstash.com](https://upstash.com) and create a free Redis database.
2. Select **us-central1**, turn on **Eviction**, and click Create.
3. Under the database settings, scroll down to the **Connect** section.
4. Select **Python (redis-py)** and copy the connection string.
   - It will look like: `rediss://default:password@endpoint-url.upstash.io:30000`
5. Save this string, you will need it for Vercel.

## 3. Deploying Everything to Vercel
We have configured a `vercel.json` file in the root of the repository that automatically tells Vercel how to build both the frontend and the Python backend simultaneously.

1. Go to [Vercel.com](https://vercel.com) and create a free account.
2. Click **Add New... -> Project**.
3. Import the `ChronoPath` repository from your GitHub.
4. **IMPORTANT CONFIGURATION:**
   - **Framework Preset:** Leave it as "Other" (Vercel will read our `vercel.json`).
   - **Root Directory:** Leave it as the default `./` (Do not select frontend!).
5. Open the **Environment Variables** dropdown and add ALL your secrets:
   - `GOOGLE_API_KEY`: Your Gemini API Key
   - `GOOGLE_MAPS_API_KEY`: Your Maps API Key
   - `REDIS_URL`: Your Upstash connection string
   - `DATABASE_URL`: Your Supabase Postgres URL
   - `NEXT_PUBLIC_FIREBASE_API_KEY`: Your Firebase keys...
6. Click **Deploy**.

## 4. How It Works
- Vercel will look at `vercel.json` and build your React app from the `frontend/` folder.
- It will then take your `api/main.py` file, install `requirements.txt`, and turn it into a Serverless Python backend.
- Any request to `your-app.vercel.app/api/...` will automatically be routed to your Python FastAPI server!
