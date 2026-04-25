import unicodedata

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Categoria, Consulta, PontoColeta, Residuo


def limpar_texto(valor: str | None) -> str:
    return (valor or "").strip()


def normalizar_busca(valor: str | None) -> str:
    texto = unicodedata.normalize("NFD", limpar_texto(valor).casefold())
    return "".join(char for char in texto if unicodedata.category(char) != "Mn")


def listar_categorias(db: Session) -> list[Categoria]:
    return list(db.scalars(select(Categoria).order_by(Categoria.nome)).all())


def listar_residuos(db: Session) -> list[Residuo]:
    return list(db.scalars(select(Residuo).order_by(Residuo.nome)).all())


def listar_pontos(db: Session) -> list[PontoColeta]:
    return list(db.scalars(select(PontoColeta).order_by(PontoColeta.nome_local)).all())


def listar_historico(db: Session) -> list[Consulta]:
    return list(db.scalars(select(Consulta).order_by(Consulta.data_consulta.desc())).all())


def obter_ou_criar_categoria(
    db: Session,
    nome: str,
    descricao: str | None = None,
) -> Categoria:
    nome_limpo = limpar_texto(nome)
    if not nome_limpo:
        raise ValueError("Informe uma categoria válida.")

    nome_normalizado = normalizar_busca(nome_limpo)
    for categoria in listar_categorias(db):
        if normalizar_busca(categoria.nome) == nome_normalizado:
            return categoria

    categoria = Categoria(nome=nome_limpo, descricao=limpar_texto(descricao) or None)
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria


def buscar_residuo_por_nome(db: Session, nome: str) -> Residuo | None:
    termo = normalizar_busca(nome)
    if not termo:
        return None

    residuos = listar_residuos(db)
    for residuo in residuos:
        if normalizar_busca(residuo.nome) == termo:
            return residuo

    for residuo in residuos:
        nome_normalizado = normalizar_busca(residuo.nome)
        if termo in nome_normalizado or nome_normalizado in termo:
            return residuo

    return None


def criar_residuo(db: Session, dados: dict[str, str]) -> Residuo:
    nome = limpar_texto(dados.get("nome"))
    if not nome:
        raise ValueError("Informe o nome do resíduo.")

    if buscar_residuo_por_nome(db, nome) and any(
        normalizar_busca(residuo.nome) == normalizar_busca(nome)
        for residuo in listar_residuos(db)
    ):
        raise ValueError("Já existe um resíduo cadastrado com esse nome.")

    categoria = obter_ou_criar_categoria(db, dados.get("categoria", ""))

    residuo = Residuo(
        nome=nome,
        categoria_id=categoria.id,
        orientacao_descarte=limpar_texto(dados.get("orientacao_descarte")),
        risco_ambiental=limpar_texto(dados.get("risco_ambiental")),
        mensagem_educativa=limpar_texto(dados.get("mensagem_educativa")),
    )

    if not residuo.orientacao_descarte or not residuo.risco_ambiental or not residuo.mensagem_educativa:
        raise ValueError("Preencha todos os campos obrigatórios do resíduo.")

    db.add(residuo)
    db.commit()
    db.refresh(residuo)
    return residuo


def criar_ponto_coleta(db: Session, dados: dict[str, str]) -> PontoColeta:
    campos = {
        "nome_local": limpar_texto(dados.get("nome_local")),
        "endereco": limpar_texto(dados.get("endereco")),
        "bairro": limpar_texto(dados.get("bairro")),
        "cidade": limpar_texto(dados.get("cidade")),
        "tipo_residuo_aceito": limpar_texto(dados.get("tipo_residuo_aceito")),
    }

    if any(not valor for valor in campos.values()):
        raise ValueError("Preencha todos os campos do ponto de coleta.")

    ponto = PontoColeta(**campos)
    db.add(ponto)
    db.commit()
    db.refresh(ponto)
    return ponto


def buscar_pontos_compativeis(
    db: Session,
    residuo: Residuo,
    localizacao_usuario: str | None = None,
) -> list[PontoColeta]:
    residuo_nome = normalizar_busca(residuo.nome)
    categoria_nome = normalizar_busca(residuo.categoria.nome)
    localizacao = normalizar_busca(localizacao_usuario)
    pontos_compativeis: list[PontoColeta] = []

    for ponto in listar_pontos(db):
        tipo_aceito = normalizar_busca(ponto.tipo_residuo_aceito)
        aceita_residuo = residuo_nome in tipo_aceito or tipo_aceito in residuo_nome
        aceita_categoria = categoria_nome and categoria_nome in tipo_aceito

        if not aceita_residuo and not aceita_categoria:
            continue

        if localizacao:
            endereco_completo = normalizar_busca(
                f"{ponto.endereco} {ponto.bairro} {ponto.cidade}"
            )
            if localizacao not in endereco_completo:
                continue

        pontos_compativeis.append(ponto)

    return pontos_compativeis


def registrar_consulta(
    db: Session,
    nome_residuo: str,
    localizacao_usuario: str | None = None,
) -> Consulta:
    nome = limpar_texto(nome_residuo)
    if not nome:
        raise ValueError("Informe o nome do resíduo para consultar.")

    consulta = Consulta(
        nome_residuo=nome,
        localizacao_usuario=limpar_texto(localizacao_usuario) or None,
    )
    db.add(consulta)
    db.commit()
    db.refresh(consulta)
    return consulta


def consultar_residuo(
    db: Session,
    nome_residuo: str,
    localizacao_usuario: str | None = None,
) -> dict[str, object]:
    consulta = registrar_consulta(db, nome_residuo, localizacao_usuario)
    residuo = buscar_residuo_por_nome(db, nome_residuo)

    if not residuo:
        return {
            "encontrado": False,
            "termo": limpar_texto(nome_residuo),
            "consulta": consulta,
            "pontos": [],
        }

    pontos = buscar_pontos_compativeis(db, residuo, localizacao_usuario)
    return {
        "encontrado": True,
        "termo": limpar_texto(nome_residuo),
        "residuo": residuo,
        "pontos": pontos,
        "consulta": consulta,
    }


def relatorio_residuos_mais_consultados(db: Session) -> list[dict[str, int | str]]:
    consultas = db.scalars(select(Consulta)).all()
    agrupado: dict[str, dict[str, int | str]] = {}

    for consulta in consultas:
        chave = normalizar_busca(consulta.nome_residuo)
        if not chave:
            continue

        if chave not in agrupado:
            agrupado[chave] = {
                "nome_residuo": limpar_texto(consulta.nome_residuo),
                "total_consultas": 0,
            }

        agrupado[chave]["total_consultas"] = int(agrupado[chave]["total_consultas"]) + 1

    return sorted(
        agrupado.values(),
        key=lambda item: (-int(item["total_consultas"]), str(item["nome_residuo"]).casefold()),
    )

