from sqlmodel import Session, create_engine, SQLModel

# Configuração do banco de dados
DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL)  # Cria o banco de dados ou conecta-se a ele

# Função para obter uma sessão do banco de dados
def get_session():
    """
    Fornece uma sessão de banco de dados para ser usada em consultas e transações.
    """
    with Session(engine) as session:
        yield session

# Criação das tabelas no banco de dados
def initialize_database():
    """
    Inicializa o banco de dados, criando as tabelas definidas nos modelos SQLModel.
    """
    SQLModel.metadata.create_all(engine)
