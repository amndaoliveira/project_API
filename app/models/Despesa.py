from sqlmodel import SQLModel, Field

class Despesa(SQLModel, table=True):
    valor: float
    descricao: str
    status: str