// Constantes
const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB
const VALID_FILE_TYPES = ['application/pdf', 'text/plain'];

// Elementos DOM
const elements = {
    form: document.getElementById('emailForm'),
    emailText: document.getElementById('emailText'),
    fileUpload: document.getElementById('fileUpload'),
    filePreview: document.getElementById('filePreview'),
    processButton: document.getElementById('processButton'),
    spinner: document.getElementById('spinner'),
    notification: document.getElementById('notification'),
    responseModal: document.getElementById('responseModal'),
    classificationResult: document.getElementById('classificationResult'),
    suggestedResponse: document.getElementById('suggestedResponse'),
    charCount: document.getElementById('charCount')
};

// Gerenciamento de Estado
const state = {
    isProcessing: false,
    currentFile: null
};

// Utilitários
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function validateFile(file) {
    if (!VALID_FILE_TYPES.includes(file.type)) {
        throw new Error('Formato de arquivo inválido. Apenas PDF e TXT são suportados.');
    }
    if (file.size > MAX_FILE_SIZE) {
        throw new Error(`Arquivo muito grande. Tamanho máximo: ${formatFileSize(MAX_FILE_SIZE)}`);
    }
}

// Feedback Visual
function showNotification(message, type) {
    elements.notification.textContent = message;
    elements.notification.className = `notification ${type} show`;
    setTimeout(() => {
        elements.notification.classList.add('hide');
        setTimeout(() => {
            elements.notification.className = `notification ${type}`;
        }, 300);
    }, 3000);
}

function setLoading(isLoading) {
    state.isProcessing = isLoading;
    elements.processButton.disabled = isLoading;
    elements.spinner.style.display = isLoading ? 'inline-block' : 'none';
    elements.emailText.disabled = isLoading;
    elements.fileUpload.disabled = isLoading;
}

// Manipulação de Arquivos
async function handleFileUpload(file) {
    try {
        validateFile(file);
        state.currentFile = file;
        elements.filePreview.innerHTML = `
            Arquivo: ${file.name} (${formatFileSize(file.size)})
            <span onclick="removeFile()" class="remove-file">×</span>
        `;
        elements.emailText.value = '';
    } catch (error) {
        showNotification(error.message, 'error');
        removeFile();
    }
}

function removeFile() {
    elements.fileUpload.value = '';
    elements.filePreview.textContent = '';
    state.currentFile = null;
}

// Processamento de Email
async function processEmail() {
    if (state.isProcessing) return;
    
    try {
        const content = await getContent();
        if (!content) {
            showNotification('Por favor, insira um texto ou selecione um arquivo.', 'error');
            return;
        }

        setLoading(true);
        const result = await sendToBackend(content);
        
        if (result.error) {
            throw new Error(result.error);
        }

        showNotification('Email processado com sucesso!', 'success');
        showResponseModal(result.category, result.response);
    } catch (error) {
        showNotification(error.message, 'error');
    } finally {
        setLoading(false);
    }
}

async function getContent() {
    if (state.currentFile) {
        return await readFileContent(state.currentFile);
    }
    return elements.emailText.value.trim();
}

async function readFileContent(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => resolve(e.target.result);
        reader.onerror = (e) => reject(new Error('Erro ao ler arquivo'));
        
        if (file.type === 'application/pdf') {
            reader.readAsArrayBuffer(file);
        } else {
            reader.readAsText(file);
        }
    });
}

// Requisições ao Backend
async function sendToBackend(content) {
    try {
        const response = await fetch(window.location.origin + '/process', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: content })
        });

        if (!response.ok) {
            if (response.status === 429) {
                throw new Error('Muitas requisições. Tente novamente mais tarde.');
            }
            throw new Error('Erro na comunicação com o servidor');
        }

        return await response.json();
    } catch (error) {
        throw new Error('Erro ao processar a requisição: ' + error.message);
    }
}

// Event Listeners
elements.fileUpload.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) handleFileUpload(file);
});

elements.emailText.addEventListener('input', (e) => {
    if (e.target.value && state.currentFile) {
        removeFile();
    }
    adjustTextareaHeight(e.target);
    updateCharCount(e.target.value.length);
});

// Inicialização
function init() {
    adjustTextareaHeight(elements.emailText);
    updateCharCount(elements.emailText.value.length);
}

init();