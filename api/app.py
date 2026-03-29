from fastapi import FastAPI, status
from api.core.settings import Settings
from fastapi.middleware.cors import CORSMiddleware

from api.routers.segments import segment_router
from api.routers.clients import client_router
from api.routers.suppliers import supplier_router

app = FastAPI()

app.include_router(segment_router)
app.include_router(client_router)
app.include_router(supplier_router)

origins = [
    Settings().URL_CORS,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.get(
    path = "/health",
    status_code = status.HTTP_200_OK,
    summary = "Verificando status da API...",
    tags = ["Health API"]
)
def health_check(): return {"status": "OK.."}
