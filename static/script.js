// Constantes e Configurações
const API_CONFIG = {
    ENDPOINTS: {
        PROCESS: '/process'
    },
    TIMEOUT: 30000,
    MAX_RETRIES: 3,
    RETRY_DELAY: 1000
};

const FILE_CONFIG = {
    MAX_SIZE: 5 * 1024 * 1024,
    VALID_TYPES: ['application/pdf', 'text/plain'],
    CHUNK_SIZE: 1024 * 1024 // 1MB para leitura em chunks
};

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

// Cache e Estado
const responseCache = new Map();
const state = {
    isProcessing: false,
    currentFile: null,
    abortController: null
};

// Utilitários Melhorados
const Utils = {
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },

    validateFile(file) {
        if (!FILE_CONFIG.VALID_TYPES.includes(file.type)) {
            throw new Error('Formato de arquivo inválido. Apenas PDF e TXT são suportados.');
        }
        if (file.size > FILE_CONFIG.MAX_SIZE) {
            throw new Error(`Arquivo muito grande. Tamanho máximo: ${this.formatFileSize(FILE_CONFIG.MAX_SIZE)}`);
        }
    },

    debounce(func, wait) {
        let timeout;
        return function(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    },

    generateRequestId() {
        return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    }
};

// Gerenciador de Notificações Melhorado
const NotificationManager = {
    timeouts: {},

    show(message, type) {
        if (this.timeouts.hide) clearTimeout(this.timeouts.hide);
        if (this.timeouts.remove) clearTimeout(this.timeouts.remove);

        elements.notification.textContent = message;
        elements.notification.className = `notification ${type} show`;

        this.timeouts.hide = setTimeout(() => {
            elements.notification.classList.add('hide');
            this.timeouts.remove = setTimeout(() => {
                elements.notification.className = `notification ${type}`;
            }, 300);
        }, 3000);
    },

    error(message) {
        this.show(message, 'error');
        console.error(message); // Log para debugging
    },

    success(message) {
        this.show(message, 'success');
    }
};

// Gerenciador de Estado Melhorado
const StateManager = {
    setLoading(isLoading) {
        state.isProcessing = isLoading;
        elements.processButton.disabled = isLoading;
        elements.spinner.style.display = isLoading ? 'inline-block' : 'none';
        elements.emailText.disabled = isLoading;
        elements.fileUpload.disabled = isLoading;

        if (isLoading) {
            state.abortController = new AbortController();
        } else {
            state.abortController = null;
        }
    },

    reset() {
        this.setLoading(false);
        state.currentFile = null;
    }
};

// Manipulação de Arquivos Melhorada
const FileManager = {
    async handleUpload(file) {
        try {
            Utils.validateFile(file);
            state.currentFile = file;
            elements.filePreview.innerHTML = `
                Arquivo: ${file.name} (${Utils.formatFileSize(file.size)})
                <span onclick="FileManager.remove()" class="remove-file">×</span>
            `;
            elements.emailText.value = '';
        } catch (error) {
            NotificationManager.error(error.message);
            this.remove();
        }
    },

    remove() {
        elements.fileUpload.value = '';
        elements.filePreview.textContent = '';
        state.currentFile = null;
    },

    async readContent(file) {
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
};

// Comunicação com Backend Melhorada
const ApiService = {
    async sendRequest(content, retryCount = 0) {
        const cacheKey = btoa(content.slice(0, 100));
        if (responseCache.has(cacheKey)) {
            return responseCache.get(cacheKey);
        }

        try {
            const response = await fetch(window.location.origin + API_CONFIG.ENDPOINTS.PROCESS, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Request-ID': Utils.generateRequestId()
                },
                body: JSON.stringify({ 
                    email: content,
                    timestamp: Date.now()
                }),
                signal: state.abortController?.signal
            });

            if (!response.ok) {
                if (response.status === 429) {
                    throw new Error('Muitas requisições. Tente novamente mais tarde.');
                }
                throw new Error(`Erro no servidor: ${response.statusText}`);
            }

            const result = await response.json();
            
            if (result.error) {
                throw new Error(result.error);
            }

            responseCache.set(cacheKey, result);
            return result;

        } catch (error) {
            if (error.name === 'AbortError') {
                throw new Error('Operação cancelada');
            }

            if (retryCount < API_CONFIG.MAX_RETRIES) {
                await new Promise(resolve => setTimeout(resolve, API_CONFIG.RETRY_DELAY * (retryCount + 1)));
                return this.sendRequest(content, retryCount + 1);
            }

            throw error;
        }
    }
};

// Processamento Principal Melhorado
async function processEmail() {
    if (state.isProcessing) return;

    try {
        const content = state.currentFile ? 
            await FileManager.readContent(state.currentFile) : 
            elements.emailText.value.trim();

        if (!content) {
            NotificationManager.error('Por favor, insira um texto ou selecione um arquivo.');
            return;
        }

        StateManager.setLoading(true);
        const result = await ApiService.sendRequest(content);
        
        NotificationManager.success('Email processado com sucesso!');
        showResponseModal(result.category, result.response);

    } catch (error) {
        NotificationManager.error(error.message);
    } finally {
        StateManager.setLoading(false);
    }
}

// Event Listeners Otimizados
elements.fileUpload.addEventListener('change', 
    Utils.debounce(e => {
        const file = e.target.files[0];
        if (file) FileManager.handleUpload(file);
    }, 300)
);

elements.emailText.addEventListener('input', 
    Utils.debounce(e => {
        if (e.target.value && state.currentFile) {
            FileManager.remove();
        }
        adjustTextareaHeight(e.target);
        updateCharCount(e.target.value.length);
    }, 100)
);

// Inicialização
function init() {
    adjustTextareaHeight(elements.emailText);
    updateCharCount(elements.emailText.value.length);
}

init();