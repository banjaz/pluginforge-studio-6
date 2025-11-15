@echo off
REM ========================================
REM PLUGINFORGE STUDIO - CONFIGURAÇÃO INICIAL (WINDOWS)
REM ========================================

echo ========================================
echo PluginForge Studio - Configuracao Inicial
echo ========================================
echo.

REM Verifica Python
echo Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Python nao encontrado. Instale Python 3.8 ou superior.
    pause
    exit /b 1
)
echo OK: Python encontrado
echo.

REM Verifica Maven
echo Verificando Maven...
mvn --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Maven nao encontrado. Instale Apache Maven.
    pause
    exit /b 1
)
echo OK: Maven encontrado
echo.

REM Verifica Java
echo Verificando Java...
java -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Java nao encontrado. Instale JDK 17 ou superior.
    pause
    exit /b 1
)
echo OK: Java encontrado
echo.

REM Cria ambiente virtual
echo Criando ambiente virtual Python...
if not exist "venv\" (
    python -m venv venv
    echo OK: Ambiente virtual criado
) else (
    echo AVISO: Ambiente virtual ja existe
)
echo.

REM Ativa ambiente virtual
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat
echo OK: Ambiente virtual ativado
echo.

REM Instala dependências
echo Instalando dependencias Python...
pip install -r requirements.txt --quiet
echo OK: Dependencias instaladas
echo.

REM Verifica API Key
echo Verificando configuracao da API...
findstr /C:"SUA_CHAVE_API_AQUI" app.py >nul 2>&1
if %errorlevel% equ 0 (
    echo ATENCAO: Voce precisa configurar sua API key!
    echo    Edite o arquivo app.py e substitua 'SUA_CHAVE_API_AQUI' pela sua chave real.
    echo.
) else (
    echo OK: API key configurada
    echo.
)

REM Finalização
echo ========================================
echo Configuracao concluida!
echo.
echo Para iniciar o servidor:
echo    python app.py
echo.
echo Ou use o script de inicializacao:
echo    start.bat
echo ========================================
pause
