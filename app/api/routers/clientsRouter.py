from fastapi import APIRouter, HTTPException, Depends ,Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app.db.database import get_db
from app.models.client import ClientModel, InfoProfessionalModel
from app.schemas.client import ClientCreate, ClienteUpdate, Client
from uuid import uuid4

client_router = APIRouter()


@client_router.get('/', response_model=List[Client])
async def clients(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    clients = db.query(ClientModel).offset(skip).limit(limit).all()
    return clients

@client_router.get('/{client_id}', response_model=Client)
async def clientId(client_id: int, db:Session = Depends(get_db)):
    client = db.query(ClientModel).filter(ClientModel.id == client_id).first()    

    if not client:
        raise HTTPException(status_code=404, detail='Client not found!')
    return client

@client_router.get('/client/{name}', response_model=Client) 
async def search_client(name: str, db: Session = Depends(get_db)):
    if not name:
        raise HTTPException(status_code=400, detail='Por favor, digite um nome')
    
    client = db.query(ClientModel).filter(ClientModel.name == name).first()

    if not client:
        raise HTTPException(status_code=404, detail='Client not found!')
    return client

@client_router.post('/', response_model=Client)
async def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    new_client = ClientModel(
        name=client.name, 
        age=client.age
        )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)

    for info in client.info_professional:
      
      new_info = InfoProfessionalModel(
           training=info.training,
           institution=info.institution, 
           company_work=info.company_work, 
           client_id = new_client.id
           )
      db.add(new_info)
      db.commit()
      db.refresh(new_info)   
    
    return new_client
        

@client_router.put('/{client_id}', response_model=Client)
async def update_client(client_id: int, client: ClienteUpdate, db: Session = Depends(get_db)):

    client_db = db.query(ClientModel).filter(ClientModel.id == client_id).first()
    if not client_db:
        raise HTTPException(status_code=404, detail='Client not found')
    
    if client.name:
        client_db.name = client.name

    if client.age:
        client_db.age = client.age

    if client.info_professional:

        db.query(InfoProfessionalModel).filter(InfoProfessionalModel.client_id == client_id).delete()
        for info in client.info_professional:
            new_info = InfoProfessionalModel(
                **info.model_dump(), client_id=client_db.id
            )
            db.add(new_info)
      
          
    db.commit()
    db.refresh(client_db)
    return {f'Message': 'Registro atualizado com sucesso, {client_db}'}

@client_router.delete('/{client_id}', response_model=dict)
async def delete_client(client_id: int, db: Session = Depends(get_db)):
    client_db = db.query(ClientModel).filter(ClientModel.id == client_id).first()

    
    if not client_db:
        raise HTTPException(status_code=404, detail='Client not found')
    db.delete(client_db)
    db.commit()
    
    return {f'Message': '{client_db} deletado com sucesso'}


