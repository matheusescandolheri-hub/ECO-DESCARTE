import unicodedata

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Categoria, Consulta, PontoColeta, Residuo


SINONIMOS_RESIDUOS = {
    "oleo de cozinha": ["oleo de cozinha", "gordura usada", "gordura pos-consumo"],
    "lixo eletronico": ["lixo eletronico", "eletroeletronicos", "eletronicos"],
    "vidro": ["vidro", "materiais reciclaveis", "reciclaveis"],
    "calica": ["calica", "entulho", "residuos de construcao"],
    "madeira": ["madeira", "moveis"],
    "movel inservivel": ["movel", "moveis", "mobiliario"],
    "residuo vegetal": ["residuo vegetal", "poda", "jardinagem"],
}

SINONIMOS_CATEGORIAS = {
    "residuo reciclavel": ["materiais reciclaveis", "reciclaveis", "vidro"],
    "residuo eletronico": ["eletroeletronicos", "eletronicos", "lixo eletronico"],
    "residuo de construcao civil": ["calica", "madeira", "entulho", "moveis"],
    "residuo vegetal": ["residuo vegetal", "poda", "jardinagem"],
}


def limpar_texto(valor: str | None) -> str:
    return (valor or "").strip()


def normalizar_busca(valor: str | None) -> str:
    texto = unicodedata.normalize("NFD", limpar_texto(valor).casefold())
    return "".join(char for char in texto if unicodedata.category(char) != "Mn")


def listar_categorias(db: Session) -> list[Categoria]:
    return list(db.scalars(select(Categoria).order_by(Categoria.nome)).all())


def listar_residuos(db: Session) -> list[Residuo]:
    return list(db.scalars(select(Residuo).order_by(Residuo.nome)).all())


def listar_pontos(db: Session, incluir_inativos: bool = False) -> list[PontoColeta]:
    query = select(PontoColeta).order_by(PontoColeta.nome_local)
    if not incluir_inativos:
        query = query.where(PontoColeta.ativo.is_(True))
    return list(db.scalars(query).all())


def listar_historico(db: Session) -> list[Consulta]:
    return list(db.scalars(select(Consulta).order_by(Consulta.data_consulta.desc())).all())


def get_or_create_categoria(
    db: Session,
    nome: str,
    descricao: str | None = None,
) -> Categoria:
    nome_limpo = limpar_texto(nome)
    if not nome_limpo:
        raise ValueError("Informe uma categoria válida.")

    nome_normalizado = normalizar_busca(nome_limpo)
    descricao_limpa = limpar_texto(descricao) or None

    for categoria in listar_categorias(db):
        if normalizar_busca(categoria.nome) == nome_normalizado:
            if descricao_limpa and categoria.descricao != descricao_limpa:
                categoria.descricao = descricao_limpa
                db.commit()
                db.refresh(categoria)
            return categoria

    categoria = Categoria(nome=nome_limpo, descricao=descricao_limpa)
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria


obter_ou_criar_categoria = get_or_create_categoria


def buscar_residuo_exato(db: Session, nome: str) -> Residuo | None:
    termo = normalizar_busca(nome)
    if not termo:
        return None

    for residuo in listar_residuos(db):
        if normalizar_busca(residuo.nome) == termo:
            return residuo

    return None


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


def get_or_create_residuo(db: Session, dados: dict[str, str]) -> Residuo:
    nome = limpar_texto(dados.get("nome"))
    if not nome:
        raise ValueError("Informe o nome do resíduo.")

    categoria = get_or_create_categoria(db, dados.get("categoria", ""))
    residuo = buscar_residuo_exato(db, nome)
    campos = {
        "nome": nome,
        "categoria_id": categoria.id,
        "orientacao_descarte": limpar_texto(dados.get("orientacao_descarte")),
        "risco_ambiental": limpar_texto(dados.get("risco_ambiental")),
        "mensagem_educativa": limpar_texto(dados.get("mensagem_educativa")),
    }

    if not campos["orientacao_descarte"] or not campos["risco_ambiental"] or not campos["mensagem_educativa"]:
        raise ValueError("Preencha todos os campos obrigatórios do resíduo.")

    if residuo:
        for campo, valor in campos.items():
            setattr(residuo, campo, valor)
    else:
        residuo = Residuo(**campos)
        db.add(residuo)

    db.commit()
    db.refresh(residuo)
    return residuo


def criar_residuo(db: Session, dados: dict[str, str]) -> Residuo:
    nome = limpar_texto(dados.get("nome"))
    if not nome:
        raise ValueError("Informe o nome do resíduo.")

    if buscar_residuo_exato(db, nome):
        raise ValueError("Já existe um resíduo cadastrado com esse nome.")

    categoria = get_or_create_categoria(db, dados.get("categoria", ""))

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
        "telefone": limpar_texto(dados.get("telefone")) or None,
        "horario_funcionamento": limpar_texto(dados.get("horario_funcionamento")) or None,
        "observacao": limpar_texto(dados.get("observacao")) or None,
        "fonte_dados": limpar_texto(dados.get("fonte_dados")) or "Cadastro manual",
        "ativo": True,
    }

    obrigatorios = ["nome_local", "endereco", "bairro", "cidade", "tipo_residuo_aceito"]
    if any(not campos[campo] for campo in obrigatorios):
        raise ValueError("Preencha todos os campos obrigatórios do ponto de coleta.")

    ponto = PontoColeta(**campos)
    db.add(ponto)
    db.commit()
    db.refresh(ponto)
    return ponto


def buscar_ponto_por_id(db: Session, ponto_id: int) -> PontoColeta | None:
    return db.get(PontoColeta, ponto_id)


def buscar_ponto_por_nome(db: Session, nome_local: str) -> PontoColeta | None:
    nome_normalizado = normalizar_busca(nome_local)
    if not nome_normalizado:
        return None

    for ponto in listar_pontos(db, incluir_inativos=True):
        if normalizar_busca(ponto.nome_local) == nome_normalizado:
            return ponto

    return None


def upsert_ponto_coleta(db: Session, dados: dict[str, str | bool]) -> PontoColeta:
    campos = {
        "nome_local": limpar_texto(str(dados.get("nome_local") or "")),
        "endereco": limpar_texto(str(dados.get("endereco") or "")),
        "bairro": limpar_texto(str(dados.get("bairro") or "")),
        "cidade": limpar_texto(str(dados.get("cidade") or "")),
        "tipo_residuo_aceito": limpar_texto(str(dados.get("tipo_residuo_aceito") or "")),
        "telefone": limpar_texto(str(dados.get("telefone") or "")) or None,
        "horario_funcionamento": limpar_texto(str(dados.get("horario_funcionamento") or "")) or None,
        "observacao": limpar_texto(str(dados.get("observacao") or "")) or None,
        "fonte_dados": limpar_texto(str(dados.get("fonte_dados") or "")) or "Cadastro manual",
        "ativo": bool(dados.get("ativo", True)),
    }

    obrigatorios = ["nome_local", "endereco", "bairro", "cidade", "tipo_residuo_aceito"]
    if any(not campos[campo] for campo in obrigatorios):
        raise ValueError("Preencha todos os campos obrigatórios do ponto de coleta.")

    ponto = buscar_ponto_por_nome(db, str(campos["nome_local"]))
    if ponto:
        for campo, valor in campos.items():
            if campo == "ativo" and ponto.ativo is False:
                continue
            setattr(ponto, campo, valor)
    else:
        ponto = PontoColeta(**campos)
        db.add(ponto)

    db.commit()
    db.refresh(ponto)
    return ponto


def remover_ponto_coleta(db: Session, ponto_id: int) -> PontoColeta | None:
    ponto = buscar_ponto_por_id(db, ponto_id)
    if not ponto:
        return None

    ponto.ativo = False
    db.commit()
    db.refresh(ponto)
    return ponto


def palavras_chave_para_residuo(residuo: Residuo) -> set[str]:
    nome = normalizar_busca(residuo.nome)
    categoria = normalizar_busca(residuo.categoria.nome)
    palavras = {nome, categoria}

    palavras.update(SINONIMOS_RESIDUOS.get(nome, []))
    palavras.update(SINONIMOS_CATEGORIAS.get(categoria, []))

    for termo in [nome, categoria]:
        palavras.update(
            parte for parte in termo.replace(",", " ").split() if len(parte) >= 5
        )

    return {normalizar_busca(palavra) for palavra in palavras if normalizar_busca(palavra)}


def buscar_pontos_compativeis(
    db: Session,
    residuo: Residuo,
    localizacao_usuario: str | None = None,
) -> list[PontoColeta]:
    palavras_chave = palavras_chave_para_residuo(residuo)
    localizacao = normalizar_busca(localizacao_usuario)
    pontos_compativeis: list[PontoColeta] = []

    for ponto in listar_pontos(db):
        tipo_aceito = normalizar_busca(ponto.tipo_residuo_aceito)
        if not any(palavra in tipo_aceito for palavra in palavras_chave):
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
