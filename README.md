# Budget API

Sistema para gerenciamento de orçamentos, precificação de serviços, pagamentos, recebimentos, faturamento e projetos.

## Funcionalidades

- **Autenticação**: Sistema de autenticação com JWT
- **Empresas (Companies)**: Cadastro, atualização e exclusão de empresas assinantes com integração Asaas
- **Planos**: Gerenciamento de planos de assinatura
- **Assinaturas (Subscriptions)**: Criação e gerenciamento de assinaturas via Asaas
- **Clientes**: Criação e gerenciamento de clientes
- **Fornecedores**: Gerenciamento de fornecedores
- **Materiais**: Controle de materiais
- **Segmentos**: Organização por segmentos
- **Usuários**: Gerenciamento de usuários por empresa
- **Orçamentos**: Criação e gerenciamento de orçamentos
- **Precificação de Serviços**: Definição e cálculo de preços de serviços
- **Pagamentos**: Gerenciamento de pagamentos
- **Recebimentos**: Controle de recebimentos
- **Faturamento**: Gestão de faturamento
- **Projetos**: Organização e acompanhamento de projetos

## Tecnologias

- Python 3.12
- FastAPI
- SQLAlchemy (Async)
- Alembic (migrations)
- Pydantic
- Asaas API (integração de pagamentos)
- MySQL

## Instalação

```bash
# Clonar o repositório
git clone https://github.com/JaksonBernardo/budget-api.git

# Entrar no diretório
cd budget-api

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Edite o .env com suas configurações

# Rodar migrations
alembic upgrade head

# Iniciar servidor
uvicorn api.app:app --reload
```

## Configuração

Copie o arquivo `.env.example` para `.env` e configure as variáveis de ambiente conforme necessário:

- `DATABASE_URL`: URL de conexão com o banco de dados
- `ASAAS_ENVIRONMENT`: Ambiente da Asaas (`sandbox` ou `production`)
- `ASAAS_API_KEY`: Chave de API da Asaas
- `URL_CORS`: URL permitida para CORS

## API Endpoints

### Auth
- `POST /api/v1/auth/login` - Autenticação de usuário

### Companies
- `POST /api/v1/companies` - Criar nova empresa e assinatura
- `GET /api/v1/companies` - Listar empresas
- `GET /api/v1/companies/{id}` - Obter empresa por ID
- `PUT /api/v1/companies/{id}` - Atualizar empresa
- `DELETE /api/v1/companies/{id}` - Deletar empresa

### Plans
- `POST /api/v1/plans` - Criar plano
- `GET /api/v1/plans` - Listar planos
- `GET /api/v1/plans/{id}` - Obter plano por ID
- `PUT /api/v1/plans/{id}` - Atualizar plano
- `DELETE /api/v1/plans/{id}` - Deletar plano

### Users
- `POST /api/v1/users` - Criar usuário
- `GET /api/v1/users` - Listar usuários
- `GET /api/v1/users/{id}` - Obter usuário por ID
- `PUT /api/v1/users/{id}` - Atualizar usuário
- `DELETE /api/v1/users/{id}` - Deletar usuário

### Clients
- `POST /api/v1/clients` - Criar cliente
- `GET /api/v1/clients` - Listar clientes
- `GET /api/v1/clients/{id}` - Obter cliente por ID
- `PUT /api/v1/clients/{id}` - Atualizar cliente
- `DELETE /api/v1/clients/{id}` - Deletar cliente

### Suppliers
- `POST /api/v1/suppliers` - Criar fornecedor
- `GET /api/v1/suppliers` - Listar fornecedores
- `GET /api/v1/suppliers/{id}` - Obter fornecedor por ID
- `PUT /api/v1/suppliers/{id}` - Atualizar fornecedor
- `DELETE /api/v1/suppliers/{id}` - Deletar fornecedor

### Materials
- `POST /api/v1/materials` - Criar material
- `GET /api/v1/materials` - Listar materiais
- `GET /api/v1/materials/{id}` - Obter material por ID
- `PUT /api/v1/materials/{id}` - Atualizar material
- `DELETE /api/v1/materials/{id}` - Deletar material

### Segments
- `POST /api/v1/segments` - Criar segmento
- `GET /api/v1/segments` - Listar segmentos
- `GET /api/v1/segments/{id}` - Obter segmento por ID
- `PUT /api/v1/segments/{id}` - Atualizar segmento
- `DELETE /api/v1/segments/{id}` - Deletar segmento

### Health
- `GET /health` - Verificar status da API

## Arquitetura

O projeto segue o padrão de camadas:

```
Routers → Services → Repositories → Models
```

- **Routers**: Definem os endpoints e fazem a orquestração
- **Services**: Contêm a lógica de negócio
- **Repositories**: Responsáveis pelo acesso ao banco de dados
- **Models**: Definem as entidades do banco de dados
- **Schemas**: Validação e serialização de dados com Pydantic

## Integração Asaas

A API integra com a Asaas para:
- Criar clientes na plataforma de pagamentos
- Gerenciar assinaturas (subscriptions)
- Atualizar dados de clientes
- Cancelar clientes e assinaturas

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

## Licença

MIT
