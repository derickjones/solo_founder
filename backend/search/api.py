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
from scripture_search import ScriptureSearchEngine
from cloud_storage import setup_cloud_storage
from prompts import get_system_prompt, build_context_prompt, get_mode_source_filter, CFM_LESSON_PROMPTS

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
            logger.error("❌ OPENAI_API_KEY environment variable required")
            raise ValueError("OPENAI_API_KEY environment variable required")
        
        # Initialize OpenAI client
        logger.info("🤖 Initializing OpenAI client...")
        openai_client = openai.OpenAI(api_key=api_key)
        logger.info("✅ OpenAI client initialized")
        
        # Initialize search engine
        logger.info("🔍 Loading search engine indexes...")
        index_dir = os.getenv("INDEX_DIR", "indexes")
        search_start = time.time()
        search_engine = ScriptureSearchEngine(index_dir=index_dir, openai_api_key=api_key)
        search_time = time.time() - search_start
        
        total_startup_time = time.time() - startup_time
        logger.info(f"✅ Search engine loaded with {search_engine.index.ntotal:,} segments in {search_time:.2f}s")
        logger.info(f"🎉 Gospel Guide API ready to serve! Total startup time: {total_startup_time:.2f}s")
        
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

# New Lesson Planner Models
class LessonPlanRequest(BaseModel):
    week: str  # e.g., "November 24–30" or week identifier
    audience: str = "adults"  # adults, family, youth, children
    custom_query: Optional[str] = None  # Additional context or specific focus

class LessonPlanResponse(BaseModel):
    week: str
    audience: str
    lesson_title: str
    lesson_plan: str
    sources_used: int
    generation_time_ms: int

# Helper functions for lesson planning
def load_cfm_content():
    """Load Come Follow Me content from JSON file"""
    try:
        cfm_path = Path(__file__).parent.parent / "scripts" / "content" / "come_follow_me.json"
        with open(cfm_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load CFM content: {e}")
        return []

def get_cfm_week_content(week_identifier: str):
    """Get all CFM content for a specific week"""
    cfm_content = load_cfm_content()
    week_content = []
    
    # Find content matching the week identifier
    for item in cfm_content:
        if week_identifier.lower() in item.get('week_info', '').lower() or \
           week_identifier.lower() in item.get('lesson_title', '').lower():
            week_content.append(item)
    
    return week_content

def extract_scripture_references(content_list: List[Dict]):
    """Extract scripture references from CFM content to get full chapters"""
    references = set()
    
    for item in content_list:
        content = item.get('content', '') + ' ' + item.get('lesson_title', '')
        
        # Extract D&C references like "Doctrine and Covenants 135-136" or "D&C 135:3"
        dc_matches = re.findall(r'(?:Doctrine and Covenants?|D&C)\s+(\d+)(?:[-–](\d+))?(?::(\d+))?', content, re.IGNORECASE)
        for match in dc_matches:
            start_section = int(match[0])
            end_section = int(match[1]) if match[1] else start_section
            for section in range(start_section, end_section + 1):
                references.add(f"Doctrine and Covenants {section}")
        
        # Extract other scripture references (Book of Mormon, Bible, etc.)
        scripture_matches = re.findall(r'(\w+(?:\s+\w+)*)\s+(\d+)(?::(\d+))?', content)
        for match in scripture_matches:
            book = match[0]
            chapter = match[1]
            # Only include if it looks like a scripture book
            if book in ['1 Nephi', '2 Nephi', 'Jacob', 'Enos', 'Jarom', 'Omni', 'Mosiah', 
                       'Alma', 'Helaman', 'Mormon', 'Ether', 'Moroni', 'Matthew', 'Mark',
                       'Luke', 'John', 'Acts', 'Romans', 'Genesis', 'Exodus', 'Psalms']:
                references.add(f"{book} {chapter}")
    
    return list(references)

@app.post("/cfm/lesson-plan", response_model=LessonPlanResponse)
async def create_lesson_plan(request: LessonPlanRequest):
    """
    Generate a comprehensive Come Follow Me lesson plan for the specified week and audience
    
    This endpoint:
    1. Retrieves all CFM content for the specified week
    2. Extracts referenced scripture chapters and retrieves their full content
    3. Searches for additional relevant materials across all sources
    4. Uses audience-specific prompts to generate structured lesson plans
    """
    if not search_engine or not openai_client:
        raise HTTPException(status_code=503, detail="Search engine or AI client not initialized")
    
    # Validate audience
    if request.audience not in CFM_LESSON_PROMPTS:
        raise HTTPException(status_code=400, detail=f"Invalid audience. Must be one of: {list(CFM_LESSON_PROMPTS.keys())}")
    
    try:
        start_time = time.time()
        
        # Step 1: Get CFM content for the week
        logger.info(f"Retrieving CFM content for week: {request.week}")
        cfm_content = get_cfm_week_content(request.week)
        
        if not cfm_content:
            raise HTTPException(status_code=404, detail=f"No CFM content found for week: {request.week}")
        
        lesson_title = cfm_content[0].get('lesson_title', 'Come Follow Me Study')
        
        # Step 2: Extract scripture references and search for full chapters
        scripture_refs = extract_scripture_references(cfm_content)
        logger.info(f"Found scripture references: {scripture_refs}")
        
        # Step 3: Build comprehensive context from multiple sources
        all_context = []
        
        # Add CFM content
        cfm_text = "\n\n--- Come Follow Me Content ---\n"
        for item in cfm_content:
            cfm_text += f"Citation: {item.get('citation', '')}\n"
            cfm_text += f"Content: {item.get('content', '')}\n\n"
        all_context.append(cfm_text)
        
        # Search for scripture chapters and related content
        search_queries = scripture_refs + [lesson_title]
        if request.custom_query:
            search_queries.append(request.custom_query)
        
        for query in search_queries[:5]:  # Limit to avoid overwhelming context
            try:
                results = search_engine.search(
                    query=query,
                    top_k=5,
                    mode_filter=MODE_FILTERS["default"],
                    min_score=0.3
                )
                
                if results:
                    context_text = f"\n\n--- Search Results for: {query} ---\n"
                    for result in results:
                        context_text += f"Source: {result['metadata'].get('citation', 'Unknown')}\n"
                        context_text += f"Content: {result['content']}\n\n"
                    all_context.append(context_text)
            except Exception as e:
                logger.warning(f"Search failed for query '{query}': {e}")
                continue
        
        # Combine all context
        combined_context = "\n".join(all_context)
        
        # Step 4: Generate lesson plan using audience-specific prompt
        system_prompt = CFM_LESSON_PROMPTS[request.audience]
        
        user_prompt = f"""
        Please create a detailed lesson plan for the Come Follow Me study week: "{request.week}"
        Lesson Title: {lesson_title}
        Target Audience: {request.audience.title()}
        
        {f"Additional Focus: {request.custom_query}" if request.custom_query else ""}
        
        Use the following retrieved content to create an accurate, engaging lesson plan:
        
        {combined_context}
        
        Please follow the structured format specified in your instructions and base all content on the retrieved sources provided above.
        """
        
        # Generate AI response
        ai_start = time.time()
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        ai_time_ms = int((time.time() - ai_start) * 1000)
        lesson_plan = response.choices[0].message.content
        
        total_time_ms = int((time.time() - start_time) * 1000)
        sources_count = len(cfm_content) + sum(1 for query in search_queries if query)
        
        logger.info(f"Generated {request.audience} lesson plan for '{request.week}' using {sources_count} sources in {total_time_ms}ms")
        
        return LessonPlanResponse(
            week=request.week,
            audience=request.audience,
            lesson_title=lesson_title,
            lesson_plan=lesson_plan,
            sources_used=sources_count,
            generation_time_ms=total_time_ms
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Lesson plan generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Lesson plan generation failed: {str(e)}")

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