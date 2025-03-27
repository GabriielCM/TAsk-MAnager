# TaskMaster - Sistema de Gerenciamento de Tempo, Tarefas e Alimentação

TaskMaster é uma aplicação web desenvolvida com Python e Flask para gerenciamento de tarefas diárias, organização de tempo e controle alimentar. Este sistema integra-se com a API do GPT para gerar insights e recomendações personalizadas, proporcionando uma experiência completa para organização pessoal.

## Recursos Principais

### 1. Gerenciamento de Tarefas
- Criação, edição e exclusão de tarefas
- Categorização por prioridades (alta, média, baixa)
- Organização por categorias personalizáveis
- Visualização em lista e grid
- Sistema de filtragem avançado
- Suporte a recorrência (diária, semanal, mensal, anual)

### 2. Sistema de Notificações
- Lembretes automáticos para tarefas próximas do prazo
- Notificações em tempo real no navegador
- Histórico de notificações
- Alertas sonoros (opcional)

### 3. Integração com API GPT
- Geração de insights e recomendações personalizadas para tarefas
- Sugestões de conteúdos e materiais relacionados
- Análise de possíveis riscos e dicas para mitigação
- Recomendações contextuais baseadas no histórico de atividades

### 4. Controle Alimentar
- Registro de refeições diárias (café da manhã, almoço, jantar, lanches)
- Cadastro e pesquisa de alimentos com informações nutricionais
- Cálculo automático de calorias e macronutrientes
- Visualização de dados nutricionais em gráficos

### 5. Dashboard Interativo
- Visão geral do dia, semana e mês
- Estatísticas de desempenho e produtividade
- Resumo nutricional com distribuição de macronutrientes
- Gráficos interativos para análise de dados

### 6. Autenticação e Segurança
- Sistema de registro e login de usuários
- Proteção de rotas com JWT
- Ambiente personalizado para cada usuário

## Tecnologias Utilizadas

### Backend
- **Python 3.8+**
- **Flask**: Framework web
- **SQLAlchemy**: ORM para interação com banco de dados
- **Flask-JWT-Extended**: Autenticação com tokens JWT
- **Flask-Migrate**: Migrações de banco de dados
- **Requests**: Integração com APIs externas

### Frontend
- **HTML5/CSS3/JavaScript**
- **Bootstrap 5**: Framework CSS para design responsivo
- **Chart.js**: Biblioteca para criação de gráficos
- **Axios**: Cliente HTTP para requisições AJAX

### Banco de Dados
- **SQLite** (desenvolvimento)
- **PostgreSQL** (produção)

### APIs e Serviços
- **API OpenAI GPT**: Geração de insights e recomendações

## Estrutura do Projeto

```
task_manager/
│
├── app/
│   ├── __init__.py             # Inicialização da aplicação Flask
│   ├── config.py               # Configurações da aplicação
│   ├── models/                 # Modelos do banco de dados
│   ├── api/                    # API endpoints
│   ├── services/               # Serviços de negócio
│   ├── static/                 # Arquivos estáticos
│   └── templates/              # Templates HTML
│
├── migrations/                 # Migrações do banco de dados
│
├── tests/                      # Testes
│
├── .env                        # Variáveis de ambiente
├── .gitignore                  # Arquivos ignorados pelo git
├── requirements.txt            # Dependências do projeto
└── README.md                   # Documentação
```

## Instalação e Configuração

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)
- Virtualenv (recomendado)

### Passos para Instalação

1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/task-manager.git
cd task-manager
```

2. Crie e ative um ambiente virtual
```bash
python -m venv venv
# No Windows
venv\Scripts\activate
# No Linux/MacOS
source venv/bin/activate
```

3. Instale as dependências
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente
```bash
# Crie um arquivo .env na raiz do projeto
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. Inicialize o banco de dados
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. Execute a aplicação
```bash
flask run
```

7. Acesse a aplicação em `http://localhost:5000`

### Configuração para Produção

Para implantar a aplicação em ambiente de produção, algumas configurações adicionais são necessárias:

1. Configure o `FLASK_ENV` para `production` no arquivo `.env`:
```
FLASK_ENV=production
```

2. Utilize um servidor WSGI como Gunicorn:
```bash
pip install gunicorn
gunicorn "app:create_app('production')" -w 4
```

3. Configure o banco de dados PostgreSQL:
```
DATABASE_URL=postgresql://username:password@localhost/databasename
```

4. Configure um proxy reverso com Nginx ou Apache

## Configuração da API GPT

Para utilizar os recursos de insights baseados em IA, é necessário configurar a integração com a API GPT:

1. Obtenha uma chave de API da OpenAI em [https://platform.openai.com](https://platform.openai.com)

2. Adicione a chave ao arquivo `.env`:
```
GPT_API_KEY=sua-chave-api-aqui
GPT_API_URL=https://api.openai.com/v1/chat/completions
```

## Estrutura do Banco de Dados

O sistema utiliza as seguintes tabelas principais:

1. **users**: Armazena informações dos usuários
2. **tasks**: Registra as tarefas do usuário
3. **task_categories**: Categorias de tarefas
4. **task_insights**: Insights gerados para as tarefas
5. **notifications**: Notificações do sistema
6. **meals**: Registros de refeições
7. **food_items**: Catálogo de alimentos
8. **meal_items**: Itens de cada refeição

## Testes

O projeto inclui testes unitários e de integração. Para executar os testes:

```bash
# Executar todos os testes
pytest

# Executar testes específicos
pytest tests/test_auth.py
```

## Documentação da API

A API REST do TaskMaster fornece acesso a todas as funcionalidades. A documentação completa está disponível em `/api/docs` após iniciar a aplicação.

### Endpoints Principais

#### Autenticação
- `POST /api/auth/register`: Registrar novo usuário
- `POST /api/auth/login`: Autenticar usuário
- `GET /api/auth/profile`: Obter perfil do usuário

#### Tarefas
- `GET /api/tasks`: Listar tarefas
- `POST /api/tasks`: Criar nova tarefa
- `GET /api/tasks/<id>`: Obter detalhes da tarefa
- `PUT /api/tasks/<id>`: Atualizar tarefa
- `DELETE /api/tasks/<id>`: Excluir tarefa
- `PUT /api/tasks/<id>/complete`: Marcar tarefa como concluída

#### Insights
- `GET /api/insights/task/<id>`: Obter insights de uma tarefa
- `POST /api/insights/task/<id>/generate`: Gerar novos insights

#### Refeições
- `GET /api/meals`: Listar refeições
- `POST /api/meals`: Registrar nova refeição
- `GET /api/meals/nutrition-summary`: Obter resumo nutricional
- `GET /api/meals/food-items`: Pesquisar alimentos
- `POST /api/meals/food-items`: Adicionar novo alimento

## Contribuindo

Contribuições são bem-vindas! Por favor, siga estes passos:

1. Faça um fork do repositório
2. Crie um branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Faça commit das suas alterações (`git commit -am 'Adiciona nova funcionalidade'`)
4. Faça push para o branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes.

## Contato

Para suporte ou perguntas, entre em contato pelo email: contato@taskmaster.com

---

Desenvolvido por [Seu Nome] © 2025