# PDF Extractor & Analyzer

A simple web application that extracts text from PDF files and provides AI-powered analysis using OpenAI.

![Application Screenshot](screenshots/app-screenshot.png)

## Features

- Upload PDF files and extract text automatically
- AI-powered analysis based on your inputs
- Clean, simple black and white interface
- No database or file storage required

## Prerequisites

Before you begin, make sure you have:

- **Python 3.8 or higher** installed on your system
- An **OpenAI API key** (get one at https://platform.openai.com/api-keys)
- Basic knowledge of using the terminal/command line

## Installation & Setup

### Step 1: Download the Project

Download or clone this repository to your computer:

```bash
git clone https://github.com/Shriiii01/PDF_EXTRACTOR.git
cd PDF_EXTRACTOR
```

![Download Instructions](screenshots/download-instructions.png)

### Step 2: Create a Virtual Environment

Create a virtual environment to keep dependencies isolated:

```bash
python3 -m venv venv
```

![Virtual Environment](screenshots/virtual-env.png)

### Step 3: Activate the Virtual Environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

You should see `(venv)` at the beginning of your command prompt.

![Activate Virtual Environment](screenshots/activate-venv.png)

### Step 4: Install Requirements

Install all required Python packages:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- FastAPI (web framework)
- Uvicorn (web server)
- PyPDF2 (PDF text extraction)
- OpenAI (AI API)
- python-dotenv (environment variables)

![Install Requirements](screenshots/install-requirements.png)

### Step 5: Set Up Your OpenAI API Key

1. Create a file named `.env` in the project root directory
2. Add your OpenAI API key to the file:

```
OPENAI_API_KEY=your_api_key_here
```

**Important:** Replace `your_api_key_here` with your actual OpenAI API key.

![Setup API Key](screenshots/setup-api-key.png)

## Running the Application

### Step 1: Start the Server

Make sure your virtual environment is activated, then run:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

You should see output like:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

![Start Server](screenshots/start-server.png)

### Step 2: Open in Browser

Open your web browser and navigate to:

```
http://localhost:8000
```

![Browser Access](screenshots/browser-access.png)

### Step 3: Use the Application

1. **Upload a PDF file** using the "Choose File" button
2. **Enter Procedure** - Describe what you're analyzing (e.g., "Vacation Singapore", "Medical Procedure")
3. **Enter Insurance Payer** - Enter relevant information (e.g., "Travel Guide", "Insurance Company")
4. **Click "Process PDF"** to analyze your document

The application will:
- Extract text from your PDF
- Send it to OpenAI for analysis
- Display the results in clear sections

![Using the App](screenshots/using-app.png)

## Stopping the Server

To stop the server, press `Ctrl+C` in the terminal where it's running.

## Troubleshooting

### Issue: "ModuleNotFoundError" or "No module named"

**Solution:** Make sure your virtual environment is activated and you've installed requirements:
```bash
source venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt
```

### Issue: "OpenAI API key not configured"

**Solution:** 
1. Make sure you created a `.env` file in the project root
2. Check that your API key is correct (no extra spaces)
3. Restart the server after creating/editing `.env`

### Issue: Port 8000 already in use

**Solution:** Use a different port:
```bash
uvicorn main:app --reload --port 8001
```
Then access at `http://localhost:8001`

### Issue: PDF text extraction fails

**Solution:** 
- Make sure your PDF contains extractable text (not just images)
- Try a different PDF file to test

## Project Structure

```
PDF_EXTRACTOR/
├── main.py              # Backend server (FastAPI)
├── requirements.txt     # Python dependencies
├── .env                 # Your API key (create this)
├── .gitignore          # Git ignore file
├── README.md           # This file
└── static/
    ├── index.html      # Frontend HTML
    ├── style.css       # Styling
    └── script.js       # Frontend JavaScript
```

## Notes

- **No database required** - Everything runs in memory
- **No file storage** - PDFs are processed but not saved
- **API costs** - OpenAI API usage will incur costs based on your usage
- **Local only** - By default, the app runs on localhost (your computer only)

## Support

If you encounter any issues, please check:
1. Python version: `python3 --version` (should be 3.8+)
2. Virtual environment is activated
3. All requirements are installed
4. `.env` file exists with valid API key
5. Server is running on the correct port

## License

This project is provided as-is for client use.
