from fastapi import FastAPI
from sqlmodel import Session, create_engine, SQLModel
from app.db import initialize_database # isso que vai criar o database
from app.routes.Usuario import routes as rotas_usuario

app = FastAPI()
app.include_router(rotas_usuario)

@app.get("/")
def test():
    return "hello test"

if __name__ == "__main__":
    print("oi, to aqui")
    initialize_database()
    print("Banco de dados inicializado com sucesso!")

