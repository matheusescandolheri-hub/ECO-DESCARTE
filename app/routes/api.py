from fastapi import APIRouter, Depends, HTTPException, Query, status
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


@router.get("/pontos", response_model=list[schemas.PontoColetaRead])
def listar_pontos(
    incluir_inativos: bool = Query(default=False),
    db: Session = Depends(get_db),
):
    return services.listar_pontos(db, incluir_inativos=incluir_inativos)


@router.post(
    "/pontos",
    response_model=schemas.PontoColetaRead,
    status_code=status.HTTP_201_CREATED,
)
def cadastrar_ponto(payload: schemas.PontoColetaCreate, db: Session = Depends(get_db)):
    try:
        return services.criar_ponto_coleta(db, payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.delete("/pontos/{ponto_id}", response_model=schemas.PontoColetaDeleteResponse)
def remover_ponto(ponto_id: int, db: Session = Depends(get_db)):
    ponto = services.remover_ponto_coleta(db, ponto_id)
    if not ponto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ponto de coleta não encontrado.",
        )

    return {
        "success": True,
        "message": "Ponto de coleta removido com sucesso.",
        "id": ponto.id,
    }


@router.get("/consultas", response_model=list[schemas.ConsultaOut])
def listar_consultas(db: Session = Depends(get_db)):
    return services.listar_historico(db)


@router.get("/relatorio", response_model=list[schemas.RelatorioItem])
def relatorio(db: Session = Depends(get_db)):
    return services.relatorio_residuos_mais_consultados(db)
