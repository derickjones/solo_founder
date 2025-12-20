#!/usr/bin/env python3
"""
FastAPI wrapper for Gospel Guide search engine
Deployed on Google Cloud Run for scalable LDS AI search
"""

import os
import json
import logging
import re
import time
import base64
import io
from typing import List, Dict, Any, Optional
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
import uvicorn
import openai
import json

# Import our search engine, cloud storage, and prompts
from .scripture_search import ScriptureSearchEngine
from .cloud_storage import setup_cloud_storage
from .prompts import get_system_prompt, build_context_prompt, get_mode_source_filter, CFM_STUDY_GUIDE_PROMPTS, CFM_LESSON_PLAN_PROMPTS, CFM_AUDIO_SUMMARY_PROMPTS

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="Gospel Guide Search API",
    description="LDS AI Scripture Study Assistant - Semantic search across Standard Works, General Conference, and Come Follow Me",
    version="1.0.0"
)

# CORS configuration for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global search engine instance
search_engine = None

# Initialize OpenAI client
openai_client = None
try:
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key:
        openai_client = openai.OpenAI(api_key=openai_api_key)
        logger.info("OpenAI client initialized successfully")
    else:
        logger.warning("OPENAI_API_KEY not found - AI responses will not be available")
except Exception as e:
    logger.error(f"Failed to initialize OpenAI client: {e}")
    openai_client = None

# Request/Response Models
class SearchRequest(BaseModel):
    query: str
    mode: str = "default"
    top_k: int = 10
    min_score: float = 0.0
    source_filter: Optional[Dict[str, Any]] = None

class SearchResult(BaseModel):
    rank: int
    score: float
    content: str
    metadata: Dict[str, Any]

class SearchResponse(BaseModel):
    query: str
    mode: str
    results: List[SearchResult]
    total_found: int
    search_time_ms: int

class HealthResponse(BaseModel):
    status: str
    version: str
    search_engine_loaded: bool
    total_segments: int

class SourcesResponse(BaseModel):
    sources: Dict[str, Any]

# New AI Q&A Models
class AskRequest(BaseModel):
    query: str
    mode: str = "default"
    top_k: int = 10
    min_score: float = 0.0
    source_filter: Optional[Dict[str, Any]] = None

class AskResponse(BaseModel):
    query: str
    mode: str
    answer: str
    sources: List[SearchResult]
    total_sources: int
    search_time_ms: int
    response_time_ms: int

# Mode to filter mapping - Free tier only
MODE_FILTERS = {
    "default": None  # Uses all sources
}

@app.on_event("startup")
async def startup_event():
    """Initialize search engine on startup"""
    global search_engine, openai_client
    try:
        logger.info("🚀 Initializing Gospel Guide search engine...")
        startup_time = time.time()
        
        # Setup Cloud Storage (download indexes if on Cloud Run)
        if os.getenv('BUCKET_NAME'):
            logger.info("📦 Setting up Cloud Storage...")
            cloud_start = time.time()
            setup_cloud_storage()
            logger.info(f"📦 Cloud Storage setup completed in {time.time() - cloud_start:.2f}s")
        
        # Check for OpenAI API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.warning("⚠️  OPENAI_API_KEY environment variable not set - CFM Deep Dive will be disabled")
            openai_client = None
        else:
            # Initialize OpenAI client
            logger.info("🤖 Initializing OpenAI client...")
            openai_client = openai.OpenAI(api_key=api_key)
            logger.info("✅ OpenAI client initialized")
        
        # Initialize search engine (optional - only if indexes exist)
        logger.info("🔍 Checking for search engine indexes...")
        index_dir = os.getenv("INDEX_DIR", "indexes")
        config_path = os.path.join(index_dir, "config.json")
        
        if os.path.exists(config_path):
            logger.info("📚 Index files found, loading search engine...")
            search_start = time.time()
            search_engine = ScriptureSearchEngine(index_dir=index_dir, openai_api_key=api_key)
            search_time = time.time() - search_start
            logger.info(f"✅ Search engine loaded with {search_engine.index.ntotal:,} segments in {search_time:.2f}s")
        else:
            logger.warning("⚠️  Search index files not found - search functionality will be disabled")
            logger.warning(f"⚠️  Looking for: {config_path}")
            search_engine = None
        
        total_startup_time = time.time() - startup_time
        if search_engine:
            logger.info(f"🚀 Gospel Guide API started successfully in {total_startup_time:.2f}s")
            logger.info(f"📊 Search engine ready with {search_engine.index.ntotal:,} segments")
        else:
            logger.info(f"🚀 Gospel Guide API started in {total_startup_time:.2f}s (search disabled)")
        
        logger.info(f"💡 OpenAI client: {'✅ Ready' if openai_client else '❌ Disabled'}")
        logger.info("🎯 CFM Deep Dive, Lesson Plans, and Audio Summary APIs are available")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize search engine: {e}")
        raise

@app.get("/", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    # Always return healthy status even if search engine not ready yet
    # This allows Cloud Run to consider the container started
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        search_engine_loaded=search_engine is not None,
        total_segments=search_engine.index.ntotal if search_engine and hasattr(search_engine, 'index') else 0
    )

@app.get("/health", response_model=HealthResponse)
async def health():
    """Alternative health check endpoint"""
    return await health_check()

@app.get("/ready")
async def readiness_check():
    """Readiness check - returns 503 if search engine not loaded"""
    if search_engine is None:
        raise HTTPException(status_code=503, detail="Search engine not ready")
    return {"status": "ready", "search_engine_loaded": True}

@app.get("/config")
async def get_config():
    """
    Returns the current configuration status of the API service
    Shows which features are available based on environment setup
    """
    config_status = {
        "search_engine": {
            "available": search_engine is not None,
            "segments_loaded": len(search_engine.metadata) if search_engine else 0
        },
        "openai_client": {
            "available": openai_client is not None,
            "features_enabled": ["lesson_planner"] if openai_client else [],
            "setup_instructions": "Set OPENAI_API_KEY environment variable in Cloud Run service configuration" if not openai_client else "Configured"
        },
        "available_endpoints": {
            "search": True,  # Always available with search engine
            "stream_response": search_engine is not None,
            "cfm_lesson_plan": search_engine is not None and openai_client is not None,
            "cfm_deep_dive": openai_client is not None,  # Only needs OpenAI, loads bundles directly
            "cfm_lesson_plans": openai_client is not None,  # New lesson plans API
            "cfm_audio_summary": openai_client is not None,   # New audio summary API
            "cfm_core_content": openai_client is not None     # New core content API
        }
    }
    
    return config_status

@app.get("/sources", response_model=SourcesResponse)
async def get_sources():
    """Get available content sources for filtering"""
    if not search_engine:
        raise HTTPException(status_code=503, detail="Search engine not initialized")
    
    sources = search_engine.get_available_sources()
    return SourcesResponse(sources=sources)

@app.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    """
    Main search endpoint with mode-based filtering
    
    Supports all 8 specialized modes:
    - default: All sources
    - book-of-mormon-only: Book of Mormon only  
    - general-conference-only: Conference talks only
    - come-follow-me: CFM 2025 content
    - youth: Recent content for teenagers
    - church-approved-only: Official sources
    - scholar: All sources with academic depth
    - personal-journal: User content (future)
    """
    if not search_engine:
        raise HTTPException(status_code=503, detail="Search engine not initialized")
    
    import time
    start_time = time.time()
    
    try:
        # Get mode-based filter
        mode_filter = MODE_FILTERS.get(request.mode)
        
        # Combine mode filter with custom filter
        final_filter = None
        if mode_filter or request.source_filter:
            final_filter = {}
            if mode_filter:
                final_filter.update(mode_filter)
            if request.source_filter:
                final_filter.update(request.source_filter)
        
        # Perform search
        results = search_engine.search(
            query=request.query,
            top_k=request.top_k,
            source_filter=final_filter,
            min_score=request.min_score
        )
        
        search_time_ms = int((time.time() - start_time) * 1000)
        
        # Convert results to response format
        search_results = [
            SearchResult(
                rank=result["rank"],
                score=result["score"],
                content=result["content"],
                metadata=result["metadata"]
            )
            for result in results
        ]
        
        logger.info(f"Search '{request.query}' (mode: {request.mode}) returned {len(results)} results in {search_time_ms}ms")
        
        return SearchResponse(
            query=request.query,
            mode=request.mode,
            results=search_results,
            total_found=len(results),
            search_time_ms=search_time_ms
        )
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/search", response_model=SearchResponse)
async def search_get(
    q: str = Query(..., description="Search query"),
    mode: str = Query("default", description="Search mode"),
    top_k: int = Query(10, description="Number of results"),
    min_score: float = Query(0.0, description="Minimum similarity score")
):
    """GET endpoint for simple searches"""
    request = SearchRequest(
        query=q,
        mode=mode,
        top_k=top_k,
        min_score=min_score
    )
    return await search(request)

@app.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    """
    AI Q&A endpoint that combines search with OpenAI response generation
    
    This endpoint:
    1. Performs semantic search to find relevant sources
    2. Builds context prompt with mode-specific instructions
    3. Generates AI response using OpenAI with proper citations
    """
    if not search_engine:
        raise HTTPException(status_code=503, detail="Search engine not initialized")
        
    if not openai_client:
        raise HTTPException(status_code=503, detail="OpenAI client not available - check OPENAI_API_KEY")

    import time
    start_time = time.time()
    
    try:
        # Step 1: Perform search to get relevant sources
        mode_filter = get_mode_source_filter(request.mode)
        
        # Combine mode filter with custom filter
        final_filter = None
        if mode_filter or request.source_filter:
            final_filter = {}
            if mode_filter:
                final_filter.update(mode_filter)
            if request.source_filter:
                final_filter.update(request.source_filter)
        
        # Search for relevant sources
        search_results = search_engine.search(
            query=request.query,
            top_k=request.top_k,
            source_filter=final_filter,
            min_score=request.min_score
        )
        
        search_time_ms = int((time.time() - start_time) * 1000)
        
        if not search_results:
            return AskResponse(
                query=request.query,
                mode=request.mode,
                answer="I couldn't find any relevant sources to answer your question. Please try rephrasing your question or using different search terms.",
                sources=[],
                total_sources=0,
                search_time_ms=search_time_ms,
                response_time_ms=0
            )
        
        # Step 2: Build context prompt with search results
        context_prompt = build_context_prompt(request.query, search_results, request.mode)
        system_prompt = get_system_prompt(request.mode)
        
        # Step 3: Generate AI response using OpenAI
        ai_start_time = time.time()
        
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",  # Using cost-efficient model for production
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": context_prompt}
            ],
            max_tokens=2000,
            temperature=0.3  # Low temperature for consistent, factual responses
        )
        
        ai_answer = response.choices[0].message.content
        ai_time_ms = int((time.time() - ai_start_time) * 1000)
        
        # Convert search results to response format
        sources = [
            SearchResult(
                rank=result["rank"],
                score=result["score"],
                content=result["content"],
                metadata=result["metadata"]
            )
            for result in search_results
        ]
        
        logger.info(f"AI Q&A '{request.query}' (mode: {request.mode}) used {len(search_results)} sources in {search_time_ms + ai_time_ms}ms")
        
        return AskResponse(
            query=request.query,
            mode=request.mode,
            answer=ai_answer,
            sources=sources,
            total_sources=len(search_results),
            search_time_ms=search_time_ms,
            response_time_ms=ai_time_ms
        )
        
    except openai.OpenAIError as e:
        logger.error(f"OpenAI API error: {e}")
        raise HTTPException(status_code=500, detail=f"AI response generation failed: {str(e)}")
    except Exception as e:
        logger.error(f"Ask endpoint error: {e}")
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")

@app.get("/ask", response_model=AskResponse)
async def ask_question_get(
    q: str = Query(..., description="Question to ask"),
    mode: str = Query("default", description="Response mode"),
    top_k: int = Query(10, description="Number of sources to use"),
    min_score: float = Query(0.0, description="Minimum similarity score")
):
    """GET endpoint for AI Q&A"""
    request = AskRequest(
        query=q,
        mode=mode,
        top_k=top_k,
        min_score=min_score
    )
    return await ask_question(request)

@app.post("/ask/stream")
async def ask_question_stream(request: AskRequest):
    """
    Streaming AI Q&A endpoint that provides real-time response generation
    
    This endpoint:
    1. Performs semantic search to find relevant sources
    2. Streams the AI response as it's being generated
    3. Sends sources metadata at the end
    """
    if not search_engine:
        raise HTTPException(status_code=503, detail="Search engine not initialized")
        
    if not openai_client:
        raise HTTPException(status_code=503, detail="OpenAI client not available - check OPENAI_API_KEY")

    async def generate_response():
        import time
        start_time = time.time()
        
        try:
            # Step 1: Perform search to get relevant sources
            logger.info(f"🔍 Starting search for: '{request.query}'")
            search_start = time.time()
            
            mode_filter = get_mode_source_filter(request.mode)
            
            # Combine mode filter with custom filter
            final_filter = None
            if mode_filter or request.source_filter:
                final_filter = {}
                if mode_filter:
                    final_filter.update(mode_filter)
                if request.source_filter:
                    final_filter.update(request.source_filter)
            
            # Search for relevant sources
            search_results = search_engine.search(
                query=request.query,
                top_k=request.top_k,
                source_filter=final_filter,
                min_score=request.min_score
            )
            
            search_time_ms = int((time.time() - start_time) * 1000)
            search_elapsed = time.time() - search_start
            logger.info(f"✅ Search completed in {search_elapsed:.3f}s, found {len(search_results)} results")
            
            # Send search metadata first
            yield f"data: {json.dumps({'type': 'search_complete', 'search_time_ms': search_time_ms, 'total_sources': len(search_results)})}\n\n"
            
            if not search_results:
                yield f"data: {json.dumps({'type': 'content', 'content': 'I could not find any relevant sources to answer your question. Please try rephrasing your question or using different search terms.'})}\n\n"
                yield f"data: {json.dumps({'type': 'done'})}\n\n"
                return
            
            # Step 2: Build context prompt with search results
            logger.info(f"📝 Building context prompt...")
            context_start = time.time()
            
            context_prompt = build_context_prompt(request.query, search_results, request.mode)
            system_prompt = get_system_prompt(request.mode)
            
            context_elapsed = time.time() - context_start
            logger.info(f"✅ Context built in {context_elapsed:.3f}s, length: {len(context_prompt)} chars")
            
            # Step 3: Stream AI response using OpenAI
            logger.info(f"🤖 Starting OpenAI streaming...")
            ai_start_time = time.time()
            
            stream = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": context_prompt}
                ],
                max_tokens=2000,
                temperature=0.3,
                stream=True  # Enable streaming
            )
            
            # Stream the response chunks
            full_response = ""
            first_chunk = True
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    
                    if first_chunk:
                        openai_first_chunk_time = time.time() - ai_start_time
                        logger.info(f"🎯 First OpenAI chunk received in {openai_first_chunk_time:.3f}s")
                        first_chunk = False
                    
                    yield f"data: {json.dumps({'type': 'content', 'content': content})}\n\n"
            
            ai_time_ms = int((time.time() - ai_start_time) * 1000)
            
            # Send sources at the end
            sources = [
                {
                    'rank': result["rank"],
                    'score': result["score"], 
                    'content': result["content"],
                    'metadata': result["metadata"]
                }
                for result in search_results
            ]
            
            yield f"data: {json.dumps({'type': 'sources', 'sources': sources})}\n\n"
            yield f"data: {json.dumps({'type': 'timing', 'response_time_ms': ai_time_ms, 'total_time_ms': search_time_ms + ai_time_ms})}\n\n"
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
            
            logger.info(f"Streaming AI Q&A '{request.query}' (mode: {request.mode}) completed in {search_time_ms + ai_time_ms}ms")
            
        except openai.OpenAIError as e:
            logger.error(f"OpenAI API error: {e}")
            yield f"data: {json.dumps({'type': 'error', 'error': f'AI response generation failed: {str(e)}'})}\n\n"
        except Exception as e:
            logger.error(f"Streaming ask endpoint error: {e}")
            yield f"data: {json.dumps({'type': 'error', 'error': f'Request failed: {str(e)}'})}\n\n"
    
    return StreamingResponse(
        generate_response(), 
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
        }
    )

@app.get("/ask/stream")
async def ask_question_stream_get(
    q: str = Query(..., description="Question to ask"),
    mode: str = Query("default", description="Response mode"), 
    top_k: int = Query(10, description="Number of sources to use"),
    min_score: float = Query(0.0, description="Minimum similarity score")
):
    """GET endpoint for streaming AI Q&A"""
    request = AskRequest(
        query=q,
        mode=mode,
        top_k=top_k,
        min_score=min_score
    )
    return await ask_question_stream(request)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )

# CFM Deep Dive Models
class CFMDeepDiveRequest(BaseModel):
    week_number: int  # Week number 2-52 for CFM 2026
    study_level: str = "intermediate"  # basic, intermediate, advanced

class CFMDeepDiveResponse(BaseModel):
    week_number: int
    week_title: str
    date_range: str
    study_level: str
    study_guide: str
    bundle_sources: int
    total_characters: int
    generation_time_ms: int

# CFM Lesson Plans Models
class CFMLessonPlanRequest(BaseModel):
    week_number: int  # Week number 2-52 for CFM 2026
    audience: str = "adult"  # adult, youth, children

class CFMLessonPlanResponse(BaseModel):
    week_number: int
    week_title: str
    date_range: str
    audience: str
    lesson_plan: str
    bundle_sources: int
    total_characters: int
    generation_time_ms: int

# CFM Audio Summary Models
class CFMAudioSummaryRequest(BaseModel):
    week_number: int  # Week number 2-52 for CFM 2026
    duration: str = "5min"  # 5min, 15min, 30min
    voice: str = "alloy"  # Voice: alloy, echo, fable, onyx, nova, shimmer

class CFMAudioSummaryResponse(BaseModel):
    week_number: int
    week_title: str
    date_range: str
    duration: str
    audio_script: str
    audio_files: Optional[Dict[str, str]] = None  # Base64 encoded audio file: {"combined": "base64..."}
    bundle_sources: int
    total_characters: int
    generation_time_ms: int

# CFM Core Content Models
class CFMCoreContentRequest(BaseModel):
    week_number: int  # Week number 2-52 for CFM 2026

class CFMCoreContentResponse(BaseModel):
    week_number: int
    week_title: str
    date_range: str
    core_content: str
    bundle_sources: int
    total_characters: int
    generation_time_ms: int

# Helper functions for CFM 2026 Deep Dive
def load_cfm_2026_bundle(week_number: int):
    """Load a specific CFM 2026 Old Testament weekly bundle"""
    try:
        # Try production path first
        bundle_dir = Path("/app/scripts/content/bundles/cfm_2026/old_testament_bundles")
        logger.info(f"Trying production path: {bundle_dir} (exists: {bundle_dir.exists()})")
        
        if not bundle_dir.exists():
            # Fallback for local development
            current_file = Path(__file__)
            bundle_dir = current_file.parent.parent / "scripts" / "content" / "bundles" / "cfm_2026" / "old_testament_bundles"
            logger.info(f"Trying local path: {bundle_dir} (exists: {bundle_dir.exists()})")
        
        if not bundle_dir.exists():
            logger.error(f"Bundle directory not found: {bundle_dir}")
            return None
        
        # List directory contents for debugging
        if bundle_dir.exists():
            files_in_dir = list(bundle_dir.iterdir())
            logger.info(f"Files in bundle directory: {[f.name for f in files_in_dir[:10]]}")  # Show first 10 files
        
        # Find the bundle file for this week - format is week_XX_Date_Scripture.json
        bundle_files = list(bundle_dir.glob(f"week_{week_number:02d}_*.json"))
        
        if not bundle_files:
            logger.error(f"No bundle file found for week {week_number} in {bundle_dir}")
            return None
            
        bundle_path = bundle_files[0]
        logger.info(f"Loading CFM 2026 bundle from: {bundle_path}")
        
        with open(bundle_path, 'r', encoding='utf-8') as f:
            bundle = json.load(f)
            logger.info(f"Loaded week {week_number} bundle: {bundle.get('title', 'Unknown')} with {len(bundle.get('content_sources', []))} sources")
            return bundle
            
    except Exception as e:
        logger.error(f"Failed to load CFM 2026 bundle for week {week_number}: {e}", exc_info=True)
        return None

def format_cfm_bundle_content(bundle: dict) -> str:
    """Format the CFM bundle content for AI processing"""
    if not bundle:
        logger.error("format_cfm_bundle_content: bundle is None or empty")
        return ""
    
    if not isinstance(bundle, dict):
        logger.error(f"format_cfm_bundle_content: bundle is not a dict, it's a {type(bundle)}: {bundle}")
        return ""
    
    content_parts = []
    
    # Add header info
    content_parts.append(f"=== COME FOLLOW ME 2026 - WEEK {bundle.get('week_number', '?')} ===")
    content_parts.append(f"Title: {bundle.get('title', 'Unknown')}")
    content_parts.append(f"Date Range: {bundle.get('date_range', 'Unknown')}")
    
    # Format primary scriptures
    primary_scriptures = []
    for scripture in bundle.get('primary_scriptures', []):
        book = scripture.get('book', '')
        chapters = scripture.get('chapters', [])
        if book and chapters:
            primary_scriptures.append(f"{book} {', '.join(chapters)}")
    content_parts.append(f"Primary Scriptures: {'; '.join(primary_scriptures)}")
    content_parts.append("")
    
    # Add all content sources
    content_sources = bundle.get('content_sources', [])
    for i, source in enumerate(content_sources, 1):
        source_type = source.get('source_type', 'Unknown')
        title = source.get('title', 'Untitled')
        content = source.get('content', '')
        
        content_parts.append(f"--- SOURCE {i}: {source_type.upper()} ---")
        content_parts.append(f"Title: {title}")
        content_parts.append(f"Content:\n{content}")
        content_parts.append("")
    
    # Add any scripture content
    if 'scripture_content' in bundle:
        content_parts.append("--- SCRIPTURE TEXT ---")
        scripture_content = bundle['scripture_content']
        
        for book, book_content in scripture_content.items():
            for chapter, chapter_content in book_content.items():
                verses = chapter_content.get('verses', {})
                
                content_parts.append(f"{book} {chapter}:")
                for verse in verses.values():
                    verse_num = verse.get('verse', '')
                    verse_text = verse.get('text', '')
                    content_parts.append(f"{verse_num}. {verse_text}")
                content_parts.append("")
    
    # Add teaching ideas if available
    if 'teaching_ideas' in bundle:
        content_parts.append("--- TEACHING IDEAS ---")
        for idea in bundle['teaching_ideas']:
            content_parts.append(f"• {idea}")
        content_parts.append("")
    
    # Add discussion questions if available
    if 'discussion_questions' in bundle:
        content_parts.append("--- DISCUSSION QUESTIONS ---")
        for question in bundle['discussion_questions']:
            content_parts.append(f"• {question}")
        content_parts.append("")
    
    # Add themes and cross-references
    if 'themes' in bundle:
        content_parts.append(f"--- KEY THEMES ---")
        content_parts.append(', '.join(bundle['themes']))
        content_parts.append("")
    
    if 'cross_references' in bundle:
        content_parts.append("--- CROSS-REFERENCES ---")
        content_parts.append(', '.join(bundle['cross_references']))
        content_parts.append("")
    
    return '\n'.join(content_parts)

@app.post("/cfm/deep-dive", response_model=CFMDeepDiveResponse)
async def create_cfm_deep_dive_study_guide(request: CFMDeepDiveRequest):
    """
    Generate a CFM 2026 Deep Dive study guide using complete weekly bundles
    
    This endpoint:
    1. Loads the complete CFM 2026 Old Testament weekly bundle (scripture text, seminary materials, etc.)
    2. Uses the entire bundle as context for AI generation
    3. Creates study guides at basic, intermediate, or advanced sophistication levels
    4. Follows the same faith-building approach as the Q&A API
    """
    if not openai_client:
        raise HTTPException(
            status_code=503, 
            detail="OpenAI API client not available. Please set the OPENAI_API_KEY environment variable."
        )
    
    # Validate week number
    if not (2 <= request.week_number <= 52):
        raise HTTPException(status_code=400, detail="Week number must be between 2 and 52 (CFM 2026 Old Testament schedule)")
    
    # Validate study level
    if request.study_level not in CFM_STUDY_GUIDE_PROMPTS:
        raise HTTPException(status_code=400, detail=f"Invalid study level. Must be one of: {list(CFM_STUDY_GUIDE_PROMPTS.keys())}")
    
    try:
        start_time = time.time()
        
        # Step 1: Load the complete CFM 2026 bundle for this week
        logger.info(f"Loading CFM 2026 bundle for week {request.week_number}")
        bundle = load_cfm_2026_bundle(request.week_number)
        logger.info(f"Bundle loaded: {type(bundle)}, keys: {list(bundle.keys()) if isinstance(bundle, dict) else 'Not a dict'}")
        
        if not bundle:
            raise HTTPException(
                status_code=404, 
                detail=f"CFM 2026 bundle not found for week {request.week_number}. Please ensure the bundle files are available."
            )
        
        # Step 2: Format the entire bundle as context
        logger.info("Formatting bundle content...")
        bundle_content = format_cfm_bundle_content(bundle)
        logger.info(f"Bundle content formatted: {len(bundle_content)} characters")
        
        if not bundle_content:
            raise HTTPException(
                status_code=500, 
                detail=f"Failed to format content for week {request.week_number}"
            )
        
        # Step 3: Get the appropriate study level prompt
        logger.info(f"Getting prompt for study level: {request.study_level}")
        system_prompt = CFM_STUDY_GUIDE_PROMPTS[request.study_level]
        
        # Step 4: Create the user prompt with the full bundle context
        user_prompt = f"""
        Please create a {request.study_level} level study guide for this Come Follow Me 2026 Old Testament week.
        
        Use the complete weekly bundle content provided below to create a comprehensive study guide that follows the same faith-building experience as Gospel Guide's Q&A system - helping people build testimony, find answers in scripture, and draw closer to Christ.
        
        COMPLETE WEEKLY BUNDLE CONTENT:
        {bundle_content}
        
        Please create a study guide that uses all the rich content provided above, following your instructions for {request.study_level} level sophistication. Ensure everything is based strictly on the bundle content provided.
        """
        
        # Step 5: Generate the study guide using OpenAI
        logger.info(f"Generating {request.study_level} study guide for week {request.week_number}")
        ai_start = time.time()
        
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=3000,  # Allow longer responses for advanced guides
            temperature=0.7
        )
        
        ai_time_ms = int((time.time() - ai_start) * 1000)
        study_guide = response.choices[0].message.content
        
        # Step 6: Prepare response data
        total_time_ms = int((time.time() - start_time) * 1000)
        bundle_sources = len(bundle.get('content_sources', []))
        total_characters = bundle.get('total_content_length', 0)
        
        logger.info(f"Generated {request.study_level} study guide for week {request.week_number} using {bundle_sources} sources ({total_characters:,} chars) in {total_time_ms}ms")
        
        # Clean title by removing leading semicolon if present
        clean_title = bundle.get('title', 'Unknown').lstrip(';')
        
        return CFMDeepDiveResponse(
            week_number=request.week_number,
            week_title=clean_title,
            date_range=bundle.get('date_range', 'Unknown'),
            study_level=request.study_level,
            study_guide=study_guide,
            bundle_sources=bundle_sources,
            total_characters=total_characters,
            generation_time_ms=total_time_ms
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"CFM Deep Dive generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Study guide generation failed: {str(e)}")

@app.post("/cfm/lesson-plans", response_model=CFMLessonPlanResponse)
async def create_cfm_lesson_plan(request: CFMLessonPlanRequest):
    """
    Generate a CFM 2026 Lesson Plan using complete weekly bundles
    
    This endpoint:
    1. Loads the complete CFM 2026 Old Testament weekly bundle
    2. Uses the entire bundle as context for AI generation
    3. Creates lesson plans for adult, youth, or children audiences
    4. Follows audience-appropriate teaching methods and activities
    """
    if not openai_client:
        raise HTTPException(
            status_code=503, 
            detail="OpenAI API client not available. Please set the OPENAI_API_KEY environment variable."
        )
    
    # Validate week number
    if not (2 <= request.week_number <= 52):
        raise HTTPException(status_code=400, detail="Week number must be between 2 and 52 (CFM 2026 Old Testament schedule)")
    
    # Validate audience
    if request.audience not in CFM_LESSON_PLAN_PROMPTS:
        raise HTTPException(status_code=400, detail=f"Invalid audience. Must be one of: {list(CFM_LESSON_PLAN_PROMPTS.keys())}")
    
    try:
        start_time = time.time()
        
        # Step 1: Load the complete CFM 2026 bundle for this week
        logger.info(f"Loading CFM 2026 bundle for week {request.week_number}")
        bundle = load_cfm_2026_bundle(request.week_number)
        logger.info(f"Bundle loaded: {type(bundle)}, keys: {list(bundle.keys()) if isinstance(bundle, dict) else 'Not a dict'}")
        
        if not bundle:
            raise HTTPException(
                status_code=404, 
                detail=f"CFM 2026 bundle not found for week {request.week_number}. Please ensure the bundle files are available."
            )
        
        # Step 2: Format the entire bundle as context
        logger.info("Formatting bundle content...")
        bundle_content = format_cfm_bundle_content(bundle)
        logger.info(f"Bundle content formatted: {len(bundle_content)} characters")
        
        if not bundle_content:
            raise HTTPException(
                status_code=500, 
                detail=f"Failed to format content for week {request.week_number}"
            )
        
        # Step 3: Get the appropriate audience prompt
        logger.info(f"Getting prompt for audience: {request.audience}")
        system_prompt = CFM_LESSON_PLAN_PROMPTS[request.audience]
        
        # Step 4: Create the user prompt with the full bundle context
        user_prompt = f"""
        Please create a {request.audience} lesson plan for this Come Follow Me 2026 Old Testament week.
        
        Use the complete weekly bundle content provided below to create a comprehensive lesson plan that follows the same faith-building experience as Gospel Guide's study system - helping people build testimony, find answers in scripture, and draw closer to Christ.
        
        COMPLETE WEEKLY BUNDLE CONTENT:
        {bundle_content}
        
        Please create a lesson plan that uses all the rich content provided above, following your instructions for {request.audience} audience. Ensure everything is based strictly on the bundle content provided.
        """
        
        # Step 5: Generate the lesson plan using OpenAI
        logger.info(f"Generating {request.audience} lesson plan for week {request.week_number}")
        ai_start = time.time()
        
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=3000,  # Allow longer responses for detailed lesson plans
            temperature=0.7
        )
        
        ai_time_ms = int((time.time() - ai_start) * 1000)
        lesson_plan = response.choices[0].message.content
        
        # Step 6: Prepare response data
        total_time_ms = int((time.time() - start_time) * 1000)
        bundle_sources = len(bundle.get('content_sources', []))
        total_characters = bundle.get('total_content_length', 0)
        
        logger.info(f"Generated {request.audience} lesson plan for week {request.week_number} using {bundle_sources} sources ({total_characters:,} chars) in {total_time_ms}ms")
        
        # Clean title by removing leading semicolon if present
        clean_title = bundle.get('title', 'Unknown').lstrip(';')
        
        return CFMLessonPlanResponse(
            week_number=request.week_number,
            week_title=clean_title,
            date_range=bundle.get('date_range', 'Unknown'),
            audience=request.audience,
            lesson_plan=lesson_plan,
            bundle_sources=bundle_sources,
            total_characters=total_characters,
            generation_time_ms=total_time_ms
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"CFM Lesson Plan generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Lesson plan generation failed: {str(e)}")

def parse_dialogue_and_generate_audio(script_text: str, voice: str = "alloy") -> Dict[str, str]:
    """
    Generate a single audio file from the summary talk script
    Returns base64 encoded audio file
    Handles long scripts by chunking if they exceed OpenAI TTS character limits
    """
    try:
        logger.info(f"Generating engaging summary talk audio with voice: {voice}")
        logger.info(f"Script length: {len(script_text)} characters")
        
        # Generate audio using OpenAI's text-to-speech API
        audio_files = {}
        
        if openai_client:
            # OpenAI TTS API has a ~4096 character limit
            MAX_CHUNK_SIZE = 3500  # Leave some buffer
            
            if len(script_text) <= MAX_CHUNK_SIZE:
                # Script is short enough - generate in one call
                logger.info("Generating audio in single call...")
                response = openai_client.audio.speech.create(
                    model="tts-1",
                    voice=voice,
                    input=script_text,
                    response_format="mp3"
                )
                audio_files['combined'] = base64.b64encode(response.content).decode()
            else:
                # Script is too long - need to chunk it
                logger.info("Script exceeds TTS limit - chunking for multiple calls...")
                audio_chunks = []
                
                # Split text into chunks at sentence boundaries
                chunks = chunk_text_smartly(script_text, MAX_CHUNK_SIZE)
                logger.info(f"Split into {len(chunks)} chunks")
                
                for i, chunk in enumerate(chunks):
                    logger.info(f"Generating audio for chunk {i+1}/{len(chunks)} ({len(chunk)} chars)")
                    response = openai_client.audio.speech.create(
                        model="tts-1",
                        voice=voice,
                        input=chunk,
                        response_format="mp3"
                    )
                    audio_chunks.append(response.content)
                
                # Combine all audio chunks
                combined_audio = b''.join(audio_chunks)
                audio_files['combined'] = base64.b64encode(combined_audio).decode()
        
        logger.info(f"Generated summary talk audio successfully")
        return audio_files
        
    except Exception as e:
        logger.error(f"Audio generation error: {e}")
        # Return empty dict on error - endpoint will still return script
        return {}


def chunk_text_smartly(text: str, max_chunk_size: int) -> List[str]:
    """
    Split text into chunks at sentence boundaries, respecting max size
    """
    chunks = []
    current_chunk = ""
    
    # Split by sentences (periods, exclamation marks, question marks)
    import re
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    for sentence in sentences:
        # If adding this sentence would exceed the limit
        if len(current_chunk) + len(sentence) + 1 > max_chunk_size:
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                # Single sentence is too long - force split at word boundaries
                words = sentence.split()
                temp_chunk = ""
                for word in words:
                    if len(temp_chunk) + len(word) + 1 > max_chunk_size:
                        if temp_chunk:
                            chunks.append(temp_chunk.strip())
                            temp_chunk = word
                        else:
                            # Single word too long - just add it
                            chunks.append(word)
                            temp_chunk = ""
                    else:
                        temp_chunk += " " + word if temp_chunk else word
                if temp_chunk:
                    current_chunk = temp_chunk
        else:
            current_chunk += " " + sentence if current_chunk else sentence
    
    # Add the final chunk
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

@app.post("/cfm/audio-summary", response_model=CFMAudioSummaryResponse)
async def create_cfm_audio_summary(request: CFMAudioSummaryRequest):
    """
    Generate a CFM 2026 Audio Summary Talk using complete weekly bundles
    
    This endpoint:
    1. Loads the complete CFM 2026 Old Testament weekly bundle
    2. Uses the entire bundle as context for AI generation
    3. Creates engaging single-speaker audio talks for 5min, 15min, or 30min durations
    4. Adds historical context, interesting facts, and gentle humor
    5. Generates audio using the selected voice
    """
    if not openai_client:
        raise HTTPException(
            status_code=503, 
            detail="OpenAI API client not available. Please set the OPENAI_API_KEY environment variable."
        )
    
    # Validate week number
    if not (2 <= request.week_number <= 52):
        raise HTTPException(status_code=400, detail="Week number must be between 2 and 52 (CFM 2026 Old Testament schedule)")
    
    # Validate duration
    if request.duration not in CFM_AUDIO_SUMMARY_PROMPTS:
        raise HTTPException(status_code=400, detail=f"Invalid duration. Must be one of: {list(CFM_AUDIO_SUMMARY_PROMPTS.keys())}")
    
    try:
        start_time = time.time()
        
        # Step 1: Load the complete CFM 2026 bundle for this week
        logger.info(f"Loading CFM 2026 bundle for week {request.week_number}")
        bundle = load_cfm_2026_bundle(request.week_number)
        logger.info(f"Bundle loaded: {type(bundle)}, keys: {list(bundle.keys()) if isinstance(bundle, dict) else 'Not a dict'}")
        
        if not bundle:
            raise HTTPException(
                status_code=404, 
                detail=f"CFM 2026 bundle not found for week {request.week_number}. Please ensure the bundle files are available."
            )
        
        # Step 2: Format the entire bundle as context
        logger.info("Formatting bundle content...")
        bundle_content = format_cfm_bundle_content(bundle)
        logger.info(f"Bundle content formatted: {len(bundle_content)} characters")
        
        if not bundle_content:
            raise HTTPException(
                status_code=500, 
                detail=f"Failed to format content for week {request.week_number}"
            )
        
        # Step 3: Get the appropriate duration prompt
        logger.info(f"Getting prompt for duration: {request.duration}")
        system_prompt = CFM_AUDIO_SUMMARY_PROMPTS[request.duration]
        
        # Step 4: Create the user prompt with the full bundle context
        user_prompt = f"""
        Please create an engaging {request.duration} audio summary talk for this Come Follow Me 2026 Old Testament week.
        
        Create a single-speaker summary talk (not a dialogue) that combines the rich weekly bundle content with fascinating historical context, interesting facts, and gentle humor. Make it feel like listening to a knowledgeable, slightly witty gospel teacher who makes scripture study come alive.
        
        COMPLETE WEEKLY BUNDLE CONTENT:
        {bundle_content}
        
        Please create an engaging summary talk that:
        1. Uses all the rich content provided above as the foundation
        2. Adds appropriate historical context and interesting facts that illuminate the scriptures
        3. Includes gentle humor and engaging storytelling
        4. Follows your {request.duration} duration guidelines
        5. Maintains reverence while being entertaining and educational
        
        Base everything on the bundle content while enriching with historical context that enhances understanding and makes the lesson come alive.
        """
        
        # Step 5: Generate the audio script using OpenAI
        logger.info(f"Generating {request.duration} audio script for week {request.week_number}")
        ai_start = time.time()
        
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=3000,  # Allow longer responses for detailed scripts
            temperature=0.7
        )
        
        ai_time_ms = int((time.time() - ai_start) * 1000)
        audio_script = response.choices[0].message.content
        
        # Step 6: Prepare response data
        total_time_ms = int((time.time() - start_time) * 1000)
        bundle_sources = len(bundle.get('content_sources', []))
        total_characters = bundle.get('total_content_length', 0)
        
        logger.info(f"Generated {request.duration} audio script for week {request.week_number} using {bundle_sources} sources ({total_characters:,} chars) in {total_time_ms}ms")
        
        # Generate audio files from the script
        logger.info("Generating audio files...")
        logger.info(f"Audio script length: {len(audio_script)} characters")
        logger.info(f"Selected voice: {request.voice}")
        audio_files = parse_dialogue_and_generate_audio(audio_script, voice=request.voice)
        logger.info(f"Audio files generated: {list(audio_files.keys()) if audio_files else 'None'}")
        
        # Clean title by removing leading semicolon if present
        clean_title = bundle.get('title', 'Unknown').lstrip(';')
        
        return CFMAudioSummaryResponse(
            week_number=request.week_number,
            week_title=clean_title,
            date_range=bundle.get('date_range', 'Unknown'),
            duration=request.duration,
            audio_script=audio_script,
            audio_files=audio_files if audio_files else None,
            bundle_sources=bundle_sources,
            total_characters=total_characters,
            generation_time_ms=total_time_ms
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"CFM Audio Summary generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Audio summary generation failed: {str(e)}")

@app.post("/cfm/core-content", response_model=CFMCoreContentResponse)
async def generate_cfm_core_content(request: CFMCoreContentRequest):
    """Generate organized core content for a specific CFM week - raw materials organized by section"""
    try:
        # Check if OpenAI client is available
        if not openai_client:
            raise HTTPException(status_code=503, detail="AI service unavailable - OpenAI API key not configured")
        
        start_time = time.time()
        logger.info(f"Generating CFM core content for week {request.week_number}")
        
        # Load the CFM 2026 Old Testament bundle for the specific week
        bundle = load_cfm_2026_bundle(request.week_number)
        if not bundle:
            raise HTTPException(status_code=404, detail=f"Week {request.week_number} bundle not found")
        
        # Build context from all content types in the bundle
        context_parts = []
        bundle_sources = 0
        total_characters = 0
        
        # Add Come Follow Me content first
        if 'come_follow_me' in bundle and bundle['come_follow_me']:
            context_parts.append("=== COME FOLLOW ME CONTENT ===")
            for item in bundle['come_follow_me']:
                content = item.get('content', '').strip()
                if content:
                    context_parts.append(content)
                    bundle_sources += 1
                    total_characters += len(content)
        
        # Add Scripture content second
        if 'scriptures' in bundle and bundle['scriptures']:
            context_parts.append("\n=== SCRIPTURE PASSAGES ===")
            for item in bundle['scriptures']:
                content = item.get('content', '').strip()
                if content:
                    context_parts.append(content)
                    bundle_sources += 1
                    total_characters += len(content)
        
        # Add Seminary content last
        if 'seminary' in bundle and bundle['seminary']:
            context_parts.append("\n=== SEMINARY MATERIALS ===")
            for item in bundle['seminary']:
                content = item.get('content', '').strip()
                if content:
                    context_parts.append(content)
                    bundle_sources += 1
                    total_characters += len(content)
        
        if not context_parts:
            raise HTTPException(status_code=404, detail=f"No content found for week {request.week_number}")
        
        context_text = "\n\n".join(context_parts)
        logger.info(f"Built context with {bundle_sources} sources, {total_characters:,} characters")
        
        # Create the core content organization prompt
        core_content_prompt = f"""You are an expert at organizing LDS study materials. Your task is to take the provided Come Follow Me content and organize it into clean, well-structured sections while preserving all original formatting, verse references, and quotes.

Please organize this content into the following structure:

# Core Study Materials - Week {request.week_number}

## 📖 Come Follow Me Lesson

[Organize the Come Follow Me content here, preserving all original formatting, headings, and structure]

## 📜 Scripture Passages  

[Present the scripture content here, maintaining verse structure and references exactly as provided]

## 🎓 Seminary Materials

[Include seminary materials here, keeping all formatting and structure intact]

IMPORTANT GUIDELINES:
- Preserve ALL original formatting, including headings, bullet points, verse numbers
- Keep all scripture references exactly as they appear
- Maintain all quotes and citations in their original form
- Do not summarize or paraphrase - present the content as organized sections
- Use clean markdown formatting for readability
- Keep verse structure intact (e.g., "1 Nephi 3:7" should stay exactly as formatted)

Content to organize:

{context_text}"""

        # Generate the organized content using OpenAI
        messages = [
            {"role": "user", "content": core_content_prompt}
        ]
        
        logger.info("Calling OpenAI API for core content organization...")
        
        # Use GPT-4 for better formatting and organization
        completion = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=4000,
            temperature=0.3  # Lower temperature for more consistent formatting
        )
        
        core_content = completion.choices[0].message.content.strip()
        
        end_time = time.time()
        total_time_ms = int((end_time - start_time) * 1000)
        
        logger.info(f"Generated core content in {total_time_ms}ms")
        logger.info(f"Core content length: {len(core_content)} characters")
        
        # Clean title by removing leading semicolon if present
        clean_title = bundle.get('title', 'Unknown').lstrip(';')
        
        return CFMCoreContentResponse(
            week_number=request.week_number,
            week_title=clean_title,
            date_range=bundle.get('date_range', 'Unknown'),
            core_content=core_content,
            bundle_sources=bundle_sources,
            total_characters=total_characters,
            generation_time_ms=total_time_ms
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"CFM Core Content generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Core content generation failed: {str(e)}")

# For local development
if __name__ == "__main__":
    logger.info("🏃 Starting Gospel Guide API server...")
    port = int(os.getenv("PORT", 8080))
    logger.info(f"🌐 Server will listen on port {port}")
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
