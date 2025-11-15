// ========================================
// PLUGINFORGE STUDIO - JAVASCRIPT
// ========================================
// Este arquivo contém toda a lógica do lado do cliente:
// - Captura do formulário
// - Validação de dados
// - Envio para o backend via AJAX
// - Exibição de loading e animações
// - Download do arquivo .jar
// ========================================

// ========================================
// ELEMENTOS DOM
// ========================================

const pluginForm = document.getElementById('pluginForm');
const submitBtn = document.getElementById('submitBtn');
const statusContainer = document.getElementById('statusContainer');
const resultContainer = document.getElementById('resultContainer');
const errorContainer = document.getElementById('errorContainer');
const statusText = document.getElementById('statusText');
const resultMessage = document.getElementById('resultMessage');
const errorMessage = document.getElementById('errorMessage');
const downloadBtn = document.getElementById('downloadBtn');
const newPluginBtn = document.getElementById('newPluginBtn');
const retryBtn = document.getElementById('retryBtn');

// Steps do progresso
const step1 = document.getElementById('step1');
const step2 = document.getElementById('step2');
const step3 = document.getElementById('step3');
const step4 = document.getElementById('step4');

// ========================================
// EVENT LISTENERS
// ========================================

// Quando o formulário for submetido
pluginForm.addEventListener('submit', async (e) => {
    e.preventDefault(); // Impede o envio padrão do formulário
    await generatePlugin();
});

// Botão "Gerar Novo Plugin"
newPluginBtn.addEventListener('click', () => {
    resetForm();
});

// Botão "Tentar Novamente"
retryBtn.addEventListener('click', () => {
    resetForm();
});

// ========================================
// FUNÇÃO PRINCIPAL - GERAR PLUGIN
// ========================================

async function generatePlugin() {
    // Coleta os dados do formulário
    const formData = {
        pluginName: document.getElementById('pluginName').value.trim(),
        pluginVersion: document.getElementById('pluginVersion').value.trim(),
        mcVersion: document.getElementById('mcVersion').value,
        description: document.getElementById('description').value.trim()
    };

    // Validação básica
    if (!formData.pluginName || !formData.description) {
        showError('Por favor, preencha todos os campos obrigatórios.');
        return;
    }

    // Remove espaços do nome do plugin
    formData.pluginName = formData.pluginName.replace(/\s+/g, '');

    // Valida formato da versão
    const versionRegex = /^\d+\.\d+\.\d+$/;
    if (!versionRegex.test(formData.pluginVersion)) {
        showError('Formato de versão inválido. Use o formato: 1.0.0');
        return;
    }

    try {
        // Mostra a tela de loading
        showLoading();
        
        // Desabilita o botão de submit
        submitBtn.disabled = true;

        // Simula progresso (puramente visual)
        simulateProgress();

        // Faz a requisição para o backend
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();

        if (response.ok && result.success) {
            // Sucesso! Redireciona para o chat do plugin
            redirectToChat(result.plugin_id, result.message);
        } else {
            // Erro retornado pelo backend
            showError(result.error || 'Erro desconhecido ao gerar o plugin.');
        }

    } catch (error) {
        // Erro de rede ou outro erro inesperado
        console.error('Erro:', error);
        showError('Erro de conexão com o servidor. Verifique se o servidor está rodando.');
    } finally {
        // Re-habilita o botão
        submitBtn.disabled = false;
    }
}

// ========================================
// FUNÇÕES DE INTERFACE
// ========================================

/**
 * Mostra a tela de loading com animação de progresso
 */
function showLoading() {
    // Esconde tudo primeiro
    pluginForm.parentElement.style.display = 'none';
    resultContainer.style.display = 'none';
    errorContainer.style.display = 'none';
    
    // Mostra o container de status
    statusContainer.style.display = 'block';
    
    // Reseta os steps
    [step1, step2, step3, step4].forEach(step => step.classList.remove('active'));
}

/**
 * Simula o progresso visual dos steps (puramente cosmético)
 */
function simulateProgress() {
    // Step 1: Gerando código com IA
    setTimeout(() => {
        step1.classList.add('active');
        statusText.textContent = 'Gerando código com IA...';
    }, 500);

    // Step 2: Criando estrutura
    setTimeout(() => {
        step1.classList.remove('active');
        step2.classList.add('active');
        statusText.textContent = 'Criando estrutura do projeto...';
    }, 8000);

    // Step 3: Compilando
    setTimeout(() => {
        step2.classList.remove('active');
        step3.classList.add('active');
        statusText.textContent = 'Compilando com Maven...';
    }, 12000);

    // Step 4: Finalizando
    setTimeout(() => {
        step3.classList.remove('active');
        step4.classList.add('active');
        statusText.textContent = 'Finalizando...';
    }, 18000);
}

/**
 * Redireciona para o chat do plugin após geração bem-sucedida
 * @param {string} pluginId - ID do plugin gerado
 * @param {string} message - Mensagem de sucesso
 */
function redirectToChat(pluginId, message) {
    // Finaliza o progresso visual
    step4.classList.add('active');
    statusText.textContent = '✅ Plugin gerado com sucesso!';
    
    // Aguarda 2 segundos para o usuário ver o sucesso, depois redireciona
    setTimeout(() => {
        window.location.href = `/plugin/${pluginId}`;
    }, 2000);
}

/**
 * Mostra a tela de sucesso com o botão de download
 * @param {string} message - Mensagem de sucesso
 * @param {string} downloadUrl - URL para download do .jar
 */
function showSuccess(message, downloadUrl) {
    // Esconde tudo
    statusContainer.style.display = 'none';
    errorContainer.style.display = 'none';
    
    // Mostra o resultado
    resultContainer.style.display = 'block';
    resultMessage.textContent = message;
    
    // Configura o botão de download
    downloadBtn.href = downloadUrl;
    
    // Inicia o download automaticamente após 1 segundo
    setTimeout(() => {
        window.location.href = downloadUrl;
    }, 1000);
}

/**
 * Mostra a tela de erro
 * @param {string} message - Mensagem de erro
 */
function showError(message) {
    // Esconde tudo
    statusContainer.style.display = 'none';
    resultContainer.style.display = 'none';
    
    // Mostra o erro
    errorContainer.style.display = 'block';
    errorMessage.textContent = message;
}

/**
 * Reseta o formulário e volta à tela inicial
 */
function resetForm() {
    // Esconde tudo
    statusContainer.style.display = 'none';
    resultContainer.style.display = 'none';
    errorContainer.style.display = 'none';
    
    // Mostra o formulário
    pluginForm.parentElement.style.display = 'block';
    
    // Limpa o formulário (opcional)
    // pluginForm.reset();
    
    // Re-habilita o botão
    submitBtn.disabled = false;
    
    // Scroll suave para o topo
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ========================================
// VALIDAÇÃO EM TEMPO REAL
// ========================================

// Valida o nome do plugin em tempo real (remove espaços)
document.getElementById('pluginName').addEventListener('input', (e) => {
    const value = e.target.value;
    const noSpaces = value.replace(/\s+/g, '');
    
    if (value !== noSpaces) {
        e.target.value = noSpaces;
    }
});

// Contador de caracteres para a descrição
document.getElementById('description').addEventListener('input', (e) => {
    const charCount = e.target.value.length;
    const minChars = 20;
    
    // Você pode adicionar um indicador visual aqui se desejar
    if (charCount < minChars) {
        e.target.style.borderColor = 'var(--warning-color)';
    } else {
        e.target.style.borderColor = 'transparent';
    }
});

// ========================================
// INICIALIZAÇÃO
// ========================================

console.log('🚀 PluginForge Studio carregado!');
console.log('✅ Sistema pronto para gerar plugins.');

// Foca no primeiro campo ao carregar
document.getElementById('pluginName').focus();
