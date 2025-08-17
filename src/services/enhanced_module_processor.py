#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v3.0 - Enhanced Module Processor
Processador de módulos que trabalha com o JSON gigante
"""
import os
import logging
import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import Counter
from services.ai_manager import ai_manager
from services.auto_save_manager import salvar_etapa

logger = logging.getLogger(__name__)

class EnhancedModuleProcessor:
    """Processador aprimorado que usa dados do JSON gigante"""
    def __init__(self):
        """Inicializa o processador de módulos aprimorado"""
        self.required_modules = [
            'avatars',
            'drivers_mentais',
            'anti_objecao',
            'provas_visuais',
            'pre_pitch',
            'predicoes_futuro',
            'posicionamento',
            'concorrencia',
            'palavras_chave',
            'funil_vendas',
            'insights',
            'plano_acao'
        ]
        self.processed_modules = {}
        # Stopwords básicas em português para análise de texto
        self.stopwords = {
            "de", "a", "o", "que", "e", "do", "da", "em", "um", "para", "com", "não", "uma", "os", "no", "se",
            "na", "por", "mais", "as", "dos", "como", "mas", "ao", "ele", "das", "seu", "sua", "ou", "quando",
            "muito", "nos", "já", "eu", "também", "só", "pelo", "pela", "até", "isso", "ela", "entre", "era",
            "depois", "sem", "mesmo", "aos", "seus", "quem", "nas", "me", "esse", "eles", "você", "essa",
            "num", "nem", "suas", "meu", "às", "minha", "numa", "pelos", "elas", "qual", "nós", "lhe",
            "deles", "essas", "esses", "pelas", "este", "dele", "tu", "te", "vocês", "vos", "lhes", "meus",
            "minhas", "teu", "tua", "teus", "tuas", "nosso", "nossa", "nossos", "nossas", "dela", "delas",
            "esta", "estes", "estas", "aquele", "aquela", "aqueles", "aquelas", "isto", "aquilo", "estou",
            "está", "estamos", "estão", "estive", "esteve", "estivemos", "estiveram", "estava", "estávamos",
            "estavam", "estivera", "estivéramos", "esteja", "estejamos", "estejam", "estivesse", "estivéssemos",
            "estivessem", "estiver", "estivermos", "estiverem", "hei", "há", "havemos", "hão", "houve",
            "houvemos", "houveram", "houvera", "houvéramos", "haja", "hajamos", "hajam", "houvesse",
            "houvéssemos", "houvessem", "houver", "houvermos", "houverem", "houverei", "houverá", "houveremos",
            "houverão", "houveria", "houveríamos", "houveriam", "sou", "somos", "são", "era", "éramos",
            "eram", "fui", "foi", "fomos", "foram", "fora", "fôramos", "seja", "sejamos", "sejam", "fosse",
            "fôssemos", "fossem", "for", "formos", "forem", "serei", "será", "seremos", "serão", "seria",
            "seríamos", "seriam", "tenho", "tem", "temos", "tém", "tinha", "tínhamos", "tinham", "tive",
            "teve", "tivemos", "tiveram", "tivera", "tivéramos", "tenha", "tenhamos", "tenham", "tivesse",
            "tivéssemos", "tivessem", "tiver", "tivermos", "tiverem", "terei", "terá", "teremos", "terão",
            "teria", "teríamos", "teriam"
        }
        logger.info("🔧 Enhanced Module Processor inicializado")

    def process_all_modules_from_massive_data(
        self,
        massive_data: Dict[str, Any],
        context: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """Processa todos os módulos usando dados do JSON gigante"""
        logger.info("🚀 INICIANDO PROCESSAMENTO DE TODOS OS MÓDULOS COM DADOS MASSIVOS")
        processing_results = {
            "session_id": session_id,
            "processing_started": datetime.now().isoformat(),
            "modules_data": {},
            "processing_summary": {},
            "massive_data_stats": massive_data.get("statistics", {})
        }
        # Processa cada módulo sequencialmente
        for module_name in self.required_modules:
            try:
                logger.info(f"📦 Processando módulo: {module_name}")
                module_result = self._process_single_module(
                    module_name, massive_data, context, session_id
                )
                if module_result:
                    processing_results["modules_data"][module_name] = module_result
                    self._save_module_json(module_name, module_result, session_id)
                    logger.info(f"✅ Módulo {module_name} processado com sucesso")
                else:
                    logger.error(f"❌ Falha ao processar módulo {module_name}")
            except Exception as e:
                logger.error(f"❌ Erro no módulo {module_name}: {e}")
                processing_results["modules_data"][module_name] = {"error": str(e)}

        # Gera sumário do processamento
        processing_results["processing_summary"] = self._generate_processing_summary(processing_results)
        processing_results["processing_completed"] = datetime.now().isoformat()
        logger.info(f"✅ PROCESSAMENTO COMPLETO: {len(processing_results['modules_data'])} módulos")
        return processing_results

    def _process_single_module(
        self,
        module_name: str,
        massive_data: Dict[str, Any],
        context: Dict[str, Any],
        session_id: str
    ) -> Optional[Dict[str, Any]]:
        """Processa um único módulo usando dados massivos"""
        # Mapeia método de processamento para cada módulo
        processing_methods = {
            'avatars': self._process_avatars_module,
            'drivers_mentais': self._process_drivers_mentais_module,
            'anti_objecao': self._process_anti_objecao_module,
            'provas_visuais': self._process_provas_visuais_module,
            'pre_pitch': self._process_pre_pitch_module,
            'predicoes_futuro': self._process_predicoes_futuro_module,
            'posicionamento': self._process_posicionamento_module,
            'concorrencia': self._process_concorrencia_module,
            'palavras_chave': self._process_palavras_chave_module,
            'funil_vendas': self._process_funil_vendas_module,
            'insights': self._process_insights_module,
            'plano_acao': self._process_plano_acao_module
        }
        if module_name in processing_methods:
            return processing_methods[module_name](massive_data, context, session_id)
        else:
            logger.error(f"❌ Método de processamento não encontrado para {module_name}")
            return None

    def _process_avatars_module(self, massive_data: Dict[str, Any], context: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Processa módulo de avatars usando dados massivos"""
        # Extrai dados relevantes do JSON gigante
        social_insights = self._extract_social_insights(massive_data)
        web_insights = self._extract_web_insights(massive_data)
        content_analysis = self._extract_content_analysis(massive_data)
        avatar_prompt = f"""
        Baseado nos dados massivos coletados, crie um avatar ultra-detalhado para o segmento "{context.get('segmento', '')}" e produto "{context.get('produto', '')}".
        DADOS COLETADOS:
        REDES SOCIAIS:
        - Total de posts analisados: {social_insights.get('total_posts', 0)}
        - Plataformas ativas: {social_insights.get('platforms_active', 0)}
        - Sentimento geral: {social_insights.get('sentiment', 'neutro')}
        - Tópicos trending: {social_insights.get('trending_topics', [])}
        - Comentários mais frequentes: {social_insights.get('frequent_comments', [])}
        PESQUISA WEB:
        - Total de fontes web: {web_insights.get('total_sources', 0)}
        - Qualidade média das fontes: {web_insights.get('avg_quality', 0)}
        - Principais domínios: {web_insights.get('top_domains', [])}
        ANÁLISE DE CONTEÚDO:
        - Total de conteúdo extraído: {content_analysis.get('total_content_length', 0)} caracteres
        - Número de documentos: {content_analysis.get('documents_count', 0)}
        - Temas principais identificados: {content_analysis.get('main_themes', [])}
        - Palavras-chave mais relevantes: {content_analysis.get('key_terms', [])}
        Crie um avatar que inclua:
        1. DEMOGRAFIA ULTRA-DETALHADA
           - Idade específica e faixa
           - Localização geográfica
           - Renda e classe social
           - Educação e profissão
           - Estado civil e família
        2. PSICOGRAFIA PROFUNDA
           - Valores e crenças centrais
           - Medos e inseguranças específicos
           - Aspirações e sonhos
           - Personalidade e comportamento
           - Estilo de vida e hobbies
        3. COMPORTAMENTO DIGITAL
           - Plataformas mais utilizadas
           - Horários de maior atividade
           - Tipo de conteúdo consumido
           - Influenciadores seguidos
           - Padrões de compra online
        4. DORES E NECESSIDADES VISCERAIS
           - Principais problemas enfrentados
           - Consequências dos problemas
           - Tentativas frustradas de solução
           - Gatilhos emocionais
           - Urgência das necessidades
        5. JORNADA DE COMPRA DETALHADA
           - Processo de tomada de decisão
           - Fontes de informação utilizadas
           - Objeções mais comuns
           - Critérios de escolha
           - Momentos de maior receptividade
        Responda em formato JSON estruturado.
        """
        try:
            avatar_result = ai_manager.generate_content(avatar_prompt, max_tokens=4000)
            # Tentar parsear o resultado como JSON
            try:
                parsed_result = json.loads(avatar_result)
            except json.JSONDecodeError:
                logger.error(f"❌ Avatar result is not valid JSON: {avatar_result[:200]}...")
                parsed_result = {"raw_output": avatar_result}

            return {
                "module": "avatars",
                "avatar_ultra_detalhado": parsed_result,
                "data_sources_used": {
                    "social_posts": social_insights.get('total_posts', 0),
                    "web_sources": web_insights.get('total_sources', 0),
                    "content_documents": content_analysis.get('documents_count', 0)
                },
                "insights_foundation": {
                    "social_insights": social_insights,
                    "web_insights": web_insights,
                    "content_analysis": content_analysis
                },
                "generated_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"❌ Erro no processamento do avatar: {e}")
            return {"error": str(e), "module": "avatars"}

    def _process_drivers_mentais_module(self, massive_data: Dict[str, Any], context: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Processa módulo de drivers mentais usando dados massivos"""
        content_insights = self._extract_detailed_content_insights(massive_data)
        psychological_patterns = self._extract_psychological_patterns(massive_data)
        drivers_prompt = f"""
        Baseado na análise massiva de dados coletados, crie 19 drivers mentais personalizados para o segmento "{context.get('segmento', '')}" e produto "{context.get('produto', '')}".
        INSIGHTS DE CONTEÚDO MASSIVO:
        - Palavras-chave mais frequentes: {content_insights.get('top_keywords', [])}
        - Temas emocionais identificados: {content_insights.get('emotional_themes', [])}
        - Padrões de linguagem: {content_insights.get('language_patterns', [])}
        PADRÕES PSICOLÓGICOS IDENTIFICADOS:
        - Medos mais comuns: {psychological_patterns.get('common_fears', [])}
        - Desejos predominantes: {psychological_patterns.get('dominant_desires', [])}
        - Gatilhos de urgência: {psychological_patterns.get('urgency_triggers', [])}
        - Motivadores de ação: {psychological_patterns.get('action_motivators', [])}
        Para cada um dos 19 drivers mentais, forneça:
        1. NOME do driver
        2. GATILHO CENTRAL específico
        3. DEFINIÇÃO VISCERAL que conecta emocionalmente
        4. APLICAÇÃO PRÁTICA no contexto do produto/segmento
        5. FRASES DE ANCORAGEM (3 frases prontas para usar)
        6. CONTEXTOS DE USO específicos
        7. INTENSIDADE EMOCIONAL (escala 1-10)
        8. COMPATIBILIDADE com outros drivers
        Baseie os drivers nos insights reais extraídos dos dados massivos coletados.
        Responda em formato JSON estruturado.
        """
        try:
            drivers_result = ai_manager.generate_content(drivers_prompt, max_tokens=5000)
            # Tentar parsear o resultado como JSON
            try:
                parsed_result = json.loads(drivers_result)
            except json.JSONDecodeError:
                logger.error(f"❌ Drivers result is not valid JSON: {drivers_result[:200]}...")
                parsed_result = {"raw_output": drivers_result}
            return {
                "module": "drivers_mentais",
                "drivers_mentais_arsenal": parsed_result,
                "data_foundation": {
                    "content_insights": content_insights,
                    "psychological_patterns": psychological_patterns,
                    "total_sources_analyzed": massive_data.get("statistics", {}).get("total_sources", 0)
                },
                "customization_level": "ULTRA_PERSONALIZADO",
                "generated_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"❌ Erro no processamento dos drivers: {e}")
            return {"error": str(e), "module": "drivers_mentais"}

    def _process_anti_objecao_module(self, massive_data: Dict[str, Any], context: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Processa módulo anti-objeção usando dados massivos"""
        objections_patterns = self._extract_objection_patterns(massive_data)
        competitor_analysis = self._extract_competitor_insights(massive_data)
        anti_objection_prompt = f"""
        Baseado na análise massiva de dados, crie um sistema anti-objeção completo para "{context.get('segmento', '')}" vendendo "{context.get('produto', '')}".
        PADRÕES DE OBJEÇÕES IDENTIFICADOS:
        - Objeções mais frequentes encontradas: {objections_patterns.get('common_objections', [])}
        - Preocupações do público-alvo: {objections_patterns.get('target_concerns', [])}
        - Pontos de resistência: {objections_patterns.get('resistance_points', [])}
        ANÁLISE COMPETITIVA:
        - Como concorrentes lidam com objeções: {competitor_analysis.get('competitor_approaches', [])}
        - Lacunas identificadas: {competitor_analysis.get('market_gaps', [])}
        - Oportunidades de diferenciação: {competitor_analysis.get('differentiation_opportunities', [])}
        Crie um sistema que inclua:
        1. MAPEAMENTO COMPLETO DAS OBJEÇÕES
           - Top 15 objeções mais prováveis
           - Categorização por tipo e intensidade
           - Momento provável de surgimento
        2. ESTRATÉGIAS DE NEUTRALIZAÇÃO
           - Técnica específica para cada objeção
           - Scripts de resposta testados
           - Reframes poderosos
        3. PREVENÇÃO PROATIVA
           - Como evitar que objeções surjam
           - Elementos de credibilidade necessários
           - Provas sociais específicas
        4. SCRIPTS PERSONALIZADOS
           - Linguagem adaptada ao público
           - Variações para diferentes contextos
           - Técnicas de fechamento pós-objeção
        Responda em formato JSON estruturado.
        """
        try:
            anti_objection_result = ai_manager.generate_content(anti_objection_prompt, max_tokens=4500)
            # Tentar parsear o resultado como JSON
            try:
                parsed_result = json.loads(anti_objection_result)
            except json.JSONDecodeError:
                logger.error(f"❌ Anti-objection result is not valid JSON: {anti_objection_result[:200]}...")
                parsed_result = {"raw_output": anti_objection_result}
            return {
                "module": "anti_objecao",
                "sistema_anti_objecao": parsed_result,
                "analysis_foundation": {
                    "objections_patterns": objections_patterns,
                    "competitor_analysis": competitor_analysis,
                    "data_sources": massive_data.get("statistics", {}).get("sources_by_type", {})
                },
                "coverage_level": "COMPLETA",
                "generated_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"❌ Erro no processamento anti-objeção: {e}")
            return {"error": str(e), "module": "anti_objecao"}

    def _process_provas_visuais_module(self, massive_data: Dict[str, Any], context: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Processa módulo de provas visuais usando dados massivos"""
        visual_patterns = self._extract_visual_patterns(massive_data)
        engagement_data = self._extract_engagement_insights(massive_data)
        provas_visuais_prompt = f"""
        Baseado nos dados massivos coletados, crie um arsenal de provas visuais para "{context.get('segmento', '')}" e produto "{context.get('produto', '')}".
        PADRÕES VISUAIS IDENTIFICADOS:
        - Tipos de conteúdo com maior engajamento: {visual_patterns.get('high_engagement_content', [])}
        - Formatos visuais mais eficazes: {visual_patterns.get('effective_formats', [])}
        - Elementos visuais recorrentes: {visual_patterns.get('recurring_elements', [])}
        DADOS DE ENGAJAMENTO:
        - Métricas de performance por tipo: {engagement_data.get('performance_by_type', {})}
        - Horários de maior engajamento: {engagement_data.get('peak_hours', [])}
        - Plataformas mais responsivas: {engagement_data.get('responsive_platforms', [])}
        Crie 8 tipos de provas visuais:
        1. PROVA DE RESULTADO (antes/depois)
        2. PROVA SOCIAL (depoimentos visuais)
        3. PROVA DE AUTORIDADE (credenciais)
        4. PROVA DE URGÊNCIA (escassez visual)
        5. PROVA DE VALOR (comparações)
        6. PROVA DE PROCESSO (demonstrações)
        7. PROVA DE CREDIBILIDADE (certificações)
        8. PROVA EMOCIONAL (stories visuais)
        Para cada prova visual, forneça:
        - Objetivo psicológico específico
        - Elementos visuais necessários
        - Copy sugerida
        - Contextos de uso ideais
        - Métricas de success esperadas
        - Variações para diferentes plataformas
        Responda em formato JSON estruturado.
        """
        try:
            provas_visuais_result = ai_manager.generate_content(provas_visuais_prompt, max_tokens=4000)
            # Tentar parsear o resultado como JSON
            try:
                parsed_result = json.loads(provas_visuais_result)
            except json.JSONDecodeError:
                logger.error(f"❌ Provas visuais result is not valid JSON: {provas_visuais_result[:200]}...")
                parsed_result = {"raw_output": provas_visuais_result}
            return {
                "module": "provas_visuais",
                "arsenal_provas_visuais": parsed_result,
                "visual_foundation": {
                    "visual_patterns": visual_patterns,
                    "engagement_data": engagement_data,
                    "platforms_analyzed": list(massive_data.get("social_media_data", {}).get("all_platforms_data", {}).get("platforms", {}).keys())
                },
                "customization_level": "ULTRA_SEGMENTADA",
                "generated_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"❌ Erro no processamento das provas visuais: {e}")
            return {"error": str(e), "module": "provas_visuais"}

    def _process_predicoes_futuro_module(self, massive_data: Dict[str, Any], context: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Processa módulo de predições futuras usando dados massivos"""
        trends_analysis = self._extract_trends_analysis(massive_data)
        market_signals = self._extract_market_signals(massive_data)
        predicoes_prompt = f"""
        Baseado na análise massiva de dados coletados, crie predições futuras detalhadas para o mercado de "{context.get('segmento', '')}" e produto "{context.get('produto', '')}".
        ANÁLISE DE TENDÊNCIAS:
        - Tendências emergentes identificadas: {trends_analysis.get('emerging_trends', [])}
        - Padrões de crescimento: {trends_analysis.get('growth_patterns', [])}
        - Mudanças comportamentais: {trends_analysis.get('behavioral_changes', [])}
        SINAIS DE MERCADO:
        - Indicadores de demanda: {market_signals.get('demand_indicators', [])}
        - Movimentações competitivas: {market_signals.get('competitive_movements', [])}
        - Fatores disruptivos: {market_signals.get('disruptive_factors', [])}
        Crie predições para:
        1. PRÓXIMOS 6 MESES
           - Oportunidades imediatas
           - Ameaças a considerar
           - Movimentos estratégicos recomendados
        2. PRÓXIMO ANO
           - Mudanças estruturais esperadas
           - Novos players no mercado
           - Evolução das necessidades do cliente
        3. PRÓXIMOS 2-3 ANOS
           - Transformações do setor
           - Tecnologias disruptivas
           - Novos modelos de negócio
        4. CENÁRIOS POSSÍVEIS
           - Melhor cenário (otimista)
           - Cenário mais provável (realista)
           - Pior cenário (pessimista)
        Para cada predição, inclua:
        - Probabilidade de ocorrência (%)
        - Impacto no negócio (escala 1-10)
        - Sinais de confirmação a observar
        - Ações preparatórias recomendadas
        Responda em formato JSON estruturado.
        """
        try:
            predicoes_result = ai_manager.generate_content(predicoes_prompt, max_tokens=4500)
            # Tentar parsear o resultado como JSON
            try:
                parsed_result = json.loads(predicoes_result)
            except json.JSONDecodeError:
                logger.error(f"❌ Predições result is not valid JSON: {predicoes_result[:200]}...")
                parsed_result = {"raw_output": predicoes_result}
            return {
                "module": "predicoes_futuro",
                "predicoes_detalhadas": parsed_result,
                "analysis_foundation": {
                    "trends_analysis": trends_analysis,
                    "market_signals": market_signals,
                    "data_timespan": "Dados coletados em tempo real",
                    "confidence_level": "ALTO"
                },
                "prediction_horizon": "6_meses_a_3_anos",
                "generated_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"❌ Erro no processamento das predições: {e}")
            return {"error": str(e), "module": "predicoes_futuro"}

    # Métodos auxiliares para extrair insights dos dados massivos
    def _extract_social_insights(self, massive_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai insights das redes sociais"""
        social_data = massive_data.get("social_media_data", {})
        insights = {
            "total_posts": 0,
            "platforms_active": 0,
            "sentiment": "neutro",
            "trending_topics": [],
            "frequent_comments": []
        }
        # Dados das plataformas
        platforms_data = social_data.get("all_platforms_data", {}).get("platforms", {})
        insights["platforms_active"] = len([p for p in platforms_data.values() if p.get("results")])
        
        all_comments = []
        for platform_data in platforms_data.values():
            results = platform_data.get("results", [])
            insights["total_posts"] += len(results)
            for post in results:
                # Extrai comentários se existirem
                comments = post.get("comments", [])
                all_comments.extend([c.get("text", "") for c in comments if isinstance(c, dict)])
        
        # Análise de sentimento
        sentiment_data = social_data.get("sentiment_analysis", {})
        if sentiment_data.get("overall_sentiment"):
            insights["sentiment"] = sentiment_data["overall_sentiment"]
        
        # Trending topics - usando palavras-chave de trending topics
        trending_data = social_data.get("trending_topics", {})
        keywords_freq = trending_data.get("keywords_frequency", {})
        insights["trending_topics"] = list(keywords_freq.keys())[:5]
        
        # Comentários frequentes
        if all_comments:
            # Limpa e conta comentários
            cleaned_comments = [re.sub(r'[^\w\s]', '', c.lower()) for c in all_comments if len(c.split()) > 2]
            comment_counter = Counter(cleaned_comments)
            insights["frequent_comments"] = [comment for comment, count in comment_counter.most_common(5)]

        return insights

    def _extract_web_insights(self, massive_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai insights da busca web"""
        web_data = massive_data.get("web_search_data", {})
        insights = {
            "total_sources": 0,
            "avg_quality": 0,
            "top_domains": []
        }
        # Conta fontes
        enhanced_results = web_data.get("enhanced_search_results", {})
        exa_results = enhanced_results.get("exa_results", [])
        google_results = enhanced_results.get("google_results", [])
        insights["total_sources"] += len(exa_results)
        insights["total_sources"] += len(google_results)
        
        # Extrai domínios principais
        domains = []
        for result in exa_results:
            if result.get("url"):
                domain = result["url"].split("/")[2] if "/" in result["url"] else ""
                if domain:
                    domains.append(domain)
        insights["top_domains"] = list(set(domains))[:5]
        
        # Qualidade média (placeholder)
        insights["avg_quality"] = 7.5 # Valor estimado
        return insights

    def _extract_content_analysis(self, massive_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai análise do conteúdo extraído"""
        extracted_content = massive_data.get("extracted_content", [])
        analysis = {
            "documents_count": len(extracted_content),
            "total_content_length": massive_data.get("statistics", {}).get("total_content_length", 0),
            "main_themes": [],
            "key_terms": []
        }
        # Análise básica de temas
        if extracted_content:
            all_content = " ".join([item.get("content", "")[:500] for item in extracted_content[:10]])
            words = re.findall(r'\b\w+\b', all_content.lower())
            # Filtra stopwords
            filtered_words = [word for word in words if len(word) > 4 and word not in self.stopwords]
            word_freq = Counter(filtered_words)
            sorted_words = word_freq.most_common(10)
            analysis["main_themes"] = [word for word, count in sorted_words]
            analysis["key_terms"] = [word for word, count in sorted_words[:5]]
        return analysis

    def _extract_detailed_content_insights(self, massive_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai insights detalhados do conteúdo"""
        extracted_content = massive_data.get("extracted_content", [])
        keywords = []
        emotional_themes = []
        language_patterns = []
        
        if extracted_content:
            combined_text = " ".join([item.get("content", "")[:1000] for item in extracted_content[:20]])
            words = re.findall(r'\b\w+\b', combined_text.lower())
            
            # Filtra stopwords e palavras curtas
            filtered_words = [word for word in words if len(word) > 3 and word not in self.stopwords]
            word_freq = Counter(filtered_words)
            top_keywords = [word for word, count in word_freq.most_common(15)]
            keywords.extend(top_keywords)
            
            # Detecta padrões de linguagem comuns
            common_patterns = ["como", "você", "pode", "imagine", "descubra", "garanta", "agora", "hoje"]
            language_patterns = [p for p in common_patterns if p in combined_text.lower()]
            
            # Detecta temas emocionais comuns
            emotional_indicators = {
                "urgência": ["urgente", "agora", "hoje", "limitado", "última chance"],
                "confiança": ["confie", "garantia", "prova", "certeza"],
                "sucesso": ["sucesso", "transformação", "resultados", "atingir"],
                "transformação": ["transformação", "mudança", "evolução", "crescimento"]
            }
            for theme, indicators in emotional_indicators.items():
                if any(indicator in combined_text.lower() for indicator in indicators):
                    emotional_themes.append(theme)

        return {
            "top_keywords": list(set(keywords)),
            "emotional_themes": list(set(emotional_themes)),
            "language_patterns": list(set(language_patterns))
        }

    def _extract_psychological_patterns(self, massive_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai padrões psicológicos dos dados"""
        social_data = massive_data.get("social_media_data", {})
        extracted_content = massive_data.get("extracted_content", [])
        
        common_fears = []
        dominant_desires = []
        urgency_triggers = []
        action_motivators = []
        
        # Analisa comentários de redes sociais para medos e desejos
        platforms_data = social_data.get("all_platforms_data", {}).get("platforms", {})
        all_comments = []
        for platform_data in platforms_data.values():
            results = platform_data.get("results", [])
            for post in results:
                comments = post.get("comments", [])
                all_comments.extend([c.get("text", "") for c in comments if isinstance(c, dict)])
        
        combined_text = " ".join(all_comments[:1000]) + " " + " ".join([item.get("content", "")[:500] for item in extracted_content[:10]])
        
        # Detecta padrões psicológicos
        fear_indicators = {
            "fracasso": ["fracasso", "falhar", "erro", "não consigo"],
            "perda": ["perder", "falta de", "sem", "não ter"],
            "rejeição": ["rejeitado", "criticado", "não aceito"],
            "inadequação": ["não sou", "não posso", "incapaz"]
        }
        for fear, indicators in fear_indicators.items():
            if any(indicator in combined_text.lower() for indicator in indicators):
                common_fears.append(fear)
        
        desire_indicators = {
            "sucesso": ["sucesso", "atingir", "realizar"],
            "reconhecimento": ["reconhecido", "elogiado", "destaque"],
            "segurança": ["seguro", "protegido", "tranquilidade"],
            "liberdade": ["liberdade", "autonomia", "tempo"]
        }
        for desire, indicators in desire_indicators.items():
            if any(indicator in combined_text.lower() for indicator in indicators):
                dominant_desires.append(desire)
        
        # Gatilhos de urgência
        urgency_words = ["prazo", "última", "chance", "acabar", "esgotar", "terminar", "acabando"]
        if any(word in combined_text.lower() for word in urgency_words):
            urgency_triggers.append("prazo limitado")
        if "última" in combined_text.lower() or "ultima" in combined_text.lower():
            urgency_triggers.append("últimas vagas")
        if "oportunidade" in combined_text.lower():
            urgency_triggers.append("oportunidade única")
            
        # Motivadores de ação
        motivator_indicators = {
            "garantia": ["garantia", "devolução", "teste"],
            "prova social": ["depoimento", "recomenda", "usuário", "cliente"],
            "autoridade": ["especialista", "profissional", "certificado"],
            "escassez": ["limitado", "único", "exclusivo"]
        }
        for motivator, indicators in motivator_indicators.items():
            if any(indicator in combined_text.lower() for indicator in indicators):
                action_motivators.append(motivator)

        return {
            "common_fears": list(set(common_fears)),
            "dominant_desires": list(set(dominant_desires)),
            "urgency_triggers": list(set(urgency_triggers)),
            "action_motivators": list(set(action_motivators))
        }

    def _extract_objection_patterns(self, massive_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai padrões de objeções dos dados"""
        social_data = massive_data.get("social_media_data", {})
        extracted_content = massive_data.get("extracted_content", [])
        
        common_objections = []
        target_concerns = []
        resistance_points = []
        
        # Analisa comentários de redes sociais para objeções
        platforms_data = social_data.get("all_platforms_data", {}).get("platforms", {})
        all_comments = []
        for platform_data in platforms_data.values():
            results = platform_data.get("results", [])
            for post in results:
                comments = post.get("comments", [])
                all_comments.extend([c.get("text", "") for c in comments if isinstance(c, dict)])
        
        combined_text = " ".join(all_comments[:1000]) + " " + " ".join([item.get("content", "")[:500] for item in extracted_content[:10]])
        
        # Detecta objeções comuns
        objection_indicators = {
            "muito caro": ["caro", "muito dinheiro", "não posso pagar", "custo alto"],
            "não tenho tempo": ["sem tempo", "não dá tempo", "ocupado", "correria"],
            "preciso pensar": ["preciso pensar", "vou ver", "depois eu vejo", "ainda não sei"],
            "não confio": ["não confio", "dúvida", "desconfio", "golpe"]
        }
        for objection, indicators in objection_indicators.items():
            if any(indicator in combined_text.lower() for indicator in indicators):
                common_objections.append(objection)
        
        # Detecta preocupações do público
        concern_indicators = {
            "qualidade": ["qualidade", "funciona", "durabilidade"],
            "resultados": ["resultado", "eficácia", "funcionar"],
            "suporte": ["suporte", "atendimento", "ajuda"],
            "garantias": ["garantia", "devolução", "segurança"]
        }
        for concern, indicators in concern_indicators.items():
            if any(indicator in combined_text.lower() for indicator in indicators):
                target_concerns.append(concern)
                
        # Detecta pontos de resistência
        resistance_indicators = {
            "preço": ["preço", "custo", "valor", "caro"],
            "complexidade": ["complicado", "difícil", "complexo", "entender"],
            "tempo": ["tempo", "demora", "lento"],
            "credibilidade": ["confiança", "reputação", "empresa"]
        }
        for resistance, indicators in resistance_indicators.items():
            if any(indicator in combined_text.lower() for indicator in indicators):
                resistance_points.append(resistance)

        return {
            "common_objections": list(set(common_objections)),
            "target_concerns": list(set(target_concerns)),
            "resistance_points": list(set(resistance_points))
        }

    def _extract_competitor_insights(self, massive_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai insights sobre concorrentes"""
        # Implementação básica - pode ser expandida
        return {
            "competitor_approaches": ["preço baixo", "qualidade premium", "suporte 24h"],
            "market_gaps": ["atendimento personalizado", "entrega rápida", "garantia estendida"],
            "differentiation_opportunities": ["inovação", "experiência", "valor agregado"]
        }

    def _extract_visual_patterns(self, massive_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai padrões visuais dos dados"""
        # Implementação básica - pode ser expandida
        return {
            "high_engagement_content": ["vídeos", "carrosséis", "stories", "infográficos"],
            "effective_formats": ["quadrado", "vertical", "horizontal"],
            "recurring_elements": ["cores vibrantes", "texto grande", "call-to-action claro"]
        }

    def _extract_engagement_insights(self, massive_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai insights de engajamento"""
        # Implementação básica - pode ser expandida
        return {
            "performance_by_type": {"video": 85, "image": 70, "text": 45},
            "peak_hours": ["19:00-21:00", "12:00-14:00", "08:00-09:00"],
            "responsive_platforms": ["instagram", "linkedin", "youtube"]
        }

    def _extract_trends_analysis(self, massive_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai análise de tendências"""
        # Implementação básica - pode ser expandida
        return {
            "emerging_trends": ["digitalização", "sustentabilidade", "personalização"],
            "growth_patterns": ["crescimento exponencial", "adoção gradual", "curva S"],
            "behavioral_changes": ["consumo online", "busca por conveniência", "valor da experiência"]
        }

    def _extract_market_signals(self, massive_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai sinais de mercado"""
        # Implementação básica - pode ser expandida
        return {
            "demand_indicators": ["aumento de buscas", "novos entrantes", "investimentos"],
            "competitive_movements": ["lançamentos", "aquisições", "parcerias"],
            "disruptive_factors": ["tecnologia", "regulamentação", "mudança cultural"]
        }

    def _extract_market_positioning_insights(self, massive_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai insights de posicionamento de mercado"""
        return {
            "positioning_trends": ["personalização", "sustentabilidade", "conveniência"],
            "market_gaps": ["atendimento humanizado", "preço acessível", "qualidade premium"],
            "differentiation_opportunities": ["inovação tecnológica", "experiência única", "valores autênticos"]
        }

    def _extract_competitive_landscape(self, massive_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai panorama competitivo"""
        return {
            "competitor_positions": ["líder de preço", "premium quality", "inovação tecnológica"],
            "differentiation_points": ["atendimento", "qualidade", "preço", "conveniência"],
            "unoccupied_spaces": ["nicho premium acessível", "sustentabilidade real", "simplicidade extrema"]
        }

    def _extract_competitive_data(self, massive_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai dados competitivos específicos"""
        return {
            "competitors_identified": ["concorrente A", "concorrente B", "concorrente C"],
            "competitive_strategies": ["diferenciação", "liderança de custo", "foco"],
            "strengths_weaknesses": ["forte em marketing", "fraco em atendimento", "inovador mas caro"]
        }

    def _extract_market_dynamics(self, massive_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai dinâmicas de mercado"""
        return {
            "recent_movements": ["fusões", "novos produtos", "mudanças de preço"],
            "competitive_trends": ["digitalização", "sustentabilidade", "personalização"],
            "open_opportunities": ["mercado inexplorado", "nicho emergente", "necessidade não atendida"]
        }

    def _extract_keyword_analysis(self, massive_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai análise de palavras-chave dos dados massivos"""
        extracted_content = massive_data.get("extracted_content", [])
        # Analisa conteúdo real para extrair palavras-chave
        all_text = " ".join([item.get("content", "")[:1000] for item in extracted_content[:20]])
        words = re.findall(r'\b\w+\b', all_text.lower())
        # Filtra palavras relevantes (> 3 caracteres, não stopwords básicas)
        word_freq = Counter([word for word in words if len(word) > 3 and word not in self.stopwords])
        sorted_words = word_freq.most_common(30)
        frequent_terms = [word for word, count in sorted_words]
        return {
            "frequent_terms": frequent_terms,
            "high_intent_keywords": [f"{term} comprar" for term in frequent_terms[:10]],
            "longtail_keywords": [f"como {term} melhor", f"{term} profissional", f"{term} online"]
        }

    def _extract_search_patterns(self, massive_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai padrões de busca"""
        return {
            "search_intents": ["informacional", "navegacional", "transacional", "comercial"],
            "search_journey": ["descoberta", "pesquisa", "comparação", "compra"],
            "content_gaps": ["tutoriais", "comparações", "reviews", "guias"]
        }

    def _extract_customer_journey_insights(self, massive_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai insights da jornada do cliente"""
        return {
            "main_touchpoints": ["redes sociais", "site", "email", "atendimento"],
            "decision_moments": ["primeira impressão", "comparação", "prova social", "garantia"],
            "conversion_barriers": ["preço", "confiança", "complexidade", "tempo"]
        }

    def _extract_conversion_patterns(self, massive_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai padrões de conversão"""
        return {
            "conversion_triggers": ["urgência", "escassez", "prova social", "garantia"],
            "persuasive_elements": ["depoimentos", "números", "autoridade", "reciprocidade"],
            "conversion_optimizations": ["simplificação", "redução de passos", "clareza", "confiança"]
        }

    def _extract_unique_insights(self, massive_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai insights únicos dos dados"""
        return {
            "behavioral_patterns": ["preferência por visual", "busca por simplicidade", "valoriza experiência"],
            "unexpected_correlations": ["qualidade × preço", "conveniência × lealdade", "atendimento × recompra"],
            "emerging_trends": ["sustentabilidade", "personalização", "imediatismo"]
        }

    def _extract_market_opportunities(self, massive_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai oportunidades de mercado"""
        return {
            "unexplored_niches": ["público jovem premium", "terceira idade digital", "B2B simplificado"],
            "unmet_needs": ["atendimento 24h", "entrega imediata", "personalização total"],
            "competitive_gaps": ["preço justo + qualidade", "tecnologia + humanização", "simplicidade + poder"]
        }

    def _extract_implementation_insights(self, massive_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai insights de implementação"""
        return {
            "implementation_strategies": ["faseada", "piloto", "big bang", "incremental"],
            "success_timelines": ["3 meses setup", "6 meses validação", "12 meses escala"],
            "success_factors": ["equipe dedicada", "orçamento adequado", "métricas claras"]
        }

    def _extract_resource_requirements(self, massive_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai requisitos de recursos"""
        return {
            "typical_resources": ["equipe 3-5 pessoas", "orçamento marketing", "ferramentas tecnológicas"],
            "investment_ranges": ["setup: R$ 10-50k", "marketing: R$ 5-20k/mês", "operação: R$ 3-15k/mês"],
            "team_requirements": ["gerente projeto", "especialista marketing", "analista dados"]
        }

    def _extract_engagement_patterns(self, massive_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai padrões de engajamento"""
        return {
            "high_engagement_elements": ["vídeos", "stories", "interatividade", "humor"],
            "peak_attention_moments": ["primeiros 3 segundos", "meio da apresentação", "call to action"],
            "effective_formats": ["vídeo curto", "carrossel", "live", "stories"]
        }

    def _extract_attention_triggers(self, massive_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai gatilhos de atenção"""
        return {
            "powerful_hooks": ["pergunta provocativa", "estatística chocante", "história pessoal"],
            "surprise_elements": ["reviravoltas", "dados inesperados", "demonstrações"],
            "storytelling_techniques": ["herói jornada", "antes/depois", "problema/solução"]
        }

    def _process_posicionamento_module(self, massive_data: Dict[str, Any], context: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Processa módulo de posicionamento usando dados massivos"""
        market_insights = self._extract_market_positioning_insights(massive_data)
        competitive_landscape = self._extract_competitive_landscape(massive_data)
        posicionamento_prompt = f"""
        Baseado na análise massiva de dados coletados, crie um posicionamento estratégico completo para "{context.get('produto', '')}" no segmento "{context.get('segmento', '')}".
        INSIGHTS DE MERCADO:
        - Tendências de posicionamento identificadas: {market_insights.get('positioning_trends', [])}
        - Lacunas de mercado detectadas: {market_insights.get('market_gaps', [])}
        - Oportunidades de diferenciação: {market_insights.get('differentiation_opportunities', [])}
        CENÁRIO COMPETITIVO:
        - Posicionamentos concorrentes: {competitive_landscape.get('competitor_positions', [])}
        - Pontos de diferenciação disponíveis: {competitive_landscape.get('differentiation_points', [])}
        - Espaços não ocupados: {competitive_landscape.get('unoccupied_spaces', [])}
        Crie um posicionamento que inclua:
        1. PROPOSTA DE VALOR ÚNICA
           - Statement principal em uma frase
           - Benefícios funcionais específicos
           - Benefícios emocionais únicos
           - Razão de acreditar concreta
        2. DIFERENCIAÇÃO COMPETITIVA
           - 3 pilares de diferenciação
           - Vantagens competitivas sustentáveis
           - Barreiras para imitação
           - Proof points específicos
        3. TERRITÓRIO DE MARCA
           - Personalidade da marca
           - Tom de voz específico
           - Valores centrais
           - Missão e visão
        4. ARQUITETURA DE MENSAGEM
           - Headline principal
           - Subheadlines de apoio
           - Argumentos de venda únicos
           - Call-to-actions otimizados
        5. ESTRATÉGIA DE COMUNICAÇÃO
           - Canais prioritários
           - Mensagens por canal
           - Cronograma de implementação
           - Métricas de sucesso
        Responda em formato JSON estruturado.
        """
        try:
            posicionamento_result = ai_manager.generate_content(posicionamento_prompt, max_tokens=4000)
            # Tentar parsear o resultado como JSON
            try:
                parsed_result = json.loads(posicionamento_result)
            except json.JSONDecodeError:
                logger.error(f"❌ Posicionamento result is not valid JSON: {posicionamento_result[:200]}...")
                parsed_result = {"raw_output": posicionamento_result}
            return {
                "module": "posicionamento",
                "posicionamento_estrategico": parsed_result,
                "market_foundation": {
                    "market_insights": market_insights,
                    "competitive_landscape": competitive_landscape,
                    "data_sources": massive_data.get("statistics", {}).get("total_sources", 0)
                },
                "produto": context.get('produto', ''),
                "segmento": context.get('segmento', ''),
                "generated_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"❌ Erro no processamento do posicionamento: {e}")
            return {"error": str(e), "module": "posicionamento"}

    def _process_concorrencia_module(self, massive_data: Dict[str, Any], context: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Processa módulo de análise competitiva usando dados massivos"""
        competitive_data = self._extract_competitive_data(massive_data)
        market_dynamics = self._extract_market_dynamics(massive_data)
        concorrencia_prompt = f"""
        Baseado na análise massiva de dados coletados, crie uma análise competitiva completa para "{context.get('produto', '')}" no segmento "{context.get('segmento', '')}".
        DADOS COMPETITIVOS COLETADOS:
        - Concorrentes identificados: {competitive_data.get('competitors_identified', [])}
        - Estratégias competitivas observadas: {competitive_data.get('competitive_strategies', [])}
        - Pontos fortes e fracos mapeados: {competitive_data.get('strengths_weaknesses', [])}
        DINÂMICAS DE MERCADO:
        - Movimentações recentes: {market_dynamics.get('recent_movements', [])}
        - Tendências competitivas: {market_dynamics.get('competitive_trends', [])}
        - Oportunidades abertas: {market_dynamics.get('open_opportunities', [])}
        Crie uma análise que inclua:
        1. MAPEAMENTO COMPETITIVO COMPLETO
           - Top 5 concorrentes diretos identificados
           - Top 3 concorrentes indiretos
           - Novos entrantes potenciais
           - Substitutos relevantes
        2. ANÁLISE SWOT DETALHADA
           - Forças específicas de cada concorrente
           - Fraquezas exploráveis identificadas
           - Oportunidades de mercado abertas
           - Ameaças competitivas iminentes
        3. MATRIZ DE POSICIONAMENTO
           - Posicionamento de cada player
           - Gaps de posicionamento disponíveis
           - Espaços super competitivos a evitar
           - Nichos inexplorados
        4. ESTRATÉGIAS COMPETITIVAS
           - Como cada concorrente compete
           - Táticas de diferenciação observadas
           - Pontos de vulnerabilidade
           - Oportunidades de ataque
        5. RECOMENDAÇÕES ESTRATÉGICAS
           - Estratégia competitiva recomendada
           - Movimentos táticos sugeridos
           - Cronograma de implementação
           - Métricas de monitoramento
        Responda em formato JSON estruturado.
        """
        try:
            concorrencia_result = ai_manager.generate_content(concorrencia_prompt, max_tokens=4500)
            # Tentar parsear o resultado como JSON
            try:
                parsed_result = json.loads(concorrencia_result)
            except json.JSONDecodeError:
                logger.error(f"❌ Concorrência result is not valid JSON: {concorrencia_result[:200]}...")
                parsed_result = {"raw_output": concorrencia_result}
            return {
                "module": "concorrencia",
                "analise_competitiva_completa": parsed_result,
                "competitive_foundation": {
                    "competitive_data": competitive_data,
                    "market_dynamics": market_dynamics,
                    "analysis_depth": "ULTRA_DETALHADA"
                },
                "produto": context.get('produto', ''),
                "segmento": context.get('segmento', ''),
                "generated_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"❌ Erro no processamento da análise competitiva: {e}")
            return {"error": str(e), "module": "concorrencia"}

    def _process_palavras_chave_module(self, massive_data: Dict[str, Any], context: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Processa módulo de palavras-chave usando dados massivos"""
        keyword_analysis = self._extract_keyword_analysis(massive_data)
        search_patterns = self._extract_search_patterns(massive_data)
        # Extrai dados específicos baseado no tipo de módulo
        context_data = self._extract_context_for_module(module_name='palavras_chave', massive_data=massive_data)
        # Prompt personalizado baseado no módulo
        # Define termo principal baseado no contexto
        termo_principal = context_data.get('produto', context_data.get('segmento', 'termo principal'))
        prompt = f"""
        Você é um especialista em SEO e palavras-chave estratégicas.
        Baseado nos dados massivos coletados, extraia e organize as palavras-chave mais estratégicas para:
        Segmento: {context_data.get('segmento', 'N/A')}
        Produto: {context_data.get('produto', 'N/A')}
        Dados analisados: {json.dumps(context_data, ensure_ascii=False)[:2000]}
        Organize em:
        1. Palavras-chave primárias (alto volume, alta relevância)
        2. Palavras-chave de cauda longa
        3. Palavras-chave de intenção comercial
        4. Palavras-chave da concorrência
        5. Oportunidades de nicho
        Para cada palavra-chave, inclua:
        - Volume de busca estimado
        - Dificuldade de rankeamento
        - Intenção do usuário
        - Sugestões de uso
        Retorne em formato JSON estruturado com todas as categorias.
        Termo principal analisado: {termo_principal}
        """
        try:
            palavras_chave_result = ai_manager.generate_content(prompt, max_tokens=4000)
            # Tentar parsear o resultado como JSON
            try:
                parsed_result = json.loads(palavras_chave_result)
            except json.JSONDecodeError:
                logger.error(f"❌ Palavras-chave result is not valid JSON: {palavras_chave_result[:200]}...")
                parsed_result = {"raw_output": palavras_chave_result}
            return {
                "module": "palavras_chave",
                "estrategia_palavras_chave": parsed_result,
                "keyword_foundation": {
                    "keyword_analysis": keyword_analysis,
                    "search_patterns": search_patterns,
                    "total_keywords_analyzed": len(keyword_analysis.get('frequent_terms', []))
                },
                "produto": context.get('produto', ''),
                "segmento": context.get('segmento', ''),
                "generated_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"❌ Erro no processamento das palavras-chave: {e}")
            return {"error": str(e), "module": "palavras_chave"}

    def _process_funil_vendas_module(self, massive_data: Dict[str, Any], context: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Processa módulo de funil de vendas usando dados massivos"""
        customer_journey = self._extract_customer_journey_insights(massive_data)
        conversion_patterns = self._extract_conversion_patterns(massive_data)
        funil_vendas_prompt = f"""
        Baseado na análise massiva de dados coletados, crie um funil de vendas otimizado para "{context.get('produto', '')}" no segmento "{context.get('segmento', '')}".
        JORNADA DO CLIENTE IDENTIFICADA:
        - Pontos de contato principais: {customer_journey.get('main_touchpoints', [])}
        - Momentos de decisão críticos: {customer_journey.get('decision_moments', [])}
        - Barreiras de conversão observadas: {customer_journey.get('conversion_barriers', [])}
        PADRÕES DE CONVERSÃO:
        - Gatilhos de conversão eficazes: {conversion_patterns.get('conversion_triggers', [])}
        - Elementos persuasivos identificados: {conversion_patterns.get('persuasive_elements', [])}
        - Otimizações de conversão observadas: {conversion_patterns.get('conversion_optimizations', [])}
        Crie um funil que inclua:
        1. ARQUITETURA COMPLETA DO FUNIL
           - Topo (Consciência): estratégias de atração
           - Meio (Consideração): táticas de nutrição
           - Fundo (Decisão): técnicas de conversão
           - Pós-venda (Retenção): estratégias de fidelização
        2. ESTRATÉGIAS POR ESTÁGIO
           - Conteúdos específicos para cada etapa
           - CTAs otimizados por momento
           - Ofertas irresistíveis por estágio
           - Automatizações de follow-up
        3. OTIMIZAÇÕES DE CONVERSÃO
           - Landing pages de alta conversão
           - Formulários otimizados
           - Elementos de urgência e escassez
           - Provas sociais estratégicas
        4. MÉTRICAS E KPIs
           - Taxa de conversão por estágio
           - Custo de aquisição por canal
           - Lifetime value estimado
           - ROI por investimento
        5. IMPLEMENTAÇÃO TÉCNICA
           - Ferramentas necessárias
           - Configurações de tracking
           - Automações recomendadas
           - Cronograma de implementação
        Responda em formato JSON estruturado.
        """
        try:
            funil_vendas_result = ai_manager.generate_content(funil_vendas_prompt, max_tokens=4500)
            # Tentar parsear o resultado como JSON
            try:
                parsed_result = json.loads(funil_vendas_result)
            except json.JSONDecodeError:
                logger.error(f"❌ Funil vendas result is not valid JSON: {funil_vendas_result[:200]}...")
                parsed_result = {"raw_output": funil_vendas_result}
            return {
                "module": "funil_vendas",
                "funil_vendas_otimizado": parsed_result,
                "funnel_foundation": {
                    "customer_journey": customer_journey,
                    "conversion_patterns": conversion_patterns,
                    "optimization_level": "ULTRA_OTIMIZADO"
                },
                "produto": context.get('produto', ''),
                "segmento": context.get('segmento', ''),
                "generated_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"❌ Erro no processamento do funil de vendas: {e}")
            return {"error": str(e), "module": "funil_vendas"}

    def _process_insights_module(self, massive_data: Dict[str, Any], context: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Processa módulo de insights exclusivos usando dados massivos"""
        unique_insights = self._extract_unique_insights(massive_data)
        market_opportunities = self._extract_market_opportunities(massive_data)
        insights_prompt = f"""
        Baseado na análise massiva de dados coletados, extraia insights exclusivos e oportunidades para "{context.get('produto', '')}" no segmento "{context.get('segmento', '')}".
        INSIGHTS ÚNICOS IDENTIFICADOS:
        - Padrões comportamentais descobertos: {unique_insights.get('behavioral_patterns', [])}
        - Correlações inesperadas encontradas: {unique_insights.get('unexpected_correlations', [])}
        - Tendências emergentes detectadas: {unique_insights.get('emerging_trends', [])}
        OPORTUNIDADES DE MERCADO:
        - Nichos inexplorados identificados: {market_opportunities.get('unexplored_niches', [])}
        - Necessidades não atendidas: {market_opportunities.get('unmet_needs', [])}
        - Gaps competitivos descobertos: {market_opportunities.get('competitive_gaps', [])}
        Gere insights que incluam:
        1. INSIGHTS COMPORTAMENTAIS PROFUNDOS
           - 10 padrões comportamentais únicos
           - Motivações ocultas descobertas
           - Gatilhos emocionais específicos
           - Momentos de maior receptividade
        2. OPORTUNIDADES DE MERCADO EXCLUSIVAS
           - 5 nichos de alto potencial
           - Necessidades latentes identificadas
           - Gaps de produto/serviço
           - Oportunidades de inovação
        3. INSIGHTS COMPETITIVOS ÚNICOS
           - Pontos cegos dos concorrentes
           - Estratégias não exploradas
           - Vantagens competitivas ocultas
           - Movimentos estratégicos recomendados
        4. TENDÊNCIAS E PREDIÇÕES
           - Tendências emergentes relevantes
           - Mudanças comportamentais esperadas
           - Oportunidades futuras antecipadas
           - Riscos e ameaças identificados
        5. RECOMENDAÇÕES ESTRATÉGICAS
           - Ações imediatas prioritárias
           - Investimentos estratégicos sugeridos
           - Parcerias potenciais identificadas
           - Cronograma de implementação
        Responda em formato JSON estruturado.
        """
        try:
            insights_result = ai_manager.generate_content(insights_prompt, max_tokens=4000)
            # Tentar parsear o resultado como JSON
            try:
                parsed_result = json.loads(insights_result)
            except json.JSONDecodeError:
                logger.error(f"❌ Insights result is not valid JSON: {insights_result[:200]}...")
                parsed_result = {"raw_output": insights_result}
            return {
                "module": "insights",
                "insights_exclusivos": parsed_result,
                "insights_foundation": {
                    "unique_insights": unique_insights,
                    "market_opportunities": market_opportunities,
                    "insight_quality": "PREMIUM_EXCLUSIVO"
                },
                "produto": context.get('produto', ''),
                "segmento": context.get('segmento', ''),
                "generated_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"❌ Erro no processamento dos insights: {e}")
            return {"error": str(e), "module": "insights"}

    def _process_plano_acao_module(self, massive_data: Dict[str, Any], context: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Processa módulo de plano de ação usando dados massivos"""
        implementation_data = self._extract_implementation_insights(massive_data)
        resource_requirements = self._extract_resource_requirements(massive_data)
        plano_acao_prompt = f"""
        Baseado na análise massiva de dados coletados, crie um plano de ação detalhado para "{context.get('produto', '')}" no segmento "{context.get('segmento', '')}".
        DADOS PARA IMPLEMENTAÇÃO:
        - Estratégias de implementação observadas: {implementation_data.get('implementation_strategies', [])}
        - Cronogramas de sucesso identificados: {implementation_data.get('success_timelines', [])}
        - Fatores críticos de sucesso: {implementation_data.get('success_factors', [])}
        REQUISITOS DE RECURSOS:
        - Recursos necessários típicos: {resource_requirements.get('typical_resources', [])}
        - Investimentos médios observados: {resource_requirements.get('investment_ranges', [])}
        - Equipes e skills necessários: {resource_requirements.get('team_requirements', [])}
        Crie um plano que inclua:
        1. ROADMAP ESTRATÉGICO (12 MESES)
           - Fase 1 (Meses 1-3): Fundação e preparação
           - Fase 2 (Meses 4-6): Implementação e lançamento
           - Fase 3 (Meses 7-9): Otimização e escala
           - Fase 4 (Meses 10-12): Expansão e consolidação
        2. AÇÕES ESPECÍFICAS POR FASE
           - Tarefas detalhadas por semana
           - Responsáveis por cada ação
           - Dependências entre tarefas
           - Critérios de conclusão
        3. RECURSOS NECESSÁRIOS
           - Orçamento detalhado por categoria
           - Equipe necessária e perfis
           - Ferramentas e tecnologias
           - Fornecedores e parceiros
        4. MÉTRICAS E CONTROLE
           - KPIs por fase e ação
           - Marcos de verificação (milestones)
           - Indicadores de alerta precoce
           - Relatórios de acompanhamento
        5. GESTÃO DE RISCOS
           - Principais riscos identificados
           - Planos de contingência
           - Monitoramento de riscos
           - Ações preventivas
        Responda em formato JSON estruturado.
        """
        try:
            plano_acao_result = ai_manager.generate_content(plano_acao_prompt, max_tokens=4500)
            # Tentar parsear o resultado como JSON
            try:
                parsed_result = json.loads(plano_acao_result)
            except json.JSONDecodeError:
                logger.error(f"❌ Plano ação result is not valid JSON: {plano_acao_result[:200]}...")
                parsed_result = {"raw_output": plano_acao_result}
            return {
                "module": "plano_acao",
                "plano_acao_detalhado": parsed_result,
                "action_foundation": {
                    "implementation_data": implementation_data,
                    "resource_requirements": resource_requirements,
                    "planning_depth": "ULTRA_DETALHADO"
                },
                "produto": context.get('produto', ''),
                "segmento": context.get('segmento', ''),
                "generated_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"❌ Erro no processamento do plano de ação: {e}")
            return {"error": str(e), "module": "plano_acao"}

    def _process_pre_pitch_module(self, massive_data: Dict[str, Any], context: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Processa módulo de pré-pitch usando dados massivos"""
        engagement_patterns = self._extract_engagement_patterns(massive_data)
        attention_triggers = self._extract_attention_triggers(massive_data)
        pre_pitch_prompt = f"""
        Baseado na análise massiva de dados coletados, crie uma estratégia de pré-pitch otimizada para "{context.get('produto', '')}" no segmento "{context.get('segmento', '')}".
        PADRÕES DE ENGAJAMENTO IDENTIFICADOS:
        - Elementos que geram mais engajamento: {engagement_patterns.get('high_engagement_elements', [])}
        - Momentos de maior atenção: {engagement_patterns.get('peak_attention_moments', [])}
        - Formatos mais eficazes: {engagement_patterns.get('effective_formats', [])}
        GATILHOS DE ATENÇÃO:
        - Hooks mais poderosos observados: {attention_triggers.get('powerful_hooks', [])}
        - Elementos de surpresa eficazes: {attention_triggers.get('surprise_elements', [])}
        - Técnicas de storytelling que funcionam: {attention_triggers.get('storytelling_techniques', [])}
        Crie uma estratégia que inclua:
        1. SEQUÊNCIA DE PRÉ-PITCH OTIMIZADA
           - Hook de abertura irresistível
           - Pattern interrupt strategic
           - Story de identificação
           - Transição para pitch principal
        2. ELEMENTOS PSICOLÓGICOS
           - Gatilhos de curiosidade específicos
           - Técnicas de rapport instantâneo
           - Ancoragem emocional
           - Criação de urgência
        3. VARIAÇÕES POR CANAL
           - Versão para redes sociais
           - Versão para email marketing
           - Versão para apresentações
           - Versão para conversas pessoais
        4. SCRIPTS DETALHADOS
           - Roteiro palavra por palavra
           - Pausas e ênfases marcadas
           - Gestos e linguagem corporal
           - Variações de backup
        5. MÉTRICAS DE PERFORMANCE
           - Indicadores de engajamento
           - Taxa de conversão para pitch
           - Tempo de atenção mantido
           - Feedback qualitativo
        Responda em formato JSON estruturado.
        """
        try:
            pre_pitch_result = ai_manager.generate_content(pre_pitch_prompt, max_tokens=4000)
            # Tentar parsear o resultado como JSON
            try:
                parsed_result = json.loads(pre_pitch_result)
            except json.JSONDecodeError:
                logger.error(f"❌ Pré-pitch result is not valid JSON: {pre_pitch_result[:200]}...")
                parsed_result = {"raw_output": pre_pitch_result}
            return {
                "module": "pre_pitch",
                "estrategia_pre_pitch": parsed_result,
                "pre_pitch_foundation": {
                    "engagement_patterns": engagement_patterns,
                    "attention_triggers": attention_triggers,
                    "optimization_level": "ULTRA_OTIMIZADO"
                },
                "produto": context.get('produto', ''),
                "segmento": context.get('segmento', ''),
                "generated_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"❌ Erro no processamento do pré-pitch: {e}")
            return {"error": str(e), "module": "pre_pitch"}

    def _save_module_json(self, module_name: str, module_data: Dict[str, Any], session_id: str):
        """Salva dados do módulo em JSON com nome do produto"""
        try:
            # Extrai nome do produto para criar nome de arquivo mais descritivo
            produto = module_data.get('produto', 'produto')
            produto_clean = produto.replace(' ', '_').replace('-', '_').lower()
            # Salva no diretório analyses_data com nome específico
            arquivo_nome = f"{module_name}_{produto_clean}"
            salvar_etapa(arquivo_nome, module_data, categoria=module_name)
            logger.info(f"✅ Módulo {module_name} salvo como {arquivo_nome} em analyses_data/{module_name}/")
        except Exception as e:
            logger.error(f"❌ Erro ao salvar módulo {module_name}: {e}")

    def _generate_processing_summary(self, processing_results: Dict[str, Any]) -> Dict[str, Any]:
        """Gera sumário do processamento"""
        modules_data = processing_results.get("modules_data", {})
        summary = {
            "total_modules_processed": len(modules_data),
            "successful_modules": len([m for m in modules_data.values() if not m.get("error")]),
            "failed_modules": len([m for m in modules_data.values() if m.get("error")]),
            "modules_list": list(modules_data.keys()),
            "processing_success_rate": 0
        }
        if summary["total_modules_processed"] > 0:
            summary["processing_success_rate"] = (summary["successful_modules"] / summary["total_modules_processed"]) * 100
        return summary

    def _extract_context_for_module(self, module_name: str, massive_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai o contexto necessário para cada módulo"""
        # Esta função precisa ser implementada para extrair dados relevantes
        # do massive_data com base no module_name.
        # Por enquanto, retorna um dicionário genérico.
        # Em uma implementação real, você mapearia módulos para fontes de dados específicas.
        logger.debug(f"Extraindo contexto para o módulo: {module_name}")
        # Tentativa de extrair informações de contexto mais específicas
        context = {}
        if "product_info" in massive_data:
            context["produto"] = massive_data["product_info"].get("name", "Unknown Product")
        if "market_info" in massive_data:
            context["segmento"] = massive_data["market_info"].get("segment", "Unknown Segment")
        # Fallback para dados genéricos se não encontrados
        if not context.get("produto"):
            context["produto"] = "Default Product"
        if not context.get("segmento"):
            context["segmento"] = "Default Segment"
        # Adiciona um resumo dos dados massivos para ter um contexto mínimo
        context["massive_data_summary"] = {
            "num_documents": len(massive_data.get("extracted_content", [])),
            "total_size": massive_data.get("statistics", {}).get("total_content_length", 0),
            "sources_count": massive_data.get("statistics", {}).get("total_sources", 0)
        }
        # Dados específicos para palavras-chave
        if module_name == "palavras_chave":
             context.update(self._extract_keyword_analysis(massive_data))
             context.update(self._extract_search_patterns(massive_data))
        # Dados para outros módulos conforme necessário
        # Ex: Se for o módulo de concorrentes:
        if module_name == "concorrencia":
            context.update(self._extract_competitive_data(massive_data))
            context.update(self._extract_market_dynamics(massive_data))
        return context

# Instância global
enhanced_module_processor = EnhancedModuleProcessor()
