@echo off
REM ========================================
REM PLUGINFORGE STUDIO - INICIALIZACAO (WINDOWS)
REM ========================================

echo ========================================
echo Iniciando PluginForge Studio...
echo ========================================
echo.

REM Ativa ambiente virtual se existir
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo OK: Ambiente virtual ativado
    echo.
) else (
    echo AVISO: Ambiente virtual nao encontrado. Execute setup.bat primeiro.
    echo.
)

REM Inicia o servidor
echo Iniciando servidor Flask...
echo Acesse: http://localhost:5000
echo.
echo Pressione Ctrl+C para parar o servidor
echo ========================================
echo.
python app.py
