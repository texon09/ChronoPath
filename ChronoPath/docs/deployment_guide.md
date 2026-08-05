# Nomad Notes - Deployment Guide

This guide details the Zero-Cost Hybrid Deployment strategy (Vercel + Render) to host Nomad Notes in a production environment.

## 1. Architecture Overview
- **Frontend (Next.js):** Deployed to Vercel (Edge network, fastest load times, 100% free).
- **Backend (FastAPI):** Deployed to **Hugging Face Spaces** using the "Gradio" workaround (100% free, **no credit card required**).
- **Caching & Rate Limiting:** Upstash Redis (Serverless Redis, Generous free tier).
- **Database:** Supabase PostgreSQL (Free tier).

## 2. Setting Up the Backend (Hugging Face Spaces)
Because Docker Spaces are now a paid feature on Hugging Face, we will use the free **Gradio SDK** as a loophole to host our FastAPI backend!

1. Create a free account on [HuggingFace.co](https://huggingface.co/join).
2. Click your profile picture -> **New Space**.
3. **Space Name:** `nomad-notes-backend`
4. **License:** MIT
5. **Select the Space SDK:** Choose **Gradio**.
6. **Space Hardware:** Free (CPU basic).
7. Click **Create Space**.
8. Go to the **Settings** tab of your new Space, scroll down to **Variables and secrets**, and add your New Secrets:
   - `GOOGLE_API_KEY`: Your Gemini API Key
   - `GOOGLE_MAPS_API_KEY`: Your Maps API Key
   - `REDIS_URL`: (From Upstash)
   - `DATABASE_URL`: (From Supabase)
9. Clone the space locally or use the "Files" tab to upload your backend files (or connect it to your GitHub). The repository now includes an `app.py` file which will automatically trick Hugging Face into launching your FastAPI backend instead of a Gradio app!

## 3. Setting Up Upstash Redis (For Caching & Rate Limiting)
Since we are using the free tier of the Gemini API (which is strictly capped at 15 RPM), we MUST use a Redis layer to enforce global rate limits and cache requests to prevent crashes.

1. Go to [Upstash.com](https://upstash.com) and create a free Redis database.
2. Under the database settings, scroll down to the **Connect** section.
3. Select **Python (redis-py)** and copy the connection string.
   - It will look like: `rediss://default:password@endpoint-url.upstash.io:30000` (Note the `rediss://` for TLS)
4. Add this string as `REDIS_URL` to your Render backend.

## 4. Setting Up the Frontend (Vercel)
1. Go to [Vercel.com](https://vercel.com) and create a new project.
2. Import the `ChronoPath` repository.
3. **Framework Preset:** Next.js
4. **Root Directory:** `frontend/`
5. **Environment Variables:**
   - `NEXT_PUBLIC_API_URL`: The URL of your deployed Render backend (e.g., `https://nomadnotes-backend.onrender.com`)
   - `NEXT_PUBLIC_FIREBASE_API_KEY`: Your Firebase client keys...

6. Click **Deploy**.

## 5. Security & Rate Limiting Details
- **CORS:** The backend is configured in `api/main.py` to only allow requests from Vercel. Be sure to update the `allow_origins` array with your actual Vercel domain once it is generated.
- **Rate Limit:** The backend enforces a strict maximum of 12 requests per minute globally. If multiple users attempt to generate a story at once, they will receive a 429 status code ("High traffic! Please wait 60 seconds").
- **Caching:** Identical requests (same coordinates and interests) bypass the AI completely and are served directly from the Redis cache instantly for 24 hours.
