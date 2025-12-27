# Gospel Study Assistant - LDS AI Study Pl### Come Follow Me Study System
- **💭 Daily Thought**: Pre-generated daily spiritual insights for each day of the year (364 total)
- **🎙️ Podcast Scripts**: P### Come Follow Me System
| Endpoint | Method | Requires | Description |
|----------|--------|----------|-------------|
| `/cfm/deep-dive` | POST | XAI_API_KEY | Study guides (Essential/Connected/Scholarly) |
| `/cfm/lesson-plans` | POST | XAI_API_KEY | Teaching materials (Adult/Youth/Children) |
| `/cfm/core-content` | POST | XAI_API_KEY | Raw CFM materials |
| `/tts/generate` | POST | GCP Auth | Basic text-to-speech |
| `/tts/podcast` | POST | GCP Auth | TTS with intro/outro music (15s/20s) |rated podcast episodes for all weeks and study levels (instant loading)
- **🎯 Three Study Types**: Deep Dive Study, Lesson Plans, Core Content
- **📊 Three Study Levels**: Essential, Connected, Scholarly
- **🎵 Audio Generation**: Google Cloud TTS with 6 Chirp 3 HD voices + intro/outro music
- **🎶 Podcast Audio**: 15s intro (fade-in) + voice content + 20s outro (10s fade-in)

> **Production-ready LDS AI Scripture Study App with complete Come Follow Me system**

## 🚀 Live Deployments
- **🌐 Fronte### Come Follow Me System
| Endpoint | Method | Requires | Description |
|----------|--------|-# Test CFM Deep Dive
curl -X POST "https://gospel-guide-api-273320302933.us-central1.run.app/cfm/deep-dive" \
  -H "Content-Type: application/json" \
  -d '{"week_number": 2, "study_level": "essential"}'

# Test TTS with Voice Selection
curl -X POST "https://gospel-guide-api-273320302933.us-central1.run.app/tts" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "voice": "Kore"}'

# Test Q&A Search------------|
| `/cfm/deep-dive` | POST | XAI_API_KEY | Study guides (Essential/Connected/Scholarly) |
| `/cfm/lesson-plans` | POST | XAI_API_KEY | Teaching materials (Adult/Youth/Children) |
| `/cfm/core-content` | POST | XAI_API_KEY | Raw CFM materials |
| `/tts` | POST | GCP Auth | Text-to-speech with voice selection |

### Static Content (Pre-Generated)
| Path | Description |
|------|-------------|
| `/podcasts/podcast_week_XX_level.json` | Pre-generated podcast scripts |
| `/daily_thoughts/week_XX_day_Y.json` | Pre-generated daily thoughts |ttps://vercel.com/derick-jones-projects/solo-founder (Vercel)
- **🔌 API**: https://gospel-guide-api-273320302933.us-central1.run.app (Google Cloud Run)
- **📚 Repository**: https://github.com/derickjones/solo_founder

---

## ✨ Key Features

### Core Capabilities
- **🧠 AI-Powered Study**: Grok AI with real-time streaming responses
- **📖 Complete LDS Library**: 58,088+ scripture segments with FAISS vector search
- **📅 Come Follow Me 2026**: Complete Old Testament study system with enhanced scripture bundles
- **🔐 Authentication**: Clerk integration with Google/Apple login
- **💳 Payment Processing**: Stripe subscription system ($4.99/month)

### Come Follow Me Study System
- **💭 Daily Thought**: Pre-generated daily spiritual insights for each day of the year (364 total)
- **�️ Podcast Scripts**: Pre-generated podcast episodes for all weeks and study levels (instant loading)
- **🎯 Three Study Types**: Deep Dive Study, Lesson Plans, Core Content
- **📊 Three Study Levels**: Essential, Connected, Scholarly
- **🎵 Audio Generation**: Google Cloud TTS with 6 Chirp 3 HD voices (3 male, 3 female)

### User Experience
- **🎨 Professional UI**: Dark theme with minimalistic, color-coded buttons
- **📱 Mobile Optimized**: Responsive design with smart auto-collapse controls
- **🎬 Full-Screen Content**: Controls auto-hide when content is generated

---

## 💰 Business Model

| Tier | Price | Features |
|------|-------|----------|
| **Free** | $0 | Basic Q&A with daily limits |
| **Premium** | $4.99/month | Unlimited queries + CFM features |

**Target Revenue**: $2,500/month with 500 subscribers

---

## 🏗️ Technical Architecture

### Project Structure
\`\`\`
solo_founder/
├── backend/                    # FastAPI Python Backend
│   ├── main.py                # API entry point
│   ├── Dockerfile             # Container configuration
│   ├── requirements.txt       # Python dependencies
│   ├── search/                # Search engine & API
│   │   ├── api.py            # FastAPI endpoints
│   │   ├── prompts.py        # AI prompt templates
│   │   ├── scripture_search.py
│   │   ├── build_embeddings.py
│   │   └── indexes/          # FAISS vector indexes
│   └── scripts/              # Content pipeline
│       ├── scrapers/         # Web scrapers
│       └── cfm_bundle_scraper/  # CFM content
│           ├── 2026/         # 52 weekly CFM bundles
│           ├── 2026_daily_thoughts/  # Pre-generated daily thoughts
│           └── generate_daily_thoughts.py  # Generation script
├── frontend/                  # Next.js 16 Frontend
│   ├── src/
│   │   ├── app/              # Next.js app router
│   │   ├── components/       # React components
│   │   ├── services/         # API integration
│   │   └── utils/            # Utilities
│   └── public/               # Static assets
│       ├── daily_thoughts/   # Pre-generated daily thought JSON files
│       └── podcasts/         # Pre-generated podcast script JSON files
└── README.md                 # This file
\`\`\`

### Frontend (Next.js 16)
- **TypeScript + Tailwind CSS**: Modern React with full type safety
- **Streaming Interface**: Real-time AI responses with CFM study generation
- **Authentication**: Clerk integration with social login
- **Payment Integration**: Stripe Checkout with subscription management

### Backend (FastAPI)
- **AI Integration**: Grok AI for content generation + Google Cloud TTS for audio
- **Streaming API**: Server-Sent Events for real-time responses
- **Vector Search**: FAISS-powered semantic search (58,088 segments)
- **CFM Bundle System**: 52 enhanced weekly bundles with complete scripture content

### Infrastructure (Google Cloud)
- **Google Cloud Run**: Auto-scaling serverless containers
- **Artifact Registry**: Secure Docker image storage
- **FAISS Index Storage**: Optimized vector search performance

---

## 📚 Content Library

| Source | Size | Segments | Status |
|--------|------|----------|--------|
| Book of Mormon | 3.9MB | 6,604 | ✅ Complete |
| Old Testament | 8.6MB | ~15,000 | ✅ Complete |
| New Testament | 3.8MB | ~8,000 | ✅ Complete |
| Doctrine & Covenants | 2.0MB | ~3,000 | ✅ Complete |
| Pearl of Great Price | 381KB | ~700 | ✅ Complete |
| General Conference | 20MB | 22,246 | ✅ Complete (2015-2025) |
| Come Follow Me | 2.5MB | 384 | ✅ Complete (2026) |
| Daily Thoughts | 500KB | 364 | ✅ Pre-generated (52 weeks × 7 days) |
| Podcast Scripts | 1.5MB | 156 | ✅ Pre-generated (52 weeks × 3 levels) |
| **TOTAL** | **48MB** | **58,608** | **✅ READY** |

---

## 🛠️ Getting Started

### Prerequisites
\`\`\`bash
# Required
- Python 3.12+
- Node.js 18+
- Google Cloud CLI
- API Keys: OpenAI, Clerk, Stripe, XAI (Grok)
\`\`\`

### Quick Start

#### Backend Setup
\`\`\`bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Local development
uvicorn main:app --reload
\`\`\`

#### Frontend Setup
\`\`\`bash
cd frontend
npm install
npm run dev
\`\`\`

### Environment Variables

#### Backend (.env)
\`\`\`bash
XAI_API_KEY=your_grok_key           # AI content generation
BUCKET_NAME=gospel-guide-content-gospel-study-474301
OPENAI_API_KEY=your_openai_key      # Embeddings for semantic search
CLERK_SECRET_KEY=your_clerk_key
STRIPE_SECRET_KEY=your_stripe_key
\`\`\`

#### Frontend (.env.local)
\`\`\`bash
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_clerk_key
STRIPE_PUBLISHABLE_KEY=your_stripe_key
NEXT_PUBLIC_API_BASE_URL=https://gospel-guide-api-273320302933.us-central1.run.app
\`\`\`

---

## 📡 API Reference

### Core Scripture Search
| Endpoint | Method | Description |
|----------|--------|-------------|
| \`/search\` | GET | Semantic scripture search with context |
| \`/ask\` | POST | AI-powered Q&A (requires OPENAI_API_KEY) |
| \`/ask/stream\` | POST | Streaming AI Q&A |

### Come Follow Me System
| Endpoint | Method | Requires | Description |
|----------|--------|----------|-------------|
| \`/cfm/deep-dive\` | POST | XAI_API_KEY | Study guides (Essential/Connected/Scholarly) |
| \`/cfm/lesson-plans\` | POST | XAI_API_KEY | Teaching materials (Adult/Youth/Children) |
| \`/cfm/audio-summary\` | POST | XAI_API_KEY | Audio talk scripts |
| \`/cfm/core-content\` | POST | XAI_API_KEY | Raw CFM materials |

### System Health
| Endpoint | Method | Description |
|----------|--------|-------------|
| \`/\` | GET | Health check |
| \`/health\` | GET | API status and version |
| \`/debug/bundle/{week}\` | GET | Bundle loading diagnostics |
| \`/config\` | GET | Environment configuration status |

### Study Level System
All CFM endpoints use consistent study levels:
- **Essential**: Foundational gospel principles and basic understanding
- **Connected**: Deeper doctrinal connections and cross-references
- **Scholarly**: Advanced theological analysis and historical context

### Daily Thought System (Pre-Generated)
Daily spiritual insights served as static JSON files for instant loading:

| Field | Description |
|-------|-------------|
| `day_name` | Day of the week (Sunday-Saturday) |
| `theme` | Daily focus (Overview, Identity, Promise, etc.) |
| `title` | Engaging title for the thought |
| `scripture` | Reference and text |
| `thought` | 150-200 word reflection |
| `application` | Practical suggestion |
| `question` | Discussion prompt |
| `historical_context` | Optional background (only when source material contains it) |

**Generation**: Uses Grok AI with CFM bundles as source material to ensure doctrinal accuracy.

---

## 🚀 Deployment

### Backend - Google Cloud Run

\`\`\`bash
cd backend

# Deploy directly (recommended)
gcloud run deploy gospel-guide-api \\
  --source . \\
  --region us-central1 \\
  --cpu 4 \\
  --memory 4Gi \\
  --timeout 300 \\
  --concurrency 20 \\
  --min-instances 1 \\
  --set-env-vars "BUCKET_NAME=gospel-guide-content-gospel-study-474301,XAI_API_KEY=your-key"
\`\`\`

#### Production Settings
| Setting | Value | Purpose |
|---------|-------|---------|
| CPU | 4 cores | Handle concurrent AI generation |
| Memory | 4 GB | Load FAISS index (340MB) + processing |
| Timeout | 300s | Allow long audio generation requests |
| Concurrency | 20 | Requests per instance |
| Min Instances | 1 | Avoid cold starts |

### Frontend - Vercel

\`\`\`bash
# Automatic deployment via GitHub integration
git push origin main  # Triggers Vercel deployment

# Manual deployment
vercel --prod
\`\`\`

---

## 🧪 Testing

\`\`\`bash
# Test CFM Deep Dive
curl -X POST "https://gospel-guide-api-273320302933.us-central1.run.app/cfm/deep-dive" \\
  -H "Content-Type: application/json" \\
  -d '{"week_number": 2, "study_level": "essential"}'

# Test Podcast TTS with Intro/Outro Music
curl -X POST "https://gospel-guide-api-273320302933.us-central1.run.app/tts/podcast" \\
  -H "Content-Type: application/json" \\
  -d '{"text": "Your podcast content here", "voice": "alnilam", "title": "My Podcast"}'

# Test Q&A Search
curl -X POST "https://gospel-guide-api-273320302933.us-central1.run.app/ask" \\
  -H "Content-Type: application/json" \\
  -d '{"query": "What is faith?", "mode": "default", "top_k": 5}'

# Health check
curl -X GET "https://gospel-guide-api-273320302933.us-central1.run.app/health"
\`\`\`

---

## 📂 Scripts & Content Pipeline

### Directory Structure
\`\`\`
backend/scripts/
├── scrapers/                    # All content scrapers
│   ├── master_scraper.py       # Scraper coordinator
│   ├── scrape_book_of_mormon.py
│   ├── scrape_old_testament.py
│   ├── scrape_new_testament.py
│   ├── scrape_doctrine_covenants.py
│   ├── scrape_pearl_great_price.py
│   ├── scrape_general_conference.py
│   ├── scrape_cfm.py
│   └── scrape_seminary.py
├── cfm_bundle_scraper/         # CFM 2026 bundle generator
│   ├── cfm_weekly_scraper.py
│   ├── generate_daily_thoughts.py  # Daily thought generator
│   ├── generate_podcast_scripts.py # Podcast script generator
│   ├── 2026/                   # 52 weekly bundles
│   └── 2026_daily_thoughts/    # Pre-generated daily thoughts
└── content/sources/            # Raw scraped content
\`\`\`

### Running Scrapers
\`\`\`bash
cd backend/scripts/scrapers

# Run specific scraper
python master_scraper.py old_testament
python master_scraper.py cfm
python master_scraper.py seminary

# Run all scrapers
python master_scraper.py --all
\`\`\`

### Building Embeddings
\`\`\`bash
cd backend/search
export OPENAI_API_KEY="your-key"
python build_embeddings.py  # ~8 minutes for 58k segments
\`\`\`

### Generating Daily Thoughts
\`\`\`bash
cd backend/scripts/cfm_bundle_scraper

# Generate single week
XAI_API_KEY='your-key' python3 generate_daily_thoughts.py --week 1

# Generate range of weeks
XAI_API_KEY='your-key' python3 generate_daily_thoughts.py --start 1 --end 52
\`\`\`

### Generating Podcast Scripts
\`\`\`bash
cd backend/scripts/cfm_bundle_scraper

# Generate single week (all 3 levels)
XAI_API_KEY='your-key' python3 generate_podcast_scripts.py --week 1

# Generate specific level
XAI_API_KEY='your-key' python3 generate_podcast_scripts.py --week 1 --level essential

# Generate range of weeks
XAI_API_KEY='your-key' python3 generate_podcast_scripts.py --start 1 --end 8

# Force regenerate existing files
XAI_API_KEY='your-key' python3 generate_podcast_scripts.py --start 1 --end 8 --force
\`\`\`

**Output**: Scripts are saved directly to \`frontend/public/podcasts/\` for instant static serving.

---

## 📈 Performance

| Metric | Value |
|--------|-------|
| Scripture Search | <200ms average |
| AI Content Generation | Real-time streaming |
| Audio Script Generation | 5-30s (depending on level) |
| Vector Search | 58,088+ segments indexed |
| Mobile Performance | Optimized for iOS/Android |

---

## 🔧 Recent Updates (December 2024)

- ✅ **Podcast TTS with Music**: `/tts/podcast` endpoint with 15s intro (fade-in) + voice + 20s outro (10s fade-in)
- ✅ **Voice Selector**: 6 Google Chirp 3 HD voices (3 male: alnilam, achird, enceladus / 3 female: aoede, autonoe, erinome)
- ✅ **Podcast Pre-Generation**: Static JSON podcast scripts for instant loading (no API latency)
- ✅ **Improved Podcast Prompts**: No "fresh insight", "aha moment", or week references
- ✅ **Daily Thought Feature**: Pre-generated daily spiritual insights for every day of the year
- ✅ **Minimalistic UI**: Cleaner, more discrete CFM selection buttons
- ✅ **Auto-Collapse UX**: Controls auto-hide when content is generated
- ✅ **Google Cloud TTS**: 20x cost reduction vs ElevenLabs ($0.016 vs $0.30 per 1K chars)
- ✅ **Study Level Rebranding**: Essential/Connected/Scholarly naming
- ✅ **Audio Script-First**: Shows transcript by default, optional audio generation

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| Study Level Errors | Use Essential/Connected/Scholarly (not Basic/Intermediate/Advanced) |
| Audio Generation | Google Cloud TTS uses service account auth (automatic on Cloud Run) |
| Content Generation | Requires XAI_API_KEY for CFM study guides |
| Bundle Loading | Debug at \`/debug/bundle/{week}\` |
| Authentication | Check Clerk configuration in middleware.ts |
| Payment Issues | Verify Stripe webhook endpoints |

---

## 🎯 Future Enhancements

- **📊 Study Progress**: User analytics and progress tracking
- **💾 Offline Mode**: Service worker for scripture access
- **👥 Social Features**: Study group sharing
- **🔍 Advanced Search**: Cross-reference discovery
- **🌍 Multi-language**: Spanish, Portuguese expansion

---

## 🎨 Specialized Study Modes

| Mode | Personality | Scope |
|------|-------------|-------|
| **Book of Mormon Only** | Missionary-minded | Testimony-bearing, mission prep |
| **General Conference Only** | Meticulous | First Presidency & Twelve, chronological |
| **Come Follow Me** | Family companion | D&C/Church History, discussion ready |
| **Youth Mode** | Seminary teacher | 14-year-old friendly, excited |
| **Scholar Mode** | BYU religion PhD | Original languages, academic depth |

---

## 📝 License

Private repository - All rights reserved.

---

> **Gospel Study Assistant** - Transforming scripture study with AI-powered insights, unified study levels (Essential/Connected/Scholarly), and comprehensive Come Follow Me resources tailored for the LDS community.
