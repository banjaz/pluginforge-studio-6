#!/usr/bin/env python3
# ========================================
# TESTE DO MAVEN
# ========================================
# Script para testar se o Maven está funcionando corretamente
# Execute: python test_maven.py
# ========================================

import subprocess
import os
import shutil
from pathlib import Path

def test_maven_installation():
    """
    Testa a instalação do Maven de forma abrangente.
    """
    print("=" * 60)
    print("🔨 TESTE DE INSTALAÇÃO DO MAVEN")
    print("=" * 60)
    
    # Lista de possíveis comandos Maven
    maven_commands = [
        'mvn',                                    # PATH padrão
        '/usr/local/bin/mvn',                     # Homebrew (macOS)
        '/opt/homebrew/bin/mvn',                  # Homebrew ARM (macOS)
        '/usr/bin/mvn',                           # APT (Linux)
        '/opt/maven/bin/mvn',                     # Maven manual (Linux)
        '/snap/bin/mvn',                          # Snap (Linux)
        str(Path.home() / 'maven/bin/mvn'),       # Maven instalado em home
    ]
    
    found_maven = False
    
    for cmd in maven_commands:
        print(f"🔍 Testando: {cmd}")
        
        try:
            # Teste 1: Verifica se o comando existe
            result = subprocess.run(
                [cmd, '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                print(f"✅ Maven funcionando: {cmd}")
                print(f"📋 Versão: {result.stdout.strip()}")
                found_maven = True
                
                # Teste adicional: verifica PATH e Java
                test_maven_path(cmd)
                break
            else:
                print(f"❌ Comando falhou: {cmd}")
                
        except subprocess.TimeoutExpired:
            print(f"⏰ Timeout: {cmd}")
        except FileNotFoundError:
            print(f"❌ Comando não encontrado: {cmd}")
        except Exception as e:
            print(f"❌ Erro inesperado: {cmd} - {str(e)}")
    
    return found_maven

def test_maven_path(cmd):
    """
    Testa detalhes adicionais do Maven.
    """
    try:
        print(f"🔍 Verificando ambiente Maven: {cmd}")
        
        # Teste Java
        java_result = subprocess.run(['java', '--version'], capture_output=True, text=True, timeout=5)
        if java_result.returncode == 0:
            print(f"☕ Java detectado: {java_result.stdout.strip().split()[0]}")
        else:
            print("⚠️  Java não detectado ou não no PATH")
        
        # Teste Maven no PATH atual
        mvn_path_result = subprocess.run(['which', 'mvn'], capture_output=True, text=True, timeout=5)
        if mvn_path_result.returncode == 0:
            print(f"📍 Maven no PATH: {mvn_path_result.stdout.strip()}")
        else:
            print("⚠️  Maven não está no PATH global")
            
    except Exception as e:
        print(f"⚠️  Erro ao verificar ambiente: {str(e)}")

def test_docker_maven():
    """
    Testa Maven via Docker como alternativa.
    """
    print("\n🐳 Testando Maven via Docker...")
    
    try:
        docker_result = subprocess.run(['docker', '--version'], capture_output=True, text=True, timeout=5)
        if docker_result.returncode == 0:
            print(f"✅ Docker detectado: {docker_result.stdout.strip()}")
            
            # Testa Maven container
            maven_docker_test = subprocess.run([
                'docker', 'run', '--rm', 'maven:3.9-eclipse-temurin-17-alpine', 'mvn', '--version'
            ], capture_output=True, text=True, timeout=30)
            
            if maven_docker_test.returncode == 0:
                print("✅ Maven Docker funcionando!")
                print(f"📋 Versão Docker Maven: {maven_docker_test.stdout.strip()}")
                return True
            else:
                print(f"❌ Maven Docker falhou: {maven_docker_test.stderr}")
                return False
        else:
            print("❌ Docker não detectado")
            return False
            
    except FileNotFoundError:
        print("❌ Docker não está instalado")
        return False
    except Exception as e:
        print(f"❌ Erro ao testar Docker: {str(e)}")
        return False

def main():
    """
    Função principal de teste.
    """
    
    # Teste Maven local
    maven_works = test_maven_installation()
    
    # Teste Docker se Maven local falhar
    docker_works = False
    if not maven_works:
        docker_works = test_docker_maven()
    
    print("\n" + "=" * 60)
    print("📊 RESULTADO DO TESTE")
    print("=" * 60)
    
    if maven_works:
        print("✅ Maven local está funcionando!")
        print("🎉 O PluginForge Studio deve funcionar normalmente.")
        
    elif docker_works:
        print("⚠️  Maven local não encontrado, mas Docker Maven funciona.")
        print("💡 O PluginForge Studio usará Docker como fallback.")
        
    else:
        print("❌ Maven não está funcionando!")
        print("📋 SOLUÇÕES:")
        print("   1. Instale o Maven: https://maven.apache.org/install.html")
        print("   2. Instale via package manager:")
        print("      - macOS: brew install maven")
        print("      - Ubuntu: sudo apt install maven")
        print("   3. Ou instale o Docker: https://docs.docker.com/get-docker/")
        
    print("=" * 60)
    
    return maven_works or docker_works

if __name__ == "__main__":
    main()