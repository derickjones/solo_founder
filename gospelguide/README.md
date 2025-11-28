# GospelGuide - AI Scripture Study Companion for Latter-day Saints

> **ChatGPT for Latter-day Saints** - Ask any gospel question and get instant, perfectly-cited answers from scriptures + General Conference + Church materials.

## 🎯 Mission

Build the most trusted AI scripture study tool in the Church. Launch with 500 lifetime licenses at $99 each to generate $49.5k in first 48 hours.

## 🏗️ Tech Stack

- **Frontend**: Next.js 15 + TypeScript + Tailwind CSS + shadcn/ui
- **Authentication**: Clerk (social login, user management + metadata storage)
- **Vector Search**: FAISS (local index files) + Google Cloud Storage
- **AI**: OpenAI (embeddings + generation) - single provider for consistency
- **Payments**: Stripe (subscriptions + one-time lifetime)
- **Backend**: Google Cloud Run (containerized RAG API)
- **Hosting**: Vercel (frontend) + Google Cloud Storage (content files)

## 💰 Pricing Strategy

### 🆓 Free Tier (5 queries/day)
- **Default Mode**: Full access to Standard Works + General Conference
- All content, smart citations, testimony-bearing responses
- **Goal**: Viral growth through generous free value

### 📅 Monthly ($7.99/month) - Unlimited + Specialized Modes
- Unlimited queries
- **Come Follow Me Mode**: Weekly family study companion
- **Youth Mode**: Seminary teacher voice for teenagers  
- **Church Approved Only**: Conservative users, official sources only

### 🏆 Lifetime ($99 - Limited 500) - Advanced Study Tools
- All Monthly modes PLUS:
- **Book of Mormon Only**: Missionary prep focused
- **General Conference Only**: Apostolic teachings exclusively
- **Scholar Mode**: BYU religion professor depth
- **Personal Journal**: Upload your own study notes

## 🎨 Specialized Study Modes

Each mode has a distinct personality and knowledge scope:

### 📖 Book of Mormon Only
*"Missionary-minded assistant"* - Testimony-bearing, mission prep focused

### 🎤 General Conference Only  
*"Meticulous apostolic teachings"* - First Presidency & Twelve only, chronological citations

### 📅 Come Follow Me 2025
*"Ultimate CFM companion"* - D&C/Church History, family discussion ready

### 👥 Youth Mode
*"Seminary teacher energy"* - 14-year-old friendly, excited, authentic testimony

### 🔒 Church Approved Only
*"Ultra-conservative"* - Standard Works, Conference, manuals, Gospel Topics Essays only

### 🎓 Scholar Mode  
*"BYU religion PhD"* - Original languages, chiasmus, JST notes, academic depth

### 📝 Personal Journal
*"Your private study companion"* - Search your uploaded notes, patriarchal blessing, personal insights

## 🗄️ Data Architecture (Database-Free)

```
Content Storage (Google Cloud Storage):
├── real_book_of_mormon.json     # ✅ COMPLETE: 6,604 verses (Nov 26)
├── old_testament.json           # 🔄 READY: Individual scraper created
├── new_testament.json           # 🔄 READY: Individual scraper created  
├── doctrine_covenants.json      # 🔄 READY: Individual scraper created
├── pearl_of_great_price.json    # ✅ TESTED: Working scraper (73 verses sample)
├── general_conference.json      # ✅ WORKING: 2015-2025 scraper ready
├── study_helps.json             # ✅ WORKING: Bible Dictionary + Study Helps
├── come_follow_me.json          # ✅ EXISTING: CFM content ready
├── scriptures.faiss             # FAISS vector index (after embedding)
├── metadata_mapping.json        # ID → citation lookup
└── /users/{clerk_id}.json       # Individual user data (optional)

User Management:
├── Clerk user metadata          # Subscription tiers, usage tracking
├── Local storage               # Chat history (browser)
└── Stripe webhooks             # Payment status updates

Current Content Status:
├── ✅ Book of Mormon: 6,604 verses COMPLETE with proper citations
├── ✅ Modular Scraping: 8 individual scrapers + master orchestrator
├── ✅ General Conference: 2015-2025 scraper (1,878+ paragraphs tested)
├── ✅ Study Helps: Working Bible Dictionary + Topical Guide scraper
└── 🎯 Ready for comprehensive content generation
```

**Key Benefits:**
- ✅ **Zero database setup** - no PostgreSQL, no connection pools
- ✅ **Ultra-low costs** - ~$0.10/month storage vs $25+ database
- ✅ **Simple deployment** - just API + files
- ✅ **Fast search** - FAISS in-memory performance

## 🚀 Development Roadmap

### Phase 1: Content & Vector Search (Days 1-3) ✅
- [x] System prompts for all specialized modes
- [x] Book of Mormon scraping: **6,604 verses COMPLETE** 
- [x] Modern LDS.org scraping method (fixed URL patterns + extraction)
- [x] **Modular Architecture**: Individual scrapers for each Standard Work
- [x] **General Conference**: 2015-2025 scraper (1,878+ paragraphs tested)
- [x] **Study Helps**: Bible Dictionary + Topical Guide scraper working
- [x] **Master Orchestrator**: Run individual scrapers or all together
- [x] Project cleanup: removed test files, cache, duplicate content
- [ ] Complete dataset generation (all Standard Works + Conference + Study Helps)
- [ ] OpenAI embeddings pipeline + FAISS index creation
- [ ] Google Cloud Storage setup for content files

### Phase 2: API & Frontend (Days 4-6)  
- [ ] Google Cloud Run RAG API (FAISS + OpenAI)
- [ ] Next.js chat interface with mode selector
- [ ] Clerk authentication + user metadata storage
- [ ] Stripe integration with usage tracking

### Phase 3: Launch (Days 7-10)
- [ ] Vercel + Cloud Run deployment
- [ ] End-to-end testing of all modes
- [ ] Demo videos + marketing materials
- [ ] Reddit launch + 500 lifetime license campaign

## 🎯 Go-to-Market Strategy

### Week 1: Free Tier Validation
**Target**: r/latterdaysaints (300k+ members)
**Message**: "Free LDS AI with perfect citations"
**Goal**: 10k+ users, validate product-market fit

### Week 2: Family Focus
**Target**: Come Follow Me Facebook groups (largest LDS communities)
**Message**: "The CFM companion every family needs"  
**Goal**: Convert families to $7.99/month

### Week 3: Lifetime Launch
**Target**: LDS educators, institute teachers, religion professors
**Message**: "Advanced study tools - only 500 available"
**Goal**: $49.5k instant revenue from lifetime licenses

## � Competitive Advantages

**vs ChatGPT**: LDS-specific training, exact scriptural citations, testimony-bearing tone
**vs LDS.org**: Natural language queries, cross-referencing, conversational AI
**vs Scripture apps**: Specialized study modes, AI insights, personal integration
**vs Database solutions**: Zero setup complexity, ultra-low operating costs, simple scaling

## 📊 Current Status (November 26, 2025)

### ✅ Completed
- **Architecture**: Database-free, all-OpenAI approach finalized
- **System Prompts**: 8 specialized modes (scholar, youth, CFM, etc.) 
- **Book of Mormon**: **6,604 verses scraped and saved** ✨
- **Modular Scraping**: 8 individual scrapers + master orchestrator created
- **General Conference**: Working 2015-2025 scraper (1,878+ paragraphs tested)
- **Study Helps**: Bible Dictionary + Topical Guide scraper functional
- **Modern Scraping**: Fixed LDS.org extraction (p.verse + span.verse-number)
- **Project Cleanup**: Removed old monolithic scraper, test files, cache files
- **Clean Structure**: Modular architecture with individual + master scrapers

### 🎯 Ready to Execute  
- **Complete Dataset**: Run all scrapers to generate full content library
- **Estimated Content**: ~50k+ verses + 10k+ conference paragraphs + study helps
- **Vector Pipeline**: OpenAI embeddings + FAISS index creation

### ⏳ Next Steps
- Run complete dataset generation with master orchestrator
- Create OpenAI embeddings + FAISS index for full content library  
- Build Google Cloud Run RAG API
- Develop Next.js frontend with Clerk auth

## 📊 Success Metrics

- **Month 1**: 10k+ free users, 500+ paid subscribers
- **Month 3**: $25k+ MRR, 500 lifetime sales completed  
- **Month 12**: $100k+ MRR, Spanish/Portuguese expansion
- **Year 2**: $500k+ ARR solo founder business

## 🔧 Local Development

```bash
# Clone and install
git clone https://github.com/derickjones/solo_founder
cd solo_founder/gospelguide

# Environment setup
cp .env.local.example .env.local
# Add your API keys (OpenAI, Clerk, Stripe, Google Cloud)

# Content preparation
cd scripts 
pip install -r requirements.txt

# Individual scrapers (run separately)
python scrape_book_of_mormon.py        # ✅ Complete (6,604 verses)
python scrape_old_testament.py         # Individual OT books
python scrape_new_testament.py         # Individual NT books  
python scrape_doctrine_covenants.py    # D&C sections + Official Declarations
python scrape_pearl_great_price.py     # PoGP books
python scrape_general_conference.py    # 2015-2025 talks
python scrape_study_helps.py          # Bible Dictionary + Study Helps

# Master orchestrator (run all at once)
python master_scraper.py              # Runs all scrapers + creates master dataset
python master_scraper.py --only general-conference  # Run specific scraper
python master_scraper.py --test       # Test mode with limits

# Build vector index (after all scraping completes)  
python create_embeddings.py

# Start development
cd .. && npm run dev
```

## 📁 Current Project Structure (Clean & Modular)

```
gospelguide/
├── README.md                             # This file  
├── .gitignore                           # Git ignore rules
├── scripts/                             # Modular content pipeline
│   ├── master_scraper.py               # 🎯 Master orchestrator (run all/specific)
│   ├── scrape_book_of_mormon.py        # ✅ Book of Mormon scraper  
│   ├── scrape_old_testament.py         # Old Testament books
│   ├── scrape_new_testament.py         # New Testament books
│   ├── scrape_doctrine_covenants.py    # D&C + Official Declarations
│   ├── scrape_pearl_great_price.py     # ✅ Pearl of Great Price scraper
│   ├── scrape_general_conference.py    # ✅ General Conference 2015-2025
│   ├── scrape_study_helps.py          # ✅ Study Helps scraper
│   ├── requirements.txt               # Python dependencies
│   └── content/                       # Scraped content storage
│       ├── real_book_of_mormon.json   # ✅ 6,604 verses (4MB)
│       ├── old_testament.json          # Generated by scraper
│       ├── new_testament.json          # Generated by scraper  
│       ├── doctrine_covenants.json     # Generated by scraper
│       ├── pearl_of_great_price.json   # ✅ Test data (73 verses)
│       ├── general_conference.json     # Generated by scraper
│       ├── study_helps.json           # Generated by scraper
│       ├── come_follow_me.json        # ✅ Existing CFM content
│       └── complete_lds_content.json  # Master dataset (all combined)
└── src/                               # Frontend code
    └── lib/
        └── prompts.ts                  # 8 specialized AI system prompts
```

**Architecture Benefits:**
- ✅ **Modular**: Run individual scrapers or master orchestrator
- ✅ **Flexible**: Generate specific content types as needed
- ✅ **Testable**: Each scraper has test modes with limits
- ✅ **Maintainable**: Clear separation of concerns
- ✅ **Scalable**: Easy to add new content sources

**Total**: 12 essential files (8 scrapers + master + support files)

## 📝 Environment Variables

```env
# OpenAI (embeddings + generation)
OPENAI_API_KEY=sk-...

# Authentication (Clerk)
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=
CLERK_SECRET_KEY=

# Payments (Stripe)
STRIPE_SECRET_KEY=
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=

# Google Cloud (storage + compute)
GOOGLE_CLOUD_PROJECT_ID=
GOOGLE_CLOUD_STORAGE_BUCKET=
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json

# Cloud Run API endpoint (after deployment)
NEXT_PUBLIC_API_URL=https://your-api-cloudrun-url
```

## 🎨 Design Philosophy

**Voice**: Warm, faithful BYU religion professor who believes every word
**Citations**: Always exact - (Alma 32:21), (Oct 2024, Nelson, "Think Celestial!")
**Testimony**: Natural, authentic testimony phrases that feel genuine
**Safety**: Sacred topics handled with reverence, policy questions redirected

## 📚 Content Sources

### Standard Works
- Book of Mormon (verse-level chunking)
- Doctrine & Covenants (section-level)
- Pearl of Great Price (chapter-level)  
- Bible (KJV, verse-level)

### Modern Revelation
- General Conference (1971-2025)
- Come Follow Me manuals (current year)
- Saints volumes 1-4
- Gospel Topics Essays

### Future Content
- Church magazines (Ensign, Liahona)
- Seminary/Institute manuals
- Handbooks (public portions)
- Multiple languages

## 🌍 Expansion Roadmap

**Year 1**: English, FAISS-based search, $500k ARR
**Year 2**: Spanish, Portuguese markets, advanced vector search (+200% growth)
**Year 3**: Mobile apps, offline sync, $2M+ ARR  
**Year 4**: Audio integration, temple prep modes, multi-modal search
**Year 5**: Exit opportunity or $5M+ lifestyle business

---

*"Build the best AI scripture study tool in the Church using simple, reliable technology. Focus on user experience over infrastructure complexity. Let the LDS community's word-of-mouth do the rest."*

**Database-free architecture = faster shipping, lower costs, higher margins.**