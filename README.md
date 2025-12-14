# Gospel Stud### ✅ **Complete Features**
- **🧠 AI-Powered Study**: OpenAI GPT-4o-mini with real-time streaming responses
- **📖 Complete LDS Library**: 58,088 scripture segments with FAISS vector search
- **📅 Come Follow Me 2026**: Complete Old Testament study system with 51 weekly bundles
- **� CFM Deep Dive API**: Comprehensive study guide generation with 3 sophistication levels
- **�👪 Multi-Audience Support**: Adult, Family, Youth, and Children study modes  
- **📚 Enhanced Content**: Seminary Teacher materials integrated (208 lessons, 47 CFM weeks)
- **🔐 Authentication**: Clerk integration with Google/Apple login
- **💳 Payment Processing**: Stripe subscription system ($4.99/month)
- **🎨 Professional UI**: Elegant dark theme with product onboarding tiles
- **📱 Mobile Responsive**: Works seamlessly across all devicesnt - LDS AI Study Platform

> **Mission**: Production-ready LDS AI Scripture Study App with complete monetization infrastructure

## 🎯 **Project Status: 🚀 MONETIZATION READY (95% Complete)**

**December 9, 2025** - Full-stack AI application with authentication, payment processing, and subscription management.

### 🚀 **Live Deployments**
- **🌐 Frontend**: https://vercel.com/derick-jones-projects/solo-founder (Vercel)
- **🔌 API**: https://gospel-guide-api-273320302933.us-central1.run.app (Google Cloud Run)
- **📚 Repository**: https://github.com/derickjones/solo_founder

### ✅ **Complete Features**
- **🧠 AI-Powered Study**: OpenAI GPT-4o-mini with real-time streaming responses
- **📖 Complete LDS Library**: 58,088 scripture segments with FAISS vector search
- **📅 Come Follow Me 2025**: Complete Doctrine & Covenants lesson planner
- **👪 Multi-Audience Support**: Adult, Family, Youth, and Children study modes
- **🔐 Authentication**: Clerk integration with Google/Apple login
- **💳 Payment Processing**: Stripe subscription system ($4.99/month)
- **🎨 Professional UI**: Elegant dark theme with product onboarding tiles
- **� Mobile Responsive**: Works seamlessly across all devices

## 🎯 **Business Model**

### 💰 **Pricing Strategy**
- **Free Tier**: Basic Q&A with daily question limits
- **Premium**: $4.99/month - Unlimited queries + Come Follow Me lesson planning
- **Target Revenue**: $2,500/month with 500 subscribers

### 📊 **Revenue Projections**
- **Conservative**: 200 subscribers × $4.99 = $998/month
- **Realistic**: 500 subscribers × $4.99 = $2,495/month  
- **Optimistic**: 1,000 subscribers × $4.99 = $4,990/month

## 🏗️ **Technical Architecture**

### ⚛️ **Frontend (Next.js 16)**
- **TypeScript + Tailwind CSS**: Modern React with full type safety
- **Dual Mode Interface**: Q&A streaming chat + CFM lesson generation
- **Product Onboarding**: Auto-hiding tiles with bullet points and color themes
- **Sidebar Controls**: Dynamic mode switching with authentication
- **Payment Integration**: Stripe Checkout with subscription management

### 🐍 **Backend (FastAPI)**
- **Streaming API**: Server-Sent Events for real-time AI responses
- **Vector Search**: FAISS-powered semantic search across 58k+ segments
- **AI Integration**: OpenAI GPT-4o-mini with specialized prompts
- **Content Pipeline**: Automated web scraping and embedding generation
- **Cloud Storage**: Google Cloud Storage for indexes and metadata

### � **Authentication & Payments**
- **Clerk**: Complete user management with social login
- **Stripe**: Subscription processing with webhook handling
- **Legal Framework**: Commercial-ready Terms of Use

## � **Project Structure**

```
solo_founder/
├── README.md                      # 📋 Project documentation
├── backend/                       # 🐍 Python Backend
│   ├── search/                    # 🔍 AI search & response system
│   │   ├── api.py                # 🌐 FastAPI with streaming endpoints
│   │   ├── scripture_search.py   # 📚 FAISS vector search
│   │   ├── prompts.py            # 🧠 AI prompt engineering
│   │   └── indexes/              # 💾 Vector database
│   ├── scripts/                  # 🕷️ Content acquisition pipeline
│   │   ├── cfm/                  # 📅 Come Follow Me system
│   │   │   ├── core/             # 🏗️ Modular CFM infrastructure
│   │   │   └── years/cfm_2026/   # 📖 2026 Old Testament bundles
│   │   ├── content/              # 📊 Generated weekly study materials
│   │   └── scrapers/             # 🔧 Scripture & lesson scrapers
│   └── deploy.sh                 # 🚀 Cloud Run deployment
│
├── frontend/                     # ⚛️ Next.js Frontend
│   ├── src/
│   │   ├── components/           # 🧩 React Components
│   │   │   ├── ChatInterface.tsx # 💬 Main chat with product tiles
│   │   │   └── Sidebar.tsx       # 📋 Mode selector + authentication
│   │   ├── app/                  # 📱 App Router with auth pages
│   │   └── services/             # 🔌 API integration
│   └── package.json              # � Dependencies + auth/payment
```

## 🚀 **Getting Started**

### 🔑 **Environment Setup**
```bash
# Frontend (.env.local)
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...

# Backend (.env)
OPENAI_API_KEY=sk-...
```

### 🏃‍♂️ **Local Development**
```bash
# Backend
cd backend/search
pip install -r requirements.txt
python3 api.py

# Frontend
cd frontend
npm install
npm run dev
```

### 🚀 **Deployment**
```bash
# Backend to Google Cloud Run
cd backend
./deploy.sh

# Frontend to Vercel
cd frontend
vercel --prod
```

## 📊 **Performance Metrics**
- **Q&A Response Time**: 2-3 seconds with streaming
- **CFM Generation**: 13-22 seconds for comprehensive lesson plans
- **🆕 CFM Deep Dive**: 20-25 seconds for advanced study guides with 6+ sources
- **Content Coverage**: 58,088 scripture segments + 239 CFM sources
- **2026 Study System**: 51 weeks of Old Testament curriculum (2M+ characters)  
- **📚 Seminary Integration**: 208 lessons mapped to 47 CFM weeks
- **Search Accuracy**: Vector similarity + AI interpretation

## � **API Endpoints**
```typescript
// Core Features
POST /ask/stream              // Streaming AI responses
POST /cfm/lesson-plan         // Generate lesson plans  
POST /cfm/deep-dive          // 🆕 Advanced study guides (Basic/Intermediate/Advanced)
GET  /search                  // Vector search
GET  /health                  // Service monitoring

// CFM Deep Dive API
POST /cfm/deep-dive
{
  "week_number": 3,           // Week 1-51 for 2026 Old Testament
  "study_level": "advanced"   // "basic" | "intermediate" | "advanced"
}

// Response includes:
{
  "week_number": 3,
  "week_title": "Genesis 1–2; Moses 2–3; Abraham 4–5", 
  "study_level": "advanced",
  "study_guide": "### Comprehensive study content...",
  "bundle_sources": 6,
  "total_characters": 48544,
  "generation_time_ms": 25515
}

// Authentication (Clerk)
GET  /sign-in                 // Custom sign-in page
GET  /sign-up                 // Registration page

// Payments (Stripe)  
POST /api/stripe/checkout     // Create subscription
POST /api/stripe/webhook      // Handle events
GET  /pricing                 // Subscription plans
```

## 🎯 **Launch Checklist**
- [x] Complete authentication system
- [x] Payment infrastructure  
- [x] Production deployment
- [x] Product onboarding experience
- [ ] Stripe account setup and live API keys
- [ ] Usage tracking implementation
- [ ] Final testing and launch

**🎉 Ready to launch with just Stripe account configuration remaining!**

---
*Built with ❤️ for the LDS community*
    A[User] --> B[Next.js Frontend<br/>Vercel]
    B --> C[Clerk Auth<br/>Google/Apple Login]
    B --> D[FastAPI Backend<br/>Google Cloud Run]
    B --> E[Stripe Checkout<br/>$4.99/month]
    D --> F[OpenAI API<br/>GPT-4o-mini]
    D --> G[FAISS Vector DB<br/>58k embeddings]
    D --> H[Google Cloud Storage<br/>Indexes & Metadata]
    C --> I[User Management<br/>Protected Routes]
    E --> J[Webhook Processing<br/>Subscription Updates]
    
    K[Web Scrapers] --> L[Content Pipeline]
    L --> M[Embedding Generator]
    M --> G
```

### 🏛️ **Backend Architecture**

#### 🔍 **Search & AI Engine** (`backend/search/`)
- **`api.py`**: FastAPI server with streaming SSE endpoints
  - `/ask-stream` - Real-time AI responses with search results for Q&A mode
  - `/cfm/lesson-plan` - Audience-specific Come Follow Me lesson generation  
  - `/cfm/deep-dive` - **🆕 Advanced study guides** with 3 sophistication levels (Basic/Intermediate/Advanced)
  - `/search` - Vector similarity search across scripture corpus
  - `/health` - Service health monitoring
  - CORS middleware for frontend integration
- **`scripture_search.py`**: FAISS-powered semantic search engine
  - OpenAI embeddings (`text-embedding-3-small`) for query vectorization
  - Metadata filtering by source, book, speaker, year
  - Cosine similarity ranking with configurable top-k results
- **`prompts.py`**: Intelligent prompt engineering system
  - Mode-specific system prompts (Youth, Scholar, General Conference)
  - **CFM Lesson Prompts**: 4 specialized prompts for Adults, Family, Youth, Children
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
- **📅 CFM Pipeline** (`cfm/`): **Complete 2026 Old Testament System**
  - **Core Infrastructure** (`core/`): Modular base classes and schema
  - **2026 Bundles** (`years/cfm_2026/`): 51-week Old Testament curriculum
  - **Unified Content** (`cfm_2026_old_testament/`): Weekly bundle generation pipeline
  - **📚 Seminary Integration**: Enhanced Seminary Teacher materials (208 lessons)
- **Individual Scrapers**: Modular content extractors
  - `scrape_book_of_mormon.py`, `scrape_general_conference.py`, etc.
  - `scrape_seminary.py` - **🆕 Seminary Teacher lesson integration**  
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
- **App Router**: Modern Next.js file-based routing with authentication
- **TypeScript**: Full type safety across components and services
- **Tailwind CSS 4**: Utility-first styling with elegant blue glow design
- **Server-Side Rendering**: Optimized SEO and performance
- **Clerk Integration**: Complete user management with social login
- **Stripe Integration**: Subscription payment processing

#### 🧩 **Component Architecture**
- **`ChatInterface.tsx`**: Main conversation component
  - **Dual Mode Support**: Q&A streaming chat + CFM lesson plan generation
  - **Smart Input**: Text input for Q&A, "Generate Lesson Plan" button for CFM
  - ReactMarkdown integration for rich text formatting
  - Message history with search result citations
  - Mode selection and audience/week configuration
  - Copy-to-clipboard functionality and keyboard shortcuts (Ctrl+/, Esc)
- **`Sidebar.tsx`**: Dynamic control interface with authentication
  - **Q&A Mode**: Source filtering (General Conference, Standard Works)
  - **CFM Mode**: Audience selection (Adult/Family/Youth/Children) and week picker
  - **Authentication Section**: User profile, sign-in/sign-up, upgrade buttons
  - Dynamic source count tracking and current week detection
  - Responsive design with elegant blue glow aesthetic

#### 🔐 **Authentication Pages**
- **`/sign-in`**: Custom Clerk sign-in page with dark theme
- **`/sign-up`**: Custom Clerk sign-up page with social login options
- **`/pricing`**: Professional pricing page with Stripe integration

#### 💳 **Payment Integration**
- **`/api/stripe/checkout`**: Stripe Checkout session creation
- **`/api/stripe/webhook`**: Subscription event handling
- **`/pricing`**: Subscription plans and pricing display

#### 🔌 **API Integration** (`services/api.ts`)
- **Streaming API Client**: Custom SSE implementation for Q&A mode
- **CFM Lesson Planner**: Direct API integration for lesson plan generation
- **Request/Response Types**: Full TypeScript interfaces for both modes
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
│
├── frontend/                     # ⚛️ Next.js Frontend
│   ├── package.json             # 📦 Dependencies + Auth/Payment
│   ├── next.config.ts           # ⚙️ Next.js config
│   ├── tsconfig.json           # 🔧 TypeScript config
│   ├── vercel.json             # 🚀 Vercel deployment
│   ├── eslint.config.mjs       # ✨ Code quality
│   ├── postcss.config.mjs      # 🎨 CSS processing
│   ├── middleware.ts           # 🛡️ Clerk auth middleware
│   ├── README.md               # 📖 Frontend docs
│   │
│   ├── public/                 # 🌐 Static assets
│   │   ├── christ.jpeg         # 🖼️ Logo image
│   │   └── *.svg              # 📐 Icon assets
│   │
│   └── src/                    # 💻 Application source
│       ├── app/                # 🏠 Next.js App Router
│       │   ├── layout.tsx      # 📱 Root layout + Clerk Provider
│       │   ├── page.tsx        # 🏡 Home page
│       │   ├── globals.css     # 🎨 Global styles
│       │   ├── favicon.ico     # 🌟 Browser icon
│       │   ├── sign-in/        # 🔐 Authentication pages
│       │   ├── sign-up/        # 📝 User registration
│       │   ├── pricing/        # 💳 Subscription plans
│       │   └── api/            # 🔌 API routes
│       │       └── stripe/     # 💰 Payment processing
│       │
│       ├── components/         # 🧩 React components
│       │   ├── ChatInterface.tsx # 💬 Main chat UI
│       │   └── Sidebar.tsx      # 📋 Source selector + Auth
│       │
│       ├── lib/               # 🛠️ Utilities
│       │   └── stripe.ts      # 💳 Stripe configuration
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

## 🎯 **Business Model & Monetization**

### 💰 **Pricing Strategy**
- **Free Tier**: 5 queries/day, basic Q&A mode only
- **Premium**: $4.99/month - Unlimited queries + Come Follow Me lesson planning
- **Target Revenue**: $2,500/month with 500 subscribers = $30K annually

### 🎯 **Revenue Projections**
- **Conservative**: 200 subscribers × $4.99 = $998/month
- **Realistic**: 500 subscribers × $4.99 = $2,495/month  
- **Optimistic**: 1,000 subscribers × $4.99 = $4,990/month

### 📊 **Customer Acquisition Strategy**
1. **Organic SEO**: Target "LDS study guide", "Come Follow Me help" keywords
2. **Social Media**: LDS Facebook groups, Instagram accounts, Reddit communities
3. **Word of Mouth**: Seminary teachers, Relief Society, Elders Quorum referrals
4. **Content Marketing**: Blog posts on gospel topics, YouTube tutorials
5. **Free Tier Conversion**: Hook users with quality, convert at daily limit

### ⚖️ **Legal Framework**
- **Commercial License**: Professional Terms of Use for LDS content usage
- **Fair Use Compliance**: Transformative AI service with proper attribution
- **Content Attribution**: Clear source citations for all scripture references
- **Privacy Policy**: GDPR/CCPA compliant user data handling

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
- **Tailwind CSS 4**: Utility-first styling with elegant blue glow design
- **Heroicons 2.2**: Consistent icon library from Tailwind team
- **ReactMarkdown 10.1**: Rich text rendering for AI responses
- **Clerk**: Complete authentication system with social login
- **Stripe**: Payment processing and subscription management

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

## 🚀 **Getting Started (Production Ready)**

### 🔑 **Environment Setup**
```bash
# Frontend environment variables (.env.local)
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Backend environment variables (.env)
OPENAI_API_KEY=sk-...
```

### 🏃‍♂️ **Quick Launch**
```bash
# Backend (API Server)
cd backend/search
pip install -r requirements.txt
python3 api.py

# Frontend (Next.js with Auth)
cd frontend
npm install
npm run dev
```

### 🎯 **Final Steps for Monetization**
1. **✅ Clerk Setup**: Create Clerk account, configure OAuth providers
2. **🔲 Stripe Setup**: Create Stripe account, add $4.99/month product
3. **🔲 Environment Variables**: Add real API keys to production
4. **🔲 Domain Setup**: Configure custom domain and SSL
5. **🔲 Analytics**: Add Google Analytics and conversion tracking

**Estimated time to launch**: 2-4 hours (primarily Stripe account setup)

## 📊 **Performance & Metrics**

### ⚡ **Application Performance**
- **Q&A Response Time**: ~2-3 seconds for AI-generated responses with streaming
- **CFM Generation Time**: 13-22 seconds for comprehensive lesson plans
- **Content Coverage**: 58,088 scripture segments across all standard works
- **Come Follow Me**: 21 weeks of 2025 Doctrine & Covenants lessons with real dates
- **Search Accuracy**: Vector similarity with contextual AI interpretation
- **Streaming**: Real-time response generation with Server-Sent Events
- **User Experience**: Sidebar-driven mode selection with audience targeting
- **Lesson Plan Sources**: 48+ sources per lesson plan for comprehensive coverage

### 💳 **Monetization Metrics**
- **Authentication**: Google/Apple social login for seamless onboarding
- **Conversion Rate**: Free tier → Premium at daily query limit
- **Payment Processing**: Stripe Checkout with 99.7% uptime
- **Subscription Management**: Automated billing and cancellation handling
- **User Retention**: Unlimited access drives daily engagement
- **Average Revenue Per User (ARPU)**: $4.99/month base rate

## 🔮 **Latest API Features & Usage**

### 🆕 **CFM Deep Dive API** - Advanced Study Guide Generation

The newest addition to the Gospel Guide API provides comprehensive study guides with three sophistication levels:

**Endpoint**: `POST /cfm/deep-dive`

**Features**:
- **📖 Complete Bundle Context**: Each week's entire content bundle sent to AI (40k+ characters)
- **🎯 Three Study Levels**: Basic, Intermediate, Advanced with increasing depth
- **📚 Multi-Source Integration**: CFM manual + Seminary materials + General Conference
- **⚡ Fast Generation**: 20-25 seconds for comprehensive study guides
- **📊 Rich Metadata**: Source count, character count, generation time included

**Request**:
```json
{
  "week_number": 3,           // Week 1-51 for 2026 Old Testament  
  "study_level": "advanced"   // "basic" | "intermediate" | "advanced"
}
```

**Response**:
```json
{
  "week_number": 3,
  "week_title": "Genesis 1–2; Moses 2–3; Abraham 4–5",
  "study_level": "advanced", 
  "study_guide": "### Complete study content with theological analysis...",
  "bundle_sources": 6,
  "total_characters": 48544,
  "generation_time_ms": 25515
}
```

**Study Level Differences**:

- **Basic**: Simple explanations, practical applications, basic questions
- **Intermediate**: Historical context, cross-references, teaching ideas  
- **Advanced**: Theological analysis, original languages, scholarly insights, prophetic patterns

**Live Example**:
```bash
curl -X POST "https://gospel-guide-api-273320302933.us-central1.run.app/cfm/deep-dive" \
  -H "Content-Type: application/json" \
  -d '{"week_number": 3, "study_level": "advanced"}'
```

This API is perfect for:
- **📖 Personal Study**: Deep theological insights and cross-references
- **👨‍🏫 Teaching Preparation**: Seminary/institute instructors  
- **👪 Family Study**: Age-appropriate content for family discussions
- **🎓 Academic Research**: Scholarly analysis with historical context

---

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

**🎯 Goal**: Launch profitable SaaS with $2,500/month recurring revenue through 500 subscribers.

**🚀 Status**: 90% monetization ready - Stripe account setup remaining!

### 🎉 **Ready-to-Launch Features**
- ✅ **Complete Authentication**: Clerk integration with Google/Apple login
- ✅ **Payment Infrastructure**: Full Stripe subscription system ($4.99/month)
- ✅ **Professional UI**: Elegant blue glow design with sidebar authentication
- ✅ **Legal Framework**: Commercial-ready Terms of Use for LDS content
- ✅ **Q&A Mode**: Real-time streaming responses with 58k+ sources
- ✅ **CFM Mode**: 4 specialized lesson planners (Adult/Family/Youth/Children)  
- ✅ **One-Click Generation**: No typing required for lesson plans
- ✅ **2025 D&C Schedule**: All 21 weeks with actual dates and titles
- ✅ **Professional Quality**: 13-22 second generation with 48+ sources per plan
- ✅ **Mobile Responsive**: Works perfectly on all devices
- ✅ **Production Deployed**: Both frontend and backend live and operational

### 🔲 **Final Launch Checklist** 
1. Create Stripe account and configure $4.99/month product
2. Add Stripe API keys to environment variables
3. Test complete payment flow end-to-end
4. Optional: Set up PostgreSQL for enhanced user tracking
5. Configure domain and go live! 🚀