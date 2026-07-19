# Features & Usage Guide

ChronoPath AI transforms your physical location into an immersive, historically accurate narrative using Agentic AI. 

## Features

### 1. Location-Aware Historical Generation
The app reads your device's GPS coordinates and reverse-geocodes them into a specific, historically relevant landmark or area. It uses **Contextual Scoping** to guarantee it is writing a story about your exact physical location, avoiding AI hallucinations about cities with the same name.

### 2. Personalized Narratives
You can specify your age, background, and origin. The **Narrative Agent** dynamically weaves this context into the generated story. For example, if you are an architect from London visiting Rome, the story will focus heavily on comparative structural engineering and building techniques.

### 3. Agentic RAG & Review
Before a story is presented to you, it must pass a **Reviewer Agent**. This agent analyzes the initial draft for historical inaccuracies and forces a rewrite if the AI hallucinates dates or facts. Furthermore, a **Safety Agent** ensures that no harmful prompt injections or PII leak into the prompt stream.

### 4. Cinematic Media Generation
ChronoPath AI does not just give you text. The **Media Agent** translates the historical themes of your location into a cinematic visual prompt, fetching a high-quality AI-generated image to accompany your story.

### 5. Semantic Journey Tracking
As you use the app, it saves your locations and topics to a PostgreSQL database. When you visit a new place, the **Context Agent** performs a vector-based semantic search across your past stories to draw callbacks and connections to places you've been before.

## Usage Guide

1. **Sign In**: Upon opening `http://localhost:3000`, click **Start Journey**. A beautiful glassmorphism popup will prompt you to authenticate via Google Firebase.
2. **Grant Location Access**: Your browser will ask for location permissions. You must allow this for the app to function.
3. **Set Persona**: In the Profile tab, fill out your Age, Origin, and Professional Background to customize your stories.
4. **Generate**: Click **Start Journey** on the home screen. A loading sequence will initiate while the backend agents fetch geography data, draft the story, review it, and generate images.
5. **Explore**: Once completed, a rich markdown-formatted story and cinematic image will be presented to you!
