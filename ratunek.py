from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError


@app.exception_handler(SQLAlchemyError)
async def db_exception_handler(request: Request, exc: SQLAlchemyError):

    return JSONResponse(
        status_code=500,
        content={"detail": "Ups! Mamy chwilowy problem z bazą danych. Spróbuj ponownie później."},
    )