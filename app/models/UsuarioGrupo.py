from sqlmodel import Field, SQLModel

class UsuarioGrupo(SQLModel, table=True):
    __tablename__ = "usuario_grupo"
    user_id: int = Field(primary_key=True, foreign_key="usuario.id")
    grupo_id: int = Field(primary_key=True, foreign_key="grupo.id")
