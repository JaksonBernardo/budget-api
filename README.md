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
- FastAPI
- SQLAlchemy
- Alembic (migrations)
- MySQL

## Instalação

```bash
# Clonar o repositório
git clone https://github.com/JaksonBernardo/budget-api.git

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

## Testes

O projeto utiliza pytest para testes automatizados.

### Instalar dependências de desenvolvimento

```bash
pip install pytest pytest-asyncio pytest-cov pytest-mock httpx
```

### Rodar testes

```bash
# Rodar todos os testes
python -m pytest

# Rodar testes com cobertura
python -m pytest --cov=api --cov-report=html

# Rodar testes específicos
python -m pytest tests/unit/
python -m pytest tests/integration/

# Rodar testes em modo verbose
python -m pytest -v
```

### Estrutura de testes

```
tests/
├── conftest.py              # Fixtures e configurações globais
├── unit/                    # Testes unitários
│   ├── repositories/        # Testes de repositórios
│   ├── services/            # Testes de serviços
│   ├── test_schemas.py      # Testes de schemas
│   └── test_exceptions.py   # Testes de exceptions
└── integration/             # Testes de integração
    └── routers/             # Testes de endpoints
```

## License

MIT
