# 🤖 Configuração do Google AI Studio (Gemini)

## ✅ Por que Google AI Studio?

- **✅ GRATUITO:** Até 15 requisições por minuto
- **✅ PODEROSO:** Gemini 1.5 Pro oferece código de alta qualidade
- **✅ RÁPIDO:** Resposta em poucos segundos
- **✅ SEM CARTÃO:** Não precisa de cartão de crédito

---

## 🚀 Passo a Passo

### 1. Obtenha sua API Key

1. **Acesse:** [aistudio.google.com](https://aistudio.google.com/)
2. **Login:** Use sua conta Google
3. **Create API Key:**
   - Clique em "Get API key" 
   - Clique em "Create API key"
   - Escolha um projeto (ou crie um novo)
   - Clique "Create API key in new project" (recomendado)

4. **Copie a chave:**
   - A chave começa com `AIza...`
   - **IMPORTANTE:** Guarde em lugar seguro!

### 2. Configure no PluginForge Studio

1. **Abra o arquivo:** `app.py`
2. **Localize a linha 24:**
   ```python
   API_KEY = "SUA_CHAVE_API_AQUI"
   ```
3. **Substitua por:**
   ```python
   API_KEY = "AIza-sua-chave-real-aqui"
   ```

### 3. Escolha o Modelo

No mesmo arquivo `app.py`, linha 33:

**Para maior qualidade (recomendado):**
```python
API_MODEL = "gemini-1.5-pro"
```

**Para velocidade:**
```python
API_MODEL = "gemini-1.5-flash"
```

---

## 📊 Comparação de Modelos

| Modelo | Qualidade | Velocidade | Custo | Uso Recomendado |
|--------|-----------|------------|-------|-----------------|
| **gemini-1.5-pro** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Gratuito | Plugin complexo |
| **gemini-1.5-flash** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Gratuito | Plugin simples |
| **gemini-1.0-pro** | ⭐⭐⭐ | ⭐⭐⭐⭐ | Gratuito | Uso geral |

---

## 🧪 Teste Rápido

1. **Inicie o servidor:**
   ```bash
   python app.py
   ```

2. **Acesse:** http://localhost:5000

3. **Teste com este exemplo:**
   - **Nome:** `TestPlugin`
   - **Descrição:** `Crie um plugin simples com comando /hello que mostra "Olá mundo!"`

4. **Se funcionar:** 🎉 Configuração correta!

---

## 🔧 Troubleshooting

### Erro: "API Key inválida"

**Solução:**
1. Verifique se copiou a chave completa
2. Confirme que não há espaços extras
3. Gere uma nova API key se necessário

### Erro: "Quota exceeded"

**Solução:**
1. Aguarde alguns minutos
2. Google AI Studio: 15 req/min gratuito
3. Considere usar `gemini-1.5-flash` para ser mais econômico

### Erro: "Model not found"

**Solução:**
1. Verifique o nome do modelo em `API_MODEL`
2. Use apenas: `gemini-1.5-pro`, `gemini-1.5-flash`, `gemini-1.0-pro`

### Plugin gerado não compila

**Possíveis causas:**
1. IA gerou código com erro
2. Tente novamente com descrição mais simples
3. Use modelo `gemini-1.5-pro` para melhor qualidade

---

## 💡 Dicas para Melhores Resultados

### ✅ Descrições Eficazes

**Bom:**
```
Crie um plugin com comando /heal que cura o jogador.
Permissão: heal.use
Cooldown: 60 segundos
Mensagem: "Você foi curado!" em verde
```

**Ruim:**
```
Plugin de cura
```

### ✅ Modelos por Tipo de Plugin

**Plugin Simples** (comandos básicos):
```
API_MODEL = "gemini-1.5-flash"
```

**Plugin Complexo** (múltiplos recursos):
```
API_MODEL = "gemini-1.5-pro"
```

**Plugin de Emergência** (precisa ser rápido):
```
API_MODEL = "gemini-1.5-flash"
```

---

## 📞 Suporte

Se tiver problemas:
1. Verifique se copiou a API key corretamente
2. Teste a API key no site do Google AI Studio
3. Consulte o README.md principal para troubleshooting geral

---

## 🎯 Próximos Passos

1. ✅ Configure a API key
2. ✅ Teste com plugin simples
3. ✅ Experimente plugins mais complexos
4. ✅ Compartilhe seus plugins criados!

---

**Desenvolvido com ❤️ para a comunidade Minecraft**
