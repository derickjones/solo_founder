# Gospel Study Assistant - LDS AI Study Platform

> **Production-ready LDS AI Scripture Study App with complete Come Follow Me system**

## 🚀 **Live Deployments**
- **🌐 Frontend**: https://vercel.com/derick-jones-projects/solo-founder (Vercel)
- **🔌 API**: https://gospel-guide-api-273320302933.us-central1.run.app (Google Cloud Run)
- **📚 Repository**: https://github.com/derickjones/solo_founder

## ✨ **Key Features**
- **🧠 AI-Powered Study**: Grok AI with real-time streaming responses
- **📖 Complete LDS Library**: 58,088+ scripture segments with FAISS vector search
- **📅 Come Follow Me 2026**: Complete Old Testament study system with enhanced scripture bundles
- **🎯 Four CFM Study Types**: Deep Dive Study, Lesson Plans, Audio Summaries, Core Content
- **� Three Study Levels**: Essential, Connected, Scholarly (user-friendly naming)
- **�🔐 Authentication**: Clerk integration with Google/Apple login
- **💳 Payment Processing**: Stripe subscription system ($4.99/month)
- **🎨 Professional UI**: Dark theme with responsive design
- **📱 Mobile Optimized**: Works perfectly on all devices

## 🎵 **Audio Generation System**
- **📊 Three Study Levels**: Essential, Connected, Scholarly with optimized prompts  
- **🎙️ Professional Voice**: ElevenLabs TTS with 5 professional voices (Rachel, Drew, Paul, Antoni, Bella)
- **🧩 Smart Text Chunking**: Handles TTS character limits seamlessly
- **🎛️ Modern Audio Player**: Speed controls, seeking, volume control, collapsible interface
- **📝 Script-First Design**: Shows transcript by default, optional audio generation

## 💰 **Business Model**
- **Free Tier**: Basic Q&A with daily limits
- **Premium**: $4.99/month - Unlimited queries + CFM features
- **Target Revenue**: $2,500/month with 500 subscribers

## 🏗️ **Technical Architecture**

### ⚛️ **Frontend (Next.js 16)**
- **TypeScript + Tailwind CSS**: Modern React with full type safety
- **Streaming Interface**: Real-time AI responses with CFM study generation
- **Study Level System**: Essential/Connected/Scholarly naming for better UX
- **Authentication**: Clerk integration with social login
- **Payment Integration**: Stripe Checkout with subscription management

### 🐍 **Backend (FastAPI)**
- **Dual AI Integration**: Grok AI for content generation + ElevenLabs TTS for audio
- **Streaming API**: Server-Sent Events for real-time responses
- **Vector Search**: FAISS-powered semantic search
- **Audio Generation**: ElevenLabs TTS with professional voices and smart text chunking
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
XAI_API_KEY=your_grok_key           # For AI content generation (CFM Deep Dive, Lesson Plans, Audio Scripts)
ELEVENLABS_API_KEY=your_elevenlabs_key  # For high-quality TTS audio generation
OPENAI_API_KEY=your_openai_key      # Legacy - kept for potential fallback
CLERK_SECRET_KEY=your_clerk_key
STRIPE_SECRET_KEY=your_stripe_key

# Frontend (.env.local)
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_clerk_key
STRIPE_PUBLISHABLE_KEY=your_stripe_key
NEXT_PUBLIC_API_BASE_URL=https://gospel-guide-api-273320302933.us-central1.run.app
```

## 📚 **API Endpoints**

### **Core Scripture Search**
- `GET /search` - Semantic scripture search with context
- `POST /search/ask` - AI-powered Q&A with streaming responses

### **Come Follow Me System**
- `POST /cfm/deep-dive` - Comprehensive study guides (Essential/Connected/Scholarly)
- `POST /cfm/lesson-plans` - Teaching materials (Adult/Youth/Children audiences)  
- `POST /cfm/audio-summary` - Generated audio talk scripts (Essential/Connected/Scholarly)
- `POST /cfm/core-content` - Raw CFM materials organized by sections

### **Study Level System**
All CFM endpoints use consistent study levels:
- **Essential**: Foundational gospel principles and basic understanding
- **Connected**: Deeper doctrinal connections and cross-references  
- **Scholarly**: Advanced theological analysis and historical context

### **System Health**
- `GET /health` - API status and version info
- `GET /debug/bundle/{week}` - Bundle loading diagnostics

## 🧪 **Testing**

```bash
# Test CFM endpoints with new study levels
curl -X POST "https://gospel-guide-api-273320302933.us-central1.run.app/cfm/deep-dive" \
  -H "Content-Type: application/json" \
  -d '{"week_number": 2, "study_level": "essential"}'

curl -X POST "https://gospel-guide-api-273320302933.us-central1.run.app/cfm/audio-summary" \
  -H "Content-Type: application/json" \
  -d '{"week_number": 2, "study_level": "connected"}'

# Test specific week bundle
curl -X GET "https://gospel-guide-api-273320302933.us-central1.run.app/debug/bundle/32"

# Health check
curl -X GET "https://gospel-guide-api-273320302933.us-central1.run.app/health"
```

## 🚀 **Deployment**

### **Docker Build & Deploy**
```bash
# Build and push to Artifact Registry
cd backend
gcloud builds submit --tag us-central1-docker.pkg.dev/gospel-study-474301/gospel-guide/gospel-guide-api .

# Deploy to Cloud Run
gcloud run deploy gospel-guide-api \
  --image us-central1-docker.pkg.dev/gospel-study-474301/gospel-guide/gospel-guide-api \
  --platform managed --region us-central1 --allow-unauthenticated \
  --memory=2Gi --cpu=1
```

### **Frontend Deployment**
```bash
# Automatic deployment via GitHub integration
git push origin main  # Triggers Vercel deployment

# Manual deployment
vercel --prod
```

## 📈 **Performance**

- **Scripture Search**: <200ms average response
- **AI Content Generation**: Real-time streaming with Grok AI
- **Audio Script Generation**: 5-30s depending on study level complexity
- **Vector Search**: 58,088+ segments indexed with FAISS
- **Mobile Performance**: Optimized for iOS/Android
- **Study Level Consistency**: Unified Essential/Connected/Scholarly across all features

## 🔧 **Recent Updates (December 2024)**

- **✅ ElevenLabs TTS Integration**: Replaced OpenAI TTS with professional-grade ElevenLabs voices for superior audio quality
- **✅ Study Level Rebranding**: Updated from Basic/Intermediate/Advanced to Essential/Connected/Scholarly for better user appeal
- **✅ Dual AI Integration**: Grok AI for content generation, ElevenLabs for audio synthesis
- **✅ TypeScript Consistency**: Fixed all type definitions across frontend and backend
- **✅ API Standardization**: All CFM endpoints now use unified study_level parameter
- **✅ User Experience**: Improved naming scheme specifically for LDS audience engagement
- **✅ Professional Audio**: 5 voice options (Rachel, Drew, Paul, Antoni, Bella) with smart chunking

## 🔧 **Troubleshooting**

- **Study Level Errors**: Ensure using Essential/Connected/Scholarly (not old Basic/Intermediate/Advanced)
- **Audio Generation**: Requires ELEVENLABS_API_KEY environment variable in production
- **Content Generation**: Requires XAI_API_KEY for CFM study guides and lesson plans
- **Bundle Loading**: Debug endpoint at `/debug/bundle/{week}` for CFM content issues
- **Authentication**: Check Clerk configuration in middleware.ts
- **Payment Issues**: Verify Stripe webhook endpoints

## 🎯 **Future Enhancements**

- **🎵 Enhanced Audio**: Background music, multiple speakers, full TTS integration
- **📊 Study Progress**: User analytics and progress tracking across study levels
- **💾 Offline Mode**: Service worker for scripture access without internet
- **👥 Social Features**: Study group sharing and collaborative discussions
- **🔍 Advanced Search**: Cross-reference discovery and thematic study paths
- **🎨 Customization**: Personalized study level preferences and content filtering

---

> **Gospel Study Assistant** - Transforming scripture study with AI-powered insights, unified study levels (Essential/Connected/Scholarly), and comprehensive Come Follow Me resources tailored for the LDS community.