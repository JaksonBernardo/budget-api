from fastapi import FastAPI, status
from api.core.settings import Settings
from fastapi.middleware.cors import CORSMiddleware

from api.routers.segments import segment_router
from api.routers.clients import client_router
from api.routers.suppliers import supplier_router
from api.routers.materials import material_router
from api.routers.users import user_router
from api.routers.auth import auth_router
from api.routers.plans import plan_router
from api.routers.companys import company_router
from api.routers.employees import employee_router
from api.routers.prices import price_router
from api.routers.services import service_router
from api.routers.budgets import budget_router

from api.observer import request_counter

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(plan_router)
app.include_router(company_router)
app.include_router(segment_router)
app.include_router(client_router)
app.include_router(supplier_router)
app.include_router(material_router)
app.include_router(employee_router)
app.include_router(price_router)
app.include_router(service_router)
app.include_router(budget_router)


origins = [
    Settings().URL_CORS,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.middleware("http")
async def count_requests(request, call_next):

    response = await call_next(request)

    request_counter.add(1, attributes={
        "status_code": response.status_code,
    })

    return response

@app.get(
    path = "/health",
    status_code = status.HTTP_200_OK,
    summary = "Verificando status da API...",
    tags = ["Health API"]
)
def health_check(): return {"status": "OK.."}
