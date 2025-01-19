from sqlmodel import SQLModel, Field

class Grupo(SQLModel, table=True):
    nome_grupo: str
    descricao_grupo: str
    