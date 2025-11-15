# 🔄 Migração para OpenRouter (Polaris Alpha)

## 🚀 Migração Concluída!

Migrei com sucesso o PluginForge Studio de **Google AI Studio (Gemini)** para **OpenRouter (Polaris Alpha)**!

## 🔥 Benefícios do Polaris Alpha

### ✅ **Vantagens Principais**
- 🆓 **100% Gratuito**: $0/M tokens (input e output)
- 🧠 **256K Tokens**: Context window massiva (vs ~32K do Gemini)
- 👨‍💻 **Especializado em Programação**: Otimizado para código Java
- 🌐 **OpenRouter**: Acesso unificado a múltiplos LLMs
- ⚡ **Performance**: Respostas rápidas e consistentes

### 📊 Comparação: Polaris vs Gemini

| Característica | Polaris Alpha | Gemini Pro |
|---|---|---|
| **Preço** | 🆓 Gratuito | 💰 Pago |
| **Context Window** | 256K tokens | ~32K tokens |
| **Especialização** | Programming-focused | Generalista |
| **API Key** | OpenRouter | Google AI Studio |
| **Latência** | ⚡ Rápida | ⚡ Rápida |

## 🔧 Mudanças Implementadas

### 1. **Configuração da API**
```python
# ANTES: Google AI Studio
API_KEY = "SUA_CHAVE_GEMINI"
API_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models"
API_MODEL = "gemini-1.5-pro"

# DEPOIS: OpenRouter
API_KEY = "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"
API_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
API_MODEL = "openrouter/polaris-alpha"
```

### 2. **Formato da Requisição**
```python
# ANTES: Formato Gemini
payload = {
    'contents': [
        {
            'parts': [{'text': prompt}]
        }
    ],
    'generationConfig': {...}
}

# DEPOIS: Formato OpenRouter (OpenAI-compatible)
payload = {
    'model': API_MODEL,
    'messages': [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': prompt}
    ],
    'temperature': 0.7,
    'max_tokens': 4096
}
```

### 3. **Estrutura da Resposta**
```python
# ANTES: Formato Gemini
content = result['candidates'][0]['content']['parts'][0]['text']

# DEPOIS: Formato OpenRouter
content = result['choices'][0]['message']['content']
```

## 🧪 Como Testar

### Teste Rápido
```bash
python test_openrouter.py
```

### Teste via Interface Web
```bash
python app.py
# Acesse: http://localhost:5000/test
```

### Teste Completo
```bash
python app.py
# Acesse: http://localhost:5000
# Preencha o formulário e gere um plugin
```

## 🔄 Alternativas (Se Necessário)

Se você quiser usar outras APIs, descomente a configuração desejada em `app.py`:

### **OpenAI GPT-4**
```python
API_KEY = "sk-..."  # Sua chave OpenAI
API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
API_MODEL = "gpt-4"
```

### **Anthropic Claude**
```python
API_KEY = "sk-ant-..."  # Sua chave Anthropic
API_ENDPOINT = "https://api.anthropic.com/v1/messages"
API_MODEL = "claude-3-sonnet-20240229"
```

### **Google AI Studio (Gemini)**
```python
API_KEY = "AIza..."  # Sua chave Gemini
API_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models"
API_MODEL = "gemini-1.5-pro"
```

## 💡 Dicas de Uso

### **Para Melhor Resultados**
1. **Descreva claramente**: Quanto mais específico, melhor o código gerado
2. **Mencione a versão**: Especifique a versão do Minecraft desejada
3. **Use exemplos**: Cite funcionalidades que você quer implementar

### **Prompt Exemplo**
```
"Crie um plugin para Minecraft 1.20 que:
- Adiciona um comando /warp para teletransporte
- Salva localizações dos warps em arquivo
- Permissões para admins criarem warps
- Mensagens coloridas para feedback"
```

## 🎯 Resultados Esperados

Com o Polaris Alpha, você deve ver:

### ✅ **Logs Positivos**
```
🚀 Chamando API OpenRouter - Modelo: openrouter/polaris-alpha
🔑 API Key: sk-or-v1-2f97c...
🔍 Estrutura completa da resposta API OpenRouter:
📄 Resposta da IA (limpa): {"main_class": "..."...
✅ JSON parseado com sucesso!
```

### ✅ **Geração Rápida**
- Plugin gerado em 10-30 segundos
- Código Java bem estruturado
- plugin.yml correto
- Arquivo .jar baixável

## 📞 Troubleshooting

### Problema: "Unauthorized"
**Solução**: Verifique se a API key do OpenRouter está correta

### Problema: "Model not found"
**Solução**: O modelo Polaris Alpha pode estar temporariamente indisponível - use Gemini como alternativa

### Problema: Resposta inválida
**Solução**: Execute `python test_openrouter.py` para diagnóstico completo

---

**Status**: ✅ **MIGRAÇÃO CONCLUÍDA**
**Data**: 2025-11-13  
**API Ativa**: OpenRouter Polaris Alpha  
**Arquivo**: test_openrouter.py para testes

🎉 **Aproveite o poder gratuito do Polaris Alpha!**