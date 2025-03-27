import requests
import json
import os
from app.models import db
from app.models.task import TaskInsight
from flask import current_app

class GPTService:
    @staticmethod
    def generate_task_insights(task):
        """
        Gera insights para uma tarefa usando a API do GPT
        """
        # Obter a chave da API do GPT das configurações
        api_key = current_app.config.get('GPT_API_KEY')
        api_url = current_app.config.get('GPT_API_URL')
        
        if not api_key:
            # Se a chave da API não estiver configurada, retornar mensagem de erro
            return {'error': 'API key not configured'}
        
        # Preparar o prompt para o GPT
        prompt = f"""
        Gere insights e recomendações para a seguinte tarefa:
        
        Título: {task.title}
        Descrição: {task.description}
        Data de Vencimento: {task.due_date.strftime('%d/%m/%Y %H:%M')}
        Prioridade: {'Alta' if task.priority == 1 else 'Média' if task.priority == 2 else 'Baixa'}
        
        Por favor, forneça:
        1. Sugestões de conteúdos e tópicos relacionados (por exemplo, materiais de estudo, vídeos, artigos).
        2. Análise de possíveis riscos, como atrasos ou falhas na execução, com dicas para mitigação.
        
        Formate a resposta em JSON com as seguintes chaves:
        - suggestions: lista de sugestões de conteúdo (cada uma com "title" e "url")
        - risks: lista de riscos potenciais (cada um com "description" e "mitigation")
        """
        
        # Preparar a requisição para a API do GPT
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'gpt-4-turbo',
            'messages': [
                {'role': 'system', 'content': 'Você é um assistente especializado em gestão de tarefas e produtividade.'},
                {'role': 'user', 'content': prompt}
            ],
            'temperature': 0.7,
            'max_tokens': 1000
        }
        
        try:
            # Enviar a requisição para a API do GPT
            response = requests.post(api_url, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            
            # Extrair a resposta
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # Analisar o conteúdo JSON da resposta
            insights_data = json.loads(content)
            
            # Salvar sugestões no banco de dados
            for suggestion in insights_data.get('suggestions', []):
                insight = TaskInsight(
                    content=suggestion['title'],
                    related_urls=suggestion.get('url', ''),
                    insight_type='suggestion',
                    task_id=task.id
                )
                db.session.add(insight)
            
            # Salvar riscos no banco de dados
            for risk in insights_data.get('risks', []):
                insight = TaskInsight(
                    content=f"{risk['description']} - Mitigação: {risk['mitigation']}",
                    insight_type='risk',
                    task_id=task.id
                )
                db.session.add(insight)
            
            db.session.commit()
            
            return insights_data
            
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Erro na requisição à API do GPT: {str(e)}")
            return {'error': f'API request error: {str(e)}'}
        except json.JSONDecodeError as e:
            current_app.logger.error(f"Erro ao decodificar a resposta JSON: {str(e)}")
            return {'error': f'JSON decode error: {str(e)}'}
        except Exception as e:
            current_app.logger.error(f"Erro ao gerar insights: {str(e)}")
            return {'error': f'Error generating insights: {str(e)}'}
    
    @staticmethod
    def get_insights_by_task(task_id):
        """
        Obtém insights existentes para uma tarefa
        """
        return TaskInsight.query.filter_by(task_id=task_id).all()