from fastapi import HTTPException
from api.exceptions import *


def map_exception(exception: Exception) -> HTTPException:

    exception_map = {
        CompanyNotFound: lambda e: HTTPException(
            status_code=getattr(e, "status_code", 404),
            detail=str(e)
        ),
        InvalidNameCompany: lambda e: HTTPException(
            status_code=getattr(e, "status_code", 400),
            detail = str(e)
        ),
        CnpjAlreadyExists: lambda e: HTTPException(
            status_code=getattr(e, "status_code", 400),
            detail = str(e)
        ),
        NameAlreadyExists: lambda e: HTTPException(
            status_code=getattr(e, "status_code", 400),
            detail = str(e)
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
        ClientNotFound: lambda e: HTTPException(
            status_code = getattr(e, "status_code", 404),
            detail = str(e)
        ),
        SupplierNotFound: lambda e: HTTPException(
            status_code = getattr(e, "status_code", 404),
            detail = str(e)
        ),
        ZeroSupplierId: lambda e: HTTPException(
            status_code = getattr(e, "status_code", 400),
            detail=str(e)
        ),
        MaterialInvalidName: lambda e: HTTPException(
            status_code = getattr(e, "status_code", 400),
            detail = str(e)
        ),
        MaterialNotFound: lambda e: HTTPException(
            status_code = getattr(e, "status_code", 404),
            detail = str(e)
        ),
        UserNotFound: lambda e: HTTPException(
            status_code=getattr(e, "status_code", 404),
            detail=str(e)
        ),
        UserAlreadyExists: lambda e: HTTPException(
            status_code=getattr(e, "status_code", 409),
            detail=str(e)
        ),
        UserAccessDenied: lambda e: HTTPException(
            status_code=getattr(e, "status_code", 403),
            detail=str(e)
        ),
        InvalidUserId: lambda e: HTTPException(
            status_code=getattr(e, "status_code", 400),
            detail=str(e)
        ),
        PlanNegativePrice: lambda e: HTTPException(
            status_code=getattr(e, "status_code", 400),
            detail=str(e)
        ),
        PlanInvalidName: lambda e: HTTPException(
            status_code=getattr(e, "status_code", 400),
            detail=str(e)
        ),
        PlanNotFound: lambda e: HTTPException(
            status_code=getattr(e, "status_code", 404),
            detail=str(e)
        ),
        PlanAlreadyExists: lambda e: HTTPException(
            status_code=getattr(e, "status_code", 409),
            detail=str(e)
        ),
        PlanHaveCompanys: lambda e: HTTPException(
            status_code=getattr(e, "status_code", 403),
            detail=str(e)
        ),
        EmployeeNotFound: lambda e: HTTPException(
            status_code=getattr(e, "status_code", 404),
            detail=str(e)
        ),
        EmployeeAccessDenied: lambda e: HTTPException(
            status_code=getattr(e, "status_code", 403),
            detail=str(e)
        ),
        EmployeeInvalidData: lambda e: HTTPException(
            status_code=400,
            detail=str(e)
        )
    }

    handler = exception_map.get(type(exception))
    if handler:
        return handler(exception)

    return HTTPException(
        status_code=500,
        detail=f"Erro interno: {str(exception)}"
    )

    

