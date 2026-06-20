from fastapi import HTTPException
from api.exceptions import *
from api.observer import request_counter

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
        ),
        PriceNotFound: lambda e: HTTPException(
            status_code=getattr(e, "status_code", 404),
            detail=str(e)
        ),
        PriceExceedValue: lambda e: HTTPException(
            status_code=getattr(e, "status_code", 400),
            detail=str(e)
        ),
        PriceInvalidName: lambda e: HTTPException(
            status_code=getattr(e, "status_code", 400),
            detail=str(e)
        ),
        PriceInvalidValue: lambda e: HTTPException(
            status_code=getattr(e, "status_code", 400),
            detail=str(e)
        ),
        ServiceNotFound: lambda e: HTTPException(
            status_code = getattr(e, "status_code", 404),
            detail = str(e)
        ),
        ServiceInvalidName: lambda e: HTTPException(
            status_code = getattr(e, "status_code", 400),
            detail = str(e)
        ),
        ServiceAccesDenied: lambda e: HTTPException(
            status_code = getattr(e, "status_code", 403),
            detail = str(e)
        ),
        ServicePriceNotFound: lambda e: HTTPException(
            status_code = getattr(e, "status_code", 404),
            detail = str(e)
        ),
        StatusBudgetNotFound: lambda e: HTTPException(
            status_code = getattr(e, "status_code", 404),
            detail = str(e)
        ),
        StatusBudgetInvalidName: lambda e: HTTPException(
            status_code = getattr(e, "status_code", 400),
            detail = str(e)
        ),
        StatusBudgetIsSaleAlreadyExists: lambda e: HTTPException(
            status_code = getattr(e, "status_code", 400),
            detail = str(e)
        ),
        StatusProjectNotFound: lambda e: HTTPException(
            status_code = getattr(e, "status_code", 404),
            detail = str(e)
        ),
        StatusProjectInvalidName: lambda e: HTTPException(
            status_code = getattr(e, "status_code", 400),
            detail = str(e)
        ),
        StatusProjectIsCompletedAlreadyExists: lambda e: HTTPException(
            status_code = getattr(e, "status_code", 400),
            detail = str(e)
        ),
        StatusProjectAccesDenied: lambda e: HTTPException(
            status_code = getattr(e, "status_code", 403),
            detail = str(e)
        ),
        BudgetNotFound: lambda e: HTTPException(
            status_code = getattr(e, "status_code", 404),
            detail = str(e)
        ),
        PaymentConditionNotFound: lambda e: HTTPException(
            status_code = getattr(e, "status_code", 404),
            detail = str(e)
        ),
        PaymentConditionAccesDenied: lambda e: HTTPException(
            status_code = getattr(e, "status_code", 403),
            detail = str(e)
        ),
        PaymentConditionAssociatedWithBudget: lambda e: HTTPException(
            status_code = getattr(e, "status_code", 400),
            detail = str(e)
        ),
        PaymentConditionInvalidName: lambda e: HTTPException(
            status_code = getattr(e, "status_code", 400),
            detail = str(e)
        ),
        PaymentConditionNameAlreadyExists: lambda e: HTTPException(
            status_code = getattr(e, "status_code", 400),
            detail = str(e)
        ),
        ProjectNotFound: lambda e: HTTPException(
            status_code = getattr(e, "status_code"),
            detail = str(e)
        ),
        ProjectInvalidOs: lambda e: HTTPException(
            status_code = getattr(e, "status_code"),
            detail = str(e)
        ),
        ProjectServiceNotFound: lambda e: HTTPException(
            status_code = getattr(e, "status_code"),
            detail = str(e)
        )
    }

    handler = exception_map.get(type(exception))
    if handler:
        http_exc = handler(exception)
        request_counter.add(1, {
            "status_code": str(http_exc.status_code),
            "exception_type": type(exception).__name__
        })
        return http_exc
    
    request_counter.add(1, {
        "status_code": "500",
        "exception_type": type(exception).__name__
    })

    return HTTPException(
        status_code=500,
        detail=f"Erro interno: {str(exception)}"
    )
