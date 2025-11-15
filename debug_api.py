#!/usr/bin/env python3
"""
Teste da API OpenRouter
"""

import requests
import json

# Configuração
API_KEY = "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"
API_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
API_MODEL = "openrouter/polaris-alpha"

def test_api():
    """Teste básico da API"""
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}',
        'HTTP-Referer': 'https://pluginforge.studio',
        'X-Title': 'PluginForge Studio'
    }
    
    payload = {
        'model': API_MODEL,
        'messages': [
            {
                'role': 'system', 
                'content': 'You are a Minecraft Spigot plugin expert. Always respond in JSON format.'
            },
            {
                'role': 'user', 
                'content': '''Create a simple welcome plugin. Return ONLY valid JSON:

{
    "main_class": "Main plugin class code here",
    "plugin_yml": "plugin.yml content here",
    "config_yml": "config.yml content here",
    "package_name": "com.example.welcome"
}

Return just the JSON, nothing else.'''
            }
        ],
        'temperature': 0.7,
        'max_tokens': 2000,
        'stream': False
    }
    
    try:
        print("🚀 Testando API OpenRouter...")
        print(f"📡 Endpoint: {API_ENDPOINT}")
        print(f"🤖 Modelo: {API_MODEL}")
        
        response = requests.post(API_ENDPOINT, headers=headers, json=payload, timeout=60)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Resposta da API:")
            print(json.dumps(result, indent=2))
            
            # Extrair conteúdo da resposta
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                print(f"\n📝 Conteúdo da resposta:")
                print(content)
                
                # Tentar parse do JSON
                try:
                    data = json.loads(content)
                    print(f"\n✅ JSON válido! Keys: {list(data.keys())}")
                    return True
                except json.JSONDecodeError as e:
                    print(f"\n❌ Erro no parse JSON: {e}")
                    return False
        else:
            print(f"❌ Erro da API: {response.status_code}")
            print(f"📄 Resposta: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Timeout: API demorou mais de 60 segundos")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão com a API")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

if __name__ == "__main__":
    success = test_api()
    if success:
        print("\n🎉 Teste da API concluído com sucesso!")
    else:
        print("\n💥 Teste da API falhou!")