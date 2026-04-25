# EcoDescarta

EcoDescarta é uma primeira versão de sistema web para orientar o descarte consciente de resíduos. A aplicação permite consultar orientações, registrar histórico, cadastrar resíduos, cadastrar pontos de coleta e visualizar um relatório simples dos itens mais consultados.

## Tecnologias

- Python 3.11+
- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite
- Jinja2 Templates
- HTML e CSS

## Como executar

1. Crie e ative um ambiente virtual, se desejar.

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Instale as dependências.

```bash
pip install -r requirements.txt
```

3. Inicie a aplicação.

```bash
uvicorn app.main:app --reload
```

4. Acesse no navegador.

```text
http://127.0.0.1:8000
```

Na primeira execução, o arquivo `eco_descarta.db` será criado automaticamente na raiz do projeto e receberá os dados iniciais.

## Páginas web

- `/` - Página inicial
- `/consulta` - Consulta de orientação de descarte
- `/residuos/novo` - Cadastro de resíduos
- `/pontos/novo` - Cadastro de pontos de coleta
- `/historico` - Histórico de consultas
- `/relatorio` - Relatório de resíduos mais consultados

## Endpoints JSON

- `GET /api/residuos`
- `POST /api/residuos`
- `GET /api/pontos`
- `POST /api/pontos`
- `GET /api/consultas`
- `GET /api/relatorio`

Exemplo de cadastro de resíduo pela API:

```json
{
  "nome": "Lâmpada",
  "categoria": "Resíduo perigoso",
  "orientacao_descarte": "Leve a lâmpada a pontos de coleta preparados para esse material.",
  "risco_ambiental": "Alto",
  "mensagem_educativa": "Lâmpadas podem conter substâncias que exigem descarte cuidadoso."
}
```

## Organização

A aplicação separa responsabilidades em módulos:

- `app/models.py` define as tabelas SQLAlchemy.
- `app/schemas.py` define os modelos Pydantic usados pela API.
- `app/services.py` concentra regras de negócio reutilizadas por web e API.
- `app/seed.py` popula categorias, resíduos e pontos iniciais.
- `app/routes/web.py` contém as páginas renderizadas com Jinja2.
- `app/routes/api.py` contém os endpoints JSON.

