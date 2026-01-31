from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field
from openai import OpenAI
import os
import logging
from dotenv import load_dotenv
from typing import List, Optional
import time
from collections import defaultdict

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Chatbot with OpenAI",
    version="1.0.0",
    description="Production-ready AI chatbot powered by OpenAI"
)

# Environment configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2048"))
RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
RATE_LIMIT_PERIOD = int(os.getenv("RATE_LIMIT_PERIOD", "60"))

# Simple in-memory rate limiting
rate_limit_store = defaultdict(list)

def check_rate_limit(client_ip: str) -> bool:
    """Check if client has exceeded rate limit"""
    current_time = time.time()

    # Clean old requests
    rate_limit_store[client_ip] = [
        req_time for req_time in rate_limit_store[client_ip]
        if current_time - req_time < RATE_LIMIT_PERIOD
    ]

    # Check if limit exceeded
    if len(rate_limit_store[client_ip]) >= RATE_LIMIT_REQUESTS:
        return False

    # Add current request
    rate_limit_store[client_ip].append(current_time)
    return True

# Configure CORS
if ENVIRONMENT == "production":
    origins = ALLOWED_HOSTS if ALLOWED_HOSTS != ["*"] else []
else:
    origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add security headers
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logger.error("OPENAI_API_KEY environment variable is not set")
    raise ValueError("OPENAI_API_KEY environment variable is not set")

try:
    client = OpenAI(api_key=api_key)
    logger.info("OpenAI client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize OpenAI client: {str(e)}")
    raise

# Pydantic models for request/response
class Message(BaseModel):
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str = Field(..., min_length=1, max_length=10000)

class ChatRequest(BaseModel):
    messages: List[Message] = Field(..., min_items=1, max_items=50)
    model: Optional[str] = Field(default="gpt-3.5-turbo")
    max_tokens: Optional[int] = Field(default=1024, ge=1, le=MAX_TOKENS)
    temperature: Optional[float] = Field(default=1.0, ge=0, le=2)

class ChatResponse(BaseModel):
    response: str
    model: str
    usage: Optional[dict] = None

# Mount static files (frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    """Serve the main HTML page"""
    try:
        return FileResponse("static/index.html")
    except Exception as e:
        logger.error(f"Error serving index.html: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "AI Chatbot",
        "version": "1.0.0",
        "environment": ENVIRONMENT
    }

@app.get("/api/status")
async def api_status():
    """API status endpoint"""
    try:
        # Test OpenAI connection
        test_response = client.models.list()
        api_available = True
    except Exception as e:
        logger.error(f"OpenAI API unavailable: {str(e)}")
        api_available = False

    return {
        "api_available": api_available,
        "environment": ENVIRONMENT,
        "max_tokens": MAX_TOKENS
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, req: Request):
    """
    Chat endpoint that sends messages to OpenAI API
    """
    client_ip = req.client.host if req.client else "unknown"

    # Rate limiting
    if not check_rate_limit(client_ip):
        logger.warning(f"Rate limit exceeded for {client_ip}")
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Please try again later."
        )

    try:
        # Validate model
        valid_models = [
            "gpt-3.5-turbo",
            "gpt-4",
            "gpt-4-turbo-preview",
            "gpt-4-turbo",
            "gpt-4o",
            "gpt-4o-mini"
        ]

        if request.model not in valid_models:
            logger.warning(f"Invalid model requested: {request.model}")
            request.model = "gpt-3.5-turbo"

        # Convert messages to OpenAI API format
        messages = [
            {"role": msg.role, "content": msg.content}
            for msg in request.messages
        ]

        logger.info(f"Chat request from {client_ip} using model {request.model}")

        # Call OpenAI API
        response = client.chat.completions.create(
            model=request.model,
            messages=messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )

        # Extract the response text
        response_text = response.choices[0].message.content

        # Usage statistics
        usage = {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens
        } if response.usage else None

        logger.info(f"Successful response for {client_ip}, tokens: {usage}")

        return ChatResponse(
            response=response_text,
            model=response.model,
            usage=usage
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your request. Please try again."
        )

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Custom 404 handler"""
    return JSONResponse(
        status_code=404,
        content={"detail": "Resource not found"}
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """Custom 500 handler"""
    logger.error(f"Internal error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")

    logger.info(f"Starting server on {host}:{port} in {ENVIRONMENT} mode")

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=(ENVIRONMENT == "development"),
        log_level="info"
    )
