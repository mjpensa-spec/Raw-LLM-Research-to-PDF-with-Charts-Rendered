# Web UI Usage Guide

## Starting the Web Server

1. **Install Dependencies** (if not already done):
```powershell
cd C:\md-research-processor
pip install -r requirements.txt
playwright install chromium
```

2. **Start the Flask Server**:
```powershell
python app.py
```

You should see:
```
============================================================
Markdown to PDF Converter - Web UI
============================================================
Server starting at: http://localhost:5000
Upload folder: C:\Users\...\Temp\md_uploads_...
Output folder: C:\Users\...\Temp\pdf_outputs_...
============================================================

Press Ctrl+C to stop the server
```

3. **Open Your Browser**:
   - Navigate to: http://localhost:5000
   - Or: http://127.0.0.1:5000

## Using the Web Interface

### Upload a File

1. **Choose a file** by:
   - Clicking the upload area
   - Dragging and dropping a file onto the upload area

2. **Supported file types**:
   - `.md` (Markdown)
   - `.markdown`
   - `.txt` (with markdown content)

3. **Maximum file size**: 16MB

### Convert to PDF

1. After selecting a file, click the **"Convert to PDF"** button
2. The system will:
   - Fix any markdown syntax issues
   - Detect and render Mermaid diagrams
   - Generate a professional PDF
   - Automatically download the PDF to your browser

### Processing Steps

You'll see status updates during processing:
- "Processing your file..."
- "Fixing markdown syntax..."
- "Rendering Mermaid diagrams..."
- "Generating PDF..."

### After Conversion

- The PDF will automatically download
- Click **"Convert Another File"** to process more files
- If there's an error, click **"Try Again"** to restart

## Features

✅ **Drag & Drop Support** - Simply drag markdown files onto the page

✅ **Automatic Syntax Fixing** - Detects and corrects markdown issues

✅ **Mermaid Rendering** - Converts all diagram types to images

✅ **Real-time Progress** - See what's happening as your file processes

✅ **Error Handling** - Clear error messages if something goes wrong

✅ **No Manual Downloads** - PDFs download automatically

## API Endpoints

If you want to integrate with the API directly:

### Health Check
```
GET /api/health
```
Returns: `{"status": "ok", "message": "..."}`

### Upload & Convert
```
POST /api/upload
Content-Type: multipart/form-data
Body: file=<your-markdown-file>
```
Returns: PDF file (application/pdf)

## Troubleshooting

### Server won't start
- Make sure Flask is installed: `pip install flask`
- Check if port 5000 is available
- Try a different port by editing `app.py` (change the port in `app.run()`)

### "Module not found" errors
```powershell
pip install -r requirements.txt
```

### Mermaid diagrams not rendering
```powershell
playwright install chromium
```

### Can't access from other devices
Change `app.run()` in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```
Then access via: `http://YOUR-IP-ADDRESS:5000`

## Stopping the Server

Press **Ctrl+C** in the terminal where the server is running

## File Cleanup

- Uploaded files are automatically deleted after processing
- Generated PDFs are cleaned up after 1 hour
- Temporary folders are managed automatically

## Security Notes

⚠️ **For development use only** - Do not expose to the internet without proper security measures

- The server runs in debug mode by default
- File uploads are limited to 16MB
- Only markdown file types are accepted
- Automatic file cleanup prevents disk space issues
