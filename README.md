# Gospel Study App - LDS AI Scripture Study Assistant

> **Production-ready AI-powered scripture study app with GPT-4o Q&A and pre-generated Come Follow Me content**

## 🚀 Live Deployments

- **🌐 Frontend**: https://gospelstudyapp.com (Vercel)
- **🔌 Backend API**: https://gospel-study-backend-273320302933.us-central1.run.app (Google Cloud Run)
- **📚 Repository**: https://github.com/derickjones/solo_founder

---

## ✨ Key Features

### Core Capabilities

- **🧠 AI-Powered Q&A**: OpenAI GPT-4o with real-time streaming responses
- **📖 Complete LDS Library**: 58,088+ scripture segments with FAISS vector search
- **📅 Come Follow Me 2026**: Complete Old Testament study system with pre-generated content
- **🔐 Authentication**: Clerk integration with Google/Apple login
- **💳 Payment Processing**: Stripe subscription system ($4.99/month)

### Come Follow Me Study System (Pre-Generated)

All CFM content is **pre-generated offline** and served as static JSON files for instant loading:

| Feature | Files | Description |
|---------|-------|-------------|
| **💭 Daily Thoughts** | 364 files | Daily spiritual insights (52 weeks × 7 days) |
| **🎙️ Podcast Scripts** | 156 files | Two-voice conversation podcasts (52 weeks × 3 levels) |
| **📚 Study Guides** | 156 files | Deep dive content (52 weeks × 3 levels) |
| **📝 Lesson Plans** | 156 files | Teaching materials (52 weeks × 3 audiences) |
| **📖 Core Content** | 52 files | Raw CFM bundle materials |

### Study Levels & Audiences

| Type | Options |
|------|---------|
| **Study Levels** | Essential, Connected, Scholarly |
| **Lesson Audiences** | Adult, Youth, Children |

### 🎙️ Enhanced Podcast Features (v3 - January 2026)

**Two-Voice Conversation Format:**
- **Sarah** (female/aoede): Host who poses intriguing questions and guides discovery
- **David** (male/alnilam): Guest who reveals insights and provides scholarly depth

**Educational Scaffolding:**
- ✅ **Addictive Hooks**: Every podcast starts with compelling mystery or discovery
- ✅ **Mystery Architecture**: Setup → tension building → satisfying resolution
- ✅ **Multi-Perspective Analysis**: Ancient Israel view + Christ's view + Modern restoration view
- ✅ **Pattern Recognition**: Systematic connections across 2-4+ dispensations
- ✅ **Historical Context**: Archaeological insights and cultural background
- ✅ **Hidden Connections**: Revealed restored truths (Moses 6:63, Abraham 3, JST insights)
- ✅ **Natural Discovery Flow**: Engaging discovery patterns and "aha moments"

**Podcast Audio Processing:**
- Multi-segment TTS generation (separate audio per speaker)
- 500ms pauses between speakers
- Professional intro/outro music with crossfades
- Normalized to -16 LUFS, 192kbps MP3 output

### User Experience

- **🎨 Professional UI**: Dark theme with minimalistic design
- **📱 Mobile Optimized**: Responsive design with smart auto-collapse controls
- **🎬 Full-Screen Content**: Controls auto-hide when content is generated| **💭 Daily Thought** | 364 files | Daily spiritual insights (52 weeks × 7 days) |# Test TTS with Voice Selection



---| **🎙️ Podcast Scripts** | 156 files | Audio scripts (52 weeks × 3 levels) |curl -X POST "https://gospel-guide-api-273320302933.us-central1.run.app/tts" \



## 💰 Business Model| **📚 Study Guides** | 156 files | Deep dive content (52 weeks × 3 levels) |  -H "Content-Type: application/json" \



| Tier | Price | Features || **📝 Lesson Plans** | 156 files | Teaching materials (52 weeks × 3 audiences) |  -d '{"text": "Hello world", "voice": "Kore"}'

|------|-------|----------|

| **Free** | $0 | Basic Q&A with daily limits || **📖 Core Content** | 52 files | Raw CFM bundle materials |

| **Premium** | $4.99/month | Unlimited queries + CFM features |

# Test Q&A Search------------|

**Target Revenue**: $2,500/month with 500 subscribers

### Study Levels & Audiences| `/cfm/deep-dive` | POST | XAI_API_KEY | Study guides (Essential/Connected/Scholarly) |

---

| Type | Options || `/cfm/lesson-plans` | POST | XAI_API_KEY | Teaching materials (Adult/Youth/Children) |

## 🏗️ Technical Architecture

|------|---------|| `/cfm/core-content` | POST | XAI_API_KEY | Raw CFM materials |

### Project Structure

```| **Study Levels** | Essential, Connected, Scholarly || `/tts` | POST | GCP Auth | Text-to-speech with voice selection |

solo_founder/

├── backend/                    # FastAPI Python Backend| **Lesson Audiences** | Adult, Youth, Children |

│   ├── main.py                # API entry point

│   ├── Dockerfile             # Container configuration### Static Content (Pre-Generated)

│   ├── requirements.txt       # Python dependencies

│   ├── assets/### Audio Generation| Path | Description |

│   │   └── intro_mp3s/        # Podcast intro/outro music

│   ├── search/                # Search engine & API- **🎵 Google Cloud TTS**: 6 Chirp 3 HD voices (3 male, 3 female)|------|-------------|

│   │   ├── api.py            # FastAPI endpoints (Q&A + TTS)

│   │   ├── google_tts.py     # Google Cloud TTS integration- **🎶 Podcast Audio**: 15s intro (fade-in) + voice content + 20s outro (10s fade-in)| `/podcasts/podcast_week_XX_level.json` | Pre-generated podcast scripts |

│   │   ├── prompts.py        # AI prompt templates (Q&A only)

│   │   ├── scripture_search.py| `/daily_thoughts/week_XX_day_Y.json` | Pre-generated daily thoughts |ttps://vercel.com/derick-jones-projects/solo-founder (Vercel)

│   │   ├── build_embeddings.py

│   │   └── indexes/          # FAISS vector indexes### User Experience- **🔌 API**: https://gospel-guide-api-273320302933.us-central1.run.app (Google Cloud Run)

│   └── scripts/              # Content pipeline

│       ├── scrapers/         # Web scrapers- **🎨 Professional UI**: Dark theme with minimalistic, color-coded buttons- **📚 Repository**: https://github.com/derickjones/solo_founder

│       └── cfm_bundle_scraper/  # CFM content generators

│           ├── 2026/                     # 52 weekly CFM source bundles- **📱 Mobile Optimized**: Responsive design with smart auto-collapse controls

│           ├── generate_core_content.py  # Extract raw bundle content

│           ├── generate_daily_thoughts.py- **🎬 Full-Screen Content**: Controls auto-hide when content is generated---

│           ├── generate_lesson_plans.py

│           ├── generate_podcast_scripts.py

│           └── generate_study_guides.py

├── frontend/                  # Next.js 16 Frontend---## ✨ Key Features

│   ├── src/

│   │   ├── app/              # Next.js app router

│   │   ├── components/       # React components (ChatInterface.tsx)

│   │   ├── services/         # API integration## 💰 Business Model### Core Capabilities

│   │   └── utils/            # Utilities

│   └── public/               # Static pre-generated content- **🧠 AI-Powered Study**: Grok AI with real-time streaming responses

│       ├── core_content/     # core_content_week_XX.json

│       ├── daily_thoughts/   # week_XX_day_Y.json| Tier | Price | Features |- **📖 Complete LDS Library**: 58,088+ scripture segments with FAISS vector search

│       ├── lesson_plans/     # lesson_plan_week_XX_[audience].json

│       ├── podcasts/         # podcast_week_XX_[level].json|------|-------|----------|- **📅 Come Follow Me 2026**: Complete Old Testament study system with enhanced scripture bundles

│       └── study_guides/     # study_guide_week_XX_[level].json

└── README.md                 # This file| **Free** | $0 | Basic Q&A with daily limits |- **🔐 Authentication**: Clerk integration with Google/Apple login

```

| **Premium** | $4.99/month | Unlimited queries + CFM features |- **💳 Payment Processing**: Stripe subscription system ($4.99/month)

### Frontend (Next.js 16)

- **TypeScript + Tailwind CSS**: Modern React with full type safety

- **Static Content Loading**: Pre-generated JSON files for instant CFM content

- **Streaming Interface**: Real-time AI responses for Q&A**Target Revenue**: $2,500/month with 500 subscribers### Come Follow Me Study System

- **Authentication**: Clerk integration with social login

- **Payment Integration**: Stripe Checkout with subscription management- **💭 Daily Thought**: Pre-generated daily spiritual insights for each day of the year (364 total)



### Backend (FastAPI)---- **�️ Podcast Scripts**: Pre-generated podcast episodes for all weeks and study levels (instant loading)

- **AI Integration**: Grok AI for Q&A + Google Cloud TTS for audio

- **Streaming API**: Server-Sent Events for real-time responses- **🎯 Three Study Types**: Deep Dive Study, Lesson Plans, Core Content

- **Vector Search**: FAISS-powered semantic search (58,088 segments)

- **CFM Bundle System**: 52 enhanced weekly bundles as source material## 🏗️ Technical Architecture- **📊 Three Study Levels**: Essential, Connected, Scholarly



### Infrastructure (Google Cloud)- **🎵 Audio Generation**: Google Cloud TTS with 6 Chirp 3 HD voices (3 male, 3 female)

- **Google Cloud Run**: Auto-scaling serverless containers

- **Artifact Registry**: Secure Docker image storage### Project Structure

- **FAISS Index Storage**: Optimized vector search performance

```### User Experience

---

solo_founder/- **🎨 Professional UI**: Dark theme with minimalistic, color-coded buttons

## 📚 Content Library

├── backend/                    # FastAPI Python Backend- **📱 Mobile Optimized**: Responsive design with smart auto-collapse controls

| Source | Size | Segments | Status |

|--------|------|----------|--------|│   ├── main.py                # API entry point- **🎬 Full-Screen Content**: Controls auto-hide when content is generated

| Book of Mormon | 3.9MB | 6,604 | ✅ Complete |

| Old Testament | 8.6MB | ~15,000 | ✅ Complete |│   ├── Dockerfile             # Container configuration

| New Testament | 3.8MB | ~8,000 | ✅ Complete |

| Doctrine & Covenants | 2.0MB | ~3,000 | ✅ Complete |│   ├── requirements.txt       # Python dependencies---

| Pearl of Great Price | 381KB | ~700 | ✅ Complete |

| General Conference | 20MB | 22,246 | ✅ Complete (2015-2025) |│   ├── search/                # Search engine & API

| Come Follow Me | 2.5MB | 384 | ✅ Complete (2026) |

| **TOTAL** | **48MB** | **58,608** | **✅ READY** |│   │   ├── api.py            # FastAPI endpoints (Q&A + TTS)## 💰 Business Model



### Pre-Generated CFM Content│   │   ├── prompts.py        # AI prompt templates (Q&A only)



| Content Type | Files | Pattern |│   │   ├── scripture_search.py| Tier | Price | Features |

|--------------|-------|---------|

| Daily Thoughts | 364 | `week_XX_day_Y.json` |│   │   ├── build_embeddings.py|------|-------|----------|

| Podcast Scripts | 156 | `podcast_week_XX_[level].json` |

| Study Guides | 156 | `study_guide_week_XX_[level].json` |│   │   └── indexes/          # FAISS vector indexes| **Free** | $0 | Basic Q&A with daily limits |

| Lesson Plans | 156 | `lesson_plan_week_XX_[audience].json` |

| Core Content | 52 | `core_content_week_XX.json` |│   └── scripts/              # Content pipeline| **Premium** | $4.99/month | Unlimited queries + CFM features |



---│       ├── scrapers/         # Web scrapers



## 🛠️ Getting Started│       └── cfm_bundle_scraper/  # CFM content generators**Target Revenue**: $2,500/month with 500 subscribers



### Prerequisites│           ├── 2026/                     # 52 weekly CFM source bundles

```bash

# Required│           ├── generate_core_content.py  # Extract raw bundle content---

- Python 3.12+

- Node.js 18+│           ├── generate_daily_thoughts.py

- Google Cloud CLI

- API Keys: XAI (Grok), Clerk, Stripe│           ├── generate_lesson_plans.py## 🏗️ Technical Architecture

```

│           ├── generate_podcast_scripts.py

### Quick Start

│           └── generate_study_guides.py### Project Structure

#### Backend Setup

```bash├── frontend/                  # Next.js 16 Frontend\`\`\`

cd backend

python -m venv venv│   ├── src/solo_founder/

source venv/bin/activate

pip install -r requirements.txt│   │   ├── app/              # Next.js app router├── backend/                    # FastAPI Python Backend



# Local development│   │   ├── components/       # React components (ChatInterface.tsx)│   ├── main.py                # API entry point

uvicorn main:app --reload

```│   │   ├── services/         # API integration│   ├── Dockerfile             # Container configuration



#### Frontend Setup│   │   └── utils/            # Utilities│   ├── requirements.txt       # Python dependencies

```bash

cd frontend│   └── public/               # Static pre-generated content│   ├── search/                # Search engine & API

npm install

npm run dev│       ├── core_content/     # core_content_week_XX.json│   │   ├── api.py            # FastAPI endpoints

```

│       ├── daily_thoughts/   # week_XX_day_Y.json│   │   ├── prompts.py        # AI prompt templates

### Environment Variables

│       ├── lesson_plans/     # lesson_plan_week_XX_[audience].json│   │   ├── scripture_search.py

#### Backend (.env)

```bash│       ├── podcasts/         # podcast_week_XX_[level].json│   │   ├── build_embeddings.py

XAI_API_KEY=your_grok_key           # AI Q&A generation

BUCKET_NAME=gospel-guide-content-gospel-study-474301│       └── study_guides/     # study_guide_week_XX_[level].json│   │   └── indexes/          # FAISS vector indexes

OPENAI_API_KEY=your_openai_key      # Embeddings for semantic search

CLERK_SECRET_KEY=your_clerk_key└── README.md                 # This file│   └── scripts/              # Content pipeline

STRIPE_SECRET_KEY=your_stripe_key

``````│       ├── scrapers/         # Web scrapers



#### Frontend (.env.local)│       └── cfm_bundle_scraper/  # CFM content

```bash

NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_clerk_key### Frontend (Next.js 16)│           ├── 2026/         # 52 weekly CFM bundles

STRIPE_PUBLISHABLE_KEY=your_stripe_key

NEXT_PUBLIC_API_BASE_URL=https://gospel-guide-api-273320302933.us-central1.run.app- **TypeScript + Tailwind CSS**: Modern React with full type safety│           ├── 2026_daily_thoughts/  # Pre-generated daily thoughts

```

- **Static Content Loading**: Pre-generated JSON files for instant CFM content│           └── generate_daily_thoughts.py  # Generation script

---

- **Streaming Interface**: Real-time AI responses for Q&A├── frontend/                  # Next.js 16 Frontend

## 📡 API Reference

- **Authentication**: Clerk integration with social login│   ├── src/

### Core Scripture Search

| Endpoint | Method | Description |- **Payment Integration**: Stripe Checkout with subscription management│   │   ├── app/              # Next.js app router

|----------|--------|-------------|

| `/search` | GET | Semantic scripture search with context |│   │   ├── components/       # React components

| `/ask` | POST | AI-powered Q&A (requires XAI_API_KEY) |

| `/ask/stream` | POST | Streaming AI Q&A |### Backend (FastAPI)│   │   ├── services/         # API integration



### Text-to-Speech- **AI Integration**: Grok AI for Q&A + Google Cloud TTS for audio│   │   └── utils/            # Utilities

| Endpoint | Method | Description |

|----------|--------|-------------|- **Streaming API**: Server-Sent Events for real-time responses│   └── public/               # Static assets

| `/tts/generate` | POST | Basic TTS with voice selection |

| `/tts/podcast` | POST | Professional podcast audio with intro/outro music |- **Vector Search**: FAISS-powered semantic search (58,088 segments)│       ├── daily_thoughts/   # Pre-generated daily thought JSON files



### System Health- **CFM Bundle System**: 52 enhanced weekly bundles as source material│       └── podcasts/         # Pre-generated podcast script JSON files

| Endpoint | Method | Description |

|----------|--------|-------------|└── README.md                 # This file

| `/` | GET | Health check |

| `/health` | GET | API status and version |### Infrastructure (Google Cloud)\`\`\`

| `/debug/bundle/{week}` | GET | Bundle loading diagnostics |

| `/config` | GET | Environment configuration status |- **Google Cloud Run**: Auto-scaling serverless containers



### Static Content (Frontend)- **Artifact Registry**: Secure Docker image storage### Frontend (Next.js 16)

All CFM content is served as static JSON from the frontend:

| Path | Description |- **FAISS Index Storage**: Optimized vector search performance- **TypeScript + Tailwind CSS**: Modern React with full type safety

|------|-------------|

| `/study_guides/study_guide_week_XX_[level].json` | Study guides |- **Streaming Interface**: Real-time AI responses with CFM study generation

| `/lesson_plans/lesson_plan_week_XX_[audience].json` | Lesson plans |

| `/core_content/core_content_week_XX.json` | Core content |---- **Authentication**: Clerk integration with social login

| `/podcasts/podcast_week_XX_[level].json` | Podcast scripts |

| `/daily_thoughts/week_XX_day_Y.json` | Daily thoughts |- **Payment Integration**: Stripe Checkout with subscription management



---## 📚 Content Library



## 🚀 Deployment### Backend (FastAPI)



### Backend - Google Cloud Run| Source | Size | Segments | Status |- **AI Integration**: Grok AI for content generation + Google Cloud TTS for audio



#### Full Deployment Command (with all env vars)|--------|------|----------|--------|- **Streaming API**: Server-Sent Events for real-time responses

```bash

cd backend && gcloud run deploy gospel-guide-api \| Book of Mormon | 3.9MB | 6,604 | ✅ Complete |- **Vector Search**: FAISS-powered semantic search (58,088 segments)

  --source . \

  --region us-central1 \| Old Testament | 8.6MB | ~15,000 | ✅ Complete |- **CFM Bundle System**: 52 enhanced weekly bundles with complete scripture content

  --cpu 4 \

  --memory 4Gi \| New Testament | 3.8MB | ~8,000 | ✅ Complete |

  --timeout 300 \

  --concurrency 20 \| Doctrine & Covenants | 2.0MB | ~3,000 | ✅ Complete |### Infrastructure (Google Cloud)

  --min-instances 1 \

  --set-env-vars "BUCKET_NAME=gospel-guide-content-gospel-study-474301,XAI_API_KEY=your-xai-key,OPENAI_API_KEY=your-openai-key"| Pearl of Great Price | 381KB | ~700 | ✅ Complete |- **Google Cloud Run**: Auto-scaling serverless containers

```

| General Conference | 20MB | 22,246 | ✅ Complete (2015-2025) |- **Artifact Registry**: Secure Docker image storage

#### Production Settings

| Setting | Value | Purpose || Come Follow Me | 2.5MB | 384 | ✅ Complete (2026) |- **FAISS Index Storage**: Optimized vector search performance

|---------|-------|---------|

| CPU | 4 cores | Handle concurrent AI generation || **TOTAL** | **48MB** | **58,608** | **✅ READY** |

| Memory | 4 GB | Load FAISS index (340MB) + processing |

| Timeout | 300s | Allow long audio generation requests |---

| Concurrency | 20 | Requests per instance |

| Min Instances | 1 | Avoid cold starts |### Pre-Generated CFM Content



### Frontend - Vercel## 📚 Content Library



```bash| Content Type | Files | Pattern |

# Automatic deployment via GitHub integration

git push origin main  # Triggers Vercel deployment|--------------|-------|---------|| Source | Size | Segments | Status |



# Manual deployment| Daily Thoughts | 364 | `week_XX_day_Y.json` ||--------|------|----------|--------|

vercel --prod

```| Podcast Scripts | 156 | `podcast_week_XX_[level].json` || Book of Mormon | 3.9MB | 6,604 | ✅ Complete |



---| Study Guides | 156 | `study_guide_week_XX_[level].json` || Old Testament | 8.6MB | ~15,000 | ✅ Complete |



## 📂 Content Generation Scripts| Lesson Plans | 156 | `lesson_plan_week_XX_[audience].json` || New Testament | 3.8MB | ~8,000 | ✅ Complete |



### Directory Structure| Core Content | 52 | `core_content_week_XX.json` || Doctrine & Covenants | 2.0MB | ~3,000 | ✅ Complete |

```

backend/scripts/| Pearl of Great Price | 381KB | ~700 | ✅ Complete |

├── scrapers/                    # All content scrapers

│   ├── master_scraper.py       # Scraper coordinator---| General Conference | 20MB | 22,246 | ✅ Complete (2015-2025) |

│   ├── scrape_book_of_mormon.py

│   ├── scrape_old_testament.py| Come Follow Me | 2.5MB | 384 | ✅ Complete (2026) |

│   ├── scrape_new_testament.py

│   ├── scrape_doctrine_covenants.py## 🛠️ Getting Started| Daily Thoughts | 500KB | 364 | ✅ Pre-generated (52 weeks × 7 days) |

│   ├── scrape_pearl_great_price.py

│   ├── scrape_general_conference.py| Podcast Scripts | 1.5MB | 156 | ✅ Pre-generated (52 weeks × 3 levels) |

│   └── scrape_cfm.py

├── cfm_bundle_scraper/         # CFM 2026 content generators### Prerequisites| **TOTAL** | **48MB** | **58,608** | **✅ READY** |

│   ├── 2026/                   # 52 weekly source bundles

│   ├── generate_core_content.py```bash

│   ├── generate_daily_thoughts.py

│   ├── generate_lesson_plans.py# Required---

│   ├── generate_podcast_scripts.py

│   └── generate_study_guides.py- Python 3.12+

└── content/sources/            # Raw scraped content

```- Node.js 18+## 🛠️ Getting Started



### Running Content Generators- Google Cloud CLI



All generators output directly to `frontend/public/` for static serving.- API Keys: XAI (Grok), Clerk, Stripe### Prerequisites



```bash```\`\`\`bash

cd backend/scripts/cfm_bundle_scraper

# Required

# Generate Core Content (no AI, raw bundle extraction)

python3 generate_core_content.py --start 1 --end 52### Quick Start- Python 3.12+



# Generate Study Guides (Essential/Connected/Scholarly)- Node.js 18+

XAI_API_KEY='your-key' python3 generate_study_guides.py --start 1 --end 52

#### Backend Setup- Google Cloud CLI

# Generate Lesson Plans (Adult/Youth/Children)

XAI_API_KEY='your-key' python3 generate_lesson_plans.py --start 1 --end 52```bash- API Keys: OpenAI, Clerk, Stripe, XAI (Grok)



# Generate Podcast Scripts (Essential/Connected/Scholarly)cd backend\`\`\`

XAI_API_KEY='your-key' python3 generate_podcast_scripts.py --start 1 --end 52

python -m venv venv

# Generate Daily Thoughts (7 days per week)

XAI_API_KEY='your-key' python3 generate_daily_thoughts.py --start 1 --end 52source venv/bin/activate### Quick Start



# Single week generationpip install -r requirements.txt

XAI_API_KEY='your-key' python3 generate_study_guides.py --week 1

#### Backend Setup

# Force regenerate existing files

XAI_API_KEY='your-key' python3 generate_study_guides.py --start 1 --end 8 --force# Local development\`\`\`bash

```

uvicorn main:app --reloadcd backend

### Running Scrapers

```bash```python -m venv venv

cd backend/scripts/scrapers

source venv/bin/activate

# Run specific scraper

python master_scraper.py old_testament#### Frontend Setuppip install -r requirements.txt

python master_scraper.py cfm

```bash

# Run all scrapers

python master_scraper.py --allcd frontend# Local development

```

npm installuvicorn main:app --reload

### Building Embeddings

```bashnpm run dev\`\`\`

cd backend/search

export OPENAI_API_KEY="your-key"```

python build_embeddings.py  # ~8 minutes for 58k segments

```#### Frontend Setup



---### Environment Variables\`\`\`bash



## 🧪 Testingcd frontend



```bash#### Backend (.env)npm install

# Test Q&A Search

curl -X POST "https://gospel-guide-api-273320302933.us-central1.run.app/ask" \```bashnpm run dev

  -H "Content-Type: application/json" \

  -d '{"query": "What is faith?", "mode": "default", "top_k": 5}'XAI_API_KEY=your_grok_key           # AI Q&A generation\`\`\`



# Test TTSBUCKET_NAME=gospel-guide-content-gospel-study-474301

curl -X POST "https://gospel-guide-api-273320302933.us-central1.run.app/tts/generate" \

  -H "Content-Type: application/json" \OPENAI_API_KEY=your_openai_key      # Embeddings for semantic search### Environment Variables

  -d '{"text": "Hello world", "voice": "alnilam"}'

CLERK_SECRET_KEY=your_clerk_key

# Test Podcast TTS

curl -X POST "https://gospel-guide-api-273320302933.us-central1.run.app/tts/podcast" \STRIPE_SECRET_KEY=your_stripe_key#### Backend (.env)

  -H "Content-Type: application/json" \

  -d '{"text": "Your podcast content here", "voice": "alnilam", "title": "My Podcast"}'```\`\`\`bash



# Health checkXAI_API_KEY=your_grok_key           # AI content generation

curl -X GET "https://gospel-guide-api-273320302933.us-central1.run.app/health"

```#### Frontend (.env.local)BUCKET_NAME=gospel-guide-content-gospel-study-474301



---```bashOPENAI_API_KEY=your_openai_key      # Embeddings for semantic search



## 📈 PerformanceNEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_clerk_keyCLERK_SECRET_KEY=your_clerk_key



| Metric | Value |STRIPE_PUBLISHABLE_KEY=your_stripe_keySTRIPE_SECRET_KEY=your_stripe_key

|--------|-------|

| Scripture Search | <200ms average |NEXT_PUBLIC_API_BASE_URL=https://gospel-guide-api-273320302933.us-central1.run.app\`\`\`

| AI Q&A Generation | Real-time streaming |

| CFM Content Loading | **Instant** (static JSON) |```

| Podcast Audio Generation | 5-30s (depending on length) |

| Vector Search | 58,088+ segments indexed |#### Frontend (.env.local)

| Mobile Performance | Optimized for iOS/Android |

---\`\`\`bash

---

NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_clerk_key

## 🔧 Recent Updates (January 2026)

## 📡 API ReferenceSTRIPE_PUBLISHABLE_KEY=your_stripe_key

- ✅ **Professional Podcast Audio**: Music bed under voice, true crossfades, normalized levels

- ✅ **New Intro Music**: inspiring-inspirational-background-music-412596.mp3NEXT_PUBLIC_API_BASE_URL=https://gospel-guide-api-273320302933.us-central1.run.app

- ✅ **Pre-Generated CFM Content**: All study guides, lesson plans, core content, and podcasts are now static JSON

- ✅ **Removed Live CFM Endpoints**: `/cfm/deep-dive`, `/cfm/lesson-plans`, `/cfm/core-content` removed from API### Core Scripture Search\`\`\`

- ✅ **Content Generators**: 5 Python scripts for offline content generation

- ✅ **Instant Loading**: Frontend loads CFM content from static files (no API latency)| Endpoint | Method | Description |

- ✅ **Cleaner Backend**: Reduced `prompts.py` by 287 lines, `api.py` by 425 lines

- ✅ **192kbps Audio**: Upgraded from 128kbps for better quality|----------|--------|-------------|---



---| `/search` | GET | Semantic scripture search with context |



## 🔧 Troubleshooting| `/ask` | POST | AI-powered Q&A (requires XAI_API_KEY) |## 📡 API Reference



| Issue | Solution || `/ask/stream` | POST | Streaming AI Q&A |

|-------|----------|

| Study Level Errors | Use Essential/Connected/Scholarly |### Core Scripture Search

| Lesson Audience Errors | Use Adult/Youth/Children |

| Audio Generation | Google Cloud TTS uses service account auth (automatic on Cloud Run) |### Text-to-Speech| Endpoint | Method | Description |

| Q&A Generation | Requires XAI_API_KEY for Grok AI |

| Bundle Loading | Debug at `/debug/bundle/{week}` || Endpoint | Method | Description ||----------|--------|-------------|

| Authentication | Check Clerk configuration in middleware.ts |

| Payment Issues | Verify Stripe webhook endpoints ||----------|--------|-------------|| \`/search\` | GET | Semantic scripture search with context |

| Missing Content | Run appropriate generator script for the week |

| `/tts` | POST | Text-to-speech with voice selection || \`/ask\` | POST | AI-powered Q&A (requires OPENAI_API_KEY) |

---

| `/tts/podcast` | POST | TTS with intro/outro music || \`/ask/stream\` | POST | Streaming AI Q&A |

## 🎯 Future Enhancements



- **📊 Study Progress**: User analytics and progress tracking

- **💾 Offline Mode**: Service worker for scripture access### System Health### Come Follow Me System

- **👥 Social Features**: Study group sharing

- **🔍 Advanced Search**: Cross-reference discovery| Endpoint | Method | Description || Endpoint | Method | Requires | Description |

- **🌍 Multi-language**: Spanish, Portuguese expansion

|----------|--------|-------------||----------|--------|----------|-------------|

---

| `/` | GET | Health check || \`/cfm/deep-dive\` | POST | XAI_API_KEY | Study guides (Essential/Connected/Scholarly) |

## 🎨 Specialized Study Modes

| `/health` | GET | API status and version || \`/cfm/lesson-plans\` | POST | XAI_API_KEY | Teaching materials (Adult/Youth/Children) |

| Mode | Personality | Scope |

|------|-------------|-------|| `/debug/bundle/{week}` | GET | Bundle loading diagnostics || \`/cfm/audio-summary\` | POST | XAI_API_KEY | Audio talk scripts |

| **Book of Mormon Only** | Missionary-minded | Testimony-bearing, mission prep |

| **General Conference Only** | Meticulous | First Presidency & Twelve, chronological || `/config` | GET | Environment configuration status || \`/cfm/core-content\` | POST | XAI_API_KEY | Raw CFM materials |

| **Come Follow Me** | Family companion | Old Testament 2026, discussion ready |

| **Youth Mode** | Seminary teacher | 14-year-old friendly, excited |

| **Scholar Mode** | BYU religion PhD | Original languages, academic depth |

### Static Content (Frontend)### System Health

---

All CFM content is served as static JSON from the frontend:| Endpoint | Method | Description |

## 📝 License

| Path | Description ||----------|--------|-------------|

Private repository - All rights reserved.

|------|-------------|| \`/\` | GET | Health check |

---

| `/study_guides/study_guide_week_XX_[level].json` | Study guides || \`/health\` | GET | API status and version |

> **Gospel Study Assistant** - Transforming scripture study with AI-powered insights, pre-generated Come Follow Me content (Essential/Connected/Scholarly), and comprehensive study resources tailored for the LDS community.

| `/lesson_plans/lesson_plan_week_XX_[audience].json` | Lesson plans || \`/debug/bundle/{week}\` | GET | Bundle loading diagnostics |

| `/core_content/core_content_week_XX.json` | Core content || \`/config\` | GET | Environment configuration status |

| `/podcasts/podcast_week_XX_[level].json` | Podcast scripts |

| `/daily_thoughts/week_XX_day_Y.json` | Daily thoughts |### Study Level System

All CFM endpoints use consistent study levels:

---- **Essential**: Foundational gospel principles and basic understanding

- **Connected**: Deeper doctrinal connections and cross-references

## 🚀 Deployment- **Scholarly**: Advanced theological analysis and historical context



### Backend - Google Cloud Run### Daily Thought System (Pre-Generated)

Daily spiritual insights served as static JSON files for instant loading:

```bash

cd backend| Field | Description |

|-------|-------------|

# Deploy directly (recommended)| `day_name` | Day of the week (Sunday-Saturday) |

gcloud run deploy gospel-guide-api \| `theme` | Daily focus (Overview, Identity, Promise, etc.) |

  --source . \| `title` | Engaging title for the thought |

  --region us-central1 \| `scripture` | Reference and text |

  --cpu 4 \| `thought` | 150-200 word reflection |

  --memory 4Gi \| `application` | Practical suggestion |

  --timeout 300 \| `question` | Discussion prompt |

  --concurrency 20 \| `historical_context` | Optional background (only when source material contains it) |

  --min-instances 1 \

  --set-env-vars "BUCKET_NAME=gospel-guide-content-gospel-study-474301,XAI_API_KEY=your-key"**Generation**: Uses Grok AI with CFM bundles as source material to ensure doctrinal accuracy.

```

---

#### Production Settings

| Setting | Value | Purpose |## 🚀 Deployment

|---------|-------|---------|

| CPU | 4 cores | Handle concurrent AI generation |### Backend - Google Cloud Run

| Memory | 4 GB | Load FAISS index (340MB) + processing |

| Timeout | 300s | Allow long audio generation requests |\`\`\`bash

| Concurrency | 20 | Requests per instance |cd backend

| Min Instances | 1 | Avoid cold starts |

# Deploy directly (recommended)

### Frontend - Vercelgcloud run deploy gospel-guide-api \\

  --source . \\

```bash  --region us-central1 \\

# Automatic deployment via GitHub integration  --cpu 4 \\

git push origin main  # Triggers Vercel deployment  --memory 4Gi \\

  --timeout 300 \\

# Manual deployment  --concurrency 20 \\

vercel --prod  --min-instances 1 \\

```  --set-env-vars "BUCKET_NAME=gospel-guide-content-gospel-study-474301,XAI_API_KEY=your-key"

\`\`\`

---

#### Production Settings

## 📂 Content Generation Scripts| Setting | Value | Purpose |

|---------|-------|---------|

### Directory Structure| CPU | 4 cores | Handle concurrent AI generation |

```| Memory | 4 GB | Load FAISS index (340MB) + processing |

backend/scripts/| Timeout | 300s | Allow long audio generation requests |

├── scrapers/                    # All content scrapers| Concurrency | 20 | Requests per instance |

│   ├── master_scraper.py       # Scraper coordinator| Min Instances | 1 | Avoid cold starts |

│   ├── scrape_book_of_mormon.py

│   ├── scrape_old_testament.py### Frontend - Vercel

│   ├── scrape_new_testament.py

│   ├── scrape_doctrine_covenants.py\`\`\`bash

│   ├── scrape_pearl_great_price.py# Automatic deployment via GitHub integration

│   ├── scrape_general_conference.pygit push origin main  # Triggers Vercel deployment

│   └── scrape_cfm.py

├── cfm_bundle_scraper/         # CFM 2026 content generators# Manual deployment

│   ├── 2026/                   # 52 weekly source bundlesvercel --prod

│   ├── generate_core_content.py\`\`\`

│   ├── generate_daily_thoughts.py

│   ├── generate_lesson_plans.py---

│   ├── generate_podcast_scripts.py

│   └── generate_study_guides.py## 🧪 Testing

└── content/sources/            # Raw scraped content

```\`\`\`bash

# Test CFM Deep Dive

### Running Content Generatorscurl -X POST "https://gospel-guide-api-273320302933.us-central1.run.app/cfm/deep-dive" \\

  -H "Content-Type: application/json" \\

All generators output directly to `frontend/public/` for static serving.  -d '{"week_number": 2, "study_level": "essential"}'



```bash# Test Podcast TTS with Intro/Outro Music

cd backend/scripts/cfm_bundle_scrapercurl -X POST "https://gospel-guide-api-273320302933.us-central1.run.app/tts/podcast" \\

  -H "Content-Type: application/json" \\

# Generate Core Content (no AI, raw bundle extraction)  -d '{"text": "Your podcast content here", "voice": "alnilam", "title": "My Podcast"}'

python3 generate_core_content.py --start 1 --end 52

# Test Q&A Search

# Generate Study Guides (Essential/Connected/Scholarly)curl -X POST "https://gospel-guide-api-273320302933.us-central1.run.app/ask" \\

XAI_API_KEY='your-key' python3 generate_study_guides.py --start 1 --end 52  -H "Content-Type: application/json" \\

  -d '{"query": "What is faith?", "mode": "default", "top_k": 5}'

# Generate Lesson Plans (Adult/Youth/Children)

XAI_API_KEY='your-key' python3 generate_lesson_plans.py --start 1 --end 52# Health check

curl -X GET "https://gospel-guide-api-273320302933.us-central1.run.app/health"

# Generate Podcast Scripts (Essential/Connected/Scholarly)\`\`\`

XAI_API_KEY='your-key' python3 generate_podcast_scripts.py --start 1 --end 52

---

# Generate Daily Thoughts (7 days per week)

XAI_API_KEY='your-key' python3 generate_daily_thoughts.py --start 1 --end 52## 📂 Scripts & Content Pipeline



# Single week generation### Directory Structure

XAI_API_KEY='your-key' python3 generate_study_guides.py --week 1\`\`\`

backend/scripts/

# Force regenerate existing files├── scrapers/                    # All content scrapers

XAI_API_KEY='your-key' python3 generate_study_guides.py --start 1 --end 8 --force│   ├── master_scraper.py       # Scraper coordinator

```│   ├── scrape_book_of_mormon.py

│   ├── scrape_old_testament.py

### Running Scrapers│   ├── scrape_new_testament.py

```bash│   ├── scrape_doctrine_covenants.py

cd backend/scripts/scrapers│   ├── scrape_pearl_great_price.py

│   ├── scrape_general_conference.py

# Run specific scraper│   ├── scrape_cfm.py

python master_scraper.py old_testament│   └── scrape_seminary.py

python master_scraper.py cfm├── cfm_bundle_scraper/         # CFM 2026 bundle generator

│   ├── cfm_weekly_scraper.py

# Run all scrapers│   ├── generate_daily_thoughts.py  # Daily thought generator

python master_scraper.py --all│   ├── generate_podcast_scripts.py # Podcast script generator

```│   ├── 2026/                   # 52 weekly bundles

│   └── 2026_daily_thoughts/    # Pre-generated daily thoughts

### Building Embeddings└── content/sources/            # Raw scraped content

```bash\`\`\`

cd backend/search

export OPENAI_API_KEY="your-key"### Running Scrapers

python build_embeddings.py  # ~8 minutes for 58k segments\`\`\`bash

```cd backend/scripts/scrapers



---# Run specific scraper

python master_scraper.py old_testament

## 🧪 Testingpython master_scraper.py cfm

python master_scraper.py seminary

```bash

# Test Q&A Search# Run all scrapers

curl -X POST "https://gospel-guide-api-273320302933.us-central1.run.app/ask" \python master_scraper.py --all

  -H "Content-Type: application/json" \\`\`\`

  -d '{"query": "What is faith?", "mode": "default", "top_k": 5}'

### Building Embeddings

# Test TTS\`\`\`bash

curl -X POST "https://gospel-guide-api-273320302933.us-central1.run.app/tts" \cd backend/search

  -H "Content-Type: application/json" \export OPENAI_API_KEY="your-key"

  -d '{"text": "Hello world", "voice": "alnilam"}'python build_embeddings.py  # ~8 minutes for 58k segments

\`\`\`

# Health check

curl -X GET "https://gospel-guide-api-273320302933.us-central1.run.app/health"### Generating Daily Thoughts

```\`\`\`bash

cd backend/scripts/cfm_bundle_scraper

---

# Generate single week

## 📈 PerformanceXAI_API_KEY='your-key' python3 generate_daily_thoughts.py --week 1



| Metric | Value |# Generate range of weeks

|--------|-------|XAI_API_KEY='your-key' python3 generate_daily_thoughts.py --start 1 --end 52

| Scripture Search | <200ms average |\`\`\`

| AI Q&A Generation | Real-time streaming |

| CFM Content Loading | **Instant** (static JSON) |### Generating Podcast Scripts

| Vector Search | 58,088+ segments indexed |\`\`\`bash

| Mobile Performance | Optimized for iOS/Android |cd backend/scripts/cfm_bundle_scraper



---# Generate single week (all 3 levels)

XAI_API_KEY='your-key' python3 generate_podcast_scripts.py --week 1

## 🔧 Recent Updates (January 2026)

# Generate specific level

- ✅ **Pre-Generated CFM Content**: All study guides, lesson plans, core content, and podcasts are now static JSONXAI_API_KEY='your-key' python3 generate_podcast_scripts.py --week 1 --level essential

- ✅ **Removed Live CFM Endpoints**: `/cfm/deep-dive`, `/cfm/lesson-plans`, `/cfm/core-content` removed from API

- ✅ **Content Generators**: 5 Python scripts for offline content generation# Generate range of weeks

- ✅ **Instant Loading**: Frontend loads CFM content from static files (no API latency)XAI_API_KEY='your-key' python3 generate_podcast_scripts.py --start 1 --end 8

- ✅ **Cleaner Backend**: Reduced `prompts.py` by 287 lines, `api.py` by 425 lines

- ✅ **Daily Thought Feature**: Pre-generated daily spiritual insights for every day of the year# Force regenerate existing files

- ✅ **Podcast TTS with Music**: 15s intro (fade-in) + voice + 20s outro (10s fade-in)XAI_API_KEY='your-key' python3 generate_podcast_scripts.py --start 1 --end 8 --force

- ✅ **Voice Selector**: 6 Google Chirp 3 HD voices (3 male: alnilam, achird, enceladus / 3 female: aoede, autonoe, erinome)\`\`\`



---**Output**: Scripts are saved directly to \`frontend/public/podcasts/\` for instant static serving.



## 🔧 Troubleshooting---



| Issue | Solution |## 📈 Performance

|-------|----------|

| Study Level Errors | Use Essential/Connected/Scholarly || Metric | Value |

| Lesson Audience Errors | Use Adult/Youth/Children ||--------|-------|

| Audio Generation | Google Cloud TTS uses service account auth (automatic on Cloud Run) || Scripture Search | <200ms average |

| Q&A Generation | Requires XAI_API_KEY for Grok AI || AI Content Generation | Real-time streaming |

| Bundle Loading | Debug at `/debug/bundle/{week}` || Audio Script Generation | 5-30s (depending on level) |

| Authentication | Check Clerk configuration in middleware.ts || Vector Search | 58,088+ segments indexed |

| Payment Issues | Verify Stripe webhook endpoints || Mobile Performance | Optimized for iOS/Android |

| Missing Content | Run appropriate generator script for the week |

---

---

## 🔧 Recent Updates (December 2024)

## 🎯 Future Enhancements

- ✅ **Podcast TTS with Music**: `/tts/podcast` endpoint with 15s intro (fade-in) + voice + 20s outro (10s fade-in)

- **📊 Study Progress**: User analytics and progress tracking- ✅ **Voice Selector**: 6 Google Chirp 3 HD voices (3 male: alnilam, achird, enceladus / 3 female: aoede, autonoe, erinome)

- **💾 Offline Mode**: Service worker for scripture access- ✅ **Podcast Pre-Generation**: Static JSON podcast scripts for instant loading (no API latency)

- **👥 Social Features**: Study group sharing- ✅ **Improved Podcast Prompts**: No "fresh insight", "aha moment", or week references

- **🔍 Advanced Search**: Cross-reference discovery- ✅ **Daily Thought Feature**: Pre-generated daily spiritual insights for every day of the year

- **🌍 Multi-language**: Spanish, Portuguese expansion- ✅ **Minimalistic UI**: Cleaner, more discrete CFM selection buttons

- ✅ **Auto-Collapse UX**: Controls auto-hide when content is generated

---- ✅ **Google Cloud TTS**: 20x cost reduction vs ElevenLabs ($0.016 vs $0.30 per 1K chars)

- ✅ **Study Level Rebranding**: Essential/Connected/Scholarly naming

## 🎨 Specialized Study Modes- ✅ **Audio Script-First**: Shows transcript by default, optional audio generation



| Mode | Personality | Scope |---

|------|-------------|-------|

| **Book of Mormon Only** | Missionary-minded | Testimony-bearing, mission prep |## 🔧 Troubleshooting

| **General Conference Only** | Meticulous | First Presidency & Twelve, chronological |

| **Come Follow Me** | Family companion | Old Testament 2026, discussion ready || Issue | Solution |

| **Youth Mode** | Seminary teacher | 14-year-old friendly, excited ||-------|----------|

| **Scholar Mode** | BYU religion PhD | Original languages, academic depth || Study Level Errors | Use Essential/Connected/Scholarly (not Basic/Intermediate/Advanced) |

| Audio Generation | Google Cloud TTS uses service account auth (automatic on Cloud Run) |

---| Content Generation | Requires XAI_API_KEY for CFM study guides |

| Bundle Loading | Debug at \`/debug/bundle/{week}\` |

## 📝 License| Authentication | Check Clerk configuration in middleware.ts |

| Payment Issues | Verify Stripe webhook endpoints |

Private repository - All rights reserved.

---

---

## 🎯 Future Enhancements

> **Gospel Study Assistant** - Transforming scripture study with AI-powered insights, pre-generated Come Follow Me content (Essential/Connected/Scholarly), and comprehensive study resources tailored for the LDS community.

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
