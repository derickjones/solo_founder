# Gospel Study Assistant - LDS AI Study Platform

> **Production-ready LDS AI Scripture Study App with complete Come Follow Me system**

## 🚀 **Live Deployments**
- **🌐 Frontend**: https://vercel.com/derick-jones-projects/solo-founder (Vercel)
- **🔌 API**: https://gospel-guide-api-273320302933.us-central1.run.app (Google Cloud Run)
- **📚 Repository**: https://github.com/derickjones/solo_founder

## ✨ **Key Features**
- **🧠 AI-Powered Study**: GPT-4o-mini with real-time streaming responses
- **📖 Complete LDS Library**: 58,088 scripture segments with FAISS vector search
- **📅 Come Follow Me 2026**: Complete Old Testament study system with enhanced scripture bundles
- **🎯 Four CFM Study Types**: Deep Dive Study, Lesson Plans, Audio Summaries, Core Content
- **🔐 Authentication**: Clerk integration with Google/Apple login
- **💳 Payment Processing**: Stripe subscription system ($4.99/month)
- **🎨 Professional UI**: Dark theme with responsive design
- **📱 Mobile Optimized**: Works perfectly on all devices

## 🎵 **Audio Generation System**
- **📊 Three Duration Levels**: 5min, 15min, 30min with optimized prompts
- **🎙️ Professional Voice**: OpenAI TTS with multiple voice options
- **🧩 Smart Text Chunking**: Handles TTS character limits seamlessly
- **🎛️ Modern Audio Player**: Speed controls, seeking, volume control, collapsible interface

## 💰 **Business Model**
- **Free Tier**: Basic Q&A with daily limits
- **Premium**: $4.99/month - Unlimited queries + CFM features
- **Target Revenue**: $2,500/month with 500 subscribers

## 🏗️ **Technical Architecture**

### ⚛️ **Frontend (Next.js 16)**
- **TypeScript + Tailwind CSS**: Modern React with full type safety
- **Streaming Interface**: Real-time AI responses with CFM study generation
- **Authentication**: Clerk integration with social login
- **Payment Integration**: Stripe Checkout with subscription management

### 🐍 **Backend (FastAPI)**
- **Streaming API**: Server-Sent Events for real-time responses
- **Vector Search**: FAISS-powered semantic search
- **Audio Generation**: OpenAI TTS with smart text chunking
- **CFM Bundle System**: 52 enhanced weekly bundles with complete scripture content
- **Authentication**: User session management and subscription validation

### 🗄️ **Data Layer**
- **Scripture Database**: 58,088 segments across all LDS standard works
- **Vector Embeddings**: OpenAI text-embedding-3-small for semantic search
- **CFM Content**: Complete 2026 Old Testament study materials with scripture text
- **Enhanced Metadata**: Timestamps, audiences, study levels, content types

### ☁️ **Infrastructure (Google Cloud)**
- **Google Cloud Run**: Auto-scaling serverless containers
- **Artifact Registry**: Secure Docker image storage
- **FAISS Index Storage**: Optimized vector search performance

## 🛠️ **Getting Started**

### **Prerequisites**
```bash
# Required
- Python 3.12+
- Node.js 18+
- Google Cloud CLI
- OpenAI API Key
- Clerk API Keys
- Stripe API Keys
```

### **Quick Start**
```bash
# Backend Setup
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend Setup  
cd frontend
npm install
npm run dev
```

### **Environment Variables**
```bash
# Backend (.env)
OPENAI_API_KEY=your_key
CLERK_SECRET_KEY=your_key
STRIPE_SECRET_KEY=your_key

# Frontend (.env.local)
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_key
STRIPE_PUBLISHABLE_KEY=your_key
```

## 📚 **API Endpoints**

### **Core Scripture Search**
- `GET /search` - Semantic scripture search with context
- `POST /search/ask` - AI-powered Q&A with streaming responses

### **Come Follow Me System**
- `POST /cfm/deep-dive` - Comprehensive study guides (3 levels)
- `POST /cfm/lesson-plans` - Teaching materials (3 audiences)  
- `POST /cfm/audio-summary` - Generated audio talks (3 durations)
- `POST /cfm/core-content` - Raw CFM materials organized

### **System Health**
- `GET /health` - API status and version info
- `GET /debug/bundle/{week}` - Bundle loading diagnostics

## 🧪 **Testing**

```bash
# Run all CFM endpoints
python test_bundle_loading.py

# Test specific week bundle
curl -X GET "https://gospel-guide-api-273320302933.us-central1.run.app/debug/bundle/32"

# Test audio generation
curl -X POST "/cfm/audio-summary" -H "Content-Type: application/json" \
-d '{"week": 32, "duration": "medium", "voice": "alloy"}'
```

## 🚀 **Deployment**

### **Docker Build & Deploy**
```bash
# Build and push to Artifact Registry
docker build -t us-central1-docker.pkg.dev/gospel-guide-api/gospel-guide-repo/backend .
docker push us-central1-docker.pkg.dev/gospel-guide-api/gospel-guide-repo/backend

# Deploy to Cloud Run
gcloud run deploy gospel-guide-api --image us-central1-docker.pkg.dev/gospel-guide-api/gospel-guide-repo/backend
```

### **Frontend Deployment**
```bash
# Deploy to Vercel
vercel --prod
```

## 📈 **Performance**

- **Scripture Search**: <200ms average response
- **AI Q&A Streaming**: Real-time token streaming
- **Audio Generation**: 23-107s depending on duration
- **Vector Search**: 58,088 segments indexed with FAISS
- **Mobile Performance**: Optimized for iOS/Android

## 🔧 **Troubleshooting**

- **Audio Generation Timeout**: Frontend 5-minute limit with error handling
- **Bundle Loading**: Debug endpoint at `/debug/bundle/{week}` 
- **Authentication**: Check Clerk configuration in middleware.ts
- **Payment Issues**: Verify Stripe webhook endpoints

## 🎯 **Future Enhancements**

- **Advanced Audio Features**: Background music, multiple speakers
- **Study Progress Tracking**: User progress analytics
- **Offline Mode**: Service worker for scripture access
- **Social Features**: Study group sharing and discussions

---

> **Gospel Study Assistant** - Transforming scripture study with AI-powered insights and comprehensive Come Follow Me resources.