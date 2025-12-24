from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
import PyPDF2
import io
import os
from dotenv import load_dotenv

# Load environment variables - explicitly load from current directory
from pathlib import Path
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client lazily
def get_openai_client():
    """Get OpenAI client, creating it if needed."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
    return OpenAI(api_key=api_key)


def extract_text_from_pdf(pdf_file: bytes) -> str:
    """Extract text from PDF file bytes."""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error extracting text from PDF: {str(e)}")


@app.post("/api/process-pdf")
async def process_pdf(
    file: UploadFile = File(...),
    procedure: str = Form(...),
    insurance_payer: str = Form(...)
):
    """
    Process PDF file and send to OpenAI API.
    """
    try:
        # Read PDF file
        pdf_bytes = await file.read()
        
        # Extract text from PDF
        extracted_text = extract_text_from_pdf(pdf_bytes)
        
        if not extracted_text:
            raise HTTPException(status_code=400, detail="No text could be extracted from the PDF")
        
        # Prepare prompt for OpenAI
        prompt = f"""Analyze this PDF text for procedure "{procedure}" and payer "{insurance_payer}".

Text: {extracted_text[:3000]}

Provide brief response:
1. Summary
2. Key Findings
3. Recommendations"""
        
        # Call OpenAI API
        client = get_openai_client()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Provide concise, structured analysis."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=500
        )
        
        ai_response = response.choices[0].message.content
        
        return JSONResponse(content={
            "success": True,
            "extracted_text": extracted_text,
            "procedure": procedure,
            "insurance_payer": insurance_payer,
            "ai_response": ai_response
        })
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_detail = str(e)
        # Log full traceback for debugging (remove in production)
        print(f"Error details: {error_detail}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {error_detail}")


@app.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/api/check-config")
async def check_config():
    """Debug endpoint to check if API key is loaded."""
    api_key = os.getenv("OPENAI_API_KEY")
    return JSONResponse(content={
        "api_key_configured": bool(api_key),
        "api_key_length": len(api_key) if api_key else 0,
        "api_key_preview": f"{api_key[:10]}..." if api_key and len(api_key) > 10 else "Not set"
    })