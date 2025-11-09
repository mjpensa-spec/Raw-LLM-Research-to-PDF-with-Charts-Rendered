// DOM Elements
const fileInput = document.getElementById('fileInput');
const fileLabel = document.getElementById('fileLabel');
const selectedFile = document.getElementById('selectedFile');
const uploadForm = document.getElementById('uploadForm');
const convertBtn = document.getElementById('convertBtn');
const progressSection = document.getElementById('progressSection');
const resultSection = document.getElementById('resultSection');
const errorSection = document.getElementById('errorSection');
const statusMessage = document.getElementById('statusMessage');
const errorMessage = document.getElementById('errorMessage');
const convertAnotherBtn = document.getElementById('convertAnotherBtn');
const tryAgainBtn = document.getElementById('tryAgainBtn');

// State
let currentFile = null;

// Event Listeners
fileInput.addEventListener('change', handleFileSelect);
uploadForm.addEventListener('submit', handleSubmit);
convertAnotherBtn.addEventListener('click', resetForm);
tryAgainBtn.addEventListener('click', resetForm);

// Drag and drop
fileLabel.addEventListener('dragover', (e) => {
    e.preventDefault();
    fileLabel.style.borderColor = 'var(--primary-color)';
    fileLabel.style.background = '#f0f7ff';
});

fileLabel.addEventListener('dragleave', (e) => {
    e.preventDefault();
    fileLabel.style.borderColor = '';
    fileLabel.style.background = '';
});

fileLabel.addEventListener('drop', (e) => {
    e.preventDefault();
    fileLabel.style.borderColor = '';
    fileLabel.style.background = '';
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        fileInput.files = files;
        handleFileSelect();
    }
});

// Functions
function handleFileSelect() {
    if (fileInput.files.length > 0) {
        currentFile = fileInput.files[0];

        // Validate file type
        const fileName = currentFile.name.toLowerCase();
        const validExtensions = ['.md', '.markdown', '.txt', '.pdf'];
        const isValid = validExtensions.some(ext => fileName.endsWith(ext));

        if (!isValid) {
            showError('Invalid file type. Please upload a .md, .markdown, or .pdf file');
            currentFile = null;
            convertBtn.disabled = true;
            return;
        }        // Validate file size (16MB max)
        const maxSize = 16 * 1024 * 1024;
        if (currentFile.size > maxSize) {
            showError('File is too large. Maximum size is 16MB');
            currentFile = null;
            convertBtn.disabled = true;
            return;
        }
        
        // Display selected file
        selectedFile.innerHTML = `
            <svg style="width: 20px; height: 20px; display: inline; margin-right: 8px;" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <strong>${currentFile.name}</strong> (${formatFileSize(currentFile.size)})
        `;
        selectedFile.classList.add('show');
        convertBtn.disabled = false;
    }
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

async function handleSubmit(e) {
    e.preventDefault();
    
    if (!currentFile) {
        showError('Please select a file first');
        return;
    }
    
    // Show progress
    showProgress();
    
    // Create form data
    const formData = new FormData();
    formData.append('file', currentFile);
    
    try {
        // Upload and process file
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Processing failed');
        }
        
        // Get the PDF blob
        const blob = await response.blob();
        
        // Create download link
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = currentFile.name.replace(/\.(md|markdown|txt|pdf)$/i, '_processed.pdf');
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        
        // Show success
        showSuccess();
        
    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'An unexpected error occurred');
    }
}

function showProgress() {
    document.querySelector('.upload-section').style.display = 'none';
    progressSection.style.display = 'block';
    resultSection.style.display = 'none';
    errorSection.style.display = 'none';
    
    // Update status messages
    const messages = [
        'Processing your file...',
        'Fixing markdown syntax...',
        'Rendering Mermaid diagrams...',
        'Generating PDF...'
    ];
    
    let messageIndex = 0;
    const messageInterval = setInterval(() => {
        messageIndex = (messageIndex + 1) % messages.length;
        statusMessage.textContent = messages[messageIndex];
    }, 2000);
    
    // Store interval ID for cleanup
    progressSection.dataset.intervalId = messageInterval;
}

function showSuccess() {
    // Clear message interval
    if (progressSection.dataset.intervalId) {
        clearInterval(parseInt(progressSection.dataset.intervalId));
    }
    
    progressSection.style.display = 'none';
    resultSection.style.display = 'block';
    errorSection.style.display = 'none';
}

function showError(message) {
    // Clear message interval
    if (progressSection.dataset.intervalId) {
        clearInterval(parseInt(progressSection.dataset.intervalId));
    }
    
    document.querySelector('.upload-section').style.display = 'none';
    progressSection.style.display = 'none';
    resultSection.style.display = 'none';
    errorSection.style.display = 'block';
    errorMessage.textContent = message;
}

function resetForm() {
    // Clear file input
    fileInput.value = '';
    currentFile = null;
    selectedFile.innerHTML = '';
    selectedFile.classList.remove('show');
    convertBtn.disabled = true;
    
    // Show upload section
    document.querySelector('.upload-section').style.display = 'block';
    progressSection.style.display = 'none';
    resultSection.style.display = 'none';
    errorSection.style.display = 'none';
}

// Health check on page load
window.addEventListener('load', async () => {
    try {
        const response = await fetch('/api/health');
        if (!response.ok) {
            console.error('Server health check failed');
        }
    } catch (error) {
        console.error('Could not connect to server:', error);
    }
});
