from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from app.db import get_session 
from app.models.Despesa import Despesa
from app.models.Grupo import Grupo
from app.models.Usuario import Usuario

routes = APIRouter(
    tags=['Grupo', 
          'Usuario',
          'Despesa']
)

def proxima_session():
    session_generator = get_session()
    return next(session_generator)

@routes.post("/criar_despesa_usuario/")
def add_despesa_ao_usuario(despesa : dict):
    valor = despesa.get("valor")
    descricao = despesa.get("descricao")
    status = despesa.get("status")
    usuario_id = despesa.get("usuario_id")
    session = proxima_session()
    
    desp = Despesa(valor=valor, descricao=descricao, status=status, usuario_id=usuario_id)

    criar_desp = session.add(desp)
    session.commit()
    session.refresh(desp)

    return criar_desp

#FAZER FUNCIONAR E TESTAR
@routes.post("/criar_despesa_grupo/{add_desp}")
def add_despesa_ao_grupo(desp : dict):

    #VER SE O GRUPO EXISTE
    grupo = session.get(Grupo, grupo_id)
    if not grupo:
        raise HTTPException(status_code=404, detail="Grupo não encontrado.")
    
    #CRIAR DESPESA E ASSOCIAR AO GRUPO
    nova_desp = Despesa(valor=valor, descricao=descricao, grupo_id=grupo_id)

    #ADD e SALVAR A DESP NO DB
    session.add(nova_desp)
    session.commit()
    session.refresh(nova_desp)

    return {"mensagem": f"Despesa '{nova_desp.descricao}' adicionada ao grupo '{grupo.nome}'", "despesa_id": nova_desp.id}

    """"
    @TODO
        criar despesa ligada ao grupo
    - Receber os dados da despesa (descrição, valor)
    - Associar a despesa ao grupo via a chave estrangeira grupo_id
    - Verificar se o grupo existe.
    - Adicionar a despesa ao banco de dados.
        
    """

    return "@TODO"

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

#TESTAR
@routes.post("/dividir_despesa/{grupo_id}")
def dividir_despesa(grupo_id : int ):

    grupo = session.get(Grupo, grupo_id)

    if not grupo:
        raise HTTPException(status_code=404, detail="Grupo não encontrado.")

    #PEGAR AS DESPESAS DO GRUPO
    despesas = session.exec(select(Despesa)
                            .where(Despesa.grupo_id == grupo_id)).all()
    if not despesas:
        raise HTTPException(status_code=404, detail="Nenhuma despesa encontrada para esse grupo.")
    
    #PEGAR OS USUARIOS DO GRUPO
    usuarios = grupo.usuarios
    if not usuarios:
        raise HTTPException(status_code=404, detail="Nenhum usuário encontrado no grupo.")
    
    #DIVISAO DA DESPESA
    valor = []
    for despesa in despesas:
        valor_individual = despesa.valor / len(usuarios)

    for usuario in usuarios:
        valor.append({
            "usuario": usuario.nome,
            "valor_a_pagar": valor_individual,
            "despesa": despesa.descricao
        })

    return {
        "mensagem": f"Despesas divididas entre {len(usuarios)} usuários do grupo '{grupo.nome}'.",
        "detalhes": valor
    }
