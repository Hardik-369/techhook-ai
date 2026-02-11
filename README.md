# TechHook AI

Automated Creator-to-LinkedIn Amplifier.

## Features
- **RSS Monitoring**: Polls YouTube feeds for new uploads.
- **AI Content**: Transforms transcripts into high-engagement LinkedIn posts.
- **Hook Images**: Generates bold, mobile-optimized images locally.
- **Automation**: Runs every 5 minutes via GitHub Actions.

## Setup

### Backend
1. `cd backend`
2. `pip install -r requirements.txt`
3. `playwright install chromium`
4. Set `GEMINI_API_KEY` environment variable.

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

## Deployment
- **Frontend**: Vercel
- **Automation**: GitHub Actions
