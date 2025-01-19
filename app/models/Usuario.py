from sqlmodel import SQLModel, Field

class Usuario(SQLModel, table=True):
    __tablename__: 'usuarios'

    id: int = Field(default=None, nullable=False, primary_key = True)
    nome: str 
    email: str =Field(default=None, nullable=False, unique=True) #definir o email como chave unica e que não pode haver outro usuário com o mesmo
    idade: int | None = Field(default=None)
  