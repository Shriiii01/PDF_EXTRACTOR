# PDF Extractor & Analyzer

A simple MVP web app that extracts text from PDF files and analyzes it using OpenAI's API.

## Features

- Upload PDF files
- Extract text from PDFs
- Send extracted text along with "Procedure" and "Insurance Payer" fields to OpenAI
- Display AI analysis results in clear sections

## Prerequisites

- Python 3.8 or higher
- OpenAI API key

## Installation

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
   - Create a `.env` file in the root directory
   - Add your API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Running the Application

1. Start the FastAPI server:
```bash
uvicorn main:app --reload
```

2. Open your browser and navigate to:
```
http://localhost:8000
```

The root URL will automatically redirect to the frontend interface.

## Usage

1. Upload a PDF file using the file input
2. Enter the "Procedure" name
3. Enter the "Insurance Payer" name
4. Click "Process PDF"
5. View the AI analysis results, extracted text, and input details

## API Endpoint

### POST `/api/process-pdf`

Processes a PDF file and returns AI analysis.

**Form Data:**
- `file`: PDF file (multipart/form-data)
- `procedure`: Procedure name (string)
- `insurance_payer`: Insurance payer name (string)

**Response:**
```json
{
  "success": true,
  "extracted_text": "...",
  "procedure": "...",
  "insurance_payer": "...",
  "ai_response": "..."
}
```

## Project Structure

```
pdf_extractor/
├── main.py              # FastAPI backend
├── static/
│   ├── index.html       # Frontend HTML
│   ├── style.css        # Frontend styles
│   └── script.js        # Frontend JavaScript
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Customizing the Prompt

The OpenAI prompt can be customized in `main.py` around line 64. The current prompt asks for a structured response with Summary, Key Findings, and Recommendations sections. Modify the `prompt` variable in the `process_pdf` function to change the analysis format.

## Notes

- No database or file storage - files are processed in memory
- No user authentication required
- PDFs are not saved after processing
- Make sure your OpenAI API key has sufficient credits
- The app uses `gpt-4o-mini` model by default (can be changed in `main.py`)