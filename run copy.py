
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

data = [
    {

    'id': 1,
    'name': 'Marcus',
    'age': '30 anos',
    'infoProfessional':[
        {
            'training': 'Analista de Desenvolvimento de Sistema Web',
            'institution': 'Universidade Federal do Paraná (UFPR)',
            'companyWork': 'Home Office'
        }
    ]
    
}, 
{
    'id': 2,
    'name': 'Patrícia',
    'age': '20 anos',
    'infoProfessional':[
        {
            'training': 'Gestão do Conhecimento',
            'institution': 'Universidade Federal do Paraná (UFPR)',
            'companyWork': 'UC'
        }
    ]
},
{
    'id': 3,
    'name': 'Mathalia',
    'age': '18 anos',
    'infoProfessional':[
        {
            'training': 'Novo aprendiz',
            'institution': 'Escola Estadual do Paraná',
            'companyWork': 'Biblioteca do Paraná'
        }
    ]
},  
]

class infoProfessional(BaseModel):
    training: str
    institution: str
    companyWork: str

class Item(BaseModel):
    id: int
    name: str
    age: str
    infoProfessional: List[infoProfessional]
    




@app.get('/')
async def root():
    return data

@app.get('/get-item/{item_id}')
def get_item(item_id:int):
    search = list(filter(lambda x:x['id'] == item_id, data))
    
    if search == []:
        return {'Erro': 'Dado não existe!' }
    
    return {'Record': search[0]}

@app.get('/get_name/{item_name}') 
# paramentro será assim http://127.0.0.1:8000/get_name?name=  ,se a requisiçao for assim ('/get_name')
def get_item(item_name: Optional[str] = None):

    if item_name is None:
        return{'Erro': 'Nome não foi fornecido'}
    
    search = list(filter(lambda x:x['name'] == item_name, data))

    if search == []:
        return {'Erro': 'Dado não existe!' }
    
    return {'Record': search[0]}

@app.post('/create-item/{item_id}')
def create_item(item_id: int, item: Item):

    search = list(filter(lambda x:x['id'] == item_id, data))

    if search:
        raise HTTPException(status_code=400, detail='O dado como esse id já existe')
    
    new_item = item.model_dump()
    data.append(new_item)

    return {f'Message': 'Registro criado com sucesso, {new_item}'}



