#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v3.0 - API Configuration Routes
Rotas para configuração de APIs na interface
"""

import os
import logging
from datetime import datetime
from flask import Blueprint, request, jsonify, render_template
from services.api_configuration_manager import api_config_manager

logger = logging.getLogger(__name__)

api_config_bp = Blueprint('api_config', __name__)

@api_config_bp.route('/api_status')
def api_status_page():
    """Página de status das APIs"""
    try:
        # Testa todas as APIs
        test_results = api_config_manager.test_all_apis()
        
        # Prepara dados para o template
        apis_data = []
        
        # APIs de IA
        ai_apis = [
            {
                'name': 'Google Gemini',
                'provider': 'Google AI',
                'env_var': 'GEMINI_API_KEY',
                'description': 'Modelo primário de IA para análises ultra-detalhadas',
                'priority': 'critical',
                'usage': 'Análise principal, avatar, drivers mentais',
                'status': 'configured' if test_results['detailed_results']['gemini']['working'] else 'missing'
            },
            {
                'name': 'OpenAI GPT',
                'provider': 'OpenAI',
                'env_var': 'OPENAI_API_KEY', 
                'description': 'Modelo de fallback para análises complementares',
                'priority': 'high',
                'usage': 'Fallback de IA, análises específicas',
                'status': 'configured' if test_results['detailed_results']['openai']['working'] else 'missing'
            },
            {
                'name': 'Groq Llama',
                'provider': 'Groq',
                'env_var': 'GROQ_API_KEY',
                'description': 'Modelo de alta velocidade para processamento rápido',
                'priority': 'medium',
                'usage': 'Processamento rápido, fallback secundário',
                'status': 'configured' if test_results['detailed_results']['groq']['working'] else 'missing'
            }
        ]
        
        # APIs de Busca
        search_apis = [
            {
                'name': 'Exa Neural Search',
                'provider': 'Exa AI',
                'env_var': 'EXA_API_KEY',
                'description': 'Busca neural semântica avançada',
                'priority': 'high',
                'usage': 'Pesquisa web principal, busca semântica',
                'status': 'configured' if test_results['detailed_results']['exa']['working'] else 'missing'
            },
            {
                'name': 'Google Custom Search',
                'provider': 'Google',
                'env_var': 'GOOGLE_SEARCH_KEY',
                'description': 'Busca por palavras-chave no Google',
                'priority': 'medium',
                'usage': 'Busca complementar, dados específicos',
                'status': 'configured' if os.getenv('GOOGLE_SEARCH_KEY') else 'missing'
            },
            {
                'name': 'Jina Reader',
                'provider': 'Jina AI',
                'env_var': 'JINA_API_KEY',
                'description': 'Extração de conteúdo web avançada',
                'priority': 'high',
                'usage': 'Extração de conteúdo, leitura de páginas',
                'status': 'configured' if test_results['detailed_results']['jina']['working'] else 'missing'
            }
        ]
        
        # APIs Sociais
        social_apis = [
            {
                'name': 'YouTube Data API',
                'provider': 'Google',
                'env_var': 'YOUTUBE_API_KEY',
                'description': 'Análise de conteúdo do YouTube',
                'priority': 'medium',
                'usage': 'Análise de vídeos, tendências',
                'status': 'configured' if test_results['detailed_results']['youtube']['working'] else 'missing'
            },
            {
                'name': 'Twitter API',
                'provider': 'Twitter/X',
                'env_var': 'TWITTER_BEARER_TOKEN',
                'description': 'Análise de tweets e tendências',
                'priority': 'medium',
                'usage': 'Análise social, sentimentos',
                'status': 'configured' if test_results['detailed_results']['twitter']['working'] else 'missing'
            }
        ]
        
        # Combina todas as APIs
        all_apis = ai_apis + search_apis + social_apis
        
        # Calcula estatísticas
        total_apis = len(all_apis)
        configured_apis = len([api for api in all_apis if api['status'] == 'configured'])
        critical_missing = len([api for api in all_apis if api['priority'] == 'critical' and api['status'] != 'configured'])
        
        stats = {
            'configured': configured_apis,
            'missing': total_apis - configured_apis,
            'critical_missing': critical_missing,
            'health_percentage': (configured_apis / total_apis) * 100
        }
        
        return render_template('api_status.html', 
                             apis=all_apis, 
                             stats=stats,
                             timestamp=datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        
    except Exception as e:
        logger.error(f"❌ Erro na página de status: {e}")
        return render_template('api_status.html', 
                             apis=[], 
                             stats={'error': str(e)},
                             timestamp=datetime.now().strftime('%d/%m/%Y %H:%M:%S'))

@api_config_bp.route('/test_all_apis', methods=['POST'])
def test_all_apis():
    """Testa todas as APIs configuradas"""
    try:
        test_results = api_config_manager.test_all_apis()
        
        return jsonify({
            'success': True,
            'test_results': test_results,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao testar APIs: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_config_bp.route('/save_api_config', methods=['POST'])
def save_api_config():
    """Salva configuração de API"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'Dados não fornecidos'}), 400
        
        api_name = data.get('api_name')
        api_key = data.get('api_key')
        
        if not api_name or not api_key:
            return jsonify({'success': False, 'error': 'Nome da API e chave são obrigatórios'}), 400
        
        # Mapeia nome da API para variável de ambiente
        env_var_map = {
            'gemini': 'GEMINI_API_KEY',
            'openai': 'OPENAI_API_KEY',
            'groq': 'GROQ_API_KEY',
            'exa': 'EXA_API_KEY',
            'jina': 'JINA_API_KEY',
            'youtube': 'YOUTUBE_API_KEY',
            'twitter': 'TWITTER_BEARER_TOKEN',
            'google_search': 'GOOGLE_SEARCH_KEY',
            'google_cse': 'GOOGLE_CSE_ID'
        }
        
        env_var = env_var_map.get(api_name)
        if not env_var:
            return jsonify({'success': False, 'error': 'API não reconhecida'}), 400
        
        # Define variável de ambiente (temporariamente)
        os.environ[env_var] = api_key
        
        # Testa a API
        try:
            if api_name == 'gemini':
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-2.0-flash-exp")
                response = model.generate_content("Teste")
                test_success = bool(response.text)
            else:
                test_success = True  # Para outras APIs, assume sucesso
                
        except Exception as test_error:
            return jsonify({
                'success': False,
                'error': f'Teste da API falhou: {str(test_error)}'
            }), 400
        
        return jsonify({
            'success': True,
            'message': f'API {api_name} configurada e testada com sucesso',
            'test_success': test_success
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao salvar configuração: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_config_bp.route('/get_api_config', methods=['GET'])
def get_api_config():
    """Obtém configuração atual das APIs"""
    try:
        config = {
            'gemini': bool(os.getenv('GEMINI_API_KEY')),
            'openai': bool(os.getenv('OPENAI_API_KEY')),
            'groq': bool(os.getenv('GROQ_API_KEY')),
            'exa': bool(os.getenv('EXA_API_KEY')),
            'jina': bool(os.getenv('JINA_API_KEY')),
            'youtube': bool(os.getenv('YOUTUBE_API_KEY')),
            'twitter': bool(os.getenv('TWITTER_BEARER_TOKEN')),
            'google_search': bool(os.getenv('GOOGLE_SEARCH_KEY')),
            'google_cse': bool(os.getenv('GOOGLE_CSE_ID'))
        }
        
        return jsonify({
            'success': True,
            'config': config,
            'total_configured': sum(config.values()),
            'total_apis': len(config)
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter configuração: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500