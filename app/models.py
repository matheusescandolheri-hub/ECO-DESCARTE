from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Categoria(Base):
    __tablename__ = "categorias"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)

    residuos: Mapped[list["Residuo"]] = relationship(back_populates="categoria")


class Residuo(Base):
    __tablename__ = "residuos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categorias.id"), nullable=False)
    orientacao_descarte: Mapped[str] = mapped_column(Text, nullable=False)
    risco_ambiental: Mapped[str] = mapped_column(String(80), nullable=False)
    mensagem_educativa: Mapped[str] = mapped_column(Text, nullable=False)

    categoria: Mapped[Categoria] = relationship(back_populates="residuos")


class PontoColeta(Base):
    __tablename__ = "pontos_coleta"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome_local: Mapped[str] = mapped_column(String(140), nullable=False)
    endereco: Mapped[str] = mapped_column(String(180), nullable=False)
    bairro: Mapped[str] = mapped_column(String(100), nullable=False)
    cidade: Mapped[str] = mapped_column(String(100), nullable=False)
    tipo_residuo_aceito: Mapped[str] = mapped_column(String(160), nullable=False)


class Consulta(Base):
    __tablename__ = "consultas"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome_residuo: Mapped[str] = mapped_column(String(120), index=True, nullable=False)
    data_consulta: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        index=True,
        nullable=False,
    )
    localizacao_usuario: Mapped[str | None] = mapped_column(String(140), nullable=True)

