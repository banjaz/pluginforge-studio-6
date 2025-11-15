# 🔄 ATUALIZAÇÃO: Google AI Studio (Gemini)

## 📋 Resumo das Alterações

O PluginForge Studio foi atualizado para usar **Google AI Studio (Gemini)** como API padrão, oferecendo uma solução **GRATUITA** e **poderosa** para geração de plugins.

---

## ✅ O que foi modificado

### 1. **Backend (app.py)**
- ✅ Endpoint alterado para `https://generativelanguage.googleapis.com/v1beta/models`
- ✅ Modelo padrão: `gemini-1.5-pro`
- ✅ Formato de requisição atualizado para Google AI Studio
- ✅ Headers e payload adaptados para Gemini API
- ✅ Tratamento de resposta ajustado

### 2. **Documentação (README.md)**
- ✅ Seção "Configuração da API" completamente reescrita
- ✅ Google AI Studio como primeira opção (recomendado)
- ✅ Instruções passo a passo para obter API key
- ✅ Comparação entre modelos (gemini-1.5-pro vs gemini-1.5-flash)
- ✅ Troubleshooting atualizado para ambos os serviços

### 3. **Guia Rápido (QUICK_START.md)**
- ✅ Google AI Studio como opção principal
- ✅ Ênfase na gratuidade (até 15 req/min)
- ✅ Instruções simplificadas

### 4. **Novo arquivo: GOOGLE_AI_SETUP.md**
- ✅ Guia completo específico para Google AI Studio
- ✅ Passo a passo detalhado
- ✅ Comparação de modelos
- ✅ Dicas para melhores resultados
- ✅ Troubleshooting específico

---

## 🚀 Benefícios da Mudança

### ✅ **Google AI Studio (Gemini)**
- **💰 GRATUITO:** Até 15 requisições por minuto
- **⚡ PODEROSO:** Gemini 1.5 Pro gera código de alta qualidade
- **🎯 SEM CARTÃO:** Não requer cartão de crédito
- **🔑 FÁCIL:** Chave API simples de obter
- **🌐 ACCESSÍVEL:** Disponível globalmente

### ⚠️ **OpenAI (anterior)**
- **💳 CUSTO:** Requer pagamento por uso
- **⏰ RATE LIMITS:** Limites mais restritivos
- **📋 CARTÃO:** Necessário cadastrar cartão

---

## 🔧 Como Usar (3 passos)

### 1️⃣ Obtenha API Key
- Acesse: [aistudio.google.com](https://aistudio.google.com/)
- Login com Google
- Clique "Get API key" → "Create API key"
- Copie a chave (começa com `AIza...`)

### 2️⃣ Configure no Código
```python
# Em app.py, linha 24:
API_KEY = "AIza-sua-chave-real-aqui"
API_MODEL = "gemini-1.5-pro"  # Recomendado
```

### 3️⃣ Execute
```bash
python app.py
```

---

## 📊 Modelos Disponíveis

| Modelo | Qualidade | Velocidade | Quando usar |
|--------|-----------|------------|-------------|
| **gemini-1.5-pro** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Plugins complexos |
| **gemini-1.5-flash** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Plugin simples/rápido |

---

## 🎯 Resultados Esperados

### **Exemplo de Plugin Gerado**

**Input:**
```
Nome: HealthPotion
Descrição: Plugin que adiciona comando /potion que dá poção de cura. 
Permissão: potion.use. Cooldown de 30 segundos.
```

**Output gerado pelo Gemini:**
```java
package com.pluginforge.healthpotion;

import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
// ... código completo e funcional
```

**Arquivo compilado:**
```
HealthPotion-1.0.0.jar ✅
```

---

## 🔄 Migração (se você usava OpenAI)

### **Antes (OpenAI):**
```python
API_KEY = "sk-..."
API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
API_MODEL = "gpt-4"
```

### **Depois (Gemini):**
```python
API_KEY = "AIza..."
API_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models"
API_MODEL = "gemini-1.5-pro"
```

---

## 📁 Arquivos Modificados

1. **`app.py`** - Backend Flask (configuração + API calls)
2. **`README.md`** - Documentação principal
3. **`QUICK_START.md`** - Guia rápido atualizado
4. **`GOOGLE_AI_SETUP.md`** - Novo arquivo (guia específico)

---

## 🆘 Troubleshooting Rápido

### "API Key inválida"
→ Verifique se copiou a chave completa (começa com `AIza...`)

### "Quota exceeded"
→ Aguarde alguns minutos (limite: 15 req/min gratuito)

### "Model not found"
→ Use apenas: `gemini-1.5-pro` ou `gemini-1.5-flash`

### Plugin não compila
→ Tente novamente ou use `gemini-1.5-pro` para melhor qualidade

---

## 🎉 Próximos Passos

1. ✅ Configure sua Google AI Studio API key
2. ✅ Teste com um plugin simples
3. ✅ Experimente plugins mais complexos
4. ✅ Compartilhe seus criativos!

---

**PluginForge Studio agora é 100% compatível com Google AI Studio!**

*Atualizado em: 2025-11-13*
