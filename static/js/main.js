document.addEventListener('DOMContentLoaded', () => {
    const elements = {
        dropZone: document.getElementById('dropZone'),
        fileInput: document.getElementById('fileInput'),
        originalPreview: document.getElementById('originalPreview'),
        colorizedPreview: document.getElementById('colorizedPreview'),
        uploadText: document.getElementById('uploadText'),
        loading: document.getElementById('loading'),
        error: document.getElementById('error'),
        downloadBtn: document.getElementById('downloadBtn'),
        progressBar: document.getElementById('progressBar')
    };

    // Event Listeners
    elements.dropZone.addEventListener('click', () => elements.fileInput.click());
    elements.dropZone.addEventListener('dragover', handleDragOver);
    elements.dropZone.addEventListener('dragleave', handleDragLeave);
    elements.dropZone.addEventListener('drop', handleDrop);
    elements.fileInput.addEventListener('change', handleFileSelect);
    elements.downloadBtn.addEventListener('click', handleDownload);

    function handleDragOver(e) {
        e.preventDefault();
        elements.dropZone.style.borderColor = 'white';
    }

    function handleDragLeave() {
        elements.dropZone.style.borderColor = 'rgba(255, 255, 255, 0.3)';
    }

    function handleDrop(e) {
        e.preventDefault();
        handleDragLeave();
        if (e.dataTransfer.files.length > 0) {
            handleFile(e.dataTransfer.files[0]);
        }
    }

    function handleFileSelect(e) {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    }

    async function handleFile(file) {
        try {
            resetUIState();
            validateFile(file);
            await showFilePreview(file);
            const response = await uploadFile(file);
            handleSuccess(response);
        } catch (error) {
            handleError(error);
        }
    }

    function resetUIState() {
        // Hide or reset some UI elements before handling a new file
        elements.colorizedPreview.style.display = 'none';
        elements.error.style.display = 'none';
        elements.downloadBtn.classList.add('hidden');
        elements.loading.style.display = 'none';
        // Notice: We do NOT hide 'uploadText' here.
    }

    function validateFile(file) {
        const validTypes = ['image/jpeg', 'image/png', 'image/jpg'];
        const maxSize = 5 * 1024 * 1024; // 5MB

        if (!validTypes.includes(file.type)) {
            throw new Error('Invalid file type. Please upload JPG/PNG images.');
        }

        if (file.size > maxSize) {
            throw new Error('File size too large. Maximum 5MB allowed.');
        }
    }

    function showFilePreview(file) {
        return new Promise((resolve) => {
            const reader = new FileReader();
            reader.onload = (e) => {
                // Show the original preview image
                elements.originalPreview.src = e.target.result;
                elements.originalPreview.style.display = 'block';

                // Remove or comment out the line that hides uploadText
                // elements.uploadText.style.display = 'none';

                resolve();
            };
            reader.readAsDataURL(file);
        });
    }

    async function uploadFile(file) {
        elements.progressBar.style.display = 'block';
        elements.loading.style.display = 'flex';

        try {
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch('/api/colorize', {
                method: 'POST',
                body: formData,
                signal: AbortSignal.timeout(30000) // 30s timeout
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Colorization failed');
            }

            return data;
        } catch (error) {
            throw new Error(error.message || 'Failed to process image');
        } finally {
            elements.progressBar.style.display = 'none';
            elements.loading.style.display = 'none';
        }
    }

    function handleSuccess(data) {
        // Show colorized image & enable download
        elements.colorizedPreview.src = data.downloadUrl;
        elements.colorizedPreview.style.display = 'block';
        elements.downloadBtn.href = data.downloadUrl;
        elements.downloadBtn.classList.remove('hidden');

        // We do NOT hide 'uploadText' here, so it stays visible.
    }

    function handleError(error) {
        // Show error message & reset some UI
        elements.error.textContent = error.message;
        elements.error.style.display = 'block';
        elements.originalPreview.style.display = 'none';
        elements.downloadBtn.classList.add('hidden');

        // If there's an error, we re-show the text (just in case):
        elements.uploadText.style.display = 'block';
    }

    function handleDownload(e) {
        if (!elements.downloadBtn.href) {
            e.preventDefault();
            handleError(new Error('No image available to download'));
        }
    }
});
