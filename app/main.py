from fastapi import FastAPI
from sqlmodel import create_engine, SQLModel # isso que vai criar o database

engine = create_engine("sqlite:///database.db") #cria o banco de dados

app = FastAPI()

def create_db():
    SQLModel.metadata.create_all(engine)


@app.on_event("startup") #mudar isso aqui
def start():
        create_db()


@app.get("/")
def test():
    return "hello test"


