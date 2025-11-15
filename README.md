# 🔧 PluginForge Studio

**Gerador Automatizado de Plugins Minecraft com IA**

Uma aplicação web que permite criar plugins de Minecraft personalizados usando Inteligência Artificial. Basta descrever o que você quer, e a IA gera, compila e entrega o plugin pronto para uso!

---

## 📋 Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Instalação](#instalação)
3. [Configuração da API](#configuração-da-api)
4. [Execução](#execução)
5. [Como Usar](#como-usar)
6. [Estrutura do Projeto](#estrutura-do-projeto)
7. [Troubleshooting](#troubleshooting)
8. [Tecnologias Utilizadas](#tecnologias-utilizadas)

---

## ✅ Pré-requisitos

Antes de começar, certifique-se de ter instalado:

### 1. **Python 3.8 ou superior**

**Verificar instalação:**
```bash
python --version
# ou
python3 --version
```

**Como instalar:**
- **Windows:** Baixe em [python.org](https://www.python.org/downloads/)
- **Linux (Ubuntu/Debian):**
  ```bash
  sudo apt update
  sudo apt install python3 python3-pip
  ```
- **macOS:**
  ```bash
  brew install python3
  ```

### 2. **Apache Maven** 

O Maven é necessário para compilar os plugins Java. 

> **⚡ Dica:** O PluginForge Studio agora inclui detecção automática de Maven e fallback via Docker!

**Teste a instalação:**
```bash
# Execute o teste automático
python test_maven.py
```

**Verificar instalação manual:**
```bash
mvn --version
```

**Como instalar:**

- **Windows:**
  1. Baixe em [maven.apache.org](https://maven.apache.org/download.cgi)
  2. Extraia para `C:\Program Files\Apache\Maven`
  3. Adicione ao PATH: `C:\Program Files\Apache\Maven\bin`

- **Linux (Ubuntu/Debian):**
  ```bash
  sudo apt update
  sudo apt install maven
  ```

- **macOS:**
  ```bash
  brew install maven
  ```

**🎯 Alternativa: Docker** (caso Maven local não funcione)
```bash
# O PluginForge Studio pode usar Maven via Docker automaticamente
# Basta ter o Docker Desktop instalado
```

### 3. **Java Development Kit (JDK) 17 ou superior**

**Verificar instalação:**
```bash
java -version
javac -version
```

**Como instalar:**

- **Windows/Linux/macOS:**
  - Baixe o **OpenJDK** em [adoptium.net](https://adoptium.net/)
  - Ou use um gerenciador de pacotes:
    ```bash
    # Ubuntu/Debian
    sudo apt install openjdk-17-jdk
    
    # macOS
    brew install openjdk@17
    ```

---

## 🚀 Instalação

### Passo 1: Clone ou Baixe o Projeto

```bash
# Se você tem o código em um repositório Git
git clone <seu-repositorio>
cd PluginForge-Studio

# Ou extraia o arquivo ZIP do projeto
```

### Passo 2: Crie um Ambiente Virtual Python (Recomendado)

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar o ambiente virtual
# Windows:
venv\Scripts\activate

# Linux/macOS:
source venv/bin/activate
```

### Passo 3: Instale as Dependências Python

```bash
pip install -r requirements.txt
```

Isso instalará:
- Flask (framework web)
- Requests (para chamadas de API)
- Outras dependências necessárias

---

## 🔑 Configuração da API

O PluginForge Studio usa uma API de IA para gerar o código dos plugins. **A configuração atual está usando OpenRouter (Polaris Alpha) que é GRATUITO!**

### 🚀 Opção 1: OpenRouter (Polaris Alpha) - ✅ PADRÃO ATUAL

**🎯 Status**: Já configurado e funcionando!
- 🆓 **100% Gratuito**: $0/M tokens
- 🧠 **256K Context**: Para plugins complexos
- 👨‍💻 **Especializado**: Otimizado para programação

**Teste a configuração atual:**
```bash
python test_openrouter.py
```

### 🔄 Alternativa 1: Google AI Studio (Gemini)

1. **Obtenha uma API Key:**
   - Acesse [aistudio.google.com](https://aistudio.google.com/)
   - Faça login e crie uma chave gratuita

2. **Configure no código (app.py):**
   ```python
   API_KEY = "AIza-sua-chave-real"
   API_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models"
   API_MODEL = "gemini-1.5-pro"
   ```

### 🔄 Alternativa 2: OpenAI (GPT-4)

1. **Obtenha uma API Key:**
   - Crie conta em [platform.openai.com](https://platform.openai.com/)
   - API key começa com `sk-...`

2. **Configure no código (app.py):**
   ```python
   API_KEY = "sk-sua-chave-openai"
   API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
   API_MODEL = "gpt-4"
   ```

### 🔄 Alternativa 3: Anthropic Claude

1. **Obtenha uma API Key:**
   - Crie conta em [console.anthropic.com](https://console.anthropic.com/)
   - API key começa com `sk-ant-...`

2. **Configure no código (app.py):**
   ```python
   API_KEY = "sk-ant-sua-chave"
   API_ENDPOINT = "https://api.anthropic.com/v1/messages"
   API_MODEL = "claude-3-sonnet-20240229"
   ```

> 📖 **Documentação completa**: Ver [MIGRACAO_OPENROUTER.md](MIGRACAO_OPENROUTER.md)

1. Altere as variáveis `API_ENDPOINT`, `API_KEY` e `API_MODEL` no `app.py`
2. Ajuste o formato da requisição na função `call_ai_api()` para ser compatível com sua API

---

## ▶️ Execução

### Passo 1: Inicie o Servidor Flask

```bash
python app.py
```

**Saída esperada:**
```
🚀 PluginForge Studio iniciado!
📍 Acesse: http://localhost:5000
⚙️  Certifique-se de configurar a API_KEY no código!
 * Running on http://0.0.0.0:5000
```

### Passo 2: Acesse no Navegador

Abra seu navegador e vá para:
```
http://localhost:5000
```

---

## 🎯 Como Usar

### 1. Preencha o Formulário

Na página principal, você verá um formulário com os seguintes campos:

- **Nome do Plugin:** Ex: `SuperHarvest`, `MegaJump`, `AutoCraft`
  - Sem espaços, use CamelCase
  
- **Versão do Plugin:** Ex: `1.0.0`
  - Formato: `major.minor.patch`
  
- **Versão do Minecraft:** Escolha de 1.16.5 até 1.20.1
  - Selecione a versão compatível com seu servidor
  
- **Descrição do Plugin:** Seja o mais detalhado possível!
  - Descreva comandos, eventos, mecânicas, mensagens
  - Exemplo:
    ```
    Crie um plugin que adiciona o comando /megajump. 
    Quando usado, o jogador pula 10 blocos de altura. 
    Só pode ser usado a cada 30 segundos. 
    Mostre uma mensagem de cooldown em vermelho quando 
    o jogador tentar usar antes do tempo.
    ```

### 2. Clique em "Gerar Plugin"

- O sistema mostrará uma animação de loading
- Você verá o progresso em 4 etapas:
  1. 🤖 Gerando código com IA
  2. 📁 Criando estrutura do projeto
  3. 🔨 Compilando com Maven
  4. ✅ Finalizando...

### 3. Baixe o Plugin

- Quando concluído, o download iniciará automaticamente
- Você receberá um arquivo `.jar` pronto para usar
- Coloque o arquivo na pasta `plugins/` do seu servidor Minecraft

### 4. Teste no Servidor

⚠️ **IMPORTANTE:** Sempre teste plugins em servidores de desenvolvimento antes de usar em produção!

---

## 📁 Estrutura do Projeto

```
PluginForge-Studio/
│
├── app.py                      # Backend Flask (servidor principal)
├── requirements.txt            # Dependências Python
├── pom.xml                    # Template Maven para compilação
├── README.md                  # Este arquivo
│
├── templates/
│   └── index.html             # Interface do usuário
│
├── static/
│   ├── style.css              # Estilos CSS
│   └── script.js              # Lógica JavaScript
│
└── workspace/                 # Diretório de projetos temporários (gerado automaticamente)
    └── [plugins compilados]
```

---

## 🔧 Troubleshooting

### 🆕 Problema: "Maven não encontrado" 

**Erro:**
```
Maven não está instalado ou não está no PATH
```

**Soluções Automáticas:**
1. **Execute o teste automático:**
   ```bash
   python test_maven.py
   ```

2. **O PluginForge Studio agora:**
   - ✅ Procura Maven em múltiplas localizações
   - ✅ Usa Docker Maven como fallback automático
   - ✅ Fornece diagnóstico detalhado

**Soluções Manuais:**
1. **Verifique instalação:** `mvn --version`
2. **Instale Maven:** Siga as [instruções de instalação](#2-apache-maven)
3. **Use Docker:** Instale Docker Desktop como alternativa
4. **Reinicie terminal** após configurar PATH

> 📖 **Documentação detalhada:** Ver [MAVEN_TROUBLESHOOTING.md](MAVEN_TROUBLESHOOTING.md)

---

### 🆕 Problema: "Erro na API da IA"

**Erro:**
```
A IA não retornou um formato válido. Tente novamente.
```

**Soluções:**
1. **Configure a API key corretamente:**
   - Obtenha chave gratuita em [aistudio.google.com](https://aistudio.google.com)
   - Edite `app.py` linha 30: `API_KEY = "sua_chave_aqui"`

2. **Teste a API:**
   - Acesse: http://localhost:5000/test
   - Execute: `python test_api.py`

> 📖 **Documentação detalhada:** Ver [CORRECAO_ERRO_API.md](CORRECAO_ERRO_API.md)

---
```

**Para Google AI Studio (Gemini):**
1. Verifique se configurou a `API_KEY` corretamente no `app.py`
2. Teste sua chave em [aistudio.google.com](https://aistudio.google.com/)
3. Verifique se não excedeu o limite de 15 req/min (gratuito)
4. Confirme que o modelo (`gemini-1.5-pro` ou `gemini-1.5-flash`) está correto

**Para OpenAI:**
1. Verifique se configurou a `API_KEY` corretamente no `app.py`
2. Teste sua chave em [platform.openai.com](https://platform.openai.com/)
3. Verifique se tem créditos disponíveis na conta
4. Confira se o modelo (`gpt-4`) está disponível para sua conta

**Para qualquer API:**
- Verifique os logs do console Flask para detalhes do erro
- Confirme que a API key não contém espaços extras

---

### Problema: "Erro na compilação"

**Erro:**
```
Erro na compilação: [detalhes]
```

**Soluções:**
1. Verifique se o Java 17+ está instalado: `java -version`
2. Limpe o cache do Maven: `mvn clean`
3. Verifique sua conexão com a internet (Maven baixa dependências)
4. Tente novamente - a IA pode ter gerado código com erro

---

### Problema: "Porta 5000 já em uso"

**Erro:**
```
Address already in use
```

**Solução:**
1. Mude a porta no final do arquivo `app.py`:
   ```python
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```
2. Acesse em `http://localhost:5001`

---

### Problema: Plugin não funciona no servidor

**Possíveis causas:**
1. **Versão incompatível:** Certifique-se de que a versão do Minecraft selecionada corresponde ao seu servidor
2. **Código gerado incorreto:** A IA pode ter cometido um erro. Tente gerar novamente com uma descrição mais clara
3. **Dependências faltando:** Alguns plugins complexos podem precisar de bibliotecas adicionais

**Como debugar:**
1. Coloque o `.jar` na pasta `plugins/` do servidor
2. Inicie o servidor e veja o console
3. Procure por erros relacionados ao seu plugin
4. Se houver erros, tente gerar novamente com uma descrição mais simples

---

## 🛠️ Tecnologias Utilizadas

### Frontend
- **HTML5:** Estrutura da página
- **CSS3:** Estilização moderna e responsiva
- **JavaScript (Vanilla):** Interatividade e AJAX

### Backend
- **Python 3.8+:** Linguagem de programação
- **Flask:** Framework web minimalista
- **Requests:** Chamadas HTTP para APIs

### Compilação
- **Apache Maven:** Build automation para Java
- **Spigot API:** API para desenvolvimento de plugins Minecraft

### IA
- **Google AI Studio (Gemini 1.5 Pro/Flash)** - ⭐ **RECOMENDADO** (Gratuito)
- **OpenAI GPT-4** (configurável)
- **Outras APIs** (configuráveis)

---

## 📝 Notas Importantes

1. **Google AI Studio:** ⭐ **RECOMENDADO** - Gratuito até 15 requisições por minuto, sem necessidade de cartão de crédito
2. **OpenAI:** Tem custo por requisição. Monitore seu uso em [platform.openai.com/usage](https://platform.openai.com/usage)

2. **Qualidade dos Plugins:** A qualidade depende da descrição fornecida. Quanto mais detalhada, melhor o resultado.

3. **Segurança:** Sempre teste plugins em servidores de desenvolvimento antes de usar em produção.

4. **Limitações:** Plugins muito complexos podem não funcionar perfeitamente na primeira tentativa. Tente simplificar a descrição.

---

## 📞 Suporte

Se encontrar problemas:
1. Verifique a seção [Troubleshooting](#troubleshooting)
2. Revise se seguiu todos os passos de instalação
3. Verifique os logs do console do Flask para mais detalhes

---

## 📄 Licença

Este projeto é de código aberto. Use e modifique como desejar!

---

## 🎉 Divirta-se criando plugins incríveis!

Desenvolvido com ❤️ | PluginForge Studio 2025
