from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CategoriaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    descricao: str | None = None


class ResiduoCreate(BaseModel):
    nome: str = Field(..., min_length=2, max_length=120)
    categoria: str = Field(..., min_length=2, max_length=100)
    orientacao_descarte: str = Field(..., min_length=8)
    risco_ambiental: str = Field(..., min_length=3, max_length=80)
    mensagem_educativa: str = Field(..., min_length=8)


class ResiduoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    orientacao_descarte: str
    risco_ambiental: str
    mensagem_educativa: str
    categoria: CategoriaOut


class PontoColetaCreate(BaseModel):
    nome_local: str = Field(..., min_length=2, max_length=140)
    endereco: str = Field(..., min_length=4, max_length=180)
    bairro: str = Field(..., min_length=2, max_length=100)
    cidade: str = Field(..., min_length=2, max_length=100)
    tipo_residuo_aceito: str = Field(..., min_length=2, max_length=160)
    telefone: str | None = Field(default=None, max_length=40)
    horario_funcionamento: str | None = Field(default=None, max_length=160)
    observacao: str | None = None
    fonte_dados: str | None = Field(default="Cadastro manual", max_length=180)


class PontoColetaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome_local: str
    endereco: str
    bairro: str
    cidade: str
    tipo_residuo_aceito: str
    telefone: str | None = None
    horario_funcionamento: str | None = None
    observacao: str | None = None
    fonte_dados: str | None = None
    ativo: bool


class PontoColetaDeleteResponse(BaseModel):
    success: bool
    message: str
    id: int


PontoColetaOut = PontoColetaRead


class ConsultaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome_residuo: str
    data_consulta: datetime
    localizacao_usuario: str | None = None


class RelatorioItem(BaseModel):
    nome_residuo: str
    total_consultas: int
