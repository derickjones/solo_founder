# Gospel Study Assistant - LDS AI Scripture Study App# Gospel Study Assistant - LDS AI Study Pl### Come Follow Me Study System

- **💭 Daily Thought**: Pre-generated daily spiritual insights for each day of the year (364 total)

> **Production-ready LDS AI Scripture Study App with pre-generated Come Follow Me content and live AI Q&A**- **🎙️ Podcast Scripts**: P### Come Follow Me System

| Endpoint | Method | Requires | Description |

## 🚀 Live Deployments|----------|--------|----------|-------------|

- **🌐 Frontend**: https://vercel.com/derick-jones-projects/solo-founder (Vercel)| `/cfm/deep-dive` | POST | XAI_API_KEY | Study guides (Essential/Connected/Scholarly) |

- **🔌 API**: https://gospel-guide-api-273320302933.us-central1.run.app (Google Cloud Run)| `/cfm/lesson-plans` | POST | XAI_API_KEY | Teaching materials (Adult/Youth/Children) |

- **📚 Repository**: https://github.com/derickjones/solo_founder| `/cfm/core-content` | POST | XAI_API_KEY | Raw CFM materials |

| `/tts/generate` | POST | GCP Auth | Basic text-to-speech |

---| `/tts/podcast` | POST | GCP Auth | TTS with intro/outro music (15s/20s) |rated podcast episodes for all weeks and study levels (instant loading)

- **🎯 Three Study Types**: Deep Dive Study, Lesson Plans, Core Content

## ✨ Key Features- **📊 Three Study Levels**: Essential, Connected, Scholarly

- **🎵 Audio Generation**: Google Cloud TTS with 6 Chirp 3 HD voices + intro/outro music

### Core Capabilities- **🎶 Podcast Audio**: 15s intro (fade-in) + voice content + 20s outro (10s fade-in)

- **🧠 AI-Powered Q&A**: Grok AI with real-time streaming responses

- **📖 Complete LDS Library**: 58,088+ scripture segments with FAISS vector search> **Production-ready LDS AI Scripture Study App with complete Come Follow Me system**

- **📅 Come Follow Me 2026**: Complete Old Testament study system with pre-generated content

- **🔐 Authentication**: Clerk integration with Google/Apple login## 🚀 Live Deployments

- **💳 Payment Processing**: Stripe subscription system ($4.99/month)- **🌐 Fronte### Come Follow Me System

| Endpoint | Method | Requires | Description |

### Come Follow Me Study System (Pre-Generated)|----------|--------|-# Test CFM Deep Dive

All CFM content is **pre-generated offline** and served as static JSON files for instant loading:curl -X POST "https://gospel-guide-api-273320302933.us-central1.run.app/cfm/deep-dive" \

  -H "Content-Type: application/json" \

| Feature | Files | Description |  -d '{"week_number": 2, "study_level": "essential"}'

|---------|-------|-------------|

| **💭 Daily Thought** | 364 files | Daily spiritual insights (52 weeks × 7 days) |# Test TTS with Voice Selection

| **🎙️ Podcast Scripts** | 156 files | Audio scripts (52 weeks × 3 levels) |curl -X POST "https://gospel-guide-api-273320302933.us-central1.run.app/tts" \

| **📚 Study Guides** | 156 files | Deep dive content (52 weeks × 3 levels) |  -H "Content-Type: application/json" \

| **📝 Lesson Plans** | 156 files | Teaching materials (52 weeks × 3 audiences) |  -d '{"text": "Hello world", "voice": "Kore"}'

| **📖 Core Content** | 52 files | Raw CFM bundle materials |

# Test Q&A Search------------|

### Study Levels & Audiences| `/cfm/deep-dive` | POST | XAI_API_KEY | Study guides (Essential/Connected/Scholarly) |

| Type | Options || `/cfm/lesson-plans` | POST | XAI_API_KEY | Teaching materials (Adult/Youth/Children) |

|------|---------|| `/cfm/core-content` | POST | XAI_API_KEY | Raw CFM materials |

| **Study Levels** | Essential, Connected, Scholarly || `/tts` | POST | GCP Auth | Text-to-speech with voice selection |

| **Lesson Audiences** | Adult, Youth, Children |

### Static Content (Pre-Generated)

### Audio Generation| Path | Description |

- **🎵 Google Cloud TTS**: 6 Chirp 3 HD voices (3 male, 3 female)|------|-------------|

- **🎶 Podcast Audio**: 15s intro (fade-in) + voice content + 20s outro (10s fade-in)| `/podcasts/podcast_week_XX_level.json` | Pre-generated podcast scripts |

| `/daily_thoughts/week_XX_day_Y.json` | Pre-generated daily thoughts |ttps://vercel.com/derick-jones-projects/solo-founder (Vercel)

### User Experience- **🔌 API**: https://gospel-guide-api-273320302933.us-central1.run.app (Google Cloud Run)

- **🎨 Professional UI**: Dark theme with minimalistic, color-coded buttons- **📚 Repository**: https://github.com/derickjones/solo_founder

- **📱 Mobile Optimized**: Responsive design with smart auto-collapse controls

- **🎬 Full-Screen Content**: Controls auto-hide when content is generated---



---## ✨ Key Features



## 💰 Business Model### Core Capabilities

- **🧠 AI-Powered Study**: Grok AI with real-time streaming responses

| Tier | Price | Features |- **📖 Complete LDS Library**: 58,088+ scripture segments with FAISS vector search

|------|-------|----------|- **📅 Come Follow Me 2026**: Complete Old Testament study system with enhanced scripture bundles

| **Free** | $0 | Basic Q&A with daily limits |- **🔐 Authentication**: Clerk integration with Google/Apple login

| **Premium** | $4.99/month | Unlimited queries + CFM features |- **💳 Payment Processing**: Stripe subscription system ($4.99/month)



**Target Revenue**: $2,500/month with 500 subscribers### Come Follow Me Study System

- **💭 Daily Thought**: Pre-generated daily spiritual insights for each day of the year (364 total)

---- **�️ Podcast Scripts**: Pre-generated podcast episodes for all weeks and study levels (instant loading)

- **🎯 Three Study Types**: Deep Dive Study, Lesson Plans, Core Content

## 🏗️ Technical Architecture- **📊 Three Study Levels**: Essential, Connected, Scholarly

- **🎵 Audio Generation**: Google Cloud TTS with 6 Chirp 3 HD voices (3 male, 3 female)

### Project Structure

```### User Experience

solo_founder/- **🎨 Professional UI**: Dark theme with minimalistic, color-coded buttons

├── backend/                    # FastAPI Python Backend- **📱 Mobile Optimized**: Responsive design with smart auto-collapse controls

│   ├── main.py                # API entry point- **🎬 Full-Screen Content**: Controls auto-hide when content is generated

│   ├── Dockerfile             # Container configuration

│   ├── requirements.txt       # Python dependencies---

│   ├── search/                # Search engine & API

│   │   ├── api.py            # FastAPI endpoints (Q&A + TTS)## 💰 Business Model

│   │   ├── prompts.py        # AI prompt templates (Q&A only)

│   │   ├── scripture_search.py| Tier | Price | Features |

│   │   ├── build_embeddings.py|------|-------|----------|

│   │   └── indexes/          # FAISS vector indexes| **Free** | $0 | Basic Q&A with daily limits |

│   └── scripts/              # Content pipeline| **Premium** | $4.99/month | Unlimited queries + CFM features |

│       ├── scrapers/         # Web scrapers

│       └── cfm_bundle_scraper/  # CFM content generators**Target Revenue**: $2,500/month with 500 subscribers

│           ├── 2026/                     # 52 weekly CFM source bundles

│           ├── generate_core_content.py  # Extract raw bundle content---

│           ├── generate_daily_thoughts.py

│           ├── generate_lesson_plans.py## 🏗️ Technical Architecture

│           ├── generate_podcast_scripts.py

│           └── generate_study_guides.py### Project Structure

├── frontend/                  # Next.js 16 Frontend\`\`\`

│   ├── src/solo_founder/

│   │   ├── app/              # Next.js app router├── backend/                    # FastAPI Python Backend

│   │   ├── components/       # React components (ChatInterface.tsx)│   ├── main.py                # API entry point

│   │   ├── services/         # API integration│   ├── Dockerfile             # Container configuration

│   │   └── utils/            # Utilities│   ├── requirements.txt       # Python dependencies

│   └── public/               # Static pre-generated content│   ├── search/                # Search engine & API

│       ├── core_content/     # core_content_week_XX.json│   │   ├── api.py            # FastAPI endpoints

│       ├── daily_thoughts/   # week_XX_day_Y.json│   │   ├── prompts.py        # AI prompt templates

│       ├── lesson_plans/     # lesson_plan_week_XX_[audience].json│   │   ├── scripture_search.py

│       ├── podcasts/         # podcast_week_XX_[level].json│   │   ├── build_embeddings.py

│       └── study_guides/     # study_guide_week_XX_[level].json│   │   └── indexes/          # FAISS vector indexes

└── README.md                 # This file│   └── scripts/              # Content pipeline

```│       ├── scrapers/         # Web scrapers

│       └── cfm_bundle_scraper/  # CFM content

### Frontend (Next.js 16)│           ├── 2026/         # 52 weekly CFM bundles

- **TypeScript + Tailwind CSS**: Modern React with full type safety│           ├── 2026_daily_thoughts/  # Pre-generated daily thoughts

- **Static Content Loading**: Pre-generated JSON files for instant CFM content│           └── generate_daily_thoughts.py  # Generation script

- **Streaming Interface**: Real-time AI responses for Q&A├── frontend/                  # Next.js 16 Frontend

- **Authentication**: Clerk integration with social login│   ├── src/

- **Payment Integration**: Stripe Checkout with subscription management│   │   ├── app/              # Next.js app router

│   │   ├── components/       # React components

### Backend (FastAPI)│   │   ├── services/         # API integration

- **AI Integration**: Grok AI for Q&A + Google Cloud TTS for audio│   │   └── utils/            # Utilities

- **Streaming API**: Server-Sent Events for real-time responses│   └── public/               # Static assets

- **Vector Search**: FAISS-powered semantic search (58,088 segments)│       ├── daily_thoughts/   # Pre-generated daily thought JSON files

- **CFM Bundle System**: 52 enhanced weekly bundles as source material│       └── podcasts/         # Pre-generated podcast script JSON files

└── README.md                 # This file

### Infrastructure (Google Cloud)\`\`\`

- **Google Cloud Run**: Auto-scaling serverless containers

- **Artifact Registry**: Secure Docker image storage### Frontend (Next.js 16)

- **FAISS Index Storage**: Optimized vector search performance- **TypeScript + Tailwind CSS**: Modern React with full type safety

- **Streaming Interface**: Real-time AI responses with CFM study generation

---- **Authentication**: Clerk integration with social login

- **Payment Integration**: Stripe Checkout with subscription management

## 📚 Content Library

### Backend (FastAPI)

| Source | Size | Segments | Status |- **AI Integration**: Grok AI for content generation + Google Cloud TTS for audio

|--------|------|----------|--------|- **Streaming API**: Server-Sent Events for real-time responses

| Book of Mormon | 3.9MB | 6,604 | ✅ Complete |- **Vector Search**: FAISS-powered semantic search (58,088 segments)

| Old Testament | 8.6MB | ~15,000 | ✅ Complete |- **CFM Bundle System**: 52 enhanced weekly bundles with complete scripture content

| New Testament | 3.8MB | ~8,000 | ✅ Complete |

| Doctrine & Covenants | 2.0MB | ~3,000 | ✅ Complete |### Infrastructure (Google Cloud)

| Pearl of Great Price | 381KB | ~700 | ✅ Complete |- **Google Cloud Run**: Auto-scaling serverless containers

| General Conference | 20MB | 22,246 | ✅ Complete (2015-2025) |- **Artifact Registry**: Secure Docker image storage

| Come Follow Me | 2.5MB | 384 | ✅ Complete (2026) |- **FAISS Index Storage**: Optimized vector search performance

| **TOTAL** | **48MB** | **58,608** | **✅ READY** |

---

### Pre-Generated CFM Content

## 📚 Content Library

| Content Type | Files | Pattern |

|--------------|-------|---------|| Source | Size | Segments | Status |

| Daily Thoughts | 364 | `week_XX_day_Y.json` ||--------|------|----------|--------|

| Podcast Scripts | 156 | `podcast_week_XX_[level].json` || Book of Mormon | 3.9MB | 6,604 | ✅ Complete |

| Study Guides | 156 | `study_guide_week_XX_[level].json` || Old Testament | 8.6MB | ~15,000 | ✅ Complete |

| Lesson Plans | 156 | `lesson_plan_week_XX_[audience].json` || New Testament | 3.8MB | ~8,000 | ✅ Complete |

| Core Content | 52 | `core_content_week_XX.json` || Doctrine & Covenants | 2.0MB | ~3,000 | ✅ Complete |

| Pearl of Great Price | 381KB | ~700 | ✅ Complete |

---| General Conference | 20MB | 22,246 | ✅ Complete (2015-2025) |

| Come Follow Me | 2.5MB | 384 | ✅ Complete (2026) |

## 🛠️ Getting Started| Daily Thoughts | 500KB | 364 | ✅ Pre-generated (52 weeks × 7 days) |

| Podcast Scripts | 1.5MB | 156 | ✅ Pre-generated (52 weeks × 3 levels) |

### Prerequisites| **TOTAL** | **48MB** | **58,608** | **✅ READY** |

```bash

# Required---

- Python 3.12+

- Node.js 18+## 🛠️ Getting Started

- Google Cloud CLI

- API Keys: XAI (Grok), Clerk, Stripe### Prerequisites

```\`\`\`bash

# Required

### Quick Start- Python 3.12+

- Node.js 18+

#### Backend Setup- Google Cloud CLI

```bash- API Keys: OpenAI, Clerk, Stripe, XAI (Grok)

cd backend\`\`\`

python -m venv venv

source venv/bin/activate### Quick Start

pip install -r requirements.txt

#### Backend Setup

# Local development\`\`\`bash

uvicorn main:app --reloadcd backend

```python -m venv venv

source venv/bin/activate

#### Frontend Setuppip install -r requirements.txt

```bash

cd frontend# Local development

npm installuvicorn main:app --reload

npm run dev\`\`\`

```

#### Frontend Setup

### Environment Variables\`\`\`bash

cd frontend

#### Backend (.env)npm install

```bashnpm run dev

XAI_API_KEY=your_grok_key           # AI Q&A generation\`\`\`

BUCKET_NAME=gospel-guide-content-gospel-study-474301

OPENAI_API_KEY=your_openai_key      # Embeddings for semantic search### Environment Variables

CLERK_SECRET_KEY=your_clerk_key

STRIPE_SECRET_KEY=your_stripe_key#### Backend (.env)

```\`\`\`bash

XAI_API_KEY=your_grok_key           # AI content generation

#### Frontend (.env.local)BUCKET_NAME=gospel-guide-content-gospel-study-474301

```bashOPENAI_API_KEY=your_openai_key      # Embeddings for semantic search

NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_clerk_keyCLERK_SECRET_KEY=your_clerk_key

STRIPE_PUBLISHABLE_KEY=your_stripe_keySTRIPE_SECRET_KEY=your_stripe_key

NEXT_PUBLIC_API_BASE_URL=https://gospel-guide-api-273320302933.us-central1.run.app\`\`\`

```

#### Frontend (.env.local)

---\`\`\`bash

NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_clerk_key

## 📡 API ReferenceSTRIPE_PUBLISHABLE_KEY=your_stripe_key

NEXT_PUBLIC_API_BASE_URL=https://gospel-guide-api-273320302933.us-central1.run.app

### Core Scripture Search\`\`\`

| Endpoint | Method | Description |

|----------|--------|-------------|---

| `/search` | GET | Semantic scripture search with context |

| `/ask` | POST | AI-powered Q&A (requires XAI_API_KEY) |## 📡 API Reference

| `/ask/stream` | POST | Streaming AI Q&A |

### Core Scripture Search

### Text-to-Speech| Endpoint | Method | Description |

| Endpoint | Method | Description ||----------|--------|-------------|

|----------|--------|-------------|| \`/search\` | GET | Semantic scripture search with context |

| `/tts` | POST | Text-to-speech with voice selection || \`/ask\` | POST | AI-powered Q&A (requires OPENAI_API_KEY) |

| `/tts/podcast` | POST | TTS with intro/outro music || \`/ask/stream\` | POST | Streaming AI Q&A |



### System Health### Come Follow Me System

| Endpoint | Method | Description || Endpoint | Method | Requires | Description |

|----------|--------|-------------||----------|--------|----------|-------------|

| `/` | GET | Health check || \`/cfm/deep-dive\` | POST | XAI_API_KEY | Study guides (Essential/Connected/Scholarly) |

| `/health` | GET | API status and version || \`/cfm/lesson-plans\` | POST | XAI_API_KEY | Teaching materials (Adult/Youth/Children) |

| `/debug/bundle/{week}` | GET | Bundle loading diagnostics || \`/cfm/audio-summary\` | POST | XAI_API_KEY | Audio talk scripts |

| `/config` | GET | Environment configuration status || \`/cfm/core-content\` | POST | XAI_API_KEY | Raw CFM materials |



### Static Content (Frontend)### System Health

All CFM content is served as static JSON from the frontend:| Endpoint | Method | Description |

| Path | Description ||----------|--------|-------------|

|------|-------------|| \`/\` | GET | Health check |

| `/study_guides/study_guide_week_XX_[level].json` | Study guides || \`/health\` | GET | API status and version |

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
