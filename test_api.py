#!/usr/bin/env python3
# ========================================
# TESTE DA API GOOGLE AI STUDIO
# ========================================
# Script para testar se a API do Gemini está funcionando
# Execute: python test_api.py
# ========================================

import requests
import json

def test_gemini_api():
    """
    Testa a API do Google AI Studio (Gemini)
    """
    # CONFIGURAÇÃO - Substitua pela sua API key real
    API_KEY = "SUA_CHAVE_API_AQUI"  # ⚠️ ALTERE AQUI
    
    if API_KEY == "SUA_CHAVE_API_AQUI":
        print("❌ ERRO: Configure sua API key no arquivo test_api.py")
        print("📍 Obtenha uma chave grátis em: https://aistudio.google.com")
        return False
    
    # Endpoint e modelo
    API_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models"
    API_MODEL = "gemini-1.5-pro"
    
    # Prompt de teste simples
    test_prompt = """Retorne APENAS este JSON, sem texto adicional:
{
    "main_class": "public class TestPlugin { public void onEnable() {} }",
    "plugin_yml": "name: Test\\nversion: 1.0.0\\nauthor: Test\\nmain: TestPlugin",
    "package_name": "com.pluginforge.test"
}"""
    
    try:
        print("🧪 Testando API do Google AI Studio...")
        print(f"🔑 API Key: {API_KEY[:10]}...")
        
        # Headers
        headers = {
            'Content-Type': 'application/json'
        }
        
        # Payload para Gemini
        url = f"{API_ENDPOINT}/{API_MODEL}:generateContent?key={API_KEY}"
        payload = {
            'contents': [
                {
                    'parts': [
                        {
                            'text': test_prompt
                        }
                    ]
                }
            ],
            'generationConfig': {
                'temperature': 0.7,
                'maxOutputTokens': 1024
            }
        }
        
        print(f"📡 Enviando requisição para: {url}")
        
        # Faz a requisição
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Resposta recebida com sucesso!")
            
            # Extrai o conteúdo
            if 'candidates' in result and len(result['candidates']) > 0:
                content = result['candidates'][0]['content']['parts'][0]['text']
                print(f"📄 Resposta bruta: {content}")
                
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
                print(f"❌ Formato de resposta inesperado: {result}")
                return False
                
        else:
            print(f"❌ Erro na API: {response.status_code}")
            print(f"📄 Resposta: {response.text}")
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
    print("🧪 TESTE DA API GOOGLE AI STUDIO (GEMINI)")
    print("=" * 60)
    
    success = test_gemini_api()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 TESTE PASSOU! A API está funcionando.")
        print("✅ Você pode usar o PluginForge Studio normalmente.")
    else:
        print("❌ TESTE FALHOU! Verifique os erros acima.")
        print("⚠️  Corrija os problemas antes de usar o PluginForge Studio.")
    print("=" * 60)

if __name__ == "__main__":
    main()