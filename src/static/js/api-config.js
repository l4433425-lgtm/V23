// ARQV30 Enhanced v3.0 - API Configuration System
console.log('⚙️ Sistema de Configuração de APIs carregado');

class ApiConfigurationManager {
    constructor() {
        this.apis = {
            'gemini': { name: 'Google Gemini', env_var: 'GEMINI_API_KEY', critical: true },
            'openai': { name: 'OpenAI GPT', env_var: 'OPENAI_API_KEY', critical: true },
            'groq': { name: 'Groq Llama', env_var: 'GROQ_API_KEY', critical: false },
            'exa': { name: 'Exa Search', env_var: 'EXA_API_KEY', critical: true },
            'jina': { name: 'Jina Reader', env_var: 'JINA_API_KEY', critical: true },
            'youtube': { name: 'YouTube API', env_var: 'YOUTUBE_API_KEY', critical: false },
            'twitter': { name: 'Twitter API', env_var: 'TWITTER_BEARER_TOKEN', critical: false },
            'google_search': { name: 'Google Search', env_var: 'GOOGLE_SEARCH_KEY', critical: false }
        };
        
        this.configuredApis = new Set();
        this.init();
    }
    
    init() {
        console.log('🔧 Inicializando gerenciador de configuração de APIs');
        this.loadCurrentStatus();
    }
    
    async loadCurrentStatus() {
        try {
            const response = await fetch('/api/get_api_config');
            const data = await response.json();
            
            if (data.success) {
                this.updateConfiguredApis(data.config);
                this.updateOverviewStats();
            }
        } catch (error) {
            console.error('Erro ao carregar status das APIs:', error);
        }
    }
    
    updateConfiguredApis(config) {
        this.configuredApis.clear();
        
        Object.keys(config).forEach(api => {
            if (config[api]) {
                this.configuredApis.add(api);
            }
        });
        
        // Atualiza status visual
        Object.keys(this.apis).forEach(api => {
            this.updateApiStatus(api, config[api] || false);
        });
    }
    
    updateApiStatus(apiName, isConfigured) {
        const statusElement = document.getElementById(`${apiName}-status`);
        if (statusElement) {
            if (isConfigured) {
                statusElement.textContent = 'Configurado';
                statusElement.className = 'api-status configured';
            } else {
                statusElement.textContent = 'Não Configurado';
                statusElement.className = 'api-status missing';
            }
        }
    }
    
    updateOverviewStats() {
        const totalApis = Object.keys(this.apis).length;
        const configuredCount = this.configuredApis.size;
        const healthScore = Math.round((configuredCount / totalApis) * 100);
        
        const configuredElement = document.getElementById('configuredCount');
        const missingElement = document.getElementById('missingCount');
        const healthElement = document.getElementById('healthScore');
        
        if (configuredElement) configuredElement.textContent = configuredCount;
        if (missingElement) missingElement.textContent = totalApis - configuredCount;
        if (healthElement) healthElement.textContent = `${healthScore}%`;
    }
    
    async testApi(apiName, apiKey) {
        try {
            const response = await fetch('/api/save_api_config', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    api_name: apiName,
                    api_key: apiKey
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.configuredApis.add(apiName);
                this.updateApiStatus(apiName, true);
                this.updateOverviewStats();
                return { success: true, message: result.message };
            } else {
                return { success: false, error: result.error };
            }
            
        } catch (error) {
            return { success: false, error: error.message };
        }
    }
    
    async testAllApis() {
        const results = {};
        
        for (const apiName of Object.keys(this.apis)) {
            const keyInput = document.getElementById(`${apiName}-key`);
            if (keyInput && keyInput.value.trim()) {
                results[apiName] = await this.testApi(apiName, keyInput.value.trim());
            }
        }
        
        return results;
    }
    
    getConfigurationStatus() {
        const totalApis = Object.keys(this.apis).length;
        const configuredCount = this.configuredApis.size;
        const criticalApis = Object.values(this.apis).filter(api => api.critical).length;
        const criticalConfigured = Object.keys(this.apis)
            .filter(key => this.apis[key].critical && this.configuredApis.has(key)).length;
        
        return {
            total: totalApis,
            configured: configuredCount,
            missing: totalApis - configuredCount,
            critical_total: criticalApis,
            critical_configured: criticalConfigured,
            health_score: Math.round((configuredCount / totalApis) * 100),
            critical_health: Math.round((criticalConfigured / criticalApis) * 100),
            ready_for_analysis: criticalConfigured >= Math.ceil(criticalApis * 0.7) // 70% das críticas
        };
    }
}

// Global functions for API configuration
async function testAndSaveApi(apiName) {
    const keyInput = document.getElementById(`${apiName}-key`);
    const apiKey = keyInput.value.trim();
    
    if (!apiKey) {
        showNotification('Por favor, insira a chave da API', 'warning');
        return;
    }
    
    const button = event.target;
    const originalContent = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Testando...';
    button.disabled = true;
    
    try {
        const result = await apiConfigManager.testApi(apiName, apiKey);
        
        if (result.success) {
            showNotification(`✅ ${apiName.toUpperCase()} configurado com sucesso!`, 'success');
            keyInput.value = ''; // Limpa o campo por segurança
        } else {
            showNotification(`❌ Erro ao configurar ${apiName}: ${result.error}`, 'error');
        }
        
    } catch (error) {
        showNotification(`❌ Erro de conexão: ${error.message}`, 'error');
    } finally {
        button.innerHTML = originalContent;
        button.disabled = false;
    }
}

async function testAndSaveGoogleSearch() {
    const keyInput = document.getElementById('google-search-key');
    const cseInput = document.getElementById('google-cse-id');
    
    const apiKey = keyInput.value.trim();
    const cseId = cseInput.value.trim();
    
    if (!apiKey || !cseId) {
        showNotification('Por favor, insira tanto a chave quanto o CSE ID', 'warning');
        return;
    }
    
    const button = event.target;
    const originalContent = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Testando...';
    button.disabled = true;
    
    try {
        // Testa Google Search Key
        const keyResult = await apiConfigManager.testApi('google_search', apiKey);
        
        if (keyResult.success) {
            // Salva CSE ID também
            await fetch('/api/save_api_config', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    api_name: 'google_cse',
                    api_key: cseId
                })
            });
            
            showNotification('✅ Google Custom Search configurado com sucesso!', 'success');
            keyInput.value = '';
            cseInput.value = '';
            
            // Atualiza status
            apiConfigManager.updateApiStatus('google-search', true);
            
        } else {
            showNotification(`❌ Erro ao configurar Google Search: ${keyResult.error}`, 'error');
        }
        
    } catch (error) {
        showNotification(`❌ Erro de conexão: ${error.message}`, 'error');
    } finally {
        button.innerHTML = originalContent;
        button.disabled = false;
    }
}

async function testAllApis() {
    const button = event.target;
    const originalContent = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Testando Todas...';
    button.disabled = true;
    
    try {
        const results = await apiConfigManager.testAllApis();
        
        let successCount = 0;
        let totalTested = 0;
        
        Object.entries(results).forEach(([api, result]) => {
            totalTested++;
            if (result.success) {
                successCount++;
            }
        });
        
        if (successCount === totalTested) {
            showNotification(`✅ Todas as ${totalTested} APIs testadas com sucesso!`, 'success');
        } else {
            showNotification(`⚠️ ${successCount}/${totalTested} APIs configuradas com sucesso`, 'warning');
        }
        
        apiConfigManager.updateOverviewStats();
        
    } catch (error) {
        showNotification(`❌ Erro ao testar APIs: ${error.message}`, 'error');
    } finally {
        button.innerHTML = originalContent;
        button.disabled = false;
    }
}

function showApiGuide() {
    const guideContent = `
        <div class="api-guide">
            <h3>🔧 Guia de Configuração de APIs</h3>
            
            <div class="guide-section">
                <h4>1. APIs Críticas (Obrigatórias)</h4>
                <ul>
                    <li><strong>Google Gemini:</strong> Modelo principal de IA</li>
                    <li><strong>Exa Search:</strong> Busca neural avançada</li>
                    <li><strong>Jina Reader:</strong> Extração de conteúdo</li>
                </ul>
            </div>
            
            <div class="guide-section">
                <h4>2. APIs Importantes (Recomendadas)</h4>
                <ul>
                    <li><strong>OpenAI:</strong> Fallback de IA</li>
                    <li><strong>YouTube:</strong> Análise de vídeos</li>
                </ul>
            </div>
            
            <div class="guide-section">
                <h4>3. Ordem de Configuração Recomendada</h4>
                <ol>
                    <li>Configure Gemini primeiro (modelo primário)</li>
                    <li>Configure Exa Search (pesquisa principal)</li>
                    <li>Configure Jina Reader (extração de conteúdo)</li>
                    <li>Configure OpenAI (fallback)</li>
                    <li>Configure APIs sociais (opcional)</li>
                </ol>
            </div>
        </div>
    `;
    
    showModal('Guia de Configuração', guideContent);
}

function showApiPricing() {
    const pricingContent = `
        <div class="api-pricing">
            <h3>💰 Informações de Preços das APIs</h3>
            
            <div class="pricing-item">
                <h4>Google Gemini</h4>
                <p>Gratuito até 15 requisições/minuto</p>
                <p>Plano pago: $0.00025 por 1K caracteres</p>
            </div>
            
            <div class="pricing-item">
                <h4>OpenAI GPT-4</h4>
                <p>$0.03 por 1K tokens de entrada</p>
                <p>$0.06 por 1K tokens de saída</p>
            </div>
            
            <div class="pricing-item">
                <h4>Exa Search</h4>
                <p>1000 buscas gratuitas/mês</p>
                <p>Plano pago: $5/mês para 5K buscas</p>
            </div>
            
            <div class="pricing-item">
                <h4>Jina Reader</h4>
                <p>1M caracteres gratuitos/mês</p>
                <p>Plano pago: $20/mês para 20M caracteres</p>
            </div>
        </div>
    `;
    
    showModal('Preços das APIs', pricingContent);
}

function showTroubleshooting() {
    const troubleshootingContent = `
        <div class="troubleshooting">
            <h3>🔧 Solução de Problemas</h3>
            
            <div class="problem-solution">
                <h4>❌ "API Key inválida"</h4>
                <ul>
                    <li>Verifique se copiou a chave completa</li>
                    <li>Confirme se a API está ativada no painel</li>
                    <li>Verifique se há créditos disponíveis</li>
                </ul>
            </div>
            
            <div class="problem-solution">
                <h4>⚠️ "Quota excedida"</h4>
                <ul>
                    <li>Aguarde reset da quota (geralmente 24h)</li>
                    <li>Considere upgrade do plano</li>
                    <li>Use APIs alternativas temporariamente</li>
                </ul>
            </div>
            
            <div class="problem-solution">
                <h4>🔄 "Erro de conexão"</h4>
                <ul>
                    <li>Verifique sua conexão com internet</li>
                    <li>Tente novamente em alguns minutos</li>
                    <li>Verifique se não há firewall bloqueando</li>
                </ul>
            </div>
        </div>
    `;
    
    showModal('Solução de Problemas', troubleshootingContent);
}

function showModal(title, content) {
    // Remove modal existente se houver
    const existingModal = document.getElementById('helpModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    const modal = document.createElement('div');
    modal.id = 'helpModal';
    modal.className = 'api-config-modal';
    modal.style.display = 'flex';
    
    modal.innerHTML = `
        <div class="api-config-content">
            <div class="api-config-header">
                <h3 class="api-config-title">${title}</h3>
                <button class="api-config-close" onclick="closeHelpModal()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="modal-body">
                ${content}
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
}

function closeHelpModal() {
    const modal = document.getElementById('helpModal');
    if (modal) {
        modal.remove();
    }
}

// Global instance
let apiConfigManager;

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    apiConfigManager = new ApiConfigurationManager();
    console.log('✅ Gerenciador de APIs inicializado');
});

// Export for use in other scripts
window.apiConfigManager = apiConfigManager;
window.testAndSaveApi = testAndSaveApi;
window.testAndSaveGoogleSearch = testAndSaveGoogleSearch;
window.testAllApis = testAllApis;
window.showApiGuide = showApiGuide;
window.showApiPricing = showApiPricing;
window.showTroubleshooting = showTroubleshooting;