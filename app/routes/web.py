from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import services
from app.database import get_db


router = APIRouter()
templates = Jinja2Templates(directory="templates")


def render(request: Request, template_name: str, context: dict | None = None):
    page_context = {"request": request}
    if context:
        page_context.update(context)
    return templates.TemplateResponse(request, template_name, page_context)


@router.get("/", response_class=HTMLResponse)
def pagina_inicial(request: Request):
    return render(request, "index.html")


@router.get("/consulta", response_class=HTMLResponse)
def pagina_consulta(request: Request):
    return render(request, "consulta.html")


@router.post("/consulta", response_class=HTMLResponse)
def realizar_consulta(
    request: Request,
    nome_residuo: str = Form(...),
    localizacao_usuario: str = Form(""),
    db: Session = Depends(get_db),
):
    try:
        resultado = services.consultar_residuo(db, nome_residuo, localizacao_usuario)
    except ValueError as exc:
        return render(
            request,
            "consulta.html",
            {
                "erro": str(exc),
                "nome_residuo": nome_residuo,
                "localizacao_usuario": localizacao_usuario,
            },
        )

    return render(
        request,
        "resultado.html",
        {
            "localizacao_usuario": localizacao_usuario,
            **resultado,
        },
    )


@router.get("/residuos/novo", response_class=HTMLResponse)
def pagina_cadastrar_residuo(request: Request, db: Session = Depends(get_db)):
    return render(
        request,
        "cadastrar_residuo.html",
        {
            "categorias": services.listar_categorias(db),
        },
    )


@router.post("/residuos/novo", response_class=HTMLResponse)
def cadastrar_residuo(
    request: Request,
    nome: str = Form(...),
    categoria: str = Form(...),
    orientacao_descarte: str = Form(...),
    risco_ambiental: str = Form(...),
    mensagem_educativa: str = Form(...),
    db: Session = Depends(get_db),
):
    dados = {
        "nome": nome,
        "categoria": categoria,
        "orientacao_descarte": orientacao_descarte,
        "risco_ambiental": risco_ambiental,
        "mensagem_educativa": mensagem_educativa,
    }

    try:
        residuo = services.criar_residuo(db, dados)
    except ValueError as exc:
        return render(
            request,
            "cadastrar_residuo.html",
            {
                "erro": str(exc),
                "dados": dados,
                "categorias": services.listar_categorias(db),
            },
        )

    return render(
        request,
        "cadastrar_residuo.html",
        {
            "sucesso": f"Resíduo '{residuo.nome}' cadastrado com sucesso.",
            "categorias": services.listar_categorias(db),
        },
    )


@router.get("/pontos/novo", response_class=HTMLResponse)
def pagina_cadastrar_ponto(request: Request):
    return render(request, "cadastrar_ponto.html")


@router.post("/pontos/novo", response_class=HTMLResponse)
def cadastrar_ponto(
    request: Request,
    nome_local: str = Form(...),
    endereco: str = Form(...),
    bairro: str = Form(...),
    cidade: str = Form(...),
    tipo_residuo_aceito: str = Form(...),
    db: Session = Depends(get_db),
):
    dados = {
        "nome_local": nome_local,
        "endereco": endereco,
        "bairro": bairro,
        "cidade": cidade,
        "tipo_residuo_aceito": tipo_residuo_aceito,
    }

    try:
        ponto = services.criar_ponto_coleta(db, dados)
    except ValueError as exc:
        return render(
            request,
            "cadastrar_ponto.html",
            {
                "erro": str(exc),
                "dados": dados,
            },
        )

    return render(
        request,
        "cadastrar_ponto.html",
        {
            "sucesso": f"Ponto de coleta '{ponto.nome_local}' cadastrado com sucesso.",
        },
    )


@router.get("/historico", response_class=HTMLResponse)
def historico(request: Request, db: Session = Depends(get_db)):
    return render(
        request,
        "historico.html",
        {
            "consultas": services.listar_historico(db),
        },
    )


@router.get("/relatorio", response_class=HTMLResponse)
def relatorio(request: Request, db: Session = Depends(get_db)):
    return render(
        request,
        "relatorio.html",
        {
            "itens": services.relatorio_residuos_mais_consultados(db),
        },
    )
