# EcoDescarta

EcoDescarta é uma aplicação web acadêmica para orientar o descarte consciente de resíduos. O sistema permite consultar um resíduo, visualizar a orientação de descarte, entender o risco ambiental e encontrar pontos de coleta compatíveis.

Esta versão também inclui uma base inicial mais realista com Ecopontos de Curitiba cadastrados a partir de dados públicos da Prefeitura de Curitiba.

## Tecnologias

- Python 3.11+
- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite
- Jinja2 Templates
- HTML
- CSS próprio

## Como Executar

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Acesse:

```text
http://127.0.0.1:8000
```

Na primeira execução, o banco `eco_descarta.db` é criado automaticamente na raiz do projeto.

## Funcionalidades

- Consulta de resíduos por nome.
- Exibição de categoria, orientação de descarte, risco ambiental e mensagem educativa.
- Busca de pontos de coleta compatíveis com o resíduo consultado.
- Cadastro de novos resíduos.
- Cadastro de novos pontos de coleta.
- Listagem de pontos de coleta ativos.
- Remoção lógica de pontos de coleta.
- Histórico de consultas.
- Relatório simples dos resíduos mais consultados.
- Endpoints JSON para integração futura.

## Rotas Web

- `GET /` - Página inicial.
- `GET /consulta` - Formulário de consulta.
- `POST /consulta` - Resultado da consulta e registro no histórico.
- `GET /residuos/novo` - Cadastro de resíduo.
- `POST /residuos/novo` - Salva novo resíduo.
- `GET /pontos` - Lista pontos de coleta ativos.
- `GET /pontos/novo` - Cadastro de ponto de coleta.
- `POST /pontos/novo` - Salva novo ponto de coleta.
- `POST /pontos/{ponto_id}/remover` - Marca um ponto de coleta como inativo.
- `GET /historico` - Histórico de consultas.
- `GET /relatorio` - Relatório de resíduos mais consultados.

## Endpoints API

- `GET /api/residuos`
- `POST /api/residuos`
- `GET /api/pontos`
- `GET /api/pontos?incluir_inativos=true`
- `POST /api/pontos`
- `DELETE /api/pontos/{ponto_id}`
- `GET /api/consultas`
- `GET /api/relatorio`

Resposta esperada ao remover um ponto pela API:

```json
{
  "success": true,
  "message": "Ponto de coleta removido com sucesso.",
  "id": 1
}
```

## Dados Mock e Seed

A seed inicial cadastra categorias, resíduos e pontos de coleta. Ela é idempotente: ao reiniciar a aplicação, os dados não são duplicados.

Categorias iniciais:

- Resíduo perigoso
- Resíduo reciclável
- Resíduo eletrônico
- Resíduo doméstico especial
- Resíduo de construção civil
- Resíduo vegetal

Resíduos iniciais:

- Pilha
- Bateria
- Óleo de cozinha
- Medicamento vencido
- Vidro
- Lixo eletrônico
- Caliça
- Madeira
- Móvel inservível
- Resíduo vegetal

## Ecopontos de Curitiba

Os pontos de coleta iniciais são baseados em dados públicos da Prefeitura de Curitiba sobre Ecopontos para descarte correto de resíduos.

Fonte usada na seed:

```text
Prefeitura de Curitiba - Ecopontos - Descarte correto de resíduos
```

Os Ecopontos cadastrados incluem unidades como Caiuá, Cajuru, CIC, Érico Veríssimo, Guaçuí, Icaraí, Jandaia, Metropolitano, Sambaqui, Vila Nova, Vila Verde, Campo de Santana e Parque Gomm.

## Remoção de Pontos de Coleta

A remoção é lógica. O registro não é apagado do banco: o campo `ativo` passa para `False`.

Na interface web:

1. Acesse `/pontos`.
2. Clique em `Remover`.
3. O ponto deixa de aparecer na listagem padrão.

Na API:

```bash
curl -X DELETE http://127.0.0.1:8000/api/pontos/1
```

Por padrão, `GET /api/pontos` retorna apenas pontos ativos. Para visualizar também os inativos:

```text
GET /api/pontos?incluir_inativos=true
```

## Banco Local

Esta versão inclui uma atualização simples de schema para adicionar novas colunas em bancos locais antigos.

Se preferir recriar tudo do zero em ambiente de desenvolvimento:

1. Pare o servidor.
2. Remova o arquivo `eco_descarta.db`.
3. Suba novamente a aplicação.

```bash
uvicorn app.main:app --reload
```

O banco será criado novamente com a seed atualizada.

## Organização do Projeto

- `app/models.py` - Modelos SQLAlchemy.
- `app/schemas.py` - Schemas Pydantic da API.
- `app/services.py` - Regras de negócio e funções reutilizáveis.
- `app/seed.py` - Dados iniciais idempotentes.
- `app/routes/web.py` - Rotas HTML com Jinja2.
- `app/routes/api.py` - Endpoints JSON.
- `templates/` - Páginas HTML.
- `static/style.css` - Estilos da interface.
