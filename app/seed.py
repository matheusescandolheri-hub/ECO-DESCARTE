from sqlalchemy import select
from sqlalchemy.orm import Session

from app import services
from app.models import Categoria, PontoColeta


CATEGORIAS_INICIAIS = [
    {
        "nome": "Resíduo perigoso",
        "descricao": "Materiais que podem causar contaminação ou risco à saúde.",
    },
    {
        "nome": "Resíduo reciclável",
        "descricao": "Materiais que podem retornar à cadeia produtiva.",
    },
    {
        "nome": "Resíduo eletrônico",
        "descricao": "Equipamentos e componentes eletrônicos sem uso.",
    },
    {
        "nome": "Resíduo doméstico especial",
        "descricao": "Itens comuns em casa que exigem descarte orientado.",
    },
]


RESIDUOS_INICIAIS = [
    {
        "nome": "Pilha",
        "categoria": "Resíduo perigoso",
        "orientacao_descarte": "Leve pilhas usadas a coletores específicos em mercados, escolas ou ecopontos. Não descarte no lixo comum.",
        "risco_ambiental": "Alto",
        "mensagem_educativa": "Pilhas podem liberar metais pesados no solo e na água quando descartadas incorretamente.",
    },
    {
        "nome": "Bateria",
        "categoria": "Resíduo perigoso",
        "orientacao_descarte": "Entregue baterias em pontos autorizados, assistências técnicas, lojas parceiras ou ecopontos.",
        "risco_ambiental": "Alto",
        "mensagem_educativa": "Baterias exigem logística reversa para reduzir contaminação e reaproveitar materiais.",
    },
    {
        "nome": "Óleo de cozinha",
        "categoria": "Resíduo doméstico especial",
        "orientacao_descarte": "Armazene o óleo frio em garrafa PET fechada e entregue em um ponto de coleta. Não jogue na pia, no ralo ou no solo.",
        "risco_ambiental": "Médio",
        "mensagem_educativa": "Um pequeno volume de óleo pode contaminar muita água e prejudicar redes de esgoto.",
    },
    {
        "nome": "Medicamento vencido",
        "categoria": "Resíduo perigoso",
        "orientacao_descarte": "Leve medicamentos vencidos ou sem uso a farmácias e unidades autorizadas para descarte seguro.",
        "risco_ambiental": "Alto",
        "mensagem_educativa": "Medicamentos no lixo comum ou no vaso sanitário podem contaminar água e afetar seres vivos.",
    },
    {
        "nome": "Vidro",
        "categoria": "Resíduo reciclável",
        "orientacao_descarte": "Separe o vidro limpo, embale cacos com segurança e identifique o material antes de entregar à coleta seletiva.",
        "risco_ambiental": "Médio",
        "mensagem_educativa": "O cuidado no descarte do vidro evita acidentes e favorece a reciclagem.",
    },
    {
        "nome": "Lixo eletrônico",
        "categoria": "Resíduo eletrônico",
        "orientacao_descarte": "Encaminhe equipamentos eletrônicos a ecopontos, campanhas de coleta ou estabelecimentos parceiros.",
        "risco_ambiental": "Alto",
        "mensagem_educativa": "Eletrônicos contêm componentes reaproveitáveis e substâncias que não devem ir para aterros comuns.",
    },
]


PONTOS_INICIAIS = [
    {
        "nome_local": "EcoPonto Central",
        "endereco": "Rua das Árvores, 120",
        "bairro": "Centro",
        "cidade": "São Paulo",
        "tipo_residuo_aceito": "Pilha, Bateria, Vidro",
    },
    {
        "nome_local": "Farmácia Vida",
        "endereco": "Avenida Saúde, 88",
        "bairro": "Jardim América",
        "cidade": "São Paulo",
        "tipo_residuo_aceito": "Medicamento vencido",
    },
    {
        "nome_local": "Mercado Verde",
        "endereco": "Rua do Comércio, 45",
        "bairro": "Centro",
        "cidade": "Campinas",
        "tipo_residuo_aceito": "Óleo de cozinha, Pilha",
    },
    {
        "nome_local": "Centro de Reciclagem Tech",
        "endereco": "Avenida Inovação, 500",
        "bairro": "Tecnopolo",
        "cidade": "Campinas",
        "tipo_residuo_aceito": "Lixo eletrônico, Bateria",
    },
]


def seed_data(db: Session) -> None:
    for dados in CATEGORIAS_INICIAIS:
        services.obter_ou_criar_categoria(db, dados["nome"], dados["descricao"])

    for dados in RESIDUOS_INICIAIS:
        if not any(
            services.normalizar_busca(residuo.nome) == services.normalizar_busca(dados["nome"])
            for residuo in services.listar_residuos(db)
        ):
            services.criar_residuo(db, dados)

    pontos_existentes = db.scalars(select(PontoColeta)).all()
    for dados in PONTOS_INICIAIS:
        ja_existe = any(
            services.normalizar_busca(ponto.nome_local) == services.normalizar_busca(dados["nome_local"])
            and services.normalizar_busca(ponto.tipo_residuo_aceito)
            == services.normalizar_busca(dados["tipo_residuo_aceito"])
            for ponto in pontos_existentes
        )
        if not ja_existe:
            db.add(PontoColeta(**dados))

    db.commit()

