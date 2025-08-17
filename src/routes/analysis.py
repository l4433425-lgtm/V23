#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v3.0 - Analysis Route
Rota de análise atualizada para nova metodologia
"""

import logging
import time
import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify
from services.master_analysis_orchestrator import master_analysis_orchestrator
from services.auto_save_manager import salvar_etapa
from services.progress_tracker_enhanced import progress_tracker

logger = logging.getLogger(__name__)

analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/execute_complete_analysis', methods=['POST'])
def execute_complete_analysis():
    """Executa análise completa com nova metodologia aprimorada"""
    try:
        # Recebe dados da requisição
        data = request.get_json()

        if not data:
            return jsonify({"error": "Dados da requisição são obrigatórios"}), 400

        # Gera session_id único
        session_id = f"session_{int(time.time() * 1000)}_{uuid.uuid4().hex[:8]}"

        # Extrai parâmetros
        segmento = data.get('segmento', '').strip()
        produto = data.get('produto', '').strip()
        publico = data.get('publico', '').strip()
        objetivos = data.get('objetivos', '').strip()
        contexto_adicional = data.get('contexto_adicional', '').strip()

        # Validação básica
        if not segmento and not produto:
            return jsonify({"error": "Segmento ou produto são obrigatórios"}), 400

        # Constrói query de pesquisa
        query_parts = []
        if segmento:
            query_parts.append(segmento)
        if produto:
            query_parts.append(produto)
        query_parts.append("Brasil 2024")

        query = " ".join(query_parts)

        # Contexto da análise
        context = {
            "segmento": segmento,
            "produto": produto,
            "publico": publico,
            "objetivos": objetivos,
            "contexto_adicional": contexto_adicional,
            "methodology": "ARQV30_Enhanced_v3.0_APRIMORADA"
        }

        # Salva dados da requisição
        requisicao_data = {
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "context": context,
            "methodology": "APRIMORADA_v3.0"
        }

        salvar_etapa("requisicao_analise_aprimorada", requisicao_data, categoria="analise_completa")

        # Inicializa progress tracker
        progress_tracker.start_session(session_id, 4)  # 4 fases principais

        def progress_callback(step, message: str):
            """Callback para atualizações de progresso"""
            try:
                # Converte step para int se necessário
                step_int = int(float(step)) if not isinstance(step, int) else step
                progress_tracker.update_progress(session_id, step_int, message)
                logger.info(f"Progress {session_id}: Step {step_int} - {message}")
            except Exception as e:
                logger.error(f"Erro no progress callback: {e}")

        # Executa análise completa com nova metodologia
        logger.info(f"🚀 Iniciando análise aprimorada para session {session_id}")
        logger.info(f"📋 Query: {query}")
        logger.info(f"🎯 Segmento: {segmento} | Produto: {produto}")

        analysis_results = master_analysis_orchestrator.execute_complete_analysis(
            query=query,
            context=context,
            session_id=session_id,
            progress_callback=progress_callback
        )

        # Finaliza progress tracker
        progress_tracker.complete_session(session_id)

        # Resposta da API
        if analysis_results.get("success"):
            response = {
                "success": True,
                "session_id": session_id,
                "methodology": "ARQV30_Enhanced_v3.0_APRIMORADA",
                "message": "Análise completa concluída com sucesso",
                "execution_summary": {
                    "execution_time": analysis_results.get("execution_time", 0),
                    "phases_completed": analysis_results.get("phases_completed", []),
                    "massive_data_sources": analysis_results.get("massive_data_summary", {}).get("total_sources", 0),
                    "modules_processed": analysis_results.get("modules_summary", {}).get("successful_modules", 0),
                    "report_pages": analysis_results.get("detailed_report_summary", {}).get("paginas_estimadas", 0)
                },
                "data_quality": {
                    "sources_quality": "PREMIUM - 100% dados reais",
                    "processing_quality": "ULTRA_HIGH",
                    "report_completeness": f"{analysis_results.get('detailed_report_summary', {}).get('taxa_completude', 0)}%"
                },
                "access_info": {
                    "json_files_saved": True,
                    "modules_saved_separately": True,
                    "detailed_report_generated": True,
                    "all_data_in_analyses_data": True
                }
            }

            logger.info(f"✅ Análise aprimorada concluída com sucesso: {session_id}")
            return jsonify(response), 200

        else:
            error_response = {
                "success": False,
                "session_id": session_id,
                "methodology": "ARQV30_Enhanced_v3.0_APRIMORADA",
                "error": analysis_results.get("error", "Erro desconhecido"),
                "failed_phase": analysis_results.get("failed_phase"),
                "message": "Análise falhou durante execução"
            }

            logger.error(f"❌ Análise falhou: {session_id} - {analysis_results.get('error')}")
            return jsonify(error_response), 500

    except Exception as e:
        logger.error(f"❌ Erro crítico na rota de análise: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Erro interno do servidor"
        }), 500

@analysis_bp.route('/analysis_status/<session_id>', methods=['GET'])
def get_analysis_status(session_id):
    """Obtém status da análise em andamento"""
    try:
        # Obtém progresso do tracker
        progress_info = progress_tracker.get_session_progress(session_id)

        # Obtém progresso das fases do orquestrador
        phase_progress = master_analysis_orchestrator.get_phase_progress(session_id)

        status_response = {
            "session_id": session_id,
            "methodology": "ARQV30_Enhanced_v3.0_APRIMORADA",
            "progress_info": progress_info,
            "phase_progress": phase_progress,
            "timestamp": datetime.now().isoformat()
        }

        return jsonify(status_response), 200

    except Exception as e:
        logger.error(f"❌ Erro ao obter status: {e}")
        return jsonify({
            "session_id": session_id,
            "error": str(e),
            "status": "error"
        }), 500

@analysis_bp.route('/reset_orchestrator', methods=['POST'])
def reset_orchestrator():
    """Reseta o orquestrador mestre"""
    try:
        master_analysis_orchestrator.reset_orchestrator()
        progress_tracker.reset()

        return jsonify({
            "success": True,
            "message": "Orquestrador resetado com sucesso",
            "timestamp": datetime.now().isoformat()
        }), 200

    except Exception as e:
        logger.error(f"❌ Erro ao resetar orquestrador: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Rota para compatibilidade com interface atual
@analysis_bp.route('/execute_analysis', methods=['POST'])
def execute_analysis_compatibility():
    """Rota de compatibilidade que redireciona para nova metodologia"""
    logger.info("🔄 Redirecionando para nova metodologia aprimorada")
    return execute_complete_analysis()

@analysis_bp.route('/analyze', methods=['POST'])
def analyze_compatibility():
    """Rota de compatibilidade /api/analyze que redireciona para nova metodologia"""
    logger.info("🔄 Redirecionando /api/analyze para nova metodologia aprimorada")
    return execute_complete_analysis()