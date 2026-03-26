from fastapi import HTTPException
from api.exceptions import (
    CompanyNotFound,
    SegmentInvalidName,
    SegmentNotFound,
    SegmentAccesDenied,
    InvalidTypeCompanyId,
    ZeroCompanyId
)


def map_exception(exception: Exception) -> HTTPException:
    """
    Mapeia exceções de domínio para HTTPException do FastAPI.
    """
    exception_map = {
        CompanyNotFound: lambda e: HTTPException(
            status_code=getattr(e, "status_code", 404),
            detail=str(e)
        ),
        SegmentNotFound: lambda e: HTTPException(
            status_code=getattr(e, "status_code", 404),
            detail=str(e)
        ),
        SegmentInvalidName: lambda e: HTTPException(
            status_code=400,
            detail=str(e)
        ),
        SegmentAccesDenied: lambda e: HTTPException(
            status_code = getattr(e, "status_code", 403),
            detail=str(e)
        ),
        InvalidTypeCompanyId: lambda e: HTTPException(
            status_code=400,
            detail=str(e)
        ),
        ZeroCompanyId: lambda e: HTTPException(
            status_code=400,
            detail=str(e)
        ),
    }

    handler = exception_map.get(type(exception))
    if handler:
        return handler(exception)

    return HTTPException(
        status_code=500,
        detail=f"Erro interno: {str(exception)}"
    )

    

