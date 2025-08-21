import sqlalchemy as sa
import sqlalchemy.orm as so
from typing import List
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
import os

Base = so.declarative_base()

# Caminho relativo para o banco
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "toolmux.db")

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False, future=True)
Session = sessionmaker(bind=engine, future=True)

# MetaData sem bind
metadata = MetaData()

# TABELA ASSOCIATIVA
tool_category = Table(
    "tool_category",
    metadata,
    autoload_with=engine
)

# =================== MODELOS ===================

class Author(Base):
    __table__ = Table("author", metadata, autoload_with=engine)
    tools: so.Mapped[List["Tool"]] = so.relationship("Tool", back_populates="author")


class InstallationType(Base):
    __table__ = Table("installation_type", metadata, autoload_with=engine)
    tools: so.Mapped[List["Tool"]] = so.relationship("Tool", back_populates="installation_type")


class Situation(Base):
    __table__ = Table("situation", metadata, autoload_with=engine)
    tools: so.Mapped[List["Tool"]] = so.relationship("Tool", back_populates="situation_tool")


class Tool(Base):
    __table__ = Table("tool", metadata, autoload_with=engine)

    author: so.Mapped["Author"] = so.relationship("Author", back_populates="tools")
    installation_type: so.Mapped["InstallationType"] = so.relationship("InstallationType", back_populates="tools")
    situation_tool: so.Mapped["Situation"] = so.relationship("Situation", back_populates="tools")
    categories: so.Mapped[List["Category"]] = so.relationship(
        "Category", secondary=tool_category, back_populates="tools"
    )


class Category(Base):
    __table__ = Table("category", metadata, autoload_with=engine)
    tools: so.Mapped[List["Tool"]] = so.relationship(
        "Tool", secondary=tool_category, back_populates="categories"
    )

