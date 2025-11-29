# Solo Founder - Gospel Guide AI

> **Mission**: Ship a paid, production-ready LDS AI Scripture Study App in <14 days

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
├── frontend/               # ⚛️ Next.js React Frontend  
│   ├── src/
│   │   ├── components/     # 🧩 ChatInterface with streaming
│   │   ├── app/           # 📱 Next.js 15 app structure
│   │   └── services/      # 🔌 API integration
│   ├── vercel.json        # ⚡ Auto-deploy configuration
│   └── package.json       # 📦 Dependencies
│
└── .gitignore             # � Security & clean repo
```

## 🎯 **Business Model**
- **Free Tier**: 5 queries/day, basic search modes
- **Premium Monthly**: $7.99/month, unlimited queries + all specialized modes  
- **Lifetime Access**: $99 (limited to 500 users), advanced study tools

## 🔧 **Tech Stack**
- **🕷️ Data Pipeline**: Python scrapers + BeautifulSoup (45MB LDS content)
- **🧠 AI Engine**: OpenAI GPT-4o-mini + FAISS vector search + custom prompts
- **⚡ Backend**: FastAPI + streaming endpoints + Google Cloud Run
- **⚛️ Frontend**: Next.js 15 + TypeScript + Tailwind CSS + real-time streaming
- **🚀 Deployment**: Vercel (frontend) + Google Cloud Run (backend) + GitHub auto-deploy

## 🚀 **Quick Start**

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
- **🎯 Search Accuracy**: Vector similarity with contextual AI interpretation
- **💻 Streaming**: Real-time response generation with Server-Sent Events

---

**🎯 Goal**: Generate $49.5k in first 48 hours with 500 lifetime licenses.

**✅ Status**: Ready for production launch! 🚀