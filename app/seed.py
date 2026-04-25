from sqlalchemy.orm import Session

from app import services


HORARIO_ECOPONTOS_CURITIBA = "Segunda a sábado, das 8h às 12h e das 13h às 17h"
FONTE_ECOPONTOS_CURITIBA = "Prefeitura de Curitiba - Ecopontos - Descarte correto de resíduos"
TIPOS_ECOPONTO_MISTO = (
    "caliça, madeira, resíduo vegetal, móveis, eletroeletrônicos, óleo de cozinha, "
    "gordura usada"
)
TIPOS_PARQUE_GOMM = "materiais recicláveis, óleo de cozinha, gordura usada"


CATEGORIAS_INICIAIS = [
    {
        "nome": "Resíduo perigoso",
        "descricao": "Materiais que oferecem risco ao meio ambiente ou à saúde quando descartados incorretamente.",
    },
    {
        "nome": "Resíduo reciclável",
        "descricao": "Materiais que podem passar por processo de reciclagem e retornar à cadeia produtiva.",
    },
    {
        "nome": "Resíduo eletrônico",
        "descricao": "Equipamentos, peças ou componentes eletrônicos sem uso ou danificados.",
    },
    {
        "nome": "Resíduo doméstico especial",
        "descricao": "Materiais gerados em ambiente doméstico que exigem descarte orientado.",
    },
    {
        "nome": "Resíduo de construção civil",
        "descricao": "Restos de pequenas obras, reformas e reparos, como caliça, madeira e entulho.",
    },
    {
        "nome": "Resíduo vegetal",
        "descricao": "Restos de poda, jardinagem e limpeza de áreas verdes.",
    },
]


RESIDUOS_INICIAIS = [
    {
        "nome": "Pilha",
        "categoria": "Resíduo perigoso",
        "orientacao_descarte": "Não descartar no lixo comum. Armazenar em local seco e entregar em ponto de coleta adequado.",
        "risco_ambiental": "Alto",
        "mensagem_educativa": "Pilhas podem conter metais pesados e contaminar o solo e a água.",
    },
    {
        "nome": "Bateria",
        "categoria": "Resíduo perigoso",
        "orientacao_descarte": "Não descartar no lixo comum. Entregar em pontos de coleta específicos ou estabelecimentos autorizados.",
        "risco_ambiental": "Alto",
        "mensagem_educativa": "Baterias podem liberar substâncias tóxicas quando descartadas incorretamente.",
    },
    {
        "nome": "Óleo de cozinha",
        "categoria": "Resíduo doméstico especial",
        "orientacao_descarte": "Não jogar na pia, no solo ou no ralo. Armazenar em garrafa fechada e entregar em ponto de coleta.",
        "risco_ambiental": "Médio",
        "mensagem_educativa": "Um litro de óleo pode contaminar grandes volumes de água.",
    },
    {
        "nome": "Medicamento vencido",
        "categoria": "Resíduo perigoso",
        "orientacao_descarte": "Não jogar no lixo comum, pia ou vaso sanitário. Entregar em farmácias ou pontos autorizados.",
        "risco_ambiental": "Alto",
        "mensagem_educativa": "Medicamentos descartados incorretamente podem contaminar a água e prejudicar a saúde pública.",
    },
    {
        "nome": "Vidro",
        "categoria": "Resíduo reciclável",
        "orientacao_descarte": "Separar com cuidado, embalar se estiver quebrado e encaminhar para reciclagem.",
        "risco_ambiental": "Médio",
        "mensagem_educativa": "O vidro pode ser reciclado, mas deve ser separado com segurança para evitar acidentes.",
    },
    {
        "nome": "Lixo eletrônico",
        "categoria": "Resíduo eletrônico",
        "orientacao_descarte": "Encaminhar equipamentos e componentes eletrônicos a ecopontos ou locais de logística reversa.",
        "risco_ambiental": "Alto",
        "mensagem_educativa": "Equipamentos eletrônicos possuem metais e componentes que exigem descarte adequado.",
    },
    {
        "nome": "Caliça",
        "categoria": "Resíduo de construção civil",
        "orientacao_descarte": "Separar de outros resíduos e encaminhar para Ecoponto autorizado.",
        "risco_ambiental": "Médio",
        "mensagem_educativa": "O descarte irregular de resíduos de construção prejudica vias públicas, rios e terrenos.",
    },
    {
        "nome": "Madeira",
        "categoria": "Resíduo de construção civil",
        "orientacao_descarte": "Separar e encaminhar para Ecoponto que receba resíduos de construção e móveis.",
        "risco_ambiental": "Médio",
        "mensagem_educativa": "Madeiras podem ser reaproveitadas ou destinadas corretamente quando separadas.",
    },
    {
        "nome": "Móvel inservível",
        "categoria": "Resíduo doméstico especial",
        "orientacao_descarte": "Encaminhar para Ecoponto ou serviço autorizado de coleta.",
        "risco_ambiental": "Médio",
        "mensagem_educativa": "Móveis descartados em vias públicas prejudicam a cidade e favorecem problemas sanitários.",
    },
    {
        "nome": "Resíduo vegetal",
        "categoria": "Resíduo vegetal",
        "orientacao_descarte": "Encaminhar restos de poda e jardinagem para Ecoponto autorizado.",
        "risco_ambiental": "Baixo",
        "mensagem_educativa": "Resíduos vegetais podem ser destinados corretamente e até reaproveitados em compostagem.",
    },
]


ECOPONTOS_CURITIBA = [
    {
        "nome_local": "Ecoponto Caiuá",
        "endereco": "Av. Juscelino Kubitschek de Oliveira - Ld, 6800",
        "bairro": "Cidade Industrial de Curitiba",
        "observacao": "Esquina com a Estrada Velha do Barigui.",
    },
    {
        "nome_local": "Ecoponto Cajuru",
        "endereco": "R. Neusa Vieira Bet, 255",
        "bairro": "Cajuru",
        "observacao": "Esquina com a R. Augusto Forbeck.",
    },
    {
        "nome_local": "Ecoponto Campo de Santana",
        "endereco": "R. Teresa de Freitas Tavares, 331",
        "bairro": "Campo de Santana",
        "observacao": "Regional Tatuquara.",
    },
    {
        "nome_local": "Ecoponto CIC",
        "endereco": "R. Orestes Thá, 1765",
        "bairro": "Cidade Industrial de Curitiba",
        "observacao": "Ecoponto misto.",
    },
    {
        "nome_local": "Ecoponto Érico Veríssimo",
        "endereco": "R. Cap. Amin Mosse, 557",
        "bairro": "Alto Boqueirão",
        "observacao": "Anexo à Praça Claudio Manoel Loyola e Silva.",
    },
    {
        "nome_local": "Ecoponto Guaçuí",
        "endereco": "R. Maria Augusta, 1",
        "bairro": "Sítio Cercado",
        "observacao": "Ecoponto misto.",
    },
    {
        "nome_local": "Ecoponto Icaraí",
        "endereco": "R. Olindo Caetani, 1330",
        "bairro": "Uberaba",
        "observacao": "Ecoponto misto.",
    },
    {
        "nome_local": "Ecoponto Jandaia",
        "endereco": "R. Jorn. José Pedro dos Santos - Pedrinho, 801",
        "bairro": "Ganchinho",
        "observacao": "Ecoponto misto.",
    },
    {
        "nome_local": "Ecoponto Metropolitano",
        "endereco": "R. da Independência, 340",
        "bairro": "São Braz",
        "observacao": "Ecoponto da Regional Santa Felicidade.",
    },
    {
        "nome_local": "Ecoponto Sambaqui",
        "endereco": "R. Rad. Souza Moreno, 30",
        "bairro": "Sítio Cercado",
        "observacao": "Ecoponto misto.",
    },
    {
        "nome_local": "Ecoponto Vila Nova",
        "endereco": "R. Ten. Cel. Vilagran Cabrita, 2495",
        "bairro": "Alto Boqueirão",
        "observacao": "Ecoponto misto.",
    },
    {
        "nome_local": "Ecoponto Vila Verde",
        "endereco": "R. Lydio Paulo Bettega, 200",
        "bairro": "Cidade Industrial de Curitiba",
        "observacao": "Ecoponto misto.",
    },
    {
        "nome_local": "Ecoponto Parque Gomm",
        "endereco": "R. Hermes Fontes, 204",
        "bairro": "Batel",
        "tipo_residuo_aceito": TIPOS_PARQUE_GOMM,
        "observacao": "Ecoponto voltado a materiais recicláveis, óleo de cozinha e gordura pós-consumo.",
    },
]


PONTOS_EXEMPLO_ANTIGOS = {
    "EcoPonto Central",
    "Farmácia Vida",
    "Mercado Verde",
    "Centro de Reciclagem Tech",
}


def desativar_pontos_exemplo_antigos(db: Session) -> None:
    for nome in PONTOS_EXEMPLO_ANTIGOS:
        ponto = services.buscar_ponto_por_nome(db, nome)
        if ponto:
            ponto.ativo = False
    db.commit()


def seed_data(db: Session) -> None:
    for dados in CATEGORIAS_INICIAIS:
        services.get_or_create_categoria(db, dados["nome"], dados["descricao"])

    for dados in RESIDUOS_INICIAIS:
        services.get_or_create_residuo(db, dados)

    for dados in ECOPONTOS_CURITIBA:
        dados_ponto = {
            "cidade": "Curitiba",
            "telefone": "156",
            "horario_funcionamento": HORARIO_ECOPONTOS_CURITIBA,
            "fonte_dados": FONTE_ECOPONTOS_CURITIBA,
            "tipo_residuo_aceito": TIPOS_ECOPONTO_MISTO,
            "ativo": True,
            **dados,
        }
        services.upsert_ponto_coleta(db, dados_ponto)

    desativar_pontos_exemplo_antigos(db)
