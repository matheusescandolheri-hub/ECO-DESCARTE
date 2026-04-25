from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, services
from app.database import get_db


router = APIRouter(prefix="/api", tags=["API"])


@router.get("/residuos", response_model=list[schemas.ResiduoOut])
def listar_residuos(db: Session = Depends(get_db)):
    return services.listar_residuos(db)


@router.post(
    "/residuos",
    response_model=schemas.ResiduoOut,
    status_code=status.HTTP_201_CREATED,
)
def cadastrar_residuo(payload: schemas.ResiduoCreate, db: Session = Depends(get_db)):
    try:
        return services.criar_residuo(db, payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/pontos", response_model=list[schemas.PontoColetaOut])
def listar_pontos(db: Session = Depends(get_db)):
    return services.listar_pontos(db)


@router.post(
    "/pontos",
    response_model=schemas.PontoColetaOut,
    status_code=status.HTTP_201_CREATED,
)
def cadastrar_ponto(payload: schemas.PontoColetaCreate, db: Session = Depends(get_db)):
    try:
        return services.criar_ponto_coleta(db, payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/consultas", response_model=list[schemas.ConsultaOut])
def listar_consultas(db: Session = Depends(get_db)):
    return services.listar_historico(db)


@router.get("/relatorio", response_model=list[schemas.RelatorioItem])
def relatorio(db: Session = Depends(get_db)):
    return services.relatorio_residuos_mais_consultados(db)

