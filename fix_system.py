
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - System Fix Script
Script para corrigir erros do sistema automaticamente
"""

import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Função principal do script de correção"""
    
    print("🚀 ARQV30 Enhanced v2.0 - System Fix Script")
    print("=" * 50)
    
    try:
        # Importa e executa o validador
        from services.system_validator import system_validator
        
        print("🔍 Executando validação completa do sistema...")
        validation_result = system_validator.validate_all_systems()
        
        print("\n📊 RELATÓRIO DE SAÚDE DO SISTEMA:")
        print("=" * 50)
        health_report = system_validator.generate_health_report()
        print(health_report)
        
        # Verifica se há erros críticos
        critical_errors = validation_result.get('critical_errors', [])
        if critical_errors:
            print(f"\n🚨 ENCONTRADOS {len(critical_errors)} ERROS CRÍTICOS!")
            print("Resolva as configurações antes de continuar.")
            return 1
        
        print("\n✅ Sistema validado com sucesso!")
        print("🚀 Agora você pode executar o sistema normalmente.")
        
        # Testa o processador unificado
        print("\n🧪 Testando processador unificado de módulos...")
        try:
            from services.unified_module_processor import unified_module_processor
            print("✅ Processador unificado carregado com sucesso!")
            print(f"📦 {len(unified_module_processor.required_modules)} módulos registrados:")
            for module_name in unified_module_processor.required_modules.keys():
                print(f"   • {module_name}")
        except Exception as e:
            print(f"❌ Erro no processador unificado: {str(e)}")
            return 1
        
        return 0
        
    except Exception as e:
        print(f"❌ ERRO CRÍTICO: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
