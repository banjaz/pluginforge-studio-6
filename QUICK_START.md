# 🚀 GUIA RÁPIDO DE INÍCIO

> **💡 DICA:** Agora compatível com **Google AI Studio (Gemini)** - **GRATUITO** até 15 requisições por minuto!

## ⚡ Início Rápido (3 passos)

### 1️⃣ Instale as Dependências

**Windows:**
```cmd
setup.bat
```

**Linux/macOS:**
```bash
bash setup.sh
```

### 2️⃣ Configure a API Key

**Opção 1: Google AI Studio (Recomendado) - ✅ GRATUITO**

1. Acesse [aistudio.google.com](https://aistudio.google.com/)
2. Faça login com Google
3. Clique "Get API key" → "Create API key"
4. Copie a chave (começa com `AIza...`)

Edite `app.py` (linha 24):
```python
API_KEY = "AIza-sua-chave-real-aqui"  # Substitua por sua chave Google AI
```

**Opção 2: OpenAI (Pago)**

Obtenha sua chave em: https://platform.openai.com/api-keys

Edite `app.py` (linha 24):
```python
API_KEY = "sk-sua-chave-openai-aqui"
API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
API_MODEL = "gpt-4"
```

### 3️⃣ Inicie o Servidor

**Windows:**
```cmd
start.bat
```

**Linux/macOS:**
```bash
bash start.sh
```

Ou simplesmente:
```bash
python app.py
```

### 4️⃣ Acesse no Navegador

Abra: **http://localhost:5000**

---

## 📋 Pré-requisitos Necessários

Antes de executar o setup, certifique-se de ter instalado:

- ✅ **Python 3.8+** → [python.org](https://python.org)
- ✅ **Java JDK 17+** → [adoptium.net](https://adoptium.net)
- ✅ **Apache Maven** → [maven.apache.org](https://maven.apache.org)

**Verificar instalações:**
```bash
python --version
java -version
mvn --version
```

---

## 💡 Exemplo de Uso

1. Preencha o formulário:
   - **Nome:** `SuperJump`
   - **Versão:** `1.0.0`
   - **Minecraft:** `1.20.1`
   - **Descrição:** 
     ```
     Crie um plugin que adiciona o comando /superjump.
     Quando usado, o jogador pula 15 blocos de altura.
     Cooldown de 30 segundos. Mensagem de cooldown em vermelho.
     Permissão: superjump.use
     ```

2. Clique em **"Gerar Plugin"**

3. Aguarde a compilação (15-30 segundos)

4. Baixe o arquivo `.jar` gerado

5. Coloque na pasta `plugins/` do seu servidor Minecraft

6. Reinicie o servidor e teste!

---

## 🆘 Problemas Comuns

### "Maven não encontrado"
→ Instale Maven e adicione ao PATH do sistema

### "Erro na API"
→ Verifique se configurou a API_KEY corretamente

### "Erro na compilação"
→ Verifique se Java 17+ está instalado

### "Plugin não funciona"
→ Verifique a versão do Minecraft selecionada

---

## 📚 Documentação Completa

Veja o arquivo **README.md** para instruções detalhadas.

---

**Desenvolvido com ❤️ | PluginForge Studio 2025**
