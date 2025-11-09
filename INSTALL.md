# Installation and Setup Guide

## Quick Start

Follow these steps to set up the Markdown Research Processor:

### 1. Install GTK3 (Windows only)

WeasyPrint requires GTK3 for PDF generation on Windows.

1. Download the GTK3 Runtime installer from:
   https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
   
2. Run the installer (choose the latest version)

3. Restart your terminal/command prompt after installation

### 2. Install Python Dependencies

Open PowerShell or Command Prompt in the project directory:

```powershell
pip install -r requirements.txt
```

This will install:
- markdown - For parsing markdown
- pymdown-extensions - Extended markdown features
- weasyprint - PDF generation
- Pillow - Image processing
- beautifulsoup4 - HTML parsing
- playwright - Browser automation for Mermaid rendering

### 3. Install Playwright Browsers

Playwright needs to download browser binaries:

```powershell
playwright install chromium
```

This downloads Chromium for rendering Mermaid diagrams.

### 4. Verify Installation

Test the installation by processing the example file:

```powershell
python main.py example_input.md -v
```

You should see output indicating the processing steps, and a PDF file will be created.

## Alternative Installation Methods

### Using a Virtual Environment (Recommended)

```powershell
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
playwright install chromium
```

### Troubleshooting

#### GTK3 Not Found Error

If you see errors about GTK3:
- Ensure GTK3 is installed correctly
- Check that GTK3 is in your system PATH
- Try restarting your computer

#### Playwright Browser Not Found

```powershell
# Reinstall browser
playwright install chromium --force
```

#### Module Import Errors

```powershell
# Upgrade pip first
python -m pip install --upgrade pip

# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

## System Requirements

- **Operating System**: Windows 10/11, macOS, or Linux
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 500MB for dependencies

## Next Steps

Once installed, see the [README.md](README.md) for usage instructions.
