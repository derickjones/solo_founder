# Solo Founder - Gospel Guide AI

> **Mission**: Ship a paid, production-ready LDS AI Scripture Study App in <14 days

## 🎯 **Project Status: ✅ COMPLETE & DEPLOYED**

**December 3, 2025** - Full-stack AI application with Come Follow Me study mode successfully deployed.

### 🚀 **Live Deployments**
- **🌐 Frontend**: https://vercel.com/derick-jones-projects/solo-founder (Vercel)
- **🔌 API**: https://gospel-guide-api-273320302933.us-central1.run.app (Google Cloud Run)
- **📚 Repository**: https://github.com/derickjones/solo_founder

### ✅ **Fully Operational Features**
- **🧠 AI-Powered Responses**: OpenAI GPT-4o-mini generates intelligent answers with proper LDS citations
- **⚡ Real-Time Streaming**: Server-Sent Events for live response generation  
- **📖 Complete LDS Library**: 58,088 scripture segments with FAISS vector search
- **📅 Come Follow Me 2025**: Integrated weekly lesson study with actual Doctrine & Covenants schedule
- **👨‍👩‍👧‍👦 Multi-Audience Support**: Adult, Family, Youth, and Children study modes
- **🔍 Smart Citations**: Exact references like "(Oct 2016, President Dieter F. Uchtdorf, 'Fourth Floor, Last Door')"
- **🎨 Dark Theme UI**: Modern chat interface with sidebar-driven mode selection
- **🔐 Secure Deployment**: Environment-based API key management

## 🆕 **Come Follow Me Features**
- **📅 2025 Schedule**: 21 weeks of Doctrine & Covenants lessons with real dates
- **🎯 Lesson Selection**: Dropdown with actual lesson titles and date ranges
- **👪 Audience Targeting**: Customized content for different family members
- **🔄 Mode Switching**: Seamless transition between Q&A and Come Follow Me study
- **📖 Current Week Detection**: Automatically selects current lesson (Dec 1-7: D&C 137-138)## 🏗️ **Architecture Overview**

### 📡 **System Architecture**
```mermaid
graph TB
    A[User] --> B[Next.js Frontend<br/>Vercel]
    B --> C[FastAPI Backend<br/>Google Cloud Run]
    C --> D[OpenAI API<br/>GPT-4o-mini]
    C --> E[FAISS Vector DB<br/>58k embeddings]
    C --> F[Google Cloud Storage<br/>Indexes & Metadata]
    
    G[Web Scrapers] --> H[Content Pipeline]
    H --> I[Embedding Generator]
    I --> E
```

### 🏛️ **Backend Architecture**

#### 🔍 **Search & AI Engine** (`backend/search/`)
- **`api.py`**: FastAPI server with streaming SSE endpoints
  - `/ask-stream` - Real-time AI responses with search results
  - `/search` - Vector similarity search across scripture corpus
  - CORS middleware for frontend integration
- **`scripture_search.py`**: FAISS-powered semantic search engine
  - OpenAI embeddings (`text-embedding-3-small`) for query vectorization
  - Metadata filtering by source, book, speaker, year
  - Cosine similarity ranking with configurable top-k results
- **`prompts.py`**: Intelligent prompt engineering system
  - Mode-specific system prompts (Youth, Scholar, General Conference)
  - Context window management for optimal AI responses
  - Source-aware filtering for targeted content delivery
- **`cloud_storage.py`**: Google Cloud Storage integration
  - Remote index management and versioning
  - Scalable metadata storage and retrieval

#### 🕷️ **Content Pipeline** (`backend/scripts/`)
- **`master_scraper.py`**: Orchestrates all content acquisition
  - Parallel scraping of LDS.org content
  - Test mode for development iterations
  - Progress tracking and error handling
- **Individual Scrapers**: Modular content extractors
  - `scrape_book_of_mormon.py`, `scrape_general_conference.py`, etc.
  - BeautifulSoup + lxml for robust HTML parsing
  - Structured JSON output with rich metadata
- **`build_embeddings.py`**: Vector index construction
  - Batch processing of 58k+ scripture segments
  - FAISS IndexFlatIP for cosine similarity search
  - Metadata persistence with pickle serialization

#### 📊 **Data Layer**
- **Content Storage**: 45MB+ of structured LDS content (JSON)
- **Vector Index**: FAISS binary index with 1536-dim embeddings
- **Metadata**: Pickle-serialized Python objects for fast lookup
- **Configuration**: JSON-based index configuration and versioning

### 🎨 **Frontend Architecture**

#### ⚛️ **Next.js 16 Application** (`frontend/src/`)
- **App Router**: Modern Next.js file-based routing
- **TypeScript**: Full type safety across components and services
- **Tailwind CSS 4**: Utility-first styling with custom neutral theme
- **Server-Side Rendering**: Optimized SEO and performance

#### 🧩 **Component Architecture**
- **`ChatInterface.tsx`**: Main conversation component
  - Real-time streaming with Server-Sent Events
  - ReactMarkdown integration for rich text formatting
  - Message history with search result citations
  - Mode selection and source filtering UI
- **`Sidebar.tsx`**: Source selection interface
  - Toggle-based filtering (General Conference, Standard Works)
  - Dynamic source count tracking
  - Responsive design with neutral color scheme

#### 🔌 **API Integration** (`services/api.ts`)
- **Streaming API Client**: Custom SSE implementation
- **Request/Response Types**: Full TypeScript interfaces
- **Mode Mapping**: Frontend mode translation to backend filters
- **Error Handling**: Comprehensive HTTP and stream error management

### 🚀 **Deployment Architecture**

#### 🌐 **Frontend Deployment** (Vercel)
- **Auto-Deploy**: GitHub main branch triggers
- **Edge Functions**: Global CDN distribution
- **Environment Variables**: Secure API endpoint configuration
- **Build Optimization**: Next.js static optimization

#### ⚡ **Backend Deployment** (Google Cloud Run)
- **Containerized FastAPI**: Docker-based deployment
- **Serverless Scaling**: 0-to-N instance auto-scaling
- **Environment Security**: Cloud-based secret management
- **Health Checks**: Automated service monitoring

### 🔧 **Development Workflow**

```bash
# Backend Development
cd backend/search
export OPENAI_API_KEY="your-key"
pip install -r requirements.txt
python3 api.py

# Frontend Development  
cd frontend
npm install
npm run dev

# Content Pipeline
cd backend/scripts
python3 master_scraper.py --test
python3 ../search/build_embeddings.py
```

## 📁 **Detailed Project Structure**

```
solo_founder/
├── README.md                      # 📋 Project documentation
├── .gitignore                     # 🔒 Security patterns
│
├── backend/                       # 🐍 Python Backend
│   ├── deploy.sh                  # 🚀 Cloud Run deployment
│   ├── Dockerfile                 # 🐳 Container config
│   ├── README.md                  # 📖 Backend docs
│   │
│   ├── scripts/                   # 🕷️ Content Acquisition
│   │   ├── master_scraper.py      # 🎯 Orchestration engine
│   │   ├── requirements.txt       # 📦 Scraper dependencies
│   │   ├── scrape_*.py           # 📚 Individual scrapers
│   │   └── content/              # 💾 Raw JSON content
│   │       ├── book_of_mormon.json
│   │       ├── general_conference.json
│   │       ├── come_follow_me.json    # 📅 2025 D&C lessons
│   │       └── complete_lds_content.json
│   │
│   ├── search/                    # 🔍 AI Search Engine
│   │   ├── api.py                # 🌐 FastAPI server
│   │   ├── scripture_search.py   # 📊 Vector search
│   │   ├── prompts.py           # 🧠 AI prompt system
│   │   ├── cloud_storage.py     # ☁️ GCS integration
│   │   ├── build_embeddings.py  # 🔢 Vector index builder
│   │   ├── test_*.py            # 🧪 Development tests
│   │   ├── requirements.txt     # 📦 API dependencies
│   │   └── indexes/             # 💾 FAISS vector database
│   │       ├── scripture_index.faiss
│   │       ├── scripture_metadata.pkl
│   │       └── config.json
│   │
│   └── src/                      # 📚 Shared libraries
│       └── lib/
│           └── prompts.ts       # 📝 TypeScript prompts
│
├── frontend/                     # ⚛️ Next.js Frontend
│   ├── package.json             # 📦 Dependencies
│   ├── next.config.ts           # ⚙️ Next.js config
│   ├── tsconfig.json           # 🔧 TypeScript config
│   ├── vercel.json             # 🚀 Vercel deployment
│   ├── eslint.config.mjs       # ✨ Code quality
│   ├── postcss.config.mjs      # 🎨 CSS processing
│   ├── README.md               # 📖 Frontend docs
│   │
│   ├── public/                 # 🌐 Static assets
│   │   ├── christ.jpeg         # 🖼️ Logo image
│   │   └── *.svg              # 📐 Icon assets
│   │
│   └── src/                    # 💻 Application source
│       ├── app/                # 🏠 Next.js App Router
│       │   ├── layout.tsx      # 📱 Root layout
│       │   ├── page.tsx        # 🏡 Home page
│       │   ├── globals.css     # 🎨 Global styles
│       │   └── favicon.ico     # 🌟 Browser icon
│       │
│       ├── components/         # 🧩 React components
│       │   ├── ChatInterface.tsx # 💬 Main chat UI
│       │   └── Sidebar.tsx      # 📋 Source selector
│       │
│       └── services/           # 🔌 API integration
│           └── api.ts          # 📡 HTTP client
```

## 🎯 **Business Model**Ship a paid, production-ready LDS AI Scripture Study App in <14 days

## 🎯 **Project Status: ✅ COMPLETE & DEPLOYED**

**November 29, 2025** - Full-stack AI application successfully deployed and functional.

### 🚀 **Live Deployments**
- **🌐 Frontend**: https://vercel.com/derick-jones-projects/solo-founder (Vercel)
- **🔌 API**: https://gospel-guide-api-273320302933.us-central1.run.app (Google Cloud Run)
- **📚 Repository**: https://github.com/derickjones/solo_founder

### ✅ **Fully Operational Features**
- **🧠 AI-Powered Responses**: OpenAI GPT-4o-mini generates intelligent answers with proper LDS citations
- **⚡ Real-Time Streaming**: Server-Sent Events for live response generation  
- **📖 Complete LDS Library**: 58,088 scripture segments with FAISS vector search
- **🎯 8 Specialized Modes**: Default, Book of Mormon only, General Conference only, etc.
- **🔍 Smart Citations**: Exact references like "(Oct 2016, President Dieter F. Uchtdorf, 'Fourth Floor, Last Door')"
- **🎨 Dark Theme UI**: Modern chat interface with streaming responses
- **🔐 Secure Deployment**: Environment-based API key management

## 📁 **Project Structure**

```
solo_founder/
├── README.md                # 📋 Main project documentation  
├── backend/                 # 🐍 Python FastAPI Backend
│   ├── search/              # 🔍 AI search & response system
│   │   ├── api.py          # 🌐 FastAPI endpoints with streaming
│   │   ├── prompts.py      # 🧠 OpenAI prompt system  
│   │   ├── scripture_search.py # 📚 FAISS vector search
│   │   └── indexes/        # 💾 58,088 scripture embeddings
│   ├── scripts/            # 🕷️ Web scrapers + content pipeline
│   ├── deploy.sh           # 🚀 Google Cloud Run deployment
│   └── Dockerfile          # 🐳 Container configuration
│
├── frontend/                     # ⚛️ Next.js React Frontend  
│   ├── src/
│   │   ├── components/          # 🧩 React Components
│   │   │   ├── ChatInterface.tsx # 💬 Streaming chat with mode sync
│   │   │   └── Sidebar.tsx      # 📋 Mode picker & source controls
│   │   ├── utils/               # 🛠️ Utility Functions
│   │   │   └── comeFollowMe.ts  # 📅 2025 D&C lesson data & logic
│   │   ├── app/                 # 📱 Next.js 16 app structure
│   │   └── services/            # 🔌 API integration
│   ├── vercel.json             # ⚡ Auto-deploy configuration
│   └── package.json            # 📦 Dependencies
│
└── .gitignore             # � Security & clean repo
```

## 🎯 **Business Model**
- **Free Tier**: 5 queries/day, basic search modes
- **Premium Monthly**: $7.99/month, unlimited queries + all specialized modes  
- **Lifetime Access**: $99 (limited to 500 users), advanced study tools

## 🔧 **Tech Stack & Dependencies**

### � **Backend Technologies**
- **FastAPI 0.104+**: Modern async web framework with automatic OpenAPI docs
- **OpenAI 1.0+**: GPT-4o-mini integration with streaming responses  
- **FAISS 1.7+**: Facebook's vector similarity search (CPU-optimized)
- **NumPy 1.24+**: Numerical computing for embedding operations
- **Google Cloud Storage 2.10+**: Scalable index and metadata storage
- **BeautifulSoup4 4.12+**: Robust HTML parsing for content scraping
- **Uvicorn**: High-performance ASGI server with auto-reload
- **Pydantic 2.4+**: Data validation and serialization

### ⚛️ **Frontend Technologies**  
- **Next.js 16.0.5**: React framework with App Router and SSR
- **React 19.2.0**: Latest React with concurrent features
- **TypeScript 5**: Full type safety and developer experience
- **Tailwind CSS 4**: Utility-first styling with custom neutral theme
- **Heroicons 2.2**: Consistent icon library from Tailwind team
- **ReactMarkdown 10.1**: Rich text rendering for AI responses

### ☁️ **Infrastructure & Deployment**
- **Google Cloud Run**: Serverless container platform with auto-scaling
- **Vercel**: Edge-optimized Next.js hosting with auto-deployment
- **Docker**: Containerized backend for consistent deployments
- **GitHub Actions**: CI/CD pipeline for automated deployments

### 🔍 **AI & Search Pipeline**
- **OpenAI Embeddings**: `text-embedding-3-small` (1536 dimensions)
- **Vector Database**: FAISS IndexFlatIP for cosine similarity
- **Content Sources**: 58,088+ scripture segments from LDS.org
- **Streaming**: Server-Sent Events for real-time AI responses

## 🚀 **Deployment Guide**

### Prerequisites
```bash
# Install Google Cloud CLI
# Configure authentication
gcloud auth login
gcloud config set project gospel-study-474301

# Set required environment variables
export OPENAI_API_KEY="your-openai-api-key-here"
```

### Backend Deployment (Google Cloud Run)
```bash
cd backend
source .env  # Ensure OPENAI_API_KEY is set

# Optional: Run pre-deployment checks
./check-deploy.sh

# Deploy to Cloud Run
./deploy.sh
```

The deploy script automatically:
- ✅ Runs pre-deployment validation (if check-deploy.sh exists)
- ✅ Uploads content files to Cloud Storage
- ✅ Builds and pushes Docker image  
- ✅ Clears conflicting environment variables
- ✅ Deploys with proper startup probes
- ✅ Tests API health after deployment

### Frontend Deployment (Vercel)
```bash
cd frontend
# Update API_BASE_URL in src/services/api.ts to your Cloud Run URL
vercel --prod
```

## 🔧 **Troubleshooting Common Issues**

### Environment Variable Conflicts
**Problem**: `Cannot update environment variable [OPENAI_API_KEY] to string literal`
**Solution**: The deploy script now automatically clears secrets/env vars to prevent conflicts.

### Cloud Storage Access Issues  
**Problem**: `Cannot access Cloud Storage bucket`
**Solution**: Ensure bucket name is `gospel-guide-content-gospel-study-474301`, not just `gospel-study-474301`

### Container Startup Failures
**Problem**: `The user-provided container failed the configured startup probe checks`
**Solutions**:
- Check logs: `gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=gospel-guide-api" --limit=20`
- Verify OPENAI_API_KEY is set: `echo $OPENAI_API_KEY`
- Check bucket exists: `gsutil ls -p gospel-study-474301`

### Service Shows Error in Console
**Problem**: Red error status in Cloud Run console
**Causes**:
- Failed recent deployments (even if older revision works)
- Environment variable type mismatches
- Missing API keys or bucket access

**Solution**: Use the updated deploy.sh which prevents these issues by:
1. Running pre-deployment validation (check-deploy.sh)
2. Clearing existing env vars/secrets automatically
3. Using proper startup probe configuration  
4. Testing deployment health automatically

### Pre-Deployment Validation
Run `./check-deploy.sh` before deploying to catch common issues:
- ✅ Google Cloud authentication
- ✅ Project configuration
- ✅ API keys and environment setup  
- ✅ Required Cloud APIs enabled
- ✅ Cloud Storage bucket exists
- ✅ Content and index files present

### Debug Commands
```bash
# Check deployment status
./check-status.sh

# Manual service status
gcloud run services describe gospel-guide-api --region=us-central1

# View recent logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=gospel-guide-api" --limit=20

# Test API health
curl https://gospel-guide-api-273320302933.us-central1.run.app/health

# Test streaming endpoint
curl -X POST "https://gospel-guide-api-273320302933.us-central1.run.app/ask/stream" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is faith?"}'
```

## 🚀 **Quick Start**

### Environment Setup
```bash
# Create .env file in backend/ directory
cd backend
echo "OPENAI_API_KEY=your-openai-api-key-here" > .env
```

### Backend (API Server)
```bash
cd backend/search
export OPENAI_API_KEY="your-openai-api-key"
pip install -r requirements.txt
python3 -c "
import uvicorn
from api import app
uvicorn.run(app, host='127.0.0.1', port=8080)
"
```

### Frontend (Next.js)
```bash  
cd frontend
npm install
npm run dev
```

## 📊 **Performance Metrics**
- **⚡ Response Time**: ~2-3 seconds for AI-generated responses
- **📚 Content Coverage**: 58,088 scripture segments across all standard works
- **📅 Come Follow Me**: 21 weeks of 2025 Doctrine & Covenants lessons with real dates
- **🎯 Search Accuracy**: Vector similarity with contextual AI interpretation
- **💻 Streaming**: Real-time response generation with Server-Sent Events
- **🎨 User Experience**: Sidebar-driven mode selection with audience targeting

## 🔮 **Planned API Features (Coming Soon)**
```typescript
// Come Follow Me API endpoints (in development)
GET  /api/cfm/lessons?year=2025           // List all CFM lessons
GET  /api/cfm/current                     // Get current week lesson
POST /api/cfm/ask                         // CFM-specific AI questions
```

## 💎 **Future Premium Mode Ideas**
*Saved for potential paid tier expansions:*

### **Specialized Study Modes**
- **`book-of-mormon-only`**: Missionary-focused mode limited to Book of Mormon text only
  - *Tone*: Enthusiastic missionary spirit with phrases like "I know this book is true"
  - *Content*: Book of Mormon + Introduction/Testimony only, no other scriptures
  - *Use Case*: Mission prep, focused Book of Mormon study

- **`general-conference-only`**: Official apostolic teachings mode (1971-present)
  - *Tone*: Formal apostolic language, exact conference citations
  - *Content*: General Conference addresses exclusively
  - *Use Case*: Conference talk study, official Church position research

- **`youth`**: Seminary teacher style for teenagers
  - *Tone*: Excited, simple language with "Isn't that so cool?!" enthusiasm
  - *Content*: All sources but age-appropriate explanations
  - *Use Case*: Youth groups, seminary discussions

- **`scholar`**: Academic depth for institute/CES instructors
  - *Tone*: BYU religion professor with original languages and detailed context
  - *Content*: All sources plus chiastic structures, JST notes, cross-references
  - *Use Case*: Advanced study, teaching preparation

- **`church-approved-only`**: Official sources verification mode
  - *Tone*: Official Church position statements
  - *Content*: Standard Works, General Conference, manuals, Gospel Topics Essays only
  - *Use Case*: Doctrinal clarification, official position verification

- **`personal-journal`**: Private study companion (future)
  - *Tone*: Personal and reverent, referencing user's study history
  - *Content*: User's uploaded notes, patriarchal blessing, study journal
  - *Use Case*: Personal revelation tracking, private study enhancement

---

**🎯 Goal**: Generate $49.5k in first 48 hours with 500 lifetime licenses.

**✅ Status**: Ready for production launch with Come Follow Me study mode! 🚀📅