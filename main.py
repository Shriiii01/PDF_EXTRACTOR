from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
import PyPDF2
import io
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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
        prompt = f"""Please analyze the following PDF text and provide information based on the procedure "{procedure}" and insurance payer "{insurance_payer}".

PDF Text:
{extracted_text}

Please provide a clear, structured response with the following sections:
1. Summary
2. Key Findings
3. Recommendations

Procedure: {procedure}
Insurance Payer: {insurance_payer}
"""
        
        # Call OpenAI API
        client = get_openai_client()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes medical documents and provides clear, structured responses."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
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
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


@app.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")