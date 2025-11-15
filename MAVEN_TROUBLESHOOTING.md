# 🔧 Solução Completa para Erro "Maven não está instalado ou não está no PATH"

## 📋 Problema

O erro **"Maven não está instalado ou não está no PATH"** ocorre quando o PluginForge Studio não consegue encontrar o executável Maven durante a compilação do plugin.

## 🔍 Causas Comuns

1. **Maven não está no PATH**: O Maven está instalado mas não está acessível globalmente
2. **Instalação incompleta**: Maven foi baixado mas não configurado corretamente
3. **PATH diferente**: O processo Python tem um ambiente diferente do terminal
4. **Java não encontrado**: Maven precisa do Java para funcionar

## ✅ Soluções Implementadas

### 🆕 Melhorias Automáticas no Código

1. **Busca multi-local**: Procura Maven em múltiplas localizações comuns
2. **Fallback Docker**: Usa Maven via Docker como alternativa
3. **Diagnóstico melhorado**: Logs detalhados para identificar o problema
4. **Testes de ambiente**: Verifica Java e configuração do PATH

### 📍 Localizações Testadas Automáticamente

```python
maven_commands = [
    'mvn',                                    # PATH padrão
    '/usr/local/bin/mvn',                     # Homebrew (macOS)
    '/opt/homebrew/bin/mvn',                  # Homebrew ARM (macOS)
    '/usr/bin/mvn',                           # APT (Linux)
    '/opt/maven/bin/mvn',                     # Maven manual (Linux)
    '/snap/bin/mvn',                          # Snap (Linux)
    '/home/user/maven/bin/mvn',               # Maven instalado em home
]
```

## 🧪 Teste e Diagnóstico

### Passo 1: Execute o Teste Automático
```bash
python test_maven.py
```

Este script irá:
- ✅ Verificar se Maven está funcionando
- ✅ Testar múltiplas localizações do Maven
- ✅ Verificar se Java está instalado
- ✅ Testar Maven via Docker como alternativa
- ✅ Fornecer soluções específicas para seu sistema

### Passo 2: Verifique o Sistema

**macOS (Homebrew):**
```bash
# Verifica se está no PATH
which mvn

# Se não estiver, adiciona ao PATH
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**Linux (APT):**
```bash
# Instala Maven
sudo apt update
sudo apt install maven

# Verifica instalação
mvn --version
```

**Windows:**
```bash
# Baixe Maven de: https://maven.apache.org/download.cgi
# Adicione ao PATH do sistema
# Verifique em: Painel Controle > Sistema > Configurações Avançadas > Variáveis de Ambiente
```

### Passo 3: Teste Docker (Alternativa)

Se o Maven local não funcionar, o PluginForge Studio usará Docker automaticamente:

```bash
# Instale o Docker Desktop
# O script testará automaticamente
```

## 🚀 Como Usar o PluginForge Studio

### ✅ Com Maven Local Funcionando
1. Execute: `python app.py`
2. Acesse: http://localhost:5000
3. Preencha o formulário
4. O plugin será compilado localmente

### 🐳 Com Docker (Fallback)
1. Execute: `python app.py`
2. O sistema detectará que precisa do Docker
3. Usará Maven via Docker automaticamente
4. **Nota**: É mais lento, mas funciona!

## 🆘 Troubleshooting Avançado

### Problema: "Java não encontrado"
```bash
# Verifica Java
java --version

# Instala OpenJDK (macOS)
brew install openjdk@17

# Instala OpenJDK (Ubuntu)
sudo apt install openjdk-17-jdk

# Adiciona Java ao PATH
echo 'export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"' >> ~/.zshrc
```

### Problema: "Permissão negada"
```bash
# Torna Maven executável (Linux/macOS)
chmod +x $(which mvn)

# Ou no diretório específico
sudo chmod +x /usr/local/bin/mvn
```

### Problema: "Maven parece estar quebrado"
```bash# Reinstala Maven completamente
# Remove instalação atual
rm -rf ~/.m2

# Reinstalar
# macOS: brew reinstall maven
# Ubuntu: sudo apt remove maven && sudo apt install maven
```

## 📋 Checklist de Verificação

### ✅ Sistema Básico
- [ ] Java 8+ instalado (`java --version`)
- [ ] Maven instalado (`mvn --version`)
- [ ] Maven no PATH (`which mvn`)
- [ ] Conexão com internet (para dependências)

### ✅ PluginForge Studio
- [ ] Execute `python test_maven.py` sem erros
- [ ] Servidor inicia sem erros (`python app.py`)
- [ ] Página web carrega (http://localhost:5000)

### ✅ Teste de Geração
- [ ] Formulário aceita dados
- [ ] Geração inicia sem erros
- [ ] Download do .jar funciona

## 🎯 Resultado Esperado

Após seguir estas instruções, você deve ver:

```
🚀 PluginForge Studio iniciado!
📍 Acesse: http://localhost:5000
✅ Maven encontrado: /usr/local/bin/mvn
🔨 Compilando com Maven: /usr/local/bin/mvn
✅ Compilação Maven concluída com sucesso!
```

## 📞 Suporte

Se o problema persistir:

1. **Execute o teste completo**: `python test_maven.py`
2. **Verifique os logs** no terminal quando iniciar o servidor
3. **Instale Maven ou Docker** conforme indicado pelo teste
4. **Reinicie o terminal** após configurar variáveis de ambiente

---

**Status**: ✅ Soluções implementadas e testadas  
**Data**: 2025-11-13  
**Versão**: PluginForge Studio v1.2