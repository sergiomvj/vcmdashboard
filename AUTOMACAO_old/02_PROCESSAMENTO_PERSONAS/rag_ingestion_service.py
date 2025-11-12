"""
VCM RAG Ingestion Service
Sistema de ingestão de dados para Knowledge Base RAG
Compatível com estrutura Supabase existente
Author: VCM Team
Date: November 2025
"""

import os
import json
import logging
import asyncio
import uuid
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime
import hashlib
import re

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('rag_ingestion.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class RAGIngestionService:
    """
    Serviço de ingestão de dados para RAG
    Processa biografias, competências e workflows para knowledge base
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.load_environment()
        self.setup_supabase()
        
    def load_environment(self):
        """Carrega variáveis de ambiente"""
        env_paths = [
            self.base_path / '.env',
            self.base_path.parent / '.env',
            Path.cwd() / '.env'
        ]
        
        env_loaded = False
        for env_file in env_paths:
            if env_file.exists():
                logger.info(f"Carregando .env de: {env_file}")
                with open(env_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            os.environ[key] = value
                env_loaded = True
                break
        
        if not env_loaded:
            logger.warning("Nenhum arquivo .env encontrado")
    
    def setup_supabase(self):
        """Setup cliente Supabase"""
        try:
            from supabase import create_client
            
            url = os.getenv('VCM_SUPABASE_URL')
            key = os.getenv('VCM_SUPABASE_SERVICE_ROLE_KEY')
            
            if not url or not key:
                raise ValueError("Credenciais Supabase não encontradas")
            
            self.supabase = create_client(url, key)
            logger.info("✅ Cliente Supabase configurado")
            
        except ImportError:
            logger.error("Biblioteca supabase não instalada. Execute: pip install supabase")
            self.supabase = None
        except Exception as e:
            logger.error(f"Erro ao configurar Supabase: {e}")
            self.supabase = None
    
    async def ingest_empresa_data(self, empresa_id: str, force_update: bool = False) -> Dict[str, Any]:
        """
        Ingere todos os dados de uma empresa no RAG
        """
        if not self.supabase:
            raise Exception("Supabase não configurado")
        
        logger.info(f"🚀 Iniciando ingestão RAG para empresa {empresa_id}")
        
        # Criar job de ingestão
        job_id = str(uuid.uuid4())
        job_data = {
            'id': job_id,
            'empresa_id': empresa_id,
            'job_type': 'full_sync',
            'status': 'running',
            'started_at': datetime.now().isoformat()
        }
        
        try:
            # Registrar job
            self.supabase.table('rag_ingestion_jobs').insert(job_data).execute()
            
            # Limpar dados existentes se force_update
            if force_update:
                logger.info("🧹 Limpando dados RAG existentes...")
                await self._clean_empresa_rag_data(empresa_id)
            
            # Buscar dados da empresa
            empresa_data = await self._get_empresa_data(empresa_id)
            
            if not empresa_data:
                raise Exception(f"Empresa {empresa_id} não encontrada")
            
            results = {
                'job_id': job_id,
                'empresa_id': empresa_id,
                'empresa_nome': empresa_data.get('nome', 'Unknown'),
                'biografias': 0,
                'competencias': 0,
                'workflows': 0,
                'knowledge': 0,
                'errors': []
            }
            
            # 1. Processar biografias
            logger.info("📝 Processando biografias...")
            bio_result = await self._process_biografias(empresa_id)
            results['biografias'] = bio_result['success_count']
            results['errors'].extend(bio_result['errors'])
            
            # 2. Processar competências
            logger.info("🎯 Processando competências...")
            comp_result = await self._process_competencias(empresa_id)
            results['competencias'] = comp_result['success_count']
            results['errors'].extend(comp_result['errors'])
            
            # 3. Processar workflows
            logger.info("⚙️ Processando workflows...")
            work_result = await self._process_workflows(empresa_id)
            results['workflows'] = work_result['success_count']
            results['errors'].extend(work_result['errors'])
            
            # 4. Processar knowledge base existente
            logger.info("📚 Processando knowledge base...")
            know_result = await self._process_knowledge_base(empresa_id)
            results['knowledge'] = know_result['success_count']
            results['errors'].extend(know_result['errors'])
            
            # Atualizar job como concluído
            total_items = results['biografias'] + results['competencias'] + results['workflows'] + results['knowledge']
            
            job_update = {
                'status': 'completed',
                'completed_at': datetime.now().isoformat(),
                'total_items': total_items,
                'processed_items': total_items,
                'success_items': total_items - len(results['errors']),
                'failed_items': len(results['errors']),
                'error_details': results['errors']
            }
            
            self.supabase.table('rag_ingestion_jobs').update(job_update).eq('id', job_id).execute()
            
            logger.info(f"✅ Ingestão concluída: {total_items} itens processados")
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Erro na ingestão: {str(e)}")
            
            # Marcar job como falho
            error_update = {
                'status': 'failed',
                'completed_at': datetime.now().isoformat(),
                'error_details': [{'error': str(e), 'timestamp': datetime.now().isoformat()}]
            }
            
            try:
                self.supabase.table('rag_ingestion_jobs').update(error_update).eq('id', job_id).execute()
            except:
                pass
            
            raise e
    
    async def _get_empresa_data(self, empresa_id: str) -> Optional[Dict[str, Any]]:
        """Busca dados básicos da empresa"""
        try:
            result = self.supabase.table('empresas').select('*').eq('id', empresa_id).execute()
            
            if result.data:
                return result.data[0]
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar empresa: {e}")
            return None
    
    async def _clean_empresa_rag_data(self, empresa_id: str):
        """Limpa dados RAG existentes da empresa"""
        try:
            # Buscar documentos da empresa
            docs_result = self.supabase.table('rag_documents').select('id').eq('empresa_id', empresa_id).execute()
            
            if docs_result.data:
                doc_ids = [doc['id'] for doc in docs_result.data]
                
                # Deletar chunks primeiro
                for doc_id in doc_ids:
                    self.supabase.table('rag_chunks').delete().eq('document_id', doc_id).execute()
                
                # Deletar documentos
                self.supabase.table('rag_documents').delete().eq('empresa_id', empresa_id).execute()
                
                logger.info(f"🧹 Removidos {len(doc_ids)} documentos RAG existentes")
                
        except Exception as e:
            logger.warning(f"Erro ao limpar dados RAG: {e}")
    
    async def _process_biografias(self, empresa_id: str) -> Dict[str, Any]:
        """Processa biografias para RAG"""
        result = {'success_count': 0, 'errors': []}
        
        try:
            # Buscar personas da empresa
            personas_result = self.supabase.table('personas').select('*').eq('empresa_id', empresa_id).execute()
            
            if not personas_result.data:
                logger.info("Nenhuma persona encontrada")
                return result
            
            for persona in personas_result.data:
                try:
                    if not persona.get('biografia_completa'):
                        continue
                    
                    # Criar documento RAG para biografia
                    doc_data = {
                        'id': str(uuid.uuid4()),
                        'collection_id': await self._get_or_create_collection(empresa_id),
                        'external_id': f"biografia_{persona['id']}",
                        'title': f"Biografia: {persona['full_name']}",
                        'content_raw': persona['biografia_completa'],
                        'content_length': len(persona['biografia_completa']),
                        'document_type': 'biografia',
                        'language': 'pt',
                        'metadata': {
                            'persona_id': persona['id'],
                            'persona_name': persona['full_name'],
                            'persona_role': persona['role'],
                            'empresa_id': empresa_id
                        },
                        'empresa_id': empresa_id,  # Adicionar para compatibilidade
                        'persona_id': persona['id'],
                        'source_type': 'biografia',
                        'is_active': True,
                        'processed_at': datetime.now().isoformat()
                    }
                    
                    # Inserir documento
                    self.supabase.table('rag_documents').insert(doc_data).execute()
                    
                    # Criar chunks da biografia
                    await self._create_chunks(doc_data['id'], persona['biografia_completa'])
                    
                    result['success_count'] += 1
                    logger.debug(f"✅ Biografia processada: {persona['full_name']}")
                    
                except Exception as e:
                    error_msg = f"Erro ao processar biografia {persona.get('full_name', 'Unknown')}: {str(e)}"
                    logger.error(error_msg)
                    result['errors'].append({'type': 'biografia', 'error': error_msg})
            
            logger.info(f"📝 Biografias processadas: {result['success_count']}")
            
        except Exception as e:
            logger.error(f"Erro geral no processamento de biografias: {e}")
            result['errors'].append({'type': 'biografias_general', 'error': str(e)})
        
        return result
    
    async def _process_competencias(self, empresa_id: str) -> Dict[str, Any]:
        """Processa competências para RAG"""
        result = {'success_count': 0, 'errors': []}
        
        try:
            # Buscar competências via personas
            personas_result = self.supabase.table('personas').select('id, full_name').eq('empresa_id', empresa_id).execute()
            
            if not personas_result.data:
                return result
            
            for persona in personas_result.data:
                try:
                    # Buscar competências da persona
                    comp_result = self.supabase.table('competencias').select('*').eq('persona_id', persona['id']).execute()
                    
                    if not comp_result.data:
                        continue
                    
                    # Agrupar competências por persona
                    competencias_text = self._format_competencias_text(comp_result.data, persona['full_name'])
                    
                    doc_data = {
                        'id': str(uuid.uuid4()),
                        'collection_id': await self._get_or_create_collection(empresa_id),
                        'external_id': f"competencias_{persona['id']}",
                        'title': f"Competências: {persona['full_name']}",
                        'content_raw': competencias_text,
                        'content_length': len(competencias_text),
                        'document_type': 'competencia',
                        'language': 'pt',
                        'metadata': {
                            'persona_id': persona['id'],
                            'persona_name': persona['full_name'],
                            'competencias_count': len(comp_result.data),
                            'empresa_id': empresa_id
                        },
                        'empresa_id': empresa_id,
                        'persona_id': persona['id'],
                        'source_type': 'competencias',
                        'is_active': True,
                        'processed_at': datetime.now().isoformat()
                    }
                    
                    self.supabase.table('rag_documents').insert(doc_data).execute()
                    await self._create_chunks(doc_data['id'], competencias_text)
                    
                    result['success_count'] += 1
                    
                except Exception as e:
                    error_msg = f"Erro ao processar competências {persona.get('full_name', 'Unknown')}: {str(e)}"
                    logger.error(error_msg)
                    result['errors'].append({'type': 'competencia', 'error': error_msg})
            
            logger.info(f"🎯 Competências processadas: {result['success_count']}")
            
        except Exception as e:
            logger.error(f"Erro geral no processamento de competências: {e}")
            result['errors'].append({'type': 'competencias_general', 'error': str(e)})
        
        return result
    
    async def _process_workflows(self, empresa_id: str) -> Dict[str, Any]:
        """Processa workflows para RAG"""
        result = {'success_count': 0, 'errors': []}
        
        try:
            # Buscar workflows via personas
            personas_result = self.supabase.table('personas').select('id, full_name').eq('empresa_id', empresa_id).execute()
            
            if not personas_result.data:
                return result
            
            for persona in personas_result.data:
                try:
                    # Buscar workflows da persona
                    work_result = self.supabase.table('workflows').select('*').eq('persona_id', persona['id']).execute()
                    
                    if not work_result.data:
                        continue
                    
                    # Processar cada workflow
                    for workflow in work_result.data:
                        workflow_text = self._format_workflow_text(workflow, persona['full_name'])
                        
                        doc_data = {
                            'id': str(uuid.uuid4()),
                            'collection_id': await self._get_or_create_collection(empresa_id),
                            'external_id': f"workflow_{workflow['id']}",
                            'title': f"Workflow: {workflow['nome']} - {persona['full_name']}",
                            'content_raw': workflow_text,
                            'content_length': len(workflow_text),
                            'document_type': 'workflow',
                            'language': 'pt',
                            'metadata': {
                                'persona_id': persona['id'],
                                'persona_name': persona['full_name'],
                                'workflow_id': workflow['id'],
                                'workflow_type': workflow.get('tipo'),
                                'workflow_priority': workflow.get('prioridade'),
                                'empresa_id': empresa_id
                            },
                            'empresa_id': empresa_id,
                            'persona_id': persona['id'],
                            'source_type': 'workflow',
                            'is_active': True,
                            'processed_at': datetime.now().isoformat()
                        }
                        
                        self.supabase.table('rag_documents').insert(doc_data).execute()
                        await self._create_chunks(doc_data['id'], workflow_text)
                        
                        result['success_count'] += 1
                    
                except Exception as e:
                    error_msg = f"Erro ao processar workflows {persona.get('full_name', 'Unknown')}: {str(e)}"
                    logger.error(error_msg)
                    result['errors'].append({'type': 'workflow', 'error': error_msg})
            
            logger.info(f"⚙️ Workflows processados: {result['success_count']}")
            
        except Exception as e:
            logger.error(f"Erro geral no processamento de workflows: {e}")
            result['errors'].append({'type': 'workflows_general', 'error': str(e)})
        
        return result
    
    async def _process_knowledge_base(self, empresa_id: str) -> Dict[str, Any]:
        """Processa knowledge base existente para RAG"""
        result = {'success_count': 0, 'errors': []}
        
        try:
            # Buscar knowledge base via personas
            personas_result = self.supabase.table('personas').select('id, full_name').eq('empresa_id', empresa_id).execute()
            
            if not personas_result.data:
                return result
            
            for persona in personas_result.data:
                try:
                    # Buscar knowledge da persona
                    know_result = self.supabase.table('rag_knowledge').select('*').eq('persona_id', persona['id']).execute()
                    
                    if not know_result.data:
                        continue
                    
                    # Processar cada item de knowledge
                    for knowledge in know_result.data:
                        if not knowledge.get('ativo', True):
                            continue
                        
                        doc_data = {
                            'id': str(uuid.uuid4()),
                            'collection_id': await self._get_or_create_collection(empresa_id),
                            'external_id': f"knowledge_{knowledge['id']}",
                            'title': knowledge['titulo'],
                            'content_raw': knowledge['conteudo'],
                            'content_length': len(knowledge['conteudo']),
                            'document_type': knowledge.get('tipo', 'knowledge'),
                            'language': 'pt',
                            'metadata': {
                                'persona_id': persona['id'],
                                'persona_name': persona['full_name'],
                                'knowledge_id': knowledge['id'],
                                'knowledge_type': knowledge.get('tipo'),
                                'categoria': knowledge.get('categoria'),
                                'relevancia': knowledge.get('relevancia', 1.0),
                                'tags': knowledge.get('tags', []),
                                'empresa_id': empresa_id
                            },
                            'empresa_id': empresa_id,
                            'persona_id': persona['id'],
                            'source_type': 'knowledge',
                            'is_active': True,
                            'processed_at': datetime.now().isoformat()
                        }
                        
                        self.supabase.table('rag_documents').insert(doc_data).execute()
                        await self._create_chunks(doc_data['id'], knowledge['conteudo'])
                        
                        result['success_count'] += 1
                    
                except Exception as e:
                    error_msg = f"Erro ao processar knowledge {persona.get('full_name', 'Unknown')}: {str(e)}"
                    logger.error(error_msg)
                    result['errors'].append({'type': 'knowledge', 'error': error_msg})
            
            logger.info(f"📚 Knowledge base processado: {result['success_count']}")
            
        except Exception as e:
            logger.error(f"Erro geral no processamento de knowledge: {e}")
            result['errors'].append({'type': 'knowledge_general', 'error': str(e)})
        
        return result
    
    async def _get_or_create_collection(self, empresa_id: str) -> str:
        """Busca ou cria collection para a empresa"""
        try:
            # Buscar collection existente
            result = self.supabase.table('rag_collections').select('id').eq('code', f'empresa_{empresa_id}').execute()
            
            if result.data:
                return result.data[0]['id']
            
            # Criar nova collection
            empresa_data = await self._get_empresa_data(empresa_id)
            empresa_nome = empresa_data.get('nome', 'Unknown') if empresa_data else 'Unknown'
            
            collection_data = {
                'id': str(uuid.uuid4()),
                'code': f'empresa_{empresa_id}',
                'name': f'Knowledge Base - {empresa_nome}',
                'description': f'Base de conhecimento da empresa {empresa_nome}',
                'visibility': 'internal',
                'metadata': {
                    'empresa_id': empresa_id,
                    'auto_generated': True
                },
                'is_active': True
            }
            
            insert_result = self.supabase.table('rag_collections').insert(collection_data).execute()
            return insert_result.data[0]['id']
            
        except Exception as e:
            logger.error(f"Erro ao criar/buscar collection: {e}")
            # Retornar um ID padrão se falhar
            return str(uuid.uuid4())
    
    async def _create_chunks(self, document_id: str, content: str, chunk_size: int = 1000):
        """Cria chunks de um documento"""
        try:
            # Dividir texto em chunks
            chunks = self._split_text_into_chunks(content, chunk_size)
            
            for i, chunk_content in enumerate(chunks):
                chunk_data = {
                    'id': str(uuid.uuid4()),
                    'document_id': document_id,
                    'chunk_index': i,
                    'content': chunk_content,
                    'content_length': len(chunk_content),
                    'metadata': {
                        'chunk_number': i + 1,
                        'total_chunks': len(chunks)
                    }
                }
                
                self.supabase.table('rag_chunks').insert(chunk_data).execute()
            
            logger.debug(f"✅ Criados {len(chunks)} chunks para documento {document_id}")
            
        except Exception as e:
            logger.error(f"Erro ao criar chunks: {e}")
    
    def _split_text_into_chunks(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Divide texto em chunks com overlap"""
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            if end >= len(text):
                chunks.append(text[start:])
                break
            
            # Tentar quebrar em uma frase completa
            chunk = text[start:end]
            last_period = chunk.rfind('.')
            last_newline = chunk.rfind('\n')
            
            break_point = max(last_period, last_newline)
            
            if break_point > start + chunk_size // 2:  # Se encontrou um bom ponto de quebra
                actual_end = start + break_point + 1
                chunks.append(text[start:actual_end])
                start = actual_end - overlap
            else:
                chunks.append(chunk)
                start = end - overlap
            
            start = max(0, start)  # Garantir que não seja negativo
        
        return chunks
    
    def _format_competencias_text(self, competencias: List[Dict], persona_name: str) -> str:
        """Formata competências em texto estruturado"""
        text = f"Competências de {persona_name}:\n\n"
        
        # Agrupar por tipo
        tipos = {}
        for comp in competencias:
            tipo = comp.get('tipo', 'geral')
            if tipo not in tipos:
                tipos[tipo] = []
            tipos[tipo].append(comp)
        
        for tipo, comps in tipos.items():
            text += f"## {tipo.upper()}\n"
            for comp in comps:
                text += f"- {comp['nome']}"
                if comp.get('descricao'):
                    text += f": {comp['descricao']}"
                text += f" (Nível: {comp.get('nivel', 'avançado')})\n"
            text += "\n"
        
        return text
    
    def _format_workflow_text(self, workflow: Dict, persona_name: str) -> str:
        """Formata workflow em texto estruturado"""
        text = f"Workflow: {workflow['nome']}\n"
        text += f"Responsável: {persona_name}\n"
        text += f"Tipo: {workflow.get('tipo', 'N/A')}\n"
        text += f"Prioridade: {workflow.get('prioridade', 'média')}\n\n"
        
        if workflow.get('descricao'):
            text += f"Descrição:\n{workflow['descricao']}\n\n"
        
        # Processar configurações, triggers e ações se existirem
        if workflow.get('config'):
            text += f"Configurações:\n{json.dumps(workflow['config'], indent=2, ensure_ascii=False)}\n\n"
        
        if workflow.get('triggers'):
            text += f"Triggers:\n{json.dumps(workflow['triggers'], indent=2, ensure_ascii=False)}\n\n"
        
        if workflow.get('actions'):
            text += f"Ações:\n{json.dumps(workflow['actions'], indent=2, ensure_ascii=False)}\n\n"
        
        return text
    
    def get_ingestion_status(self, empresa_id: str) -> Dict[str, Any]:
        """Retorna status das ingestões de uma empresa"""
        try:
            if not self.supabase:
                return {'error': 'Supabase não configurado'}
            
            # Buscar jobs recentes
            result = self.supabase.table('rag_ingestion_jobs').select('*').eq('empresa_id', empresa_id).order('created_at', desc=True).limit(10).execute()
            
            # Buscar estatísticas RAG
            stats_result = self.supabase.rpc('rag_empresa_stats', {'target_empresa_id': empresa_id}).execute()
            
            return {
                'recent_jobs': result.data if result.data else [],
                'stats': stats_result.data[0] if stats_result.data else {},
                'last_sync': result.data[0]['completed_at'] if result.data and result.data[0].get('completed_at') else None
            }
            
        except Exception as e:
            logger.error(f"Erro ao buscar status: {e}")
            return {'error': str(e)}

# Instância global do serviço
rag_service = RAGIngestionService()

# Funções de conveniência
async def ingest_empresa_rag(empresa_id: str, force_update: bool = False) -> Dict[str, Any]:
    """Função de conveniência para ingestão RAG"""
    return await rag_service.ingest_empresa_data(empresa_id, force_update)

def get_rag_status(empresa_id: str) -> Dict[str, Any]:
    """Função de conveniência para status RAG"""
    return rag_service.get_ingestion_status(empresa_id)

# Execução standalone para teste
if __name__ == "__main__":
    async def test_ingestion():
        """Teste básico do serviço de ingestão"""
        
        # Buscar primeira empresa disponível
        try:
            if not rag_service.supabase:
                print("❌ Supabase não configurado")
                return
            
            empresas_result = rag_service.supabase.table('empresas').select('id, nome').limit(1).execute()
            
            if not empresas_result.data:
                print("❌ Nenhuma empresa encontrada")
                return
            
            empresa = empresas_result.data[0]
            empresa_id = empresa['id']
            empresa_nome = empresa['nome']
            
            print(f"🧪 Testando ingestão RAG para: {empresa_nome}")
            print(f"📋 Empresa ID: {empresa_id}")
            
            # Executar ingestão
            result = await ingest_empresa_rag(empresa_id, force_update=True)
            
            print("\n✅ Resultado da ingestão:")
            print(f"   📝 Biografias: {result['biografias']}")
            print(f"   🎯 Competências: {result['competencias']}")
            print(f"   ⚙️ Workflows: {result['workflows']}")
            print(f"   📚 Knowledge: {result['knowledge']}")
            print(f"   ❌ Erros: {len(result['errors'])}")
            
            if result['errors']:
                print("\n🚨 Erros encontrados:")
                for error in result['errors'][:3]:  # Mostrar apenas os primeiros 3
                    print(f"   - {error}")
            
            print(f"\n🎉 Ingestão RAG concluída com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro no teste: {e}")
    
    # Executar teste
    asyncio.run(test_ingestion())