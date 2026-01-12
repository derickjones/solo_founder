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
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
import uvicorn
import openai
import json

# Import our search engine, cloud storage, prompts, and TTS
from .scripture_search import ScriptureSearchEngine
from .cloud_storage import setup_cloud_storage
from .prompts import get_system_prompt, build_context_prompt, get_mode_source_filter
from .google_tts import create_google_tts_client

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

# Initialize OpenAI API client for Q&A
openai_client = None
try:
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key:
        openai_client = openai.OpenAI(
            api_key=openai_api_key
        )
        logger.info("OpenAI API client initialized successfully for Q&A")
    else:
        logger.warning("OPENAI_API_KEY not found - AI responses will not be available")
except Exception as e:
    logger.error(f"Failed to initialize OpenAI API client: {e}")
    openai_client = None

# Initialize Grok/XAI API client for CFM content generation
grok_client = None
try:
    xai_api_key = os.getenv("XAI_API_KEY")
    if xai_api_key:
        grok_client = openai.OpenAI(
            api_key=xai_api_key,
            base_url="https://api.x.ai/v1"
        )
        logger.info("Grok API client (xAI) initialized successfully for CFM content")
    else:
        logger.warning("XAI_API_KEY not found - CFM content generation will not be available")
except Exception as e:
    logger.error(f"Failed to initialize Grok API client: {e}")
    grok_client = None

# Initialize Google Cloud TTS client (for audio generation with caching)
tts_client = None
audio_cache_manager = None
try:
    tts_client = create_google_tts_client(enable_cache=True)  # Enable caching by default
    if tts_client:
        logger.info("✅ Google Cloud TTS client initialized successfully")
        # Get cache manager reference from TTS client
        if hasattr(tts_client, 'cache_manager') and tts_client.cache_manager:
            audio_cache_manager = tts_client.cache_manager
            logger.info("✅ Audio cache manager available")
    else:
        logger.warning("⚠️ Google Cloud TTS client not available - audio generation will be disabled")
except Exception as e:
    logger.error(f"Failed to initialize Google Cloud TTS client: {e}")
    tts_client = None

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
    global search_engine
    try:
        logger.info("🚀 Initializing Gospel Guide search engine...")
        startup_time = time.time()
        
        # Setup Cloud Storage (download indexes if on Cloud Run)
        if os.getenv('BUCKET_NAME'):
            logger.info("📦 Setting up Cloud Storage...")
            cloud_start = time.time()
            setup_cloud_storage()
            logger.info(f"📦 Cloud Storage setup completed in {time.time() - cloud_start:.2f}s")
        
        # Log API client status
        if not grok_client:
            logger.warning("⚠️  Grok client not available - CFM Deep Dive will be disabled")
        else:
            logger.info("✅ Grok API client ready for CFM content generation")
        
        # Initialize search engine (optional - only if indexes exist)
        logger.info("🔍 Checking for search engine indexes...")
        index_dir = os.getenv("INDEX_DIR", "search/indexes")
        config_path = os.path.join(index_dir, "config.json")
        
        if os.path.exists(config_path):
            logger.info("📚 Index files found, loading search engine...")
            search_start = time.time()
            # Use OPENAI_API_KEY for embeddings in search engine
            openai_api_key = os.getenv("OPENAI_API_KEY")
            search_engine = ScriptureSearchEngine(index_dir=index_dir, openai_api_key=openai_api_key)
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
            "features_enabled": ["q&a"] if openai_client else [],
            "setup_instructions": "Set OPENAI_API_KEY environment variable in Cloud Run service configuration" if not openai_client else "Configured"
        },
        "grok_client": {
            "available": grok_client is not None,
            "features_enabled": ["cfm_deep_dive", "lesson_plans", "audio_summary", "core_content"] if grok_client else [],
            "setup_instructions": "Set XAI_API_KEY environment variable in Cloud Run service configuration" if not grok_client else "Configured"
        },
        "available_endpoints": {
            "search": True,  # Always available with search engine
            "stream_response": search_engine is not None and openai_client is not None,
            "cfm_lesson_plan": search_engine is not None and grok_client is not None,
            "cfm_deep_dive": grok_client is not None,  # Only needs Grok, loads bundles directly
            "cfm_lesson_plans": grok_client is not None,  # New lesson plans API
            "cfm_audio_summary": tts_client is not None,   # Google Cloud TTS audio summary API
            "cfm_core_content": grok_client is not None     # New core content API
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
            model="gpt-4o",  # Using GPT-4o for high-quality gospel Q&A
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
                model="gpt-4o",
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

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )

# Podcast TTS with Intro/Outro Music
class TTSPodcastRequest(BaseModel):
    # Multi-speaker conversation format (Option A - new format)
    script: Optional[List[Dict[str, str]]] = None  # [{"speaker": "host", "text": "..."}]
    voices: Optional[Dict[str, str]] = None  # {"host": "aoede", "guest": "alnilam"}
    
    # Single speaker format (Option B - backward compatible)
    text: Optional[str] = None
    voice: str = "aoede"  # Default voice
    
    title: str = "Podcast Audio"  # Title for the audio player
    pause_between_speakers_ms: int = 500  # Pause between different speakers
    speaker_overlap_ms: int = 0  # Optional overlap for natural conversation (0 = no overlap)
    
    # Caching metadata (optional - for better cache organization)
    content_type: Optional[str] = None  # podcast, study_guide, lesson_plan, core_content, daily_thoughts
    week_number: Optional[int] = None  # Week number for cache key
    study_level: Optional[str] = None  # Study level (essential, connected, scholarly)
    audience: Optional[str] = None  # Audience for lesson plans (adult, youth, children)

class TTSPodcastResponse(BaseModel):
    audio_base64: str  # Base64 encoded MP3 audio
    title: str
    character_count: int
    total_duration_sec: float
    generation_time_ms: int

# Helper functions for CFM 2026 Deep Dive
@app.get("/debug/paths")
async def debug_paths():
    """Debug endpoint to check available paths and files"""
    import os
    from pathlib import Path
    
    debug_info = {
        "current_working_dir": os.getcwd(),
        "app_directory_exists": Path("/app").exists(),
        "search_paths": []
    }
    
    # Check all possible bundle paths
    paths_to_check = [
        "/Users/derickjones/Documents/VS-Code/solo_founder/backend/scripts/cfm_bundle_scraper/2026",
        "/app/scripts/cfm_bundle_scraper/2026",
        "scripts/cfm_bundle_scraper/2026",
        "./scripts/cfm_bundle_scraper/2026",
        "backend/scripts/cfm_bundle_scraper/2026"
    ]
    
    for path_str in paths_to_check:
        path = Path(path_str)
        path_info = {
            "path": str(path),
            "exists": path.exists(),
            "is_dir": path.is_dir() if path.exists() else False
        }
        
        if path.exists() and path.is_dir():
            try:
                files = list(path.glob("cfm_2026_week_*.json"))
                path_info["json_files_count"] = len(files)
                path_info["first_few_files"] = [f.name for f in files[:3]]
            except Exception as e:
                path_info["error"] = str(e)
                
        debug_info["search_paths"].append(path_info)
    
    # Check if we can find any bundle files anywhere
    try:
        current_path = Path(".")
        all_json_files = list(current_path.glob("**/cfm_2026_week_*.json"))
        debug_info["found_bundle_files"] = [str(f) for f in all_json_files[:5]]
    except Exception as e:
        debug_info["glob_error"] = str(e)
    
    return debug_info

def load_cfm_2026_bundle(week_number: int):
    """Load a specific CFM 2026 Old Testament weekly bundle from enhanced scraper"""
    try:
        # Define all possible paths upfront
        possible_paths = [
            Path("/Users/derickjones/Documents/VS-Code/solo_founder/backend/scripts/cfm_bundle_scraper/2026"),
            Path("/app/scripts/cfm_bundle_scraper/2026"),
            Path("scripts/cfm_bundle_scraper/2026"),
            Path("./scripts/cfm_bundle_scraper/2026"),
            Path("backend/scripts/cfm_bundle_scraper/2026")
        ]
        
        bundle_dir = None
        for path in possible_paths:
            if path.exists() and path.is_dir():
                bundle_dir = path
                break
        
        if not bundle_dir:
            logger.error(f"Enhanced CFM bundle directory not found in any location. Checked paths: {[str(p) for p in possible_paths]}")
            return None
        
        logger.info(f"Using enhanced CFM bundle directory: {bundle_dir}")
        
        # Enhanced bundle format: cfm_2026_week_XX.json
        bundle_path = bundle_dir / f"cfm_2026_week_{week_number:02d}.json"
        
        if not bundle_path.exists():
            logger.error(f"Enhanced bundle file not found: {bundle_path}")
            return None
        
        logger.info(f"Loading enhanced CFM 2026 bundle from: {bundle_path}")
        
        with open(bundle_path, 'r', encoding='utf-8') as f:
            bundle = json.load(f)
            
        # Count total content sources
        cfm_content = bundle.get('cfm_lesson_content', {})
        scripture_content = bundle.get('scripture_content', [])
        total_sources = len(scripture_content) + (1 if cfm_content else 0)
        
        logger.info(f"Loaded enhanced week {week_number} bundle: {bundle.get('title', 'Unknown')}")
        logger.info(f"Bundle contains {len(scripture_content)} scripture chapters and CFM lesson content")
        logger.info(f"Total content sources: {total_sources}")
        
        return bundle
            
    except Exception as e:
        logger.error(f"Failed to load enhanced CFM 2026 bundle for week {week_number}: {e}", exc_info=True)
        return None

def format_cfm_bundle_content(bundle: dict) -> str:
    """Format the enhanced CFM bundle content for AI processing"""
    if not bundle:
        logger.error("format_cfm_bundle_content: bundle is None or empty")
        return ""
    
    if not isinstance(bundle, dict):
        logger.error(f"format_cfm_bundle_content: bundle is not a dict, it's a {type(bundle)}: {bundle}")
        return ""
    
    content_parts = []
    
    # Add header info using new format
    content_parts.append(f"=== COME FOLLOW ME 2026 - WEEK {bundle.get('week_number', '?')} ===")
    content_parts.append(f"Title: {bundle.get('title', 'Unknown')}")
    content_parts.append(f"Date Range: {bundle.get('date_range', 'Unknown')}")
    
    # Format CFM lesson content
    cfm_content = bundle.get('cfm_lesson_content', {})
    if cfm_content:
        content_parts.append("\n--- CFM LESSON CONTENT ---")
        content_parts.append(f"Scripture References: {cfm_content.get('scripture_references', 'None')}")
        
        # Add introduction
        if cfm_content.get('introduction'):
            content_parts.append(f"\nIntroduction:\n{cfm_content['introduction']}")
        
        # Add learning sections
        learning_sections = cfm_content.get('learning_at_home_church', [])
        if learning_sections:
            content_parts.append(f"\n--- LEARNING AT HOME AND CHURCH ({len(learning_sections)} sections) ---")
            for i, section in enumerate(learning_sections, 1):
                title = section.get('title', f'Section {i}')
                content = section.get('content', '')
                content_parts.append(f"\n{i}. {title}")
                content_parts.append(content)
        
        # Add teaching children sections  
        teaching_sections = cfm_content.get('teaching_children', [])
        if teaching_sections:
            content_parts.append(f"\n--- TEACHING CHILDREN ({len(teaching_sections)} sections) ---")
            for i, section in enumerate(teaching_sections, 1):
                title = section.get('title', f'Section {i}')
                content = section.get('content', '')
                content_parts.append(f"\n{i}. {title}")
                content_parts.append(content)
    
    # Format scripture content from enhanced bundles
    scripture_content = bundle.get('scripture_content', [])
    if scripture_content:
        content_parts.append(f"\n--- SCRIPTURE TEXT ({len(scripture_content)} chapters) ---")
        
        for scripture in scripture_content:
            reference = scripture.get('reference', 'Unknown')
            verses = scripture.get('verses', [])
            summary = scripture.get('summary', '')
            
            content_parts.append(f"\n{reference}:")
            if summary:
                content_parts.append(f"Summary: {summary}")
            
            # Add verse content (limit to avoid overwhelming context)
            verses_to_include = verses[:50]  # First 50 verses per chapter
            for i, verse in enumerate(verses_to_include, 1):
                if isinstance(verse, str):
                    # Enhanced format: verses are strings with verse number already included
                    content_parts.append(verse)
                else:
                    # Legacy format: verses are dictionaries
                    verse_num = verse.get('verse', '')
                    verse_text = verse.get('text', '')
                    if verse_num and verse_text:
                        content_parts.append(f"{verse_num}. {verse_text}")
            
            if len(verses) > 50:
                content_parts.append(f"... and {len(verses) - 50} more verses")
            content_parts.append("")
    
    result = "\n".join(content_parts)
    
    # Log content statistics
    total_chars = len(result)
    scripture_chapters = len(scripture_content)
    cfm_sections = len(cfm_content.get('learning_at_home_church', [])) + len(cfm_content.get('teaching_children', []))
    
    logger.info(f"Formatted bundle content: {total_chars:,} characters, {scripture_chapters} scripture chapters, {cfm_sections} CFM sections")
    
    return result

def generate_audio_with_tts(script_text: str, voice: str = "cfm_male") -> Dict[str, str]:
    """
    Generate audio file from script using Google Cloud TTS
    Returns base64 encoded audio file
    """
    try:
        logger.info(f"🔊 Generating audio with Google Cloud TTS voice: {voice}")
        logger.info(f"📝 Script length: {len(script_text)} characters")
        
        audio_files = {}
        
        if tts_client:
            # Generate audio using Google Cloud TTS
            audio_b64 = tts_client.generate_audio_base64(
                text=script_text,
                voice=voice
            )
            
            if audio_b64:
                audio_files['combined'] = audio_b64
                logger.info("✅ Successfully generated audio with Google Cloud TTS")
            else:
                logger.error("❌ Google Cloud TTS audio generation returned empty result")
        else:
            logger.warning("⚠️ Google Cloud TTS client not available")
        
        return audio_files
        
    except Exception as e:
        logger.error(f"❌ Google Cloud TTS audio generation error: {e}")
        # Return empty dict on error - endpoint will still return script
        return {}


@app.post("/tts/podcast", response_model=TTSPodcastResponse)
async def generate_podcast_tts(request: TTSPodcastRequest):
    """
    Generate podcast audio with clean voice and music intro/outro.
    
    Audio structure:
    - Intro: 0-7s music at full volume
    - Music fade-out: 5s-14s (9 second fade to silence)
    - Voice starts: 11s (4 seconds into the fade-out)
    - Voice: Full volume, no background music during main content
    - Outro fade-in: Music fades in 10 seconds before voice ends
    - Outro: 30 seconds of music after voice ends (with 8s fade-out at end)
    - Final: Normalized with -1dB headroom
    
    Supports caching: Final audio is cached to avoid regeneration
    """
    import time
    import hashlib
    from pydub import AudioSegment
    from pydub.effects import normalize
    start_time = time.time()
    
    # Determine if this is conversation or single-speaker format
    is_conversation = bool(request.script and request.voices)
    
    if is_conversation:
        logger.info(f"🎙️ Podcast TTS request: conversation format with {len(request.script)} segments")
    else:
        logger.info(f"🎙️ Podcast TTS request: {len(request.text) if request.text else 0} characters, voice={request.voice}")
    
    if not tts_client:
        raise HTTPException(status_code=503, detail="TTS service not available")
    
    # Validate request
    if not is_conversation:
        if not request.text or len(request.text.strip()) < 10:
            raise HTTPException(status_code=400, detail="Text must be at least 10 characters")
        
        # Limit text length to prevent abuse (100k chars max)
        if len(request.text) > 100000:
            raise HTTPException(status_code=400, detail="Text too long. Maximum 100,000 characters.")
    else:
        if not request.script or len(request.script) == 0:
            raise HTTPException(status_code=400, detail="Script array cannot be empty")
    
    # ========== CHECK CACHE FIRST ==========
    cache_key = None
    if audio_cache_manager:
        try:
            # Generate cache key based on content
            if is_conversation:
                # Use script content for cache key
                script_text = " ".join([f"{seg.get('speaker', '')}: {seg.get('text', '')}" for seg in request.script])
                content_hash = hashlib.sha256(script_text.encode()).hexdigest()[:16]
            else:
                content_hash = hashlib.sha256(request.text.encode()).hexdigest()[:16]
            
            # Determine content type and build appropriate cache key
            content_type = request.content_type or "podcast"
            voice_suffix = f"_{request.voice}" if request.voice else ""
            
            if content_type == "study_guide" and request.week_number and request.study_level:
                cache_key = f"audio-cache/study_guide/study_guide_week_{request.week_number:02d}_{request.study_level}{voice_suffix}.mp3"
            elif content_type == "lesson_plan" and request.week_number and request.audience:
                cache_key = f"audio-cache/lesson_plan/lesson_plan_week_{request.week_number:02d}_{request.audience}{voice_suffix}.mp3"
            elif content_type == "core_content" and request.week_number:
                cache_key = f"audio-cache/core_content/core_content_week_{request.week_number:02d}{voice_suffix}.mp3"
            elif content_type == "daily_thoughts" and request.week_number:
                cache_key = f"audio-cache/daily_thoughts/daily_thoughts_week_{request.week_number:02d}{voice_suffix}.mp3"
            elif content_type == "podcast":
                cache_key = f"audio-cache/podcast/podcast_{content_hash}{voice_suffix}.mp3"
            else:
                # Generic fallback using content hash
                cache_key = f"audio-cache/{content_type}/{content_type}_{content_hash}{voice_suffix}.mp3"
            
            # Check if we have cached audio
            cached_audio = audio_cache_manager.get_cached_audio(cache_key)
            if cached_audio:
                logger.info(f"🎯 Returning cached audio: {cache_key}")
                audio_b64 = base64.b64encode(cached_audio).decode('utf-8')
                
                # Estimate character count and duration
                character_count = len(request.text) if request.text else sum(len(seg.get('text', '')) for seg in (request.script or []))
                cached_duration = len(cached_audio) / 24000  # Rough estimate for MP3 @192kbps
                
                total_time_ms = int((time.time() - start_time) * 1000)
                
                return TTSPodcastResponse(
                    audio_base64=audio_b64,
                    title=request.title,
                    character_count=character_count,
                    total_duration_sec=cached_duration,
                    generation_time_ms=total_time_ms
                )
        except Exception as e:
            logger.warning(f"Cache check failed: {e}, proceeding with generation")
    
    try:
        # Find the intro/outro music file
        music_paths = [
            Path(__file__).parent.parent / "assets" / "intro_mp3s" / "inspiring-inspirational-background-music-412596.mp3",
            Path("/app/assets/intro_mp3s/inspiring-inspirational-background-music-412596.mp3"),
        ]
        
        music_file = None
        for path in music_paths:
            if path.exists():
                music_file = path
                break
        
        if not music_file:
            logger.warning("⚠️ Intro music file not found, falling back to standard TTS")
            # Fall back to standard TTS without music
            fallback_text = request.text if request.text else ""
            audio_b64 = tts_client.generate_audio_base64(
                text=fallback_text,
                voice=request.voice
            )
            total_time_ms = int((time.time() - start_time) * 1000)
            return TTSPodcastResponse(
                audio_base64=audio_b64,
                title=request.title,
                character_count=len(fallback_text),
                total_duration_sec=0.0,
                generation_time_ms=total_time_ms
            )
        
        # ========== DETERMINE FORMAT: CONVERSATION OR SINGLE SPEAKER ==========
        if request.script and request.voices:
            # Multi-speaker conversation format
            logger.info(f"🎭 Generating conversation with {len(request.script)} segments")
            
            voice_segments = []
            total_chars = 0
            
            for idx, line in enumerate(request.script):
                speaker = line.get('speaker', 'host')
                text = line.get('text', '')
                voice_name = request.voices.get(speaker, 'aoede')
                
                if not text.strip():
                    continue
                
                total_chars += len(text)
                
                # Generate this speaker's audio segment
                logger.info(f"  Generating segment {idx + 1}/{len(request.script)}: {speaker} ({voice_name})")
                segment_b64 = tts_client.generate_audio_base64(text, voice_name)
                
                if not segment_b64:
                    logger.warning(f"  Failed to generate segment {idx + 1}, skipping")
                    continue
                
                segment_bytes = base64.b64decode(segment_b64)
                audio_seg = AudioSegment.from_mp3(io.BytesIO(segment_bytes))
                
                voice_segments.append(audio_seg)
                
                # Add pause between speakers (except after last segment)
                if idx < len(request.script) - 1:
                    pause_duration = request.pause_between_speakers_ms
                    voice_segments.append(AudioSegment.silent(duration=pause_duration))
            
            # Concatenate all voice segments into one track
            if voice_segments:
                voice = sum(voice_segments)
            else:
                raise HTTPException(status_code=500, detail="No voice segments generated")
            
            character_count = total_chars
            
        else:
            # Single speaker format (backward compatible)
            if not request.text:
                raise HTTPException(status_code=400, detail="Either 'text' or 'script' must be provided")
            
            logger.info(f"🎙️ Generating single-speaker audio")
            voice_audio_b64 = tts_client.generate_audio_base64(
                text=request.text,
                voice=request.voice
            )
            
            if not voice_audio_b64:
                raise HTTPException(status_code=500, detail="Voice audio generation failed")
            
            voice_audio_bytes = base64.b64decode(voice_audio_b64)
            voice = AudioSegment.from_mp3(io.BytesIO(voice_audio_bytes))
            character_count = len(request.text)
        
        # Load music for intro/outro
        music = AudioSegment.from_mp3(str(music_file))
        
        # ========== TIMING CONFIGURATION ==========
        intro_duration_ms = 5000           # 5s intro at full volume
        music_fadeout_ms = 9000            # 9s fade out (5s-14s)
        voice_start_ms = 11000             # Voice starts at 11s
        outro_fadein_ms = 10000            # 10s fade in before voice ends
        outro_duration_ms = 30000          # 30s outro after voice
        outro_final_fadeout_ms = 8000      # 8s fade out at very end
        
        voice_duration_ms = len(voice)
        
        # Total duration needed for music
        total_duration_needed = intro_duration_ms + music_fadeout_ms + outro_fadein_ms + outro_duration_ms
        
        # Ensure music is long enough (loop if needed with crossfade for seamless loop)
        while len(music) < total_duration_needed + 5000:
            music = music.append(music, crossfade=2000)
        
        # ========== BUILD INTRO + FADE OUT ==========
        # Intro: 0-13s at full volume
        intro_music = music[:intro_duration_ms]
        
        # Fade out: 5s-14s (9 second fade)
        fadeout_section = music[intro_duration_ms:intro_duration_ms + music_fadeout_ms]
        fadeout_section = fadeout_section.fade_out(duration=music_fadeout_ms)
        
        intro_with_fadeout = intro_music + fadeout_section
        
        # ========== VOICE TRACK (NO FADE-IN, FULL VOLUME) ==========
        # Voice starts at 18 seconds at FULL volume (no fade-in)
        voice_with_padding = AudioSegment.silent(duration=voice_start_ms) + voice
        
        # ========== BUILD OUTRO (FADE IN UNDER LAST 10s OF VOICE) ==========
        # Calculate when outro should start fading in (10s before voice ends)
        outro_start_position = voice_start_ms + voice_duration_ms - outro_fadein_ms
        
        # Get music section for outro (fade-in + full outro)
        outro_music_start = intro_duration_ms + music_fadeout_ms
        outro_total_length = outro_fadein_ms + outro_duration_ms
        outro_music = music[outro_music_start:outro_music_start + outro_total_length]
        
        # First 10s: fade in from silence
        outro_fadein = outro_music[:outro_fadein_ms].fade_in(duration=outro_fadein_ms)
        
        # Next 30s: full volume with fade out at end
        outro_full = outro_music[outro_fadein_ms:outro_fadein_ms + outro_duration_ms]
        outro_full = outro_full.fade_out(duration=outro_final_fadeout_ms)
        
        complete_outro = outro_fadein + outro_full
        
        # ========== FINAL MIX ==========
        # Calculate silence duration between intro fadeout and outro fadein
        silence_duration = max(0, voice_duration_ms - music_fadeout_ms - outro_fadein_ms)
        
        # Build base music track: intro + fadeout + silence + outro
        base_track = intro_with_fadeout + AudioSegment.silent(duration=silence_duration)
        
        # Pad base track to match where outro should start
        if len(base_track) < outro_start_position:
            base_track = base_track + AudioSegment.silent(duration=outro_start_position - len(base_track))
        
        # Add outro music (this will overlay on last 10s of voice + 30s after)
        base_track = base_track[:outro_start_position] + complete_outro
        
        # Ensure voice track is padded to match base track length
        if len(voice_with_padding) < len(base_track):
            voice_with_padding = voice_with_padding + AudioSegment.silent(duration=len(base_track) - len(voice_with_padding))
        
        # Overlay voice on top of music track
        final_audio = base_track.overlay(voice_with_padding)
        
        # Normalize to consistent levels
        final_audio = normalize(final_audio)
        final_audio = final_audio - 1  # -1dB headroom
        
        # Export to MP3 bytes with good quality
        output_buffer = io.BytesIO()
        final_audio.export(output_buffer, format="mp3", bitrate="192k")
        output_buffer.seek(0)
        final_audio_bytes = output_buffer.read()
        final_audio_b64 = base64.b64encode(final_audio_bytes).decode('utf-8')
        
        # ========== UPLOAD TO CACHE ==========
        if cache_key and audio_cache_manager:
            try:
                upload_success = audio_cache_manager.upload_to_cache(cache_key, final_audio_bytes)
                if upload_success:
                    logger.info(f"💾 Cached audio for future requests: {cache_key}")
                else:
                    logger.warning(f"⚠️ Failed to cache audio: {cache_key}")
            except Exception as e:
                logger.warning(f"Cache upload failed: {e}, but returning generated audio")
        
        total_duration_sec = len(final_audio) / 1000.0
        total_time_ms = int((time.time() - start_time) * 1000)
        
        logger.info(f"✅ Podcast TTS generated in {total_time_ms}ms, duration: {total_duration_sec:.1f}s")
        
        return TTSPodcastResponse(
            audio_base64=final_audio_b64,
            title=request.title,
            character_count=character_count,
            total_duration_sec=total_duration_sec,
            generation_time_ms=total_time_ms
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Podcast TTS generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Podcast TTS generation failed: {str(e)}")


# =============================================================================
# CACHE MANAGEMENT ENDPOINTS
# =============================================================================

@app.get("/cache/stats")
async def get_cache_stats():
    """
    Get audio cache statistics
    
    Returns information about cached audio files including:
    - Total files and storage size
    - Breakdown by content type
    - Age of oldest/newest files
    - Files over 30 days old (ready for cleanup)
    """
    if not audio_cache_manager:
        raise HTTPException(
            status_code=503,
            detail="Audio cache not available"
        )
    
    try:
        stats = audio_cache_manager.get_cache_stats()
        logger.info(f"📊 Cache stats requested: {stats.get('total_files', 0)} files")
        return stats
    except Exception as e:
        logger.error(f"Error getting cache stats: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get cache stats: {str(e)}"
        )


@app.delete("/cache/cleanup")
async def cleanup_cache(older_than_days: int = 30):
    """
    Delete cache files older than specified age
    
    Args:
        older_than_days: Maximum age in days (default: 30)
        
    Returns:
        Cleanup results including files deleted and storage freed
        
    Use this endpoint to manually trigger cache cleanup (recommended monthly)
    """
    if not audio_cache_manager:
        raise HTTPException(
            status_code=503,
            detail="Audio cache not available"
        )
    
    if older_than_days < 1 or older_than_days > 365:
        raise HTTPException(
            status_code=400,
            detail="older_than_days must be between 1 and 365"
        )
    
    try:
        logger.info(f"🧹 Starting cache cleanup: deleting files older than {older_than_days} days")
        result = audio_cache_manager.cleanup_old_files(max_age_days=older_than_days)
        
        logger.info(
            f"✅ Cache cleanup complete: {result['deleted_files']} files deleted, "
            f"{result['freed_mb']}MB freed"
        )
        
        return {
            "message": f"Cache cleanup complete",
            "deleted_files": result['deleted_files'],
            "freed_mb": result['freed_mb'],
            "kept_files": result['kept_files'],
            "oldest_remaining_age_days": result['oldest_remaining_age_days'],
            "cleanup_threshold_days": older_than_days
        }
        
    except Exception as e:
        logger.error(f"Error during cache cleanup: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Cache cleanup failed: {str(e)}"
        )


@app.delete("/cache/clear")
async def clear_all_cache():
    """
    Delete ALL cached audio files (nuclear option)
    
    Returns:
        Clear results including total files deleted and storage freed
        
    WARNING: This will delete all cached audio. Use with caution!
    All audio will need to be regenerated on next request.
    """
    if not audio_cache_manager:
        raise HTTPException(
            status_code=503,
            detail="Audio cache not available"
        )
    
    try:
        logger.warning("💣 Clearing ALL audio cache - this cannot be undone!")
        result = audio_cache_manager.clear_all_cache()
        
        logger.info(
            f"✅ Cache cleared: {result['deleted_files']} files deleted, "
            f"{result['freed_mb']}MB freed"
        )
        
        return {
            "message": "All audio cache cleared",
            "deleted_files": result['deleted_files'],
            "freed_mb": result['freed_mb']
        }
        
    except Exception as e:
        logger.error(f"Error clearing cache: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear cache: {str(e)}"
        )


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
