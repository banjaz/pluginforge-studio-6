# ========================================
# PLUGINFORGE STUDIO - BACKEND FLASK COMPLETO
# ========================================
# Sistema completo com:
# - Autenticação de usuários
# - Banco de dados SQLite (local) / PostgreSQL (produção)
# - Chat por plugin
# - Histórico de plugins
# - Sistema de upgrades
# ========================================

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, session, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
import shutil
import subprocess
import uuid
import json

# Carregar variáveis de ambiente
load_dotenv()
import requests
from datetime import datetime, UTC
from pathlib import Path

# Importa os modelos
from models import db, User, Plugin, Chat, Message, PluginVersion, init_db

# Inicializa a aplicação Flask
app = Flask(__name__)

# ========================================
# CONFIGURAÇÕES
# ========================================

# Detect environment (Render sets RENDER=true)
IS_PRODUCTION = os.getenv('RENDER') == 'true'

# Database configuration
if IS_PRODUCTION:
    # Use PostgreSQL on Render
    DATABASE_URL = os.getenv('DATABASE_URL', '')
    # Render uses postgres:// but SQLAlchemy needs postgresql://
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    print(f"🚀 Production mode: Using PostgreSQL")
else:
    # Use SQLite locally
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pluginforge.db'
    print(f"💻 Development mode: Using SQLite")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Secret key for sessions (use environment variable in production)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'pluginforge-secret-key-2024')

# Configuração da autenticação
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Faça login para acessar esta página.'

# API Configuration (use environment variable in production)
API_KEY = os.getenv('OPENROUTER_API_KEY', "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")
API_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
API_MODEL = "kwaipilot/kat-coder-pro:free"  # Modelo válido da OpenRouter

# Diretório base para projetos temporários
WORKSPACE_DIR = Path(__file__).parent / "workspace"
WORKSPACE_DIR.mkdir(exist_ok=True)

# ========================================
# CUSTOM JINJA2 FILTERS
# ========================================

@app.template_filter('nl2br')
def nl2br_filter(text):
    """Convert newlines to HTML breaks"""
    if text is None:
        return ''
    return text.replace('\n', '<br>')

# ========================================
# AUTENTICAÇÃO
# ========================================

@login_manager.user_loader
def load_user(user_id):
    """Carregar usuário por ID"""
    # Método compatível com SQLAlchemy 1.x e 2.x
    try:
        # Tenta usar o método mais novo (SQLAlchemy 2.x)
        # User model uses UUID string as primary key, not integer
        return db.session.get(User, user_id)
    except AttributeError:
        # Fallback para método antigo (SQLAlchemy 1.x)
        return User.query.get(user_id)

# ========================================
# ROTAS DE AUTENTICAÇÃO
# ========================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username', '')
        password = data.get('password', '')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return jsonify({
                'success': True,
                'message': 'Login realizado com sucesso!',
                'redirect': '/dashboard'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Usuário ou senha incorretos.'
            }), 401
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Página de registro"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username', '')
        email = data.get('email', '')
        password = data.get('password', '')
        
        # Validações
        if not username or not email or not password:
            return jsonify({
                'success': False,
                'error': 'Todos os campos são obrigatórios.'
            }), 400
        
        if User.query.filter_by(username=username).first():
            return jsonify({
                'success': False,
                'error': 'Nome de usuário já existe.'
            }), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({
                'success': False,
                'error': 'E-mail já está cadastrado.'
            }), 400
        
        # Cria novo usuário
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        
        return jsonify({
            'success': True,
            'message': 'Conta criada com sucesso!',
            'redirect': '/dashboard'
        })
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    """Fazer logout"""
    logout_user()
    return redirect(url_for('login'))

# ========================================
# ROTAS PRINCIPAIS
# ========================================

@app.route('/')
def index():
    """Página inicial - redireciona para login se não autenticado"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard do usuário com lista de plugins"""
    user_plugins = Plugin.query.filter_by(user_id=current_user.id).order_by(Plugin.updated_at.desc()).all()
    return render_template('dashboard.html', plugins=user_plugins, current_plugin_id=None)

@app.route('/plugin/new')
@login_required
def new_plugin():
    """Página para criar novo plugin"""
    return render_template('new_plugin.html')

@app.route('/plans')
@login_required
def plans():
    """Página de planos de assinatura"""
    return render_template('plans.html', current_plugin_id=None)

@app.route('/profile')
@login_required
def profile():
    """PROFILE UPGRADE: Dedicated profile page with settings"""
    section = request.args.get('section', 'profile')
    return render_template('profile.html', section=section, current_plugin_id=None)

@app.route('/plugin/<plugin_id>')
@login_required
def plugin_detail(plugin_id):
    """Página de detalhes do plugin com chat"""
    plugin = Plugin.query.filter_by(id=plugin_id, user_id=current_user.id).first_or_404()
    
    # Pega ou cria um chat ativo
    chat = Chat.query.filter_by(plugin_id=plugin_id, is_active=True).first()
    if not chat:
        chat = Chat(plugin_id=plugin_id, title='Nova Conversa')
        db.session.add(chat)
        db.session.commit()
    
    messages = Message.query.filter_by(chat_id=chat.id).order_by(Message.created_at.asc()).all()
    
    return render_template('plugin_chat.html', plugin=plugin, chat=chat, messages=messages, current_plugin_id=plugin_id)

# ========================================
# FUNÇÕES DE VALIDAÇÃO
# ========================================

def validate_java_syntax(java_code):
    """Valida sintaxe básica do código Java"""
    errors = []
    
    # Verificar strings não fechadas
    in_string = False
    escape_next = False
    line_num = 1
    
    for i, char in enumerate(java_code):
        if char == '\n':
            line_num += 1
            
        if escape_next:
            escape_next = False
            continue
            
        if char == '\\':
            escape_next = True
            continue
            
        if char == '"' and not escape_next:
            in_string = not in_string
    
    if in_string:
        errors.append(f"String literal não fechada na linha {line_num}")
    
    # Verificar chaves balanceadas
    brace_count = 0
    paren_count = 0
    bracket_count = 0
    
    for line in java_code.split('\n'):
        # Contar caracteres (ignorando strings)
        in_string_line = False
        escape_next_line = False
        
        for char in line:
            if escape_next_line:
                escape_next_line = False
                continue
                
            if char == '\\':
                escape_next_line = True
                continue
                
            if char == '"':
                in_string_line = not in_string_line
                continue
                
            if not in_string_line:
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                elif char == '(':
                    paren_count += 1
                elif char == ')':
                    paren_count -= 1
                elif char == '[':
                    bracket_count += 1
                elif char == ']':
                    bracket_count -= 1
    
    if brace_count != 0:
        errors.append(f"Chaves não balanceadas: {brace_count} {'excesso' if brace_count > 0 else 'faltando'}")
    
    if paren_count != 0:
        errors.append(f"Parênteses não balanceados: {paren_count} {'excesso' if paren_count > 0 else 'faltando'}")
    
    if bracket_count != 0:
        errors.append(f"Colchetes não balanceados: {bracket_count} {'excesso' if bracket_count > 0 else 'faltando'}")
    
    return errors

# ========================================
# ROTAS DE API
# ========================================

@app.route('/api/generate', methods=['POST'])
@login_required
def generate_plugin():
    """Gerar novo plugin com IA"""
    try:
        print("🔄 Iniciando geração de plugin...")
        data = request.get_json()
        
        if not data:
            print("❌ Dados JSON não fornecidos")
            return jsonify({
                'success': False,
                'error': 'Dados não fornecidos no formato JSON.'
            }), 400
        
        plugin_name = data.get('pluginName', 'MyPlugin').replace(" ", "")
        mc_version = data.get('mcVersion', '1.20.1')
        description = data.get('description', '')
        plugin_version = data.get('pluginVersion', '1.0.0')
        features = data.get('features', '')
        
        print(f"📝 Dados recebidos:")
        print(f"   - Plugin Name: {plugin_name}")
        print(f"   - MC Version: {mc_version}")
        print(f"   - Description: {description[:50]}...")
        print(f"   - Version: {plugin_version}")
        print(f"   - Features: {features[:50]}...")
        
        if not description.strip():
            print("❌ Descrição vazia")
            return jsonify({
                'success': False,
                'error': 'Descrição do plugin não pode estar vazia.'
            }), 400

        # Construir prompt para IA
        full_description = f"{description}\n\nFuncionalidades: {features}" if features else description
        
        prompt = f"""Você é o PluginCraft AI, especialista em desenvolvimento de plugins para Minecraft Spigot.

Tarefa: Gere um plugin completo para Minecraft {mc_version} com base na seguinte descrição:

NOME DO PLUGIN: {plugin_name}
VERSÃO: {plugin_version}
DESCRIÇÃO: {full_description}

INSTRUÇÕES CRÍTICAS DE SINTAXE JAVA:
1. **OBRIGATÓRIO**: Todas as strings devem ter aspas DUPLAS de abertura e fechamento (")
2. **OBRIGATÓRIO**: Escape todas as aspas duplas dentro de strings com \\"
3. **OBRIGATÓRIO**: Strings com múltiplas linhas devem usar concatenação + ou \\n
4. **OBRIGATÓRIO**: Todos os parênteses, chaves e colchetes devem ser fechados
5. **OBRIGATÓRIO**: Cada linha de código deve terminar com ; (ponto e vírgula)
6. **CRITICAL**: Teste mentalmente se o código compila antes de retornar

EXEMPLO DE STRING CORRETA:
String message = "Olá mundo! Esta é uma mensagem válida.";
String complex = "Múltiplas aspas: \\"importante\\" e \\"crítico\\"";

EXEMPLO DE STRING INCORRETA (NÃO FAÇA):
String bad = "texto sem fechar
String worse = "texto com "aspas" dentro sem escape

INSTRUÇÕES DE CONTEÚDO:
- Gere o código Java completo e funcional
- Use boas práticas de programação Java
- Inclua comentários explicativos no código
- O código deve estar pronto para compilação Maven
- Use spigot-api {mc_version} importações corretas

**OBRIGATÓRIO**: Retorne APENAS o JSON válido, sem markdown, sem explicações, sem code blocks

FORMATO OBRIGATÓRIO (retorne APENAS isto, nada mais):
{{
    "main_class": "conteúdo completo da classe principal Java aqui",
    "plugin_yml": "conteúdo completo do arquivo plugin.yml aqui",
    "config_yml": "conteúdo completo do arquivo config.yml aqui (com configurações padrão do plugin)",
    "package_name": "com.pluginforge.{plugin_name.lower()}"
}}

IMPORTANTE: Retorne apenas o JSON acima, sem texto adicional, sem formatação markdown."""

        print(f"📡 Gerando plugin '{plugin_name}' para usuário {current_user.username}...")
        
        # Chamar API
        print("🤖 Chamando AI API...")
        ai_response = call_ai_api(prompt)
        
        if not ai_response:
            print("❌ API não retornou resposta")
            return jsonify({
                'success': False,
                'error': 'Falha ao gerar código com a IA. Verifique sua API key.'
            }), 500
        
        print("✅ Resposta da IA recebida")

        # Parse do JSON
        try:
            print("📋 Fazendo parse do JSON...")
            code_data = json.loads(ai_response)
            main_class_code = code_data.get('main_class', '')
            plugin_yml_code = code_data.get('plugin_yml', '')
            config_yml_code = code_data.get('config_yml', '')
            package_name = code_data.get('package_name', f'com.pluginforge.{plugin_name.lower()}')
            
            print(f"📄 Código principal: {len(main_class_code)} caracteres")
            print(f"📄 plugin.yml: {len(plugin_yml_code)} caracteres")
            print(f"📄 config.yml: {len(config_yml_code)} caracteres")
            print(f"📄 Package: {package_name}")
            
            # Se a IA não gerou config.yml, criar um padrão básico
            if not config_yml_code:
                print("📝 Gerando config.yml padrão...")
                config_yml_code = f"""# Configuração do plugin {plugin_name}
# Gerado automaticamente pelo PluginForge Studio

# Mensagens do plugin
messages:
  enabled: '&aPlugin ativado com sucesso!'
  disabled: '&cPlugin desativado!'

# Configurações gerais
settings:
  debug: false
  language: 'pt_BR'
"""
        except json.JSONDecodeError as e:
            print(f"❌ Erro no parse JSON: {e}")
            return jsonify({
                'success': False,
                'error': f'A IA não retornou um formato válido. Detalhes: {str(e)}'
            }), 500

        # Criar plugin no banco
        print("💾 Criando plugin no banco de dados...")
        plugin = Plugin(
            user_id=current_user.id,
            name=plugin_name,
            version=plugin_version,
            minecraft_version=mc_version,
            description=description,
            plugin_author=current_user.username,
            features=features,
            status='generating'
        )
        db.session.add(plugin)
        db.session.commit()
        print(f"✅ Plugin criado com ID: {plugin.id}")

        # Criar chat para o plugin
        print("💬 Criando chat para o plugin...")
        chat = Chat(
            plugin_id=plugin.id,
            title=f'Geração de {plugin_name}'
        )
        db.session.add(chat)
        db.session.commit()
        print(f"✅ Chat criado com ID: {chat.id}")

        # Adicionar mensagem do usuário no chat
        print("👤 Adicionando mensagem do usuário...")
        user_message = Message(
            chat_id=chat.id,
            role='user',
            content=f"Gerar plugin: {plugin_name}\n\nDescrição: {full_description}"
        )
        db.session.add(user_message)
        db.session.commit()

        # Adicionar resposta da IA no chat
        print("🤖 Adicionando resposta da IA...")
        ai_message = Message(
            chat_id=chat.id,
            role='assistant',
            content=f'Plugin gerado com sucesso!\n\nArquivos criados:\n- {plugin_name}.java\n- plugin.yml\n- config.yml',
            content_type='plugin_generation',
            generated_code=main_class_code,
            plugin_yml=plugin_yml_code,
            package_name=package_name
        )
        db.session.add(ai_message)
        db.session.commit()

        # Criar estrutura do projeto
        print("📁 Criando estrutura do projeto...")
        project_id = str(uuid.uuid4())[:8]
        project_dir = WORKSPACE_DIR / f"{plugin_name}_{project_id}"
        
        print(f"📂 Diretório do projeto: {project_dir}")
        
        # Estrutura Maven
        src_dir = project_dir / "src" / "main" / "java"
        resources_dir = project_dir / "src" / "main" / "resources"
        src_dir.mkdir(parents=True, exist_ok=True)
        resources_dir.mkdir(parents=True, exist_ok=True)
        
        # Package path
        package_path = src_dir / package_name.replace('.', '/')
        package_path.mkdir(parents=True, exist_ok=True)
        
        # Salvar arquivos Java
        print("💾 Salvando arquivo Java principal...")
        main_class_file = package_path / f"{plugin_name}.java"
        with open(main_class_file, 'w', encoding='utf-8') as f:
            f.write(main_class_code)
        
        # Validação de sintaxe Java básica
        print("🔍 Validando sintaxe Java...")
        syntax_errors = validate_java_syntax(main_class_code)
        if syntax_errors:
            print(f"❌ Erros de sintaxe detectados:")
            for error in syntax_errors:
                print(f"   - {error}")
            
            # Atualizar plugin com erro de sintaxe
            plugin.status = 'error'
            plugin.error_message = f"Erros de sintaxe Java: {'; '.join(syntax_errors)}"
            db.session.commit()
            
            return jsonify({
                'success': False,
                'error': f"Erros de sintaxe Java detectados: {'; '.join(syntax_errors)}"
            }), 400
        
        print("✅ Sintaxe Java validada com sucesso!")
        
        # Salvar arquivos de recursos (TODOS em src/main/resources/)
        print("💾 Salvando plugin.yml...")
        plugin_yml_file = resources_dir / "plugin.yml"
        with open(plugin_yml_file, 'w', encoding='utf-8') as f:
            f.write(plugin_yml_code)
        
        # IMPORTANTE: Salvar config.yml em src/main/resources/ para ser incluído no JAR
        print("💾 Salvando config.yml...")
        config_yml_file = resources_dir / "config.yml"
        with open(config_yml_file, 'w', encoding='utf-8') as f:
            f.write(config_yml_code)
        
        print(f"✅ Arquivos salvos em src/main/resources/: plugin.yml, config.yml")
        
        # Gerar pom.xml com placeholders substituídos
        print("📋 Gerando pom.xml...")
        pom_template = Path(__file__).parent / "pom.xml"
        if pom_template.exists():
            with open(pom_template, 'r', encoding='utf-8') as f:
                pom_content = f.read()
            
            # Substituir placeholders com valores reais
            pom_content = pom_content.replace('{PLUGIN_NAME}', plugin_name)
            pom_content = pom_content.replace('{PLUGIN_VERSION}', plugin_version)
            pom_content = pom_content.replace('{MC_VERSION}', mc_version)
            
            # Salvar pom.xml gerado
            pom_file = project_dir / "pom.xml"
            with open(pom_file, 'w', encoding='utf-8') as f:
                f.write(pom_content)
            
            print(f"✅ pom.xml gerado com placeholders substituídos")
            print(f"   - Plugin: {plugin_name}")
            print(f"   - Versão: {plugin_version}")
            print(f"   - Minecraft: {mc_version}")
        else:
            print("❌ pom.xml template não encontrado")
        
        # Compilar
        print("🔨 Iniciando compilação Maven...")
        compile_result = compile_with_maven(project_dir)
        
        # Atualizar status do plugin
        print("📊 Atualizando status do plugin...")
        if compile_result['success']:
            plugin.status = 'compiled'
            plugin.compiled_file = str(project_dir / "target" / f"{plugin_name}-{plugin_version}.jar")
            print("✅ Plugin compilado com sucesso!")
        else:
            plugin.status = 'error'
            plugin.error_message = compile_result['error']
            print(f"❌ Erro na compilação: {compile_result['error']}")
        
        plugin.last_compile_attempt = datetime.now(UTC)
        db.session.commit()

        # Criar versão inicial
        print("📝 Criando versão inicial...")
        version = PluginVersion(
            plugin_id=plugin.id,
            version_number=plugin_version,
            changes='Versão inicial gerada',
            main_code=main_class_code,
            plugin_yml_content=plugin_yml_code,
            package_name=package_name
        )
        db.session.add(version)
        db.session.commit()

        print("🎉 Plugin gerado com sucesso!")
        return jsonify({
            'success': True,
            'message': 'Plugin gerado com sucesso!',
            'plugin_id': plugin.id,
            'chat_id': chat.id,
            'download_url': f'/api/download/{project_id}/{plugin_name}-{plugin_version}.jar' if compile_result['success'] else None,
            'compile_status': compile_result['success'],
            'error': compile_result.get('error')
        })

    except Exception as e:
        print(f"❌ Erro crítico: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500

@app.route('/api/chat/send', methods=['POST'])
@login_required
def send_message():
    """Enviar mensagem no chat do plugin"""
    try:
        data = request.get_json()
        chat_id = data.get('chat_id')
        message_content = data.get('message')
        
        # Verificar se o chat pertence ao usuário
        chat = Chat.query.join(Plugin).filter(
            Chat.id == chat_id,
            Plugin.user_id == current_user.id
        ).first_or_404()
        
        # Adicionar mensagem do usuário
        user_message = Message(
            chat_id=chat_id,
            role='user',
            content=message_content
        )
        db.session.add(user_message)
        db.session.commit()
        
        # Gerar resposta da IA com contexto
        context_messages = []
        recent_messages = Message.query.filter_by(chat_id=chat_id).order_by(Message.created_at.desc()).limit(10).all()
        
        for msg in reversed(recent_messages[:-1]):  # Exclui a última mensagem (que é a do usuário)
            context_messages.append({
                'role': msg.role,
                'content': msg.content
            })
        
        # Check if this is a modification request
        modification_keywords = ['modify', 'change', 'update', 'edit', 'alter', 'fix', 'improve', 'add feature', 'remove', 'refactor']
        is_modification_request = any(keyword in message_content.lower() for keyword in modification_keywords)
        
        # Get current plugin code if this is a modification request
        current_code = None
        current_yml = None
        if is_modification_request:
            # Get the latest version from database
            latest_version = PluginVersion.query.filter_by(plugin_id=chat.plugin_id).order_by(PluginVersion.created_at.desc()).first()
            if latest_version:
                current_code = latest_version.main_code
                current_yml = latest_version.plugin_yml_content
        
        # Prompt do sistema
        if is_modification_request and current_code:
            system_prompt = f"""Você é um assistente especializado em desenvolvimento e MODIFICAÇÃO de plugins Minecraft Spigot.
Você está trabalhando no plugin '{chat.plugin.name}' que já foi gerado anteriormente.

CÓDIGO ATUAL DO PLUGIN:
```java
{current_code[:2000]}  # First 2000 chars to avoid token limits
```

Context: O plugin tem as seguintes características:
- Nome: {chat.plugin.name}
- Versão: {chat.plugin.version}
- MC Version: {chat.plugin.minecraft_version}
- Descrição: {chat.plugin.description}
- Status: {chat.plugin.status}

IMPORTANTE: O usuário está pedindo para MODIFICAR o código existente.

Sua tarefa é:
1. Analisar o código atual fornecido acima
2. Entender as modificações solicitadas pelo usuário
3. Aplicar as modificações ao código
4. Retornar o código COMPLETO modificado no formato JSON

Se a modificação for simples (mensagens, configurações), apenas descreva as mudanças.
Se a modificação for significativa (nova funcionalidade, mudança de lógica), retorne o código completo modificado.

FORMATO PARA MODIFICAÇÕES SIGNIFICATIVAS (retorne JSON quando o código for alterado):
{{
    "modification_type": "code_change",
    "main_class": "código Java COMPLETO modificado aqui",
    "plugin_yml": "plugin.yml COMPLETO (se alterado)",
    "config_yml": "config.yml COMPLETO (se alterado)",
    "changes_summary": "Resumo detalhado das mudanças feitas"
}}

FORMATO PARA DISCUSSÕES SIMPLES (sem alteração de código):
{{
    "modification_type": "discussion",
    "response": "sua resposta em texto normal aqui"
}}

Sempre forneça código Java funcional e completo quando houver modificação."""
        else:
            system_prompt = f"""Você é um assistente especializado em desenvolvimento de plugins Minecraft Spigot. 
Você está trabalhando no plugin '{chat.plugin.name}' que já foi gerado anteriormente.

Context: O plugin tem as seguintes características:
- Nome: {chat.plugin.name}
- Versão: {chat.plugin.version}
- MC Version: {chat.plugin.minecraft_version}
- Descrição: {chat.plugin.description}
- Features: {chat.plugin.features}

Sua tarefa é ajudar o usuário a melhorar, modificar ou adicionar funcionalidades ao plugin. 
Sempre forneça código Java funcional e completo quando necessário."""
        
        # Construir prompt completo
        full_prompt = f"{system_prompt}\n\nPedido do usuário: {message_content}"
        
        # Chamar API
        ai_response = call_ai_api(full_prompt)
        
        if not ai_response:
            ai_message_content = "Desculpe, não consegui gerar uma resposta. Tente novamente."
            
            # Adicionar resposta da IA
            ai_message = Message(
                chat_id=chat_id,
                role='assistant',
                content=ai_message_content
            )
            db.session.add(ai_message)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message_id': ai_message.id,
                'content': ai_message_content
            })
        
        # Try to parse as JSON for code modifications
        try:
            ai_data = json.loads(ai_response)
            
            if ai_data.get('modification_type') == 'code_change':
                # This is a code modification - apply it!
                print(f"🔧 Applying code modifications to plugin {chat.plugin.name}...")
                
                modification_result = apply_plugin_modification(
                    plugin=chat.plugin,
                    new_code=ai_data.get('main_class'),
                    new_plugin_yml=ai_data.get('plugin_yml'),
                    new_config_yml=ai_data.get('config_yml'),
                    changes_summary=ai_data.get('changes_summary', 'Code modified by AI')
                )
                
                if modification_result['success']:
                    ai_message_content = f"✅ Modificações aplicadas com sucesso!\n\n{ai_data.get('changes_summary', 'Código atualizado.')}\n\nO plugin foi recompilado e está pronto para download."
                    
                    # Add success message to chat
                    ai_message = Message(
                        chat_id=chat_id,
                        role='assistant',
                        content=ai_message_content,
                        content_type='plugin_update',
                        generated_code=ai_data.get('main_class'),
                        plugin_yml=ai_data.get('plugin_yml')
                    )
                    db.session.add(ai_message)
                    db.session.commit()
                    
                    return jsonify({
                        'success': True,
                        'message_id': ai_message.id,
                        'content': ai_message_content,
                        'plugin_modified': True,
                        'compile_status': modification_result['compile_status']
                    })
                else:
                    ai_message_content = f"❌ Falha ao aplicar modificações: {modification_result['error']}"
            elif ai_data.get('modification_type') == 'discussion':
                ai_message_content = ai_data.get('response', ai_response)
            else:
                # Unknown format, use raw response
                ai_message_content = ai_response
        except json.JSONDecodeError:
            # Not JSON, use as regular text response
            ai_message_content = ai_response
        
        # Adicionar resposta da IA
        ai_message = Message(
            chat_id=chat_id,
            role='assistant',
            content=ai_message_content
        )
        db.session.add(ai_message)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message_id': ai_message.id,
            'content': ai_message_content
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao processar mensagem: {str(e)}'
        }), 500

def apply_plugin_modification(plugin, new_code, new_plugin_yml, new_config_yml, changes_summary):
    """Apply modifications to an existing plugin and recompile"""
    try:
        print(f"🔧 Starting plugin modification for {plugin.name}...")
        
        # Update plugin status
        plugin.status = 'generating'
        plugin.updated_at = datetime.now(UTC)
        db.session.commit()
        
        # Create new project directory
        project_id = str(uuid.uuid4())[:8]
        project_dir = WORKSPACE_DIR / f"{plugin.name}_{project_id}"
        
        # Maven structure
        src_dir = project_dir / "src" / "main" / "java"
        resources_dir = project_dir / "src" / "main" / "resources"
        src_dir.mkdir(parents=True, exist_ok=True)
        resources_dir.mkdir(parents=True, exist_ok=True)
        
        # Get package name from latest version or generate
        latest_version = PluginVersion.query.filter_by(plugin_id=plugin.id).order_by(PluginVersion.created_at.desc()).first()
        package_name = latest_version.package_name if latest_version else f'com.pluginforge.{plugin.name.lower()}'
        
        # Package path
        package_path = src_dir / package_name.replace('.', '/')
        package_path.mkdir(parents=True, exist_ok=True)
        
        # Save modified Java file
        main_class_file = package_path / f"{plugin.name}.java"
        with open(main_class_file, 'w', encoding='utf-8') as f:
            f.write(new_code)
        
        # Validate syntax
        print("🔍 Validating modified Java syntax...")
        syntax_errors = validate_java_syntax(new_code)
        if syntax_errors:
            plugin.status = 'error'
            plugin.error_message = f"Syntax errors in modified code: {'; '.join(syntax_errors)}"
            db.session.commit()
            
            return {
                'success': False,
                'error': f"Syntax errors: {'; '.join(syntax_errors)}",
                'compile_status': False
            }
        
        # Save resource files (use existing if not modified)
        if new_plugin_yml:
            with open(resources_dir / "plugin.yml", 'w', encoding='utf-8') as f:
                f.write(new_plugin_yml)
        else:
            # Use existing plugin.yml
            if latest_version and latest_version.plugin_yml_content:
                with open(resources_dir / "plugin.yml", 'w', encoding='utf-8') as f:
                    f.write(latest_version.plugin_yml_content)
        
        if new_config_yml:
            with open(resources_dir / "config.yml", 'w', encoding='utf-8') as f:
                f.write(new_config_yml)
        else:
            # Generate default config.yml
            default_config = f"""# Configuration for {plugin.name}
messages:
  enabled: '&aPlugin enabled!'
  disabled: '&cPlugin disabled!'
settings:
  debug: false
"""
            with open(resources_dir / "config.yml", 'w', encoding='utf-8') as f:
                f.write(default_config)
        
        # Generate pom.xml
        pom_template = Path(__file__).parent / "pom.xml"
        if pom_template.exists():
            with open(pom_template, 'r', encoding='utf-8') as f:
                pom_content = f.read()
            
            pom_content = pom_content.replace('{PLUGIN_NAME}', plugin.name)
            pom_content = pom_content.replace('{PLUGIN_VERSION}', plugin.version)
            pom_content = pom_content.replace('{MC_VERSION}', plugin.minecraft_version)
            
            with open(project_dir / "pom.xml", 'w', encoding='utf-8') as f:
                f.write(pom_content)
        
        # Compile
        print("🔨 Compiling modified plugin with Maven...")
        compile_result = compile_with_maven(project_dir)
        
        # Update plugin status
        if compile_result['success']:
            plugin.status = 'compiled'
            plugin.compiled_file = str(project_dir / "target" / f"{plugin.name}-{plugin.version}.jar")
            print("✅ Modified plugin compiled successfully!")
        else:
            plugin.status = 'error'
            plugin.error_message = compile_result['error']
            print(f"❌ Compilation error: {compile_result['error']}")
        
        plugin.last_compile_attempt = datetime.now(UTC)
        db.session.commit()
        
        # Create new version entry
        new_version = PluginVersion(
            plugin_id=plugin.id,
            version_number=plugin.version,
            changes=changes_summary,
            main_code=new_code,
            plugin_yml_content=new_plugin_yml or (latest_version.plugin_yml_content if latest_version else ''),
            package_name=package_name
        )
        db.session.add(new_version)
        db.session.commit()
        
        return {
            'success': True,
            'compile_status': compile_result['success'],
            'error': compile_result.get('error')
        }
        
    except Exception as e:
        print(f"❌ Error applying modifications: {str(e)}")
        import traceback
        traceback.print_exc()
        
        plugin.status = 'error'
        plugin.error_message = f"Modification error: {str(e)}"
        db.session.commit()
        
        return {
            'success': False,
            'error': str(e),
            'compile_status': False
        }


@app.route('/api/download/<project_id>/<filename>')
@login_required
def download_plugin(project_id, filename):
    """Download do plugin compilado"""
    # Buscar o arquivo
    for project_dir in WORKSPACE_DIR.iterdir():
        if project_id in project_dir.name:
            jar_path = project_dir / "target" / filename
            if jar_path.exists():
                return send_file(
                    jar_path,
                    as_attachment=True,
                    download_name=filename,
                    mimetype='application/java-archive'
                )
    
    return jsonify({'error': 'Arquivo não encontrado'}), 404

@app.route('/api/plugin/<plugin_id>/download')
@login_required
def download_plugin_by_id(plugin_id):
    """Download do plugin usando o ID do plugin"""
    # Buscar plugin no banco
    plugin = Plugin.query.filter_by(id=plugin_id, user_id=current_user.id).first_or_404()
    
    # Verificar se o plugin foi compilado
    if not plugin.compiled_file or plugin.status != 'compiled':
        return jsonify({'error': 'Plugin ainda não foi compilado'}), 400
    
    # Verificar se o arquivo existe
    jar_path = Path(plugin.compiled_file)
    if not jar_path.exists():
        return jsonify({'error': 'Arquivo JAR não encontrado no servidor'}), 404
    
    # Enviar arquivo
    return send_file(
        jar_path,
        as_attachment=True,
        download_name=jar_path.name,
        mimetype='application/java-archive'
    )

@app.route('/api/dashboard/plugins', methods=['GET'])
@login_required
def get_dashboard_plugins():
    """API endpoint for auto-refresh dashboard - returns plugin data"""
    try:
        user_plugins = Plugin.query.filter_by(user_id=current_user.id).order_by(Plugin.updated_at.desc()).all()
        
        plugins_data = []
        for plugin in user_plugins:
            plugins_data.append({
                'id': plugin.id,
                'name': plugin.name,
                'version': plugin.version,
                'minecraft_version': plugin.minecraft_version,
                'description': plugin.description,
                'status': plugin.status,
                'created_at': plugin.created_at.isoformat(),
                'updated_at': plugin.updated_at.isoformat()
            })
        
        return jsonify({
            'success': True,
            'plugins': plugins_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/plugin/<plugin_id>/recreate', methods=['POST'])
@login_required
def recreate_plugin(plugin_id):
    """Recreate a failed plugin with option to modify parameters"""
    try:
        # Get the original plugin
        original_plugin = Plugin.query.filter_by(id=plugin_id, user_id=current_user.id).first_or_404()
        
        # Only allow recreation for error status plugins
        if original_plugin.status != 'error':
            return jsonify({
                'success': False,
                'error': 'Only plugins with error status can be recreated'
            }), 400
        
        # Get optional parameter modifications from request
        data = request.get_json() or {}
        
        # Use modified parameters or fall back to originals
        plugin_name = data.get('pluginName', original_plugin.name).replace(" ", "")
        mc_version = data.get('mcVersion', original_plugin.minecraft_version)
        description = data.get('description', original_plugin.description)
        plugin_version = data.get('pluginVersion', original_plugin.version)
        features = data.get('features', original_plugin.features or '')
        
        print(f"🔄 Recreating plugin '{plugin_name}' for user {current_user.username}...")
        print(f"   Original plugin ID: {plugin_id}")
        print(f"   Previous error: {original_plugin.error_message}")
        
        # Build improved prompt with error context
        full_description = f"{description}\n\nFuncionalidades: {features}" if features else description
        
        # Enhanced prompt with error learning
        prompt = f"""Você é o PluginCraft AI, especialista em desenvolvimento de plugins para Minecraft Spigot.

Tarefa: Gere um plugin completo para Minecraft {mc_version} com base na seguinte descrição:

NOME DO PLUGIN: {plugin_name}
VERSÃO: {plugin_version}
DESCRIÇÃO: {full_description}

IMPORTANTE - APRENDIZADO DE ERRO ANTERIOR:
Este plugin falhou anteriormente com o seguinte erro:
{original_plugin.error_message[:500] if original_plugin.error_message else 'Erro de compilação'}

Por favor, EVITE este erro e gere código AINDA MAIS CUIDADOSO com sintaxe.

INSTRUÇÕES CRÍTICAS DE SINTAXE JAVA:
1. **OBRIGATÓRIO**: Todas as strings devem ter aspas DUPLAS de abertura e fechamento (")
2. **OBRIGATÓRIO**: Escape todas as aspas duplas dentro de strings com \\"
3. **OBRIGATÓRIO**: Strings com múltiplas linhas devem usar concatenação + ou \\n
4. **OBRIGATÓRIO**: Todos os parênteses, chaves e colchetes devem ser fechados
5. **OBRIGATÓRIO**: Cada linha de código deve terminar com ; (ponto e vírgula)
6. **CRITICAL**: Teste mentalmente se o código compila antes de retornar
7. **CRITICAL**: Não use caracteres especiais ou Unicode em strings sem escape adequado

EXEMPLO DE STRING CORRETA:
String message = "Olá mundo! Esta é uma mensagem válida.";
String complex = "Múltiplas aspas: \\"importante\\" e \\"crítico\\"";

EXEMPLO DE STRING INCORRETA (NÃO FAÇA):
String bad = "texto sem fechar
String worse = "texto com "aspas" dentro sem escape

INSTRUÇÕES DE CONTEÚDO:
- Gere o código Java completo e funcional
- Use boas práticas de programação Java
- Inclua comentários explicativos no código
- O código deve estar pronto para compilação Maven
- Use spigot-api {mc_version} importações corretas

**OBRIGATÓRIO**: Retorne APENAS o JSON válido, sem markdown, sem explicações, sem code blocks

FORMATO OBRIGATÓRIO (retorne APENAS isto, nada mais):
{{
    "main_class": "conteúdo completo da classe principal Java aqui",
    "plugin_yml": "conteúdo completo do arquivo plugin.yml aqui",
    "config_yml": "conteúdo completo do arquivo config.yml aqui (com configurações padrão do plugin)",
    "package_name": "com.pluginforge.{plugin_name.lower()}"
}}

IMPORTANTE: Retorne apenas o JSON acima, sem texto adicional, sem formatação markdown."""

        print(f"📡 Generating plugin with improved error handling...")
        
        # Call AI API
        ai_response = call_ai_api(prompt)
        
        if not ai_response:
            return jsonify({
                'success': False,
                'error': 'Failed to generate code with AI. Please check your API key.'
            }), 500
        
        # Parse JSON
        try:
            code_data = json.loads(ai_response)
            main_class_code = code_data.get('main_class', '')
            plugin_yml_code = code_data.get('plugin_yml', '')
            config_yml_code = code_data.get('config_yml', '')
            package_name = code_data.get('package_name', f'com.pluginforge.{plugin_name.lower()}')
            
            # Generate default config.yml if not provided
            if not config_yml_code:
                config_yml_code = f"""# Configuration for {plugin_name}
# Generated automatically by PluginForge Studio

messages:
  enabled: '&aPlugin enabled successfully!'
  disabled: '&cPlugin disabled!'

settings:
  debug: false
  language: 'en_US'
"""
        except json.JSONDecodeError as e:
            return jsonify({
                'success': False,
                'error': f'AI did not return valid format. Details: {str(e)}'
            }), 500
        
        # Update the existing plugin instead of creating new one
        original_plugin.status = 'generating'
        original_plugin.error_message = None
        original_plugin.updated_at = datetime.now(UTC)
        
        # Update parameters if modified
        original_plugin.name = plugin_name
        original_plugin.version = plugin_version
        original_plugin.minecraft_version = mc_version
        original_plugin.description = description
        original_plugin.features = features
        
        db.session.commit()
        print(f"✅ Plugin updated in database")
        
        # Create new chat message for recreation
        chat = Chat.query.filter_by(plugin_id=plugin_id, is_active=True).first()
        if not chat:
            chat = Chat(plugin_id=plugin_id, title=f'Recreation of {plugin_name}')
            db.session.add(chat)
            db.session.commit()
        
        # Add recreation message
        recreation_message = Message(
            chat_id=chat.id,
            role='system',
            content=f'Plugin recreation initiated. Attempting to fix previous error and regenerate...'
        )
        db.session.add(recreation_message)
        db.session.commit()
        
        # Create project structure
        project_id = str(uuid.uuid4())[:8]
        project_dir = WORKSPACE_DIR / f"{plugin_name}_{project_id}"
        
        # Maven structure
        src_dir = project_dir / "src" / "main" / "java"
        resources_dir = project_dir / "src" / "main" / "resources"
        src_dir.mkdir(parents=True, exist_ok=True)
        resources_dir.mkdir(parents=True, exist_ok=True)
        
        # Package path
        package_path = src_dir / package_name.replace('.', '/')
        package_path.mkdir(parents=True, exist_ok=True)
        
        # Save Java file
        main_class_file = package_path / f"{plugin_name}.java"
        with open(main_class_file, 'w', encoding='utf-8') as f:
            f.write(main_class_code)
        
        # Validate syntax
        print("🔍 Validating Java syntax...")
        syntax_errors = validate_java_syntax(main_class_code)
        if syntax_errors:
            original_plugin.status = 'error'
            original_plugin.error_message = f"Java syntax errors: {'; '.join(syntax_errors)}"
            db.session.commit()
            
            return jsonify({
                'success': False,
                'error': f"Java syntax errors detected: {'; '.join(syntax_errors)}"
            }), 400
        
        # Save resource files
        with open(resources_dir / "plugin.yml", 'w', encoding='utf-8') as f:
            f.write(plugin_yml_code)
        
        with open(resources_dir / "config.yml", 'w', encoding='utf-8') as f:
            f.write(config_yml_code)
        
        # Generate pom.xml
        pom_template = Path(__file__).parent / "pom.xml"
        if pom_template.exists():
            with open(pom_template, 'r', encoding='utf-8') as f:
                pom_content = f.read()
            
            pom_content = pom_content.replace('{PLUGIN_NAME}', plugin_name)
            pom_content = pom_content.replace('{PLUGIN_VERSION}', plugin_version)
            pom_content = pom_content.replace('{MC_VERSION}', mc_version)
            
            with open(project_dir / "pom.xml", 'w', encoding='utf-8') as f:
                f.write(pom_content)
        
        # Compile
        print("🔨 Compiling with Maven...")
        compile_result = compile_with_maven(project_dir)
        
        # Update plugin status
        if compile_result['success']:
            original_plugin.status = 'compiled'
            original_plugin.compiled_file = str(project_dir / "target" / f"{plugin_name}-{plugin_version}.jar")
            print("✅ Plugin recreated and compiled successfully!")
        else:
            original_plugin.status = 'error'
            original_plugin.error_message = compile_result['error']
            print(f"❌ Compilation error: {compile_result['error']}")
        
        original_plugin.last_compile_attempt = datetime.now(UTC)
        db.session.commit()
        
        # Create new version entry
        new_version = PluginVersion(
            plugin_id=original_plugin.id,
            version_number=plugin_version,
            changes=f'Recreated after error. Previous error: {original_plugin.error_message[:200] if original_plugin.error_message else "Unknown"}',
            main_code=main_class_code,
            plugin_yml_content=plugin_yml_code,
            package_name=package_name
        )
        db.session.add(new_version)
        db.session.commit()
        
        # Add AI success/error message to chat
        if compile_result['success']:
            success_message = Message(
                chat_id=chat.id,
                role='assistant',
                content=f'Plugin recreated successfully! The previous error has been fixed.',
                content_type='plugin_generation',
                generated_code=main_class_code,
                plugin_yml=plugin_yml_code,
                package_name=package_name
            )
        else:
            success_message = Message(
                chat_id=chat.id,
                role='assistant',
                content=f'Recreation attempted but compilation failed: {compile_result["error"][:200]}',
                content_type='text'
            )
        db.session.add(success_message)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Plugin recreated successfully!' if compile_result['success'] else 'Recreation attempted but compilation failed',
            'plugin_id': original_plugin.id,
            'compile_status': compile_result['success'],
            'error': compile_result.get('error')
        })
        
    except Exception as e:
        print(f"❌ Critical error in recreation: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Internal error: {str(e)}'
        }), 500

# ========================================
# FUNÇÕES AUXILIARES (mantidas do código original)
# ========================================

def call_ai_api(prompt):
    """Chama a API da IA para gerar código"""
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_KEY}',
            'HTTP-Referer': 'https://pluginforge.studio',
            'X-Title': 'PluginForge Studio'
        }
        
        system_prompt = "Você é um especialista em desenvolvimento de plugins Minecraft Spigot. Sempre retorne código em formato JSON."
        
        payload = {
            'model': API_MODEL,
            'messages': [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': prompt}
            ],
            'temperature': 0.7,
            'max_tokens': 4096,
            'stream': False
        }
        
        print(f"🚀 Chamando API OpenRouter - Modelo: {API_MODEL}")
        print(f"🔑 API Key: {API_KEY[:20]}...")
        
        response = requests.post(API_ENDPOINT, headers=headers, json=payload, timeout=60)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            if 'choices' in result and len(result['choices']) > 0:
                choice = result['choices'][0]
                
                if 'message' in choice and 'content' in choice['message']:
                    content = choice['message']['content']
                    
                    # Limpa a resposta
                    content = content.strip()
                    if content.startswith('```json'):
                        content = content[7:]
                    elif content.startswith('```'):
                        content = content[3:]
                    
                    if content.endswith('```'):
                        content = content[:-3]
                    
                    print(f"✅ Resposta da IA recebida: {len(content)} caracteres")
                    return content.strip()
            else:
                print(f"❌ Resposta da API não contém choices: {result}")
        else:
            print(f"❌ Erro da API - Status: {response.status_code}")
            print(f"❌ Resposta da API: {response.text}")
                    
        return None
            
    except requests.exceptions.Timeout:
        print("❌ Timeout: API demorou mais de 60 segundos para responder")
        return None
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão: Não foi possível conectar com a API")
        return None
    except Exception as e:
        print(f"❌ Erro inesperado ao chamar API: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def compile_with_maven(project_dir):
    """
    Compila o projeto Maven usando múltiplos métodos para garantir compatibilidade.
    
    Args:
        project_dir (Path): Diretório do projeto Maven
        
    Returns:
        dict: {'success': bool, 'error': str}
    """
    
    # Lista de possíveis caminhos para o Maven (ordenado por preferência)
    maven_commands = [
        # Windows - comandos que funcionam na prática
        'mvn.cmd',                                # CMD extension (Windows)
        'mvn',                                    # PATH padrão
        'C:\\apache-maven-3.9.11\\bin\\mvn.cmd', # Apache Maven 3.9.11 (Windows)
        # macOS paths
        '/usr/local/bin/mvn',                     # Homebrew (macOS)
        '/opt/homebrew/bin/mvn',                  # Homebrew ARM (macOS)
        # Linux paths
        '/usr/bin/mvn',                           # APT (Linux)
        '/opt/maven/bin/mvn',                     # Maven manual (Linux)
        '/snap/bin/mvn',                          # Snap (Linux)
        str(Path.home() / 'maven/bin/mvn'),       # Maven instalado em home
        # Windows Program Files (menos comum)
        'C:\\Program Files\\Apache\\Maven\\bin\\mvn.cmd',
        'C:\\Program Files\\Maven\\bin\\mvn.cmd',
        # Alternative Windows paths
        str(Path('C:/Program Files/Apache/Maven/bin/mvn.cmd')),
        str(Path('C:/Program Files/Maven/bin/mvn.cmd')),
    ]
    
    print(f"🔍 Procurando Maven em: {len(maven_commands)} localizações...")
    
    # Método 1: Tenta executar Maven diretamente
    maven_executable = find_maven_executable(maven_commands)
    
    if maven_executable:
        print(f"✅ Maven encontrado: {maven_executable}")
        return execute_maven_compilation(maven_executable, project_dir)
    
    # Método 2: Tenta usar Maven via Docker
    print("🐳 Maven não encontrado localmente, tentando via Docker...")
    return compile_with_maven_docker(project_dir)

def find_maven_executable(commands):
    """
    Procura pelo executável Maven em várias localizações.
    
    Args:
        commands (list): Lista de comandos Maven para testar
        
    Returns:
        str: Caminho do Maven encontrado ou None
    """
    print(f"🔍 Testando {len(commands)} comandos Maven...")
    
    for i, cmd in enumerate(commands, 1):
        try:
            print(f"   [{i}/{len(commands)}] Testando: {cmd}")
            # Testa se o comando existe e funciona
            result = subprocess.run(
                [cmd, '--version'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                version_info = result.stdout.strip() if result.stdout else "Unknown version"
                print(f"✅ Maven encontrado: {cmd}")
                print(f"   📦 Versão: {version_info}")
                return cmd
            else:
                print(f"   ❌ Comando falhou (código: {result.returncode})")
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError) as e:
            print(f"   ❌ Erro ao testar {cmd}: {str(e)}")
        except Exception as e:
            print(f"   ❌ Erro inesperado com {cmd}: {str(e)}")
    
    print("❌ Nenhum executável Maven foi encontrado!")
    return None

def execute_maven_compilation(maven_cmd, project_dir):
    """
    Executa a compilação Maven usando o comando encontrado.
    
    Args:
        maven_cmd (str): Comando Maven para executar
        project_dir (Path): Diretório do projeto
        
    Returns:
        dict: {'success': bool, 'error': str}
    """
    try:
        print(f"🔨 Compilando com Maven: {maven_cmd}")
        
        # Verificar se o diretório do projeto existe
        if not project_dir.exists():
            error_msg = f"Diretório do projeto não encontrado: {project_dir}"
            print(f"❌ {error_msg}")
            return {'success': False, 'error': error_msg}
        
        # Verificar se pom.xml existe
        pom_file = project_dir / "pom.xml"
        if not pom_file.exists():
            error_msg = f"Arquivo pom.xml não encontrado: {pom_file}"
            print(f"❌ {error_msg}")
            return {'success': False, 'error': error_msg}
        
        print(f"📂 Diretório de trabalho: {project_dir}")
        print(f"📄 Arquivo pom.xml: {pom_file}")
        
        # Executa o Maven
        result = subprocess.run(
            [maven_cmd, 'clean', 'install'],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=300  # Timeout de 5 minutos
        )
        
        if result.returncode == 0:
            print("✅ Compilação Maven concluída com sucesso!")
            if result.stdout:
                print(f"📤 Output Maven:\n{result.stdout}")
            return {'success': True, 'error': None}
        else:
            # Mostrar detalhes completos do erro
            error_details = []
            if result.stderr:
                error_details.append(f"❌ ERRO STDERR:\n{result.stderr}")
            if result.stdout:
                error_details.append(f"📤 STDOUT:\n{result.stdout}")
            if not result.stderr and not result.stdout:
                error_details.append("❌ Nenhum output de erro capturado")
            
            error_msg = f"Erro na compilação Maven:\n" + "\n\n".join(error_details)
            print(f"❌ {error_msg}")
            return {
                'success': False,
                'error': error_msg
            }
            
    except subprocess.TimeoutExpired:
        error_msg = 'Compilação excedeu o tempo limite (5 minutos)'
        print(f"❌ {error_msg}")
        return {'success': False, 'error': error_msg}
    except FileNotFoundError as e:
        error_msg = f'Arquivo ou comando não encontrado: {str(e)}. Verifique se Maven está instalado corretamente.'
        print(f"❌ {error_msg}")
        print(f"💡 Comandos Maven testados: {maven_commands}")
        return {'success': False, 'error': error_msg}
    except PermissionError as e:
        error_msg = f'Erro de permissão: {str(e)}. Execute como administrador ou verifique permissões de pasta.'
        print(f"❌ {error_msg}")
        return {'success': False, 'error': error_msg}
    except Exception as e:
        error_msg = f'Erro inesperado na compilação: {str(e)}'
        print(f"❌ {error_msg}")
        return {'success': False, 'error': error_msg}

def compile_with_maven_docker(project_dir):
    """
    Compila o projeto Maven usando Docker como fallback.
    
    Args:
        project_dir (Path): Diretório do projeto Maven
        
    Returns:
        dict: {'success': bool, 'error': str}
    """
    try:
        print("🐳 Tentando compilação via Docker...")
        
        # Comando Docker para Maven
        docker_cmd = [
            'docker', 'run', '--rm',
            '-v', f'{project_dir}:/workspace',
            '-w', '/workspace',
            'maven:3.9-eclipse-temurin-17-alpine',
            'mvn', 'clean', 'install'
        ]
        
        result = subprocess.run(
            docker_cmd,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            print("✅ Compilação Docker Maven concluída com sucesso!")
            return {'success': True, 'error': None}
        else:
            error_msg = f"Erro na compilação Docker:\n{result.stderr}"
            print(f"❌ Erro na compilação Docker: {error_msg}")
            return {
                'success': False,
                'error': f"{error_msg}\n\n💡 Dica: Instale o Maven localmente para compilar mais rápido."
            }
            
    except subprocess.TimeoutExpired:
        error_msg = 'Compilação Docker excedeu o tempo limite (5 minutos)'
        print(f"❌ {error_msg}")
        return {'success': False, 'error': error_msg}
    except FileNotFoundError:
        error_msg = 'Docker não está instalado. Instale o Maven localmente ou o Docker.'
        print(f"❌ {error_msg}")
        return {'success': False, 'error': error_msg}
    except Exception as e:
        error_msg = f'Erro inesperado na compilação Docker: {str(e)}'
        print(f"❌ {error_msg}")
        return {'success': False, 'error': error_msg}

# ========================================
# SUBSCRIPTION MANAGEMENT ROUTES
# ========================================

@app.route('/api/subscription/upgrade', methods=['POST'])
@login_required
def upgrade_subscription():
    """
    Upgrade user subscription plan
    In production, this would integrate with a payment processor like Stripe
    """
    try:
        data = request.get_json()
        plan = data.get('plan', '').lower()
        
        # Validate plan
        valid_plans = ['basic', 'pro', 'premium']
        if plan not in valid_plans:
            return jsonify({
                'success': False,
                'error': 'Invalid plan selected'
            }), 400
        
        # In production, you would:
        # 1. Create a Stripe Checkout Session
        # 2. Redirect user to payment page
        # 3. Handle webhook to confirm payment
        # 4. Update user's subscription in database
        
        # For now, we'll allow instant upgrade for testing
        # WARNING: Remove this in production and implement proper payment flow
        if plan != 'basic':
            # Simulate successful upgrade (FOR DEMO ONLY)
            current_user.subscription_plan = plan
            current_user.subscription_status = 'active'
            current_user.subscription_start = datetime.now(UTC)
            # Set subscription end to 30 days from now
            from datetime import timedelta
            current_user.subscription_end = datetime.now(UTC) + timedelta(days=30)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': f'Successfully upgraded to {plan.upper()} plan!',
                'plan': plan,
                'redirect': '/dashboard'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Cannot downgrade to basic plan through this endpoint'
            }), 400
            
    except Exception as e:
        print(f"❌ Subscription upgrade error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to upgrade subscription'
        }), 500

@app.route('/api/subscription/cancel', methods=['POST'])
@login_required
def cancel_subscription():
    """
    Cancel user subscription
    In production, this would cancel the Stripe subscription
    """
    try:
        # In production: Cancel Stripe subscription
        # For now, just update the database
        current_user.subscription_plan = 'basic'
        current_user.subscription_status = 'cancelled'
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Subscription cancelled successfully',
            'redirect': '/dashboard'
        })
        
    except Exception as e:
        print(f"❌ Subscription cancellation error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to cancel subscription'
        }), 500

# ========================================
# INICIALIZAÇÃO
# ========================================

# Inicializar banco de dados
with app.app_context():
    init_db(app)

if __name__ == '__main__':
    print("🚀 PluginForge Studio iniciado com sistema completo!")
    print("📍 Acesse: http://localhost:5002")
    print("👤 Sistema de login e chat ativado")
    print("💾 Banco de dados SQLite configurado")
    print("🔨 Sistema de compilação Maven ativo")
    
    # Inicia o servidor Flask
    app.run(debug=True, host='0.0.0.0', port=5003)