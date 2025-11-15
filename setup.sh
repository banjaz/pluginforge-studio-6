#!/bin/bash
# ========================================
# PLUGINFORGE STUDIO - SCRIPT DE INICIALIZAÇÃO
# ========================================
# Este script automatiza a configuração inicial
# ========================================

echo "🚀 PluginForge Studio - Configuração Inicial"
echo "============================================="
echo ""

# Verifica Python
echo "📍 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.8 ou superior."
    exit 1
fi
echo "✅ Python $(python3 --version) encontrado"
echo ""

# Verifica Maven
echo "📍 Verificando Maven..."
if ! command -v mvn &> /dev/null; then
    echo "❌ Maven não encontrado. Por favor, instale Apache Maven."
    exit 1
fi
echo "✅ Maven $(mvn --version | head -n 1) encontrado"
echo ""

# Verifica Java
echo "📍 Verificando Java..."
if ! command -v java &> /dev/null; then
    echo "❌ Java não encontrado. Por favor, instale JDK 17 ou superior."
    exit 1
fi
echo "✅ Java $(java -version 2>&1 | head -n 1) encontrado"
echo ""

# Cria ambiente virtual
echo "📦 Criando ambiente virtual Python..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Ambiente virtual criado"
else
    echo "⚠️  Ambiente virtual já existe"
fi
echo ""

# Ativa ambiente virtual
echo "🔌 Ativando ambiente virtual..."
source venv/bin/activate
echo "✅ Ambiente virtual ativado"
echo ""

# Instala dependências
echo "📥 Instalando dependências Python..."
pip install -r requirements.txt --quiet
echo "✅ Dependências instaladas"
echo ""

# Verifica API Key
echo "🔑 Verificando configuração da API..."
if grep -q "SUA_CHAVE_API_AQUI" app.py; then
    echo "⚠️  ATENÇÃO: Você precisa configurar sua API key!"
    echo "   Edite o arquivo app.py e substitua 'SUA_CHAVE_API_AQUI' pela sua chave real."
    echo ""
else
    echo "✅ API key configurada"
    echo ""
fi

# Finalização
echo "============================================="
echo "✅ Configuração concluída!"
echo ""
echo "Para iniciar o servidor:"
echo "  python app.py"
echo ""
echo "Ou use o script de inicialização:"
echo "  ./start.sh"
echo "============================================="
