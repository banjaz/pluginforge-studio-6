/* ========================================
   PLUGINFORGE STUDIO - JAVASCRIPT PRINCIPAL
   ======================================== */

// Configuração global
window.PluginForge = {
    config: {
        apiTimeout: 60000,
        maxRetries: 3,
        chatRefreshInterval: 5000
    },
    
    // Utilitários
    utils: {
        // Formatação de datas
        formatDate: function(date) {
            return new Intl.DateTimeFormat('pt-BR', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit'
            }).format(new Date(date));
        },
        
        // Escape de HTML
        escapeHtml: function(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        },
        
        // Validação de email
        validateEmail: function(email) {
            const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return re.test(email);
        },
        
        // Validação de nome de plugin
        validatePluginName: function(name) {
            return /^[a-zA-Z][a-zA-Z0-9]*$/.test(name);
        },
        
        // Debounce function
        debounce: function(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        }
    },
    
    // Gerenciamento de API
    api: {
        // Request com retry
        request: async function(url, options = {}) {
            const defaults = {
                timeout: window.PluginForge.config.apiTimeout,
                headers: {
                    'Content-Type': 'application/json',
                }
            };
            
            const config = { ...defaults, ...options };
            
            let attempts = 0;
            while (attempts < window.PluginForge.config.maxRetries) {
                try {
                    const controller = new AbortController();
                    const timeoutId = setTimeout(() => controller.abort(), config.timeout);
                    
                    const response = await fetch(url, {
                        ...config,
                        signal: controller.signal
                    });
                    
                    clearTimeout(timeoutId);
                    
                    if (!response.ok) {
                        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                    }
                    
                    return await response.json();
                } catch (error) {
                    attempts++;
                    if (attempts >= window.PluginForge.config.maxRetries) {
                        throw error;
                    }
                    
                    // Aguardar antes de tentar novamente
                    await new Promise(resolve => setTimeout(resolve, 1000 * attempts));
                }
            }
        },
        
        // Métodos HTTP específicos
        get: function(url) {
            return this.request(url, { method: 'GET' });
        },
        
        post: function(url, data) {
            return this.request(url, {
                method: 'POST',
                body: JSON.stringify(data)
            });
        },
        
        put: function(url, data) {
            return this.request(url, {
                method: 'PUT',
                body: JSON.stringify(data)
            });
        },
        
        delete: function(url) {
            return this.request(url, { method: 'DELETE' });
        }
    },
    
    // Gerenciamento de UI
    ui: {
        // Loading spinner
        showLoading: function(element, text = 'Carregando...') {
            if (typeof element === 'string') {
                element = document.querySelector(element);
            }
            
            if (element) {
                element.innerHTML = `
                    <div class="text-center p-3">
                        <div class="spinner-border text-primary" role="status">
                            <span class="visually-hidden">Carregando...</span>
                        </div>
                        <div class="mt-2">${text}</div>
                    </div>
                `;
                element.disabled = true;
            }
        },
        
        // Esconder loading
        hideLoading: function(element, originalContent = '') {
            if (typeof element === 'string') {
                element = document.querySelector(element);
            }
            
            if (element) {
                element.innerHTML = originalContent;
                element.disabled = false;
            }
        },
        
        // Mostrar toast/notificação
        showToast: function(message, type = 'info', duration = 4000) {
            const toastId = 'toast-' + Date.now();
            const toast = document.createElement('div');
            toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
            toast.style.cssText = `
                top: 20px; 
                right: 20px; 
                z-index: 9999; 
                min-width: 300px;
                max-width: 500px;
            `;
            toast.id = toastId;
            
            toast.innerHTML = `
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            
            document.body.appendChild(toast);
            
            // Auto-remove
            setTimeout(() => {
                const element = document.getElementById(toastId);
                if (element) {
                    element.remove();
                }
            }, duration);
            
            return toastId;
        },
        
        // Confirm dialog
        confirm: function(message, callback) {
            if (confirm(message)) {
                callback();
            }
        },
        
        // Modal
        showModal: function(modalId) {
            const modal = new bootstrap.Modal(document.getElementById(modalId));
            modal.show();
        },
        
        // Progress bar
        updateProgress: function(elementId, percentage, text = '') {
            const element = document.getElementById(elementId);
            if (element) {
                element.style.width = percentage + '%';
                if (text) {
                    const textElement = element.parentElement.nextElementSibling;
                    if (textElement) {
                        textElement.textContent = text;
                    }
                }
            }
        }
    },
    
    // Gerenciamento de formulários
    forms: {
        // Validação de formulário
        validate: function(formElement) {
            const inputs = formElement.querySelectorAll('input[required], textarea[required], select[required]');
            let isValid = true;
            
            inputs.forEach(input => {
                const value = input.value.trim();
                const isEmpty = !value;
                
                // Remove previous error state
                input.classList.remove('is-invalid');
                
                if (isEmpty) {
                    input.classList.add('is-invalid');
                    isValid = false;
                }
                
                // Validações específicas
                if (input.type === 'email' && value) {
                    if (!window.PluginForge.utils.validateEmail(value)) {
                        input.classList.add('is-invalid');
                        isValid = false;
                    }
                }
                
                if (input.name === 'pluginName' && value) {
                    if (!window.PluginForge.utils.validatePluginName(value)) {
                        input.classList.add('is-invalid');
                        input.title = 'Nome deve começar com letra e conter apenas letras e números';
                        isValid = false;
                    }
                }
            });
            
            return isValid;
        },
        
        // Serializar formulário
        serialize: function(formElement) {
            const formData = new FormData(formElement);
            const data = {};
            
            for (let [key, value] of formData.entries()) {
                data[key] = value;
            }
            
            return data;
        }
    },
    
    // Chat management
    chat: {
        // Scroll para o final
        scrollToBottom: function() {
            const chatContainer = document.querySelector('.chat-container');
            if (chatContainer) {
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }
        },
        
        // Adicionar mensagem
        addMessage: function(role, content, timestamp = null) {
            const chatContainer = document.getElementById('chatMessages');
            if (!chatContainer) return;
            
            const messageDiv = document.createElement('div');
            messageDiv.className = `message mb-3 ${role === 'user' ? 'message-user' : 'message-ai'}`;
            
            const timeStr = timestamp ? 
                window.PluginForge.utils.formatDate(timestamp) : 
                window.PluginForge.utils.formatDate(new Date());
            
            messageDiv.innerHTML = `
                <div class="d-flex ${role === 'user' ? 'justify-content-end' : 'justify-content-start'}">
                    <div class="${role === 'user' ? 'bg-primary text-white' : 'bg-light'} rounded p-3" style="max-width: 80%;">
                        <div class="d-flex align-items-center mb-1">
                            ${role === 'user' ? 
                                '<i class="fas fa-user me-2"></i><strong>Você</strong>' : 
                                '<i class="fas fa-robot me-2"></i><strong>PluginCraft AI</strong>'
                            }
                        </div>
                        <div>${content.replace(/\n/g, '<br>')}</div>
                        <small class="${role === 'user' ? 'text-white-50' : 'text-muted'}">
                            ${timeStr}
                        </small>
                    </div>
                </div>
            `;
            
            chatContainer.appendChild(messageDiv);
            this.scrollToBottom();
            
            return messageDiv;
        },
        
        // Typing indicator
        showTyping: function() {
            return this.addMessage('ai', '<i class="fas fa-ellipsis-h fa-spin"></i> Digitando...');
        },
        
        // Remove typing indicator
        hideTyping: function(typingElement) {
            if (typingElement && typingElement.parentNode) {
                typingElement.parentNode.remove();
            }
        }
    },
    
    // Plugin management
    plugins: {
        // Download plugin
        download: function(pluginId, filename) {
            window.PluginForge.ui.showToast('Iniciando download...', 'info');
            
            const link = document.createElement('a');
            link.href = `/api/download/${pluginId}/${filename}`;
            link.download = filename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            
            window.PluginForge.ui.showToast('Download iniciado!', 'success');
        },
        
        // Recompile plugin
        recompile: async function(pluginId) {
            try {
                window.PluginForge.ui.showToast('Recompilando plugin...', 'info');
                
                const response = await window.PluginForge.api.post(`/api/plugins/${pluginId}/recompile`);
                
                if (response.success) {
                    window.PluginForge.ui.showToast('Plugin recompilado com sucesso!', 'success');
                    setTimeout(() => location.reload(), 2000);
                } else {
                    throw new Error(response.error);
                }
            } catch (error) {
                window.PluginForge.ui.showToast(`Erro ao recompilar: ${error.message}`, 'danger');
            }
        }
    },
    
    // Inicialização
    init: function() {
        console.log('🚀 PluginForge Studio inicializado');
        
        // Auto-scroll para chat
        this.chat.scrollToBottom();
        
        // Configurar tooltips
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
        
        // Configurar validação de formulários
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', function(e) {
                if (!window.PluginForge.forms.validate(this)) {
                    e.preventDefault();
                    window.PluginForge.ui.showToast('Por favor, corrija os erros no formulário.', 'warning');
                }
            });
        });
        
        // Event listeners globais
        document.addEventListener('keydown', function(e) {
            // Ctrl+Enter para enviar mensagens no chat
            if (e.ctrlKey && e.key === 'Enter') {
                const chatForm = document.getElementById('chatForm');
                if (chatForm) {
                    chatForm.dispatchEvent(new Event('submit'));
                }
            }
        });
    }
};

// Auto-inicialização quando DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    window.PluginForge.init();
});

// Global error handler
window.addEventListener('error', function(e) {
    console.error('Erro global:', e.error);
    window.PluginForge.ui.showToast('Ocorreu um erro inesperado.', 'danger');
});

// Unhandled promise rejections
window.addEventListener('unhandledrejection', function(e) {
    console.error('Promise rejection:', e.reason);
    e.preventDefault();
    window.PluginForge.ui.showToast('Erro de conexão. Tente novamente.', 'danger');
});

// Export para uso em outros scripts
window.PluginForgeAPI = window.PluginForge.api;
window.PluginForgeUI = window.PluginForge.ui;