from sqlmodel import Field, SQLModel

class UsuarioGrupo(SQLModel, table=True):
    __tablename__ = "user_group"
    user_id: int = Field(primary_key=True, foreign_key="usuario.id")
    group_id: int = Field(primary_key=True, foreign_key="grupo.id")
