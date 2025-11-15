#!/bin/bash
# ========================================
# PLUGINFORGE STUDIO - SCRIPT DE INICIALIZAÇÃO
# ========================================
# Inicia o servidor Flask
# ========================================

echo "🚀 Iniciando PluginForge Studio..."
echo ""

# Ativa ambiente virtual se existir
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Ambiente virtual ativado"
else
    echo "⚠️  Ambiente virtual não encontrado. Execute ./setup.sh primeiro."
fi

# Inicia o servidor
echo "🌐 Iniciando servidor Flask..."
echo "📍 Acesse: http://localhost:5000"
echo ""
python app.py
