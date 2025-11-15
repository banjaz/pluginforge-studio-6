# ========================================
# PLUGINFORGE STUDIO - BACKEND FLASK
# ========================================
# Este arquivo contém toda a lógica do servidor:
# - Servir a página principal
# - Receber dados do formulário
# - Chamar a API da IA para gerar código
# - Compilar o plugin usando Maven
# - Retornar o arquivo .jar para download
# ========================================

from flask import Flask, render_template, request, jsonify, send_file
import os
import shutil
import subprocess
import uuid
import json
import requests
from pathlib import Path

# Inicializa a aplicação Flask
app = Flask(__name__)

# ========================================
# CONFIGURAÇÕES
# ========================================

# CONFIGURAÇÃO ATUAL: OpenRouter com Polaris Alpha
# 🔥 Modelo: openrouter/polaris-alpha (GRATUITO - 256K tokens de contexto)
API_KEY = "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"
API_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"  # OpenRouter Endpoint
API_MODEL = "openrouter/polaris-alpha"  # Polaris Alpha - Gratuito e potente

# ALTERNATIVAS:
# - Google AI Studio: API_KEY + "https://generativelanguage.googleapis.com/v1beta/models" + "gemini-1.5-pro"
# - OpenAI: API_KEY + "https://api.openai.com/v1/chat/completions" + "gpt-4"
# - Anthropic: API_KEY + "https://api.anthropic.com/v1/messages" + "claude-3-sonnet-20240229"

# Diretório base para projetos temporários
WORKSPACE_DIR = Path(__file__).parent / "workspace"
WORKSPACE_DIR.mkdir(exist_ok=True)

# ========================================
# ROTA PRINCIPAL - PÁGINA INICIAL
# ========================================

@app.route('/')
def index():
    """
    Serve a página principal (index.html) onde o usuário preenche o formulário.
    """
    return render_template('index.html')

# ========================================
# ROTA DE TESTE - ENDPOINT /test
# ========================================

@app.route('/test', methods=['GET'])
def test_api():
    """
    Rota de teste para verificar se a API da IA está funcionando.
    """
    try:
        # Teste simples para a API
        test_prompt = """Retorne apenas este JSON:
{
    "main_class": "public class TestPlugin { public void onEnable() {} }",
    "plugin_yml": "name: Test\\nversion: 1.0.0\\nauthor: Test\\nmain: TestPlugin",
    "package_name": "com.pluginforge.test"
}"""
        
        print("🧪 Testando API da IA...")
        ai_response = call_ai_api(test_prompt)
        
        if ai_response:
            return jsonify({
                'success': True,
                'message': 'API funcionando!',
                'response': ai_response
            })
        else:
            return jsonify({
                'success': False,
                'error': 'API não respondeu. Verifique a API_KEY.'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro no teste: {str(e)}'
        }), 500

# ========================================
# ROTA DE GERAÇÃO - ENDPOINT /generate
# ========================================

@app.route('/generate', methods=['POST'])
def generate_plugin():
    """
    Endpoint que recebe os dados do formulário e processa a geração do plugin.
    
    Fluxo:
    1. Recebe dados do formulário (nome, versão MC, descrição)
    2. Cria um prompt para a IA
    3. Envia o prompt para a API da IA
    4. Recebe o código Java e plugin.yml
    5. Cria estrutura de diretórios Maven
    6. Compila o projeto com Maven
    7. Retorna o link para download do .jar
    """
    try:
        # ========================================
        # PASSO 1: Receber dados do formulário
        # ========================================
        data = request.get_json()
        plugin_name = data.get('pluginName', 'MyPlugin').replace(" ", "")
        mc_version = data.get('mcVersion', '1.20.1')
        description = data.get('description', '')
        plugin_version = data.get('pluginVersion', '1.0.0')
        
        # Valida se a descrição foi fornecida
        if not description.strip():
            return jsonify({
                'success': False,
                'error': 'Descrição do plugin não pode estar vazia.'
            }), 400

        # ========================================
        # PASSO 2: Construir o prompt para a IA
        # ========================================
        prompt = f"""Você é o PluginCraft AI, especialista em desenvolvimento de plugins para Minecraft Spigot.

Tarefa: Gere um plugin completo para Minecraft {mc_version} com base na seguinte descrição:

NOME DO PLUGIN: {plugin_name}
VERSÃO: {plugin_version}
DESCRIÇÃO: {description}

INSTRUÇÕES CRÍTICAS:
1. Gere o código Java completo e funcional
2. Use boas práticas de programação Java
3. Inclua comentários explicativos no código
4. O código deve estar pronto para compilação
5. **OBRIGATÓRIO**: Retorne APENAS o JSON válido, sem markdown, sem explicações, sem code blocks

FORMATO OBRIGATÓRIO (retorne APENAS isto, nada mais):
{{
    "main_class": "conteúdo completo da classe principal Java aqui",
    "plugin_yml": "conteúdo completo do arquivo plugin.yml aqui",
    "package_name": "com.pluginforge.{plugin_name.lower()}"
}}

IMPORTANTE: Retorne apenas o JSON acima, sem texto adicional, sem formatação markdown."""

        # ========================================
        # PASSO 3: Chamar a API da IA
        # ========================================
        print(f"📡 Chamando API da IA para gerar o plugin '{plugin_name}'...")
        
        ai_response = call_ai_api(prompt)
        
        # Processa a resposta da IA
        if not ai_response:
            return jsonify({
                'success': False,
                'error': 'Falha ao gerar código com a IA. Verifique sua API key.'
            }), 500

        print(f"📋 Resposta completa da IA: {ai_response}")

        # ========================================
        # PASSO 4: Extrair código da resposta
        # ========================================
        try:
            # Tenta fazer parse do JSON retornado pela IA
            code_data = json.loads(ai_response)
            main_class_code = code_data.get('main_class', '')
            plugin_yml_code = code_data.get('plugin_yml', '')
            package_name = code_data.get('package_name', f'com.pluginforge.{plugin_name.lower()}')
            
            print(f"✅ JSON parseado com sucesso!")
            print(f"📄 main_class: {len(main_class_code)} chars")
            print(f"📄 plugin_yml: {len(plugin_yml_code)} chars")
            print(f"📦 package_name: {package_name}")
            
        except json.JSONDecodeError as e:
            # Se a IA não retornou JSON válido, mostra detalhes do erro
            print(f"❌ Erro ao fazer parse do JSON: {e}")
            print(f"📄 Tentativa de parsing de: '{ai_response}'")
            return jsonify({
                'success': False,
                'error': f'A IA não retornou um formato válido. Detalhes: {str(e)}'
            }), 500

        # ========================================
        # PASSO 5: Criar estrutura de diretórios Maven
        # ========================================
        project_id = str(uuid.uuid4())[:8]  # ID único para o projeto
        project_dir = WORKSPACE_DIR / f"{plugin_name}_{project_id}"
        
        # Estrutura de pastas Maven
        src_dir = project_dir / "src" / "main" / "java"
        resources_dir = project_dir / "src" / "main" / "resources"
        
        # Cria os diretórios
        src_dir.mkdir(parents=True, exist_ok=True)
        resources_dir.mkdir(parents=True, exist_ok=True)
        
        # Converte package name em caminho de diretório (ex: com.pluginforge.myplugin -> com/pluginforge/myplugin)
        package_path = src_dir / package_name.replace('.', '/')
        package_path.mkdir(parents=True, exist_ok=True)
        
        # ========================================
        # PASSO 6: Salvar arquivos gerados
        # ========================================
        
        # Salva a classe principal Java
        main_class_file = package_path / f"{plugin_name}.java"
        with open(main_class_file, 'w', encoding='utf-8') as f:
            f.write(main_class_code)
        
        # Salva o plugin.yml
        plugin_yml_file = resources_dir / "plugin.yml"
        with open(plugin_yml_file, 'w', encoding='utf-8') as f:
            f.write(plugin_yml_code)
        
        # Copia e customiza o pom.xml
        pom_template = Path(__file__).parent / "pom.xml"
        pom_target = project_dir / "pom.xml"
        
        with open(pom_template, 'r', encoding='utf-8') as f:
            pom_content = f.read()
        
        # Substitui os placeholders
        pom_content = pom_content.replace('{PLUGIN_NAME}', plugin_name)
        pom_content = pom_content.replace('{PLUGIN_VERSION}', plugin_version)
        pom_content = pom_content.replace('{MC_VERSION}', mc_version)
        
        with open(pom_target, 'w', encoding='utf-8') as f:
            f.write(pom_content)
        
        # ========================================
        # PASSO 7: Compilar com Maven
        # ========================================
        print(f"🔨 Compilando plugin com Maven...")
        
        compile_result = compile_with_maven(project_dir)
        
        if not compile_result['success']:
            return jsonify({
                'success': False,
                'error': f'Erro na compilação: {compile_result["error"]}'
            }), 500
        
        # ========================================
        # PASSO 8: Localizar o arquivo .jar gerado
        # ========================================
        jar_file = project_dir / "target" / f"{plugin_name}-{plugin_version}.jar"
        
        if not jar_file.exists():
            return jsonify({
                'success': False,
                'error': 'Arquivo .jar não foi gerado. Erro na compilação.'
            }), 500
        
        # ========================================
        # PASSO 9: Retornar sucesso com caminho do arquivo
        # ========================================
        print(f"✅ Plugin '{plugin_name}' gerado com sucesso!")
        
        return jsonify({
            'success': True,
            'message': f'Plugin {plugin_name} gerado com sucesso!',
            'download_url': f'/download/{project_id}/{plugin_name}-{plugin_version}.jar'
        })
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500

# ========================================
# ROTA DE DOWNLOAD
# ========================================

@app.route('/download/<project_id>/<filename>')
def download_file(project_id, filename):
    """
    Serve o arquivo .jar para download.
    """
    # Encontra o diretório do projeto
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

# ========================================
# FUNÇÕES AUXILIARES
# ========================================

def call_ai_api(prompt):
    """
    Chama a API da IA para gerar o código do plugin usando OpenRouter (Polaris Alpha).
    
    Args:
        prompt (str): Prompt descrevendo o plugin desejado
        
    Returns:
        str: Resposta da IA contendo o código gerado (em JSON)
    """
    try:
        # Headers para OpenRouter (compatível com OpenAI)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_KEY}',
            'HTTP-Referer': 'https://pluginforge.studio',
            'X-Title': 'PluginForge Studio'
        }
        
        # Constrói o prompt completo com sistema + user message
        system_prompt = "Você é um especialista em desenvolvimento de plugins Minecraft Spigot. Sempre retorne código em formato JSON."
        
        # Payload para OpenRouter (formato OpenAI)
        payload = {
            'model': API_MODEL,
            'messages': [
                {
                    'role': 'system',
                    'content': system_prompt
                },
                {
                    'role': 'user', 
                    'content': prompt
                }
            ],
            'temperature': 0.7,
            'max_tokens': 4096,
            'stream': False
        }
        
        print(f"🚀 Chamando API OpenRouter - Modelo: {API_MODEL}")
        print(f"🔑 API Key: {API_KEY[:10]}...")
        
        response = requests.post(API_ENDPOINT, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"🔍 Estrutura completa da resposta API OpenRouter:")
            print(f"📄 Keys principais: {list(result.keys())}")
            print(f"📋 Resposta completa: {result}")
            
            # Formato OpenRouter/OpenAI
            if 'choices' in result and len(result['choices']) > 0:
                choice = result['choices'][0]
                print(f"🎯 Choice: {choice}")
                
                if 'message' in choice and 'content' in choice['message']:
                    content = choice['message']['content']
                    print(f"📦 Content extraído: {content[:200]}...")
                    
                    # Limpa a resposta removendo markdown e espaços extras
                    content = content.strip()
                    
                    # Remove code blocks se existir
                    if content.startswith('```json'):
                        content = content[7:]
                    elif content.startswith('```'):
                        content = content[3:]
                    
                    if content.endswith('```'):
                        content = content[:-3]
                    
                    content = content.strip()
                    
                    print(f"📄 Resposta da IA (limpa): {content[:200]}...")
                    
                    return content
                else:
                    print(f"❌ Estrutura inesperada no choice: {choice}")
                    return None
            else:
                print(f"❌ Resposta inválida da API: {result}")
                return None
        else:
            print(f"❌ Erro na API OpenRouter: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Erro ao chamar API: {str(e)}")
        return None

def compile_with_maven(project_dir):
    """
    Compila o projeto Maven usando múltiplos métodos para garantir compatibilidade.
    
    Args:
        project_dir (Path): Diretório do projeto Maven
        
    Returns:
        dict: {'success': bool, 'error': str}
    """
    
    # Lista de possíveis caminhos para o Maven
    maven_commands = [
        'mvn',                                    # PATH padrão
        '/usr/local/bin/mvn',                     # Homebrew (macOS)
        '/opt/homebrew/bin/mvn',                  # Homebrew ARM (macOS)
        '/usr/bin/mvn',                           # APT (Linux)
        '/opt/maven/bin/mvn',                     # Maven manual (Linux)
        '/snap/bin/mvn',                          # Snap (Linux)
        str(Path.home() / 'maven/bin/mvn'),       # Maven instalado em home
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
    for cmd in commands:
        try:
            # Testa se o comando existe e funciona
            result = subprocess.run(
                [cmd, '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                print(f"✅ Maven encontrado via comando: {cmd}")
                return cmd
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            continue
    
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
            return {'success': True, 'error': None}
        else:
            error_msg = f"Erro na compilação Maven:\n{result.stderr}"
            print(f"❌ Erro na compilação: {error_msg}")
            return {
                'success': False,
                'error': error_msg
            }
            
    except subprocess.TimeoutExpired:
        error_msg = 'Compilação excedeu o tempo limite (5 minutos)'
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
# INICIALIZAÇÃO DO SERVIDOR
# ========================================

if __name__ == '__main__':
    print("🚀 PluginForge Studio iniciado!")
    print("📍 Acesse: http://localhost:5000")
    print("⚙️  Certifique-se de configurar a API_KEY no código!")
    
    # Inicia o servidor Flask
    app.run(debug=True, host='0.0.0.0', port=5000)
