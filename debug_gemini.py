#!/usr/bin/env python3
# ========================================
# DIAGNÓSTICO DA API GEMINI
# ========================================
# Script para analisar exatamente como a API Gemini responde
# Execute: python debug_gemini.py
# ========================================

import requests
import json

def debug_gemini_api():
    """
    Diagnóstico completo da API do Google AI Studio
    """
    # CONFIGURAÇÃO - Substitua pela sua API key real
    API_KEY = "SUA_CHAVE_API_AQUI"  # ⚠️ ALTERE AQUI
    
    if API_KEY == "SUA_CHAVE_API_AQUI":
        print("❌ ERRO: Configure sua API key no arquivo debug_gemini.py")
        print("📍 Obtenha uma chave grátis em: https://aistudio.google.com")
        return False
    
    # Endpoint e modelo
    API_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models"
    API_MODEL = "gemini-1.5-pro"
    
    # Prompt de teste simples
    test_prompt = """Retorne apenas este JSON, sem formatação:
{
    "teste": "funcionando"
}"""
    
    try:
        print("🔍 DIAGNÓSTICO COMPLETO DA API GEMINI")
        print("=" * 60)
        print(f"🔑 API Key: {API_KEY[:10]}...")
        print(f"🎯 Modelo: {API_MODEL}")
        
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
        
        print(f"📡 URL: {url}")
        print(f"📦 Payload: {json.dumps(payload, indent=2)}")
        print()
        
        # Faz a requisição
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Response Headers: {dict(response.headers)}")
        print()
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Resposta recebida com sucesso!")
            print("📋 ESTRUTURA COMPLETA DA RESPOSTA:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            print()
            
            # Análise detalhada da estrutura
            print("🔍 ANÁLISE DA ESTRUTURA:")
            print("=" * 40)
            
            # Keys principais
            print(f"📄 Keys principais: {list(result.keys())}")
            
            # Candidates
            if 'candidates' in result:
                print(f"🎯 Candidates encontrados: {len(result['candidates'])}")
                for i, candidate in enumerate(result['candidates']):
                    print(f"  Candidate {i}:")
                    print(f"    Keys: {list(candidate.keys())}")
                    
                    if 'content' in candidate:
                        content = candidate['content']
                        print(f"    Content keys: {list(content.keys())}")
                        
                        if 'parts' in content:
                            parts = content['parts']
                            print(f"    Parts encontrados: {len(parts)}")
                            for j, part in enumerate(parts):
                                print(f"      Part {j}: {part}")
                        elif 'text' in content:
                            print(f"    Text direto: {content['text']}")
            
            # Verifica outras possíveis estruturas
            for key in result.keys():
                if key not in ['candidates', 'promptFeedback']:
                    print(f"⚠️  Key inesperada: {key} = {result[key]}")
            
            # Teste de extração
            print("\n🧪 TESTE DE EXTRAÇÃO:")
            print("=" * 30)
            
            try:
                if 'candidates' in result and len(result['candidates']) > 0:
                    candidate = result['candidates'][0]
                    
                    # Tenta extrair de 'content.parts.text'
                    if 'content' in candidate and 'parts' in candidate['content'] and len(candidate['content']['parts']) > 0:
                        text = candidate['content']['parts'][0]['text']
                        print(f"✅ Extraído via content.parts[0].text: {text}")
                        return True
                    
                    # Tenta extrair de 'content.text'
                    elif 'content' in candidate and 'text' in candidate['content']:
                        text = candidate['content']['text']
                        print(f"✅ Extraído via content.text: {text}")
                        return True
                    
                    # Tenta extrair de 'text'
                    elif 'text' in candidate:
                        text = candidate['text']
                        print(f"✅ Extraído via text direto: {text}")
                        return True
                    
                    else:
                        print(f"❌ Nenhum formato de texto encontrado")
                        return False
                else:
                    print(f"❌ Não há candidates na resposta")
                    return False
                    
            except Exception as e:
                print(f"❌ Erro na extração: {str(e)}")
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
    debug_gemini_api()

if __name__ == "__main__":
    main()