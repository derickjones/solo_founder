# Solo Founder - Gospel Study AI Project

> **Mission**: Ship a paid, production-ready LDS AI Scripture Study App in <14 days

## 🎯 **Project Status: 95% Complete**

**November 29, 2025** - Full-stack application deployed and functional.

### 🚀 **Live Deployments**
- **API**: https://gospel-guide-api-273320302933.us-central1.run.app
- **Frontend**: Deployed on Vercel (connected to production API)
- **Repository**: https://github.com/derickjones/solo_founder

### ✅ **What's Working**
- Complete LDS content pipeline (58,088 segments across 45MB)
- OpenAI embeddings + FAISS vector search
- FastAPI backend deployed on Google Cloud Run  
- Next.js frontend with chat interface deployed on Vercel
- 8 specialized search modes (Book of Mormon, General Conference, etc.)

### ⚠️ **Single Issue Remaining**
- Search returns placeholders instead of full text content
- **Fix**: Rebuild embeddings with content included (~15 minutes)
- **Then**: 100% functional Gospel Study app ready for users

## 📁 **Project Structure**

```
├── gospelguide/              # Backend & AI Pipeline
│   ├── scripts/             # ✅ Web scrapers + 45MB content
│   ├── search/              # ✅ OpenAI + FAISS search engine  
│   ├── Dockerfile           # ✅ Google Cloud Run deployment
│   └── README.md           # Full project documentation
│
├── gospelguide-frontend/     # Next.js Frontend
│   ├── src/app/            # ✅ Chat interface + dark theme
│   ├── src/components/     # ✅ Sidebar with source filtering
│   ├── src/services/       # ✅ API integration
│   └── vercel.json         # ✅ Vercel deployment config
│
└── .env                     # 🔐 Secure API keys
```

## 🎯 **Business Model**
- **Free**: 5 queries/day, basic modes
- **Monthly**: $7.99, unlimited + specialized modes  
- **Lifetime**: $99 (limited 500), advanced study tools

## 🔧 **Tech Stack**
- **Data**: Python scrapers + BeautifulSoup
- **AI**: OpenAI embeddings + FAISS vector search
- **Backend**: FastAPI + Google Cloud Run
- **Frontend**: Next.js 15 + TypeScript + Tailwind CSS
- **Deploy**: Vercel + Google Cloud + GitHub Actions

---

**Goal**: Generate $49.5k in first 48 hours with 500 lifetime licenses.

See `gospelguide/README.md` for detailed technical documentation.