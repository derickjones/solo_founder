# GospelGuide - AI Scripture Study Companion for Latter-day Saints

> **ChatGPT for Latter-day Saints** - Ask any gospel question and get instant, perfectly-cited answers from scriptures + General Conference + Church materials.

## 🎯 Mission

Build the most trusted AI scripture study tool in the Church. Launch with 500 lifetime licenses at $99 each to generate $49.5k in first 48 hours.

## 🏗️ Tech Stack

- **Frontend**: Next.js 15 + TypeScript + Tailwind CSS + shadcn/ui
- **Authentication**: Clerk (social login, user management)
- **Database**: Supabase (Postgres + pgvector for embeddings)
- **AI**: OpenAI embeddings + Grok (xAI) for generation
- **Payments**: Stripe (subscriptions + one-time lifetime)
- **Hosting**: Vercel (frontend) + edge functions
- **Analytics**: PostHog (user behavior tracking)

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

## 🗄️ Database Schema

```sql
-- Core tables
documents      -- Scripture verses, conference talks, manuals (with vector embeddings)
users          -- Authentication, subscription tiers, usage tracking  
conversations  -- Chat history organized by topic
messages       -- Individual chat messages with AI responses

-- Key features
- pgvector for semantic search
- Usage limits by tier (5/day free, unlimited paid)
- Citation tracking for accuracy verification
- Mode-specific content filtering
```

## 🚀 Development Roadmap

### Phase 1: Foundation (Days 1-4)
- [x] Database schema with pgvector
- [x] System prompts for all modes
- [ ] Content ingestion (Standard Works + General Conference)
- [ ] Embeddings pipeline (OpenAI)

### Phase 2: AI & UI (Days 5-8)  
- [ ] RAG API with vector search + Grok generation
- [ ] Chat interface with mode selector
- [ ] Clerk authentication
- [ ] Stripe integration (3 tiers)

### Phase 3: Launch (Days 9-12)
- [ ] Vercel deployment + PWA
- [ ] Demo videos + marketing assets
- [ ] Reddit launch (r/latterdaysaints)
- [ ] LDS Facebook groups campaign
- [ ] 500 lifetime license blitz

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

## 🏆 Competitive Advantages

**vs ChatGPT**: LDS-specific knowledge, exact citations, reverent tone
**vs LDS.org**: Natural language queries, cross-referencing, conversational
**vs Scripture apps**: AI insights, specialized modes, personal integration

## 📊 Success Metrics

- **Month 1**: 10k+ free users, 500+ paid subscribers
- **Month 3**: $25k+ MRR, 500 lifetime sales completed  
- **Month 12**: $100k+ MRR, Spanish/Portuguese expansion
- **Year 2**: $500k+ ARR solo founder business

## 🔧 Local Development

```bash
# Clone and install
git clone https://github.com/yourusername/gospelguide
cd gospelguide
npm install

# Environment setup
cp .env.local.example .env.local
# Add your API keys (Supabase, OpenAI, Grok, Clerk, Stripe)

# Database setup
# Run scripts/schema.sql in your Supabase project

# Start development
npm run dev
```

## 📝 Environment Variables

```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# Authentication (Clerk)
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=
CLERK_SECRET_KEY=

# AI APIs
OPENAI_API_KEY=           # For embeddings
XAI_API_KEY=              # For Grok generation

# Payments
STRIPE_SECRET_KEY=
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=

# Analytics
NEXT_PUBLIC_POSTHOG_KEY=
NEXT_PUBLIC_POSTHOG_HOST=
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

**Year 1**: English, core features, $500k ARR
**Year 2**: Spanish, Portuguese markets (+200% growth potential)
**Year 3**: Mobile apps, offline sync, $2M+ ARR
**Year 4**: Audio integration, temple prep modes
**Year 5**: Exit opportunity or $5M+ lifestyle business

---

*"Build the best AI scripture study tool in the Church, charge $99 lifetime to 500 early believers, then let referrals and word-of-mouth in the tightest online communities on earth do the rest."*

**That's it. No fluff, no investors, no employees needed for the first $3M–$5M.**