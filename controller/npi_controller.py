import io

import pandas as pd
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database.connection import get_db
from models.calculation import Calculation
from services.npi_service import evaluate_rpn

router = APIRouter()


class Operation(BaseModel):
    operation: str  # exemple d'ops "3 4 +"


@router.post("/calculate/")
def calculate(operation: Operation, db: Session = Depends(get_db)):
    try:
        result = evaluate_rpn(operation.operation)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    calc = Calculation(operation=operation.operation, result=result)
    db.add(calc)
    db.commit()
    db.refresh(calc)

    return {"operation": operation.operation, "result": result}


@router.get("/calculations/")
def get_calculations_csv(db: Session = Depends(get_db)):
    calculations = db.query(Calculation).all()
    data = [{"operation": calc.operation, "result": calc.result} for calc in calculations]
    df = pd.DataFrame(data)
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    stream.seek(0)

    response = StreamingResponse(stream, media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=calculations.csv"

    return response
