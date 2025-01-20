from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from app.db import get_session 
from app.models.Despesa import Despesa
from app.models.Usuario import Usuario

routes = APIRouter()

def proxima_session():
    session_generator = get_session()
    return next(session_generator)

@routes.post("/add_despesa")
def add_despesa(despesa : dict):
    valor = despesa.get("valor")
    descricao = despesa.get("descricao")
    status = despesa.get("status")
    usuario_id = despesa.get("usuario_id")
    session = proxima_session()
    
    desp = Despesa(valor=valor, descricao=descricao, status=status, usuario_id=usuario_id)

    created_desp = session.add(desp)
    session.commit()
    session.refresh(desp)

    return created_desp

@routes.get("/listar_despesa")
def listar_despesa():
    session = proxima_session()
    statement = select (Despesa)
    desp = session.exec(statement).all()
    return desp

@routes.put("/atualizar_despesa/{despesa_id}")
def atualizar_despesa(despesa_id: int, despesa:Despesa):
    session = proxima_session()
    desp = session.get(Despesa,despesa_id)
    if not desp:
        raise HTTPException(status_code=404, detail="Despesa não encontrada")
    
    #Atualiza os campos fornecidos
    desp.valor = despesa.valor or desp.valor
    desp.descricao = despesa.descricao or desp.descricao
    desp.status = despesa.status or desp.status

    session.add(desp)
    session.commit()
    session.refresh(desp)
    return desp

@routes.delete("/deletar_despesa/{despesa_id}")
def deletar_despesa(despesa_id : int):
    session = proxima_session()
    desp = session.get(Despesa, despesa_id)
    if not desp:
        raise HTTPException(status_code=404, detail="Despesa não encontrada")
    
    session.delete(desp)
    session.commit()
    return{"message":"Despesa deletada com sucesso"}

@routes.get("/selecionar_despesa/{despesa_id}")
def selecionar_despesa(despesa_id: int):
    session = proxima_session()
    desp = session.get(Despesa, despesa_id)
    if not desp:
        raise HTTPException(status_code=404, detail="Despesa não encontrada")
    
    return desp

"""procura as despesas do usuário pelo id"""
@routes.get("/desp_por_user/{usuario_id}")
def desp_por_user(usuario_id : int):
    session = proxima_session()
    statement = select(Despesa).where(Despesa.usuario_id == usuario_id) #o id da despesa seja igual ao id do usuario
    results = session.exec(statement).all()
    if not results:
        raise HTTPException(status_code=404, detail="Nenhuma despesa encontrada para esse usuário")
    for despesa in results:
        print(despesa)

    return results