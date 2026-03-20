# Budget API

Sistema para gerenciamento de orçamentos, precificação de serviços, pagamentos, recebimentos, faturamento e projetos.

## Funcionalidades

- **Orçamentos**: Criação e gerenciamento de orçamentos
- **Precificação de Serviços**: Definição e cálculo de preços de serviços
- **Pagamentos**: Gerenciamento de pagamentos
- **Recebimentos**: Controle de recebimentos
- **Faturamento**: Gestão de faturamento
- **Projetos**: Organização e acompanhamento de projetos

## Tecnologias

- Python
- FastAPI (ou Flask/Django - a definir)
- SQLAlchemy
- Alembic (migrations)
- PostgreSQL/SQLite

## Instalação

```bash
# Clonar o repositório
git clone <repository-url>

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env

# Rodar migrations
alembic upgrade head

# Iniciar servidor
uvicorn app.main:app --reload
```

## Configuração

Copie o arquivo `.env.example` para `.env` e configure as variáveis de ambiente conforme necessário.

## License

MIT
