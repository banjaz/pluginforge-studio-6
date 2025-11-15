#!/usr/bin/env python3
# ========================================
# TESTE DA API OPENROUTER (POLARIS ALPHA)
# ========================================
# Script para testar se a API do OpenRouter está funcionando
# Execute: python test_openrouter.py
# ========================================

import requests
import json

def test_openrouter_api():
    """
    Testa a API do OpenRouter (Polaris Alpha)
    """
    # CONFIGURAÇÃO
    API_KEY = "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"
    
    if API_KEY == "SUA_CHAVE_API_AQUI":
        print("❌ ERRO: Configure sua API key no arquivo test_openrouter.py")
        print("📍 Obtenha uma chave em: https://openrouter.ai/keys")
        return False
    
    # Endpoint e modelo
    API_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
    API_MODEL = "openrouter/polaris-alpha"
    
    # Prompt de teste simples
    test_prompt = """Retorne APENAS este JSON, sem texto adicional:
{
    "main_class": "public class TestPlugin { public void onEnable() {} }",
    "plugin_yml": "name: Test\\nversion: 1.0.0\\nauthor: Test\\nmain: TestPlugin",
    "package_name": "com.pluginforge.test"
}"""
    
    try:
        print("🧪 Testando API do OpenRouter (Polaris Alpha)...")
        print(f"🔑 API Key: {API_KEY[:10]}...")
        print(f"🎯 Modelo: {API_MODEL}")
        print(f"🌐 Endpoint: {API_ENDPOINT}")
        
        # Headers para OpenRouter
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_KEY}',
            'HTTP-Referer': 'https://pluginforge.studio',
            'X-Title': 'PluginForge Studio Test'
        }
        
        # Payload para OpenRouter (formato OpenAI)
        payload = {
            'model': API_MODEL,
            'messages': [
                {
                    'role': 'system',
                    'content': 'Você é um especialista em desenvolvimento de plugins Minecraft Spigot. Sempre retorne código em formato JSON.'
                },
                {
                    'role': 'user', 
                    'content': test_prompt
                }
            ],
            'temperature': 0.7,
            'max_tokens': 1024,
            'stream': False
        }
        
        print(f"📦 Payload: {json.dumps(payload, indent=2)}")
        
        # Faz a requisição
        response = requests.post(API_ENDPOINT, headers=headers, json=payload, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Resposta recebida com sucesso!")
            
            # Análise da estrutura
            print(f"📄 Keys principais: {list(result.keys())}")
            print(f"📋 Resposta completa: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            # Extrai o conteúdo
            if 'choices' in result and len(result['choices']) > 0:
                choice = result['choices'][0]
                print(f"🎯 Choice: {choice}")
                
                if 'message' in choice and 'content' in choice['message']:
                    content = choice['message']['content']
                    print(f"📦 Content extraído: {content}")
                    
                    # Limpa a resposta
                    content = content.strip()
                    if content.startswith('```json'):
                        content = content[7:]
                    elif content.startswith('```'):
                        content = content[3:]
                    
                    if content.endswith('```'):
                        content = content[:-3]
                    
                    content = content.strip()
                    print(f"🧹 Resposta limpa: {content}")
                    
                    # Tenta fazer parse do JSON
                    try:
                        parsed = json.loads(content)
                        print("✅ JSON válido!")
                        print(f"📦 Package: {parsed.get('package_name', 'N/A')}")
                        print(f"📄 Main class: {len(parsed.get('main_class', ''))} chars")
                        print(f"📄 Plugin.yml: {len(parsed.get('plugin_yml', ''))} chars")
                        return True
                        
                    except json.JSONDecodeError as e:
                        print(f"❌ Erro no JSON: {e}")
                        print(f"📄 Tentativa de parsing: '{content}'")
                        return False
                else:
                    print(f"❌ Estrutura inesperada no choice: {choice}")
                    return False
            else:
                print(f"❌ Não há choices na resposta: {result}")
                return False
                
        else:
            print(f"❌ Erro na API: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Timeout: A API demorou muito para responder")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão: Verifique sua internet")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")
        return False

def main():
    """
    Função principal
    """
    print("=" * 60)
    print("🧪 TESTE DA API OPENROUTER (POLARIS ALPHA)")
    print("=" * 60)
    
    success = test_openrouter_api()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 TESTE PASSOU! A API OpenRouter está funcionando.")
        print("✅ Polaris Alpha está pronto para gerar plugins!")
        print("💡 Benefícios do Polaris Alpha:")
        print("   - 256K tokens de contexto")
        print("   - Gratuito ($0/M tokens)")
        print("   - Especializado em programação")
    else:
        print("❌ TESTE FALHOU! Verifique os erros acima.")
        print("⚠️  Corrija os problemas antes de usar o PluginForge Studio.")
    print("=" * 60)

if __name__ == "__main__":
    main()