# Budget API 🚀

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenTelemetry](https://img.shields.io/badge/OpenTelemetry-Enabled-blueviolet.svg)](https://opentelemetry.io/)

Sistema robusto para gerenciamento de orçamentos, precificação de serviços, pagamentos, faturamento e controle de projetos. Desenvolvido com foco em escalabilidade, observabilidade e integração contínua.

## 📋 Visão Geral

O **Budget API** é uma solução completa para empresas que buscam automatizar seu fluxo financeiro e operacional. Desde a gestão de planos e assinaturas até o faturamento detalhado de projetos, a API oferece uma base sólida e monitorável para operações críticas.

## ✨ Funcionalidades Principais

- 🔐 **Autenticação Segura**: Implementação de JWT (JSON Web Tokens) para controle de acesso.
- 🏢 **Gestão Multitenant**: Gerenciamento de empresas, usuários e permissões.
- 💳 **Integração Asaas**: Automação completa de pagamentos, assinaturas e recebíveis via API Asaas.
- 📊 **Precificação Inteligente**: Motores de cálculo para serviços, materiais e margens.
- 🏗️ **Gestão de Projetos**: Controle de orçamentos e acompanhamento de entregáveis.
- 📈 **Observabilidade Full-Stack**: Monitoramento em tempo real com OpenTelemetry e Grafana LGTM.

## 🛠️ Stack Tecnológica

### Backend & Core
- **FastAPI**: Framework web de alta performance.
- **SQLAlchemy 2.0**: ORM assíncrono para manipulação de dados.
- **Pydantic V2**: Validação de dados e definições de schemas.
- **Alembic**: Gerenciamento de migrações de banco de dados.

### Banco de Dados
- **MySQL / MariaDB**: Armazenamento relacional robusto.
- **aiomysql**: Driver assíncrono para máxima performance.

### Observabilidade (LGTM Stack)
- **OpenTelemetry**: Coleta de métricas e traces.
- **Grafana**: Dashboards e visualização de dados.
- **Mimir/Prometheus**: Armazenamento de métricas.
- **Loki**: Agregação de logs.

## 🏗️ Arquitetura

O projeto adota uma arquitetura em camadas bem definida, facilitando a manutenção e testabilidade:

```text
Routers (API) ──► Services (Business Logic) ──► Repositories (Data Access) ──► Models (Entities)
```

- **Schemas**: Contratos de entrada e saída (Pydantic).
- **Security**: Middlewares e dependências de segurança.
- **Observer**: Camada de instrumentação para telemetria.

## 🚀 Como Começar

### Pré-requisitos
- Python 3.12+
- Docker & Docker Compose (Recomendado)
- MySQL 8.0+

### Instalação via Docker (Recomendado)

1. Clone o repositório:
   ```bash
   git clone https://github.com/JaksonBernardo/budget-api.git
   cd budget-api
   ```

2. Configure as variáveis de ambiente:
   ```bash
   cp .env.example .env
   # Edite as credenciais no arquivo .env
   ```

3. Suba o ambiente completo (API + Monitoring):
   ```bash
   docker-compose up -d
   ```

A API estará disponível em `http://localhost:8001` e o Grafana em `http://localhost:3000`.

### Instalação Manual

1. Crie e ative o ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate # Linux/Mac
   # ou .\venv\Scripts\activate no Windows
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   # Para desenvolvimento:
   pip install -e .[dev]
   ```

3. Execute as migrações:
   ```bash
   alembic upgrade head
   ```

4. Inicie o servidor:
   ```bash
   uvicorn api.app:app --reload --port 8001
   ```

## 📊 Observabilidade

A API está instrumentada para exportar métricas via OTLP. O dashboard customizado pode ser acessado no Grafana, onde é possível monitorar:
- Volume de requisições por endpoint.
- Taxa de sucesso/erro (HTTP status codes).
- Latência de processamento.
- Métricas de negócio (ex: tentativas de login).

## 🧪 Testes

Garantimos a qualidade do código através de uma suíte de testes abrangente.

```bash
# Rodar todos os testes
pytest

# Gerar relatório de cobertura (HTML)
pytest --cov-report=html
```

## 📂 Estrutura de Pastas

```text
.
├── api/
│   ├── core/           # Configurações globais
│   ├── features/       # Lógicas transversais
│   ├── models/         # Entidades SQLAlchemy
│   ├── repositories/   # Camada de persistência
│   ├── routers/        # Endpoints da API
│   ├── schemas/        # Modelos Pydantic
│   ├── services/       # Regras de negócio
│   └── observer.py     # Configuração OpenTelemetry
├── migrations/         # Arquivos do Alembic
├── tests/              # Testes unitários e integração
└── docker-compose.yml  # Orquestração de containers
```

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---
Desenvolvido por [Jakson Bernardo](https://github.com/JaksonBernardo)
