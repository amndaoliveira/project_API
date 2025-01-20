from sqlmodel import SQLModel, Field

class Grupo(SQLModel, table=True):
    __tablename__: 'grupo'

    id: int | None = Field(default=None, primary_key=True)
    nome_grupo: str
    descricao_grupo: str
    