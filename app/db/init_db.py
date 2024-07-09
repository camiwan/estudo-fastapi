from app.db.database import engine
from app.models.client import Base as ClientBase
from app.models.userModel import  Base as UserBase

#Cria a tablela nos banco de dados: nome da tabela e os campos
def init_db():
    ClientBase.metadata.create_all(bind=engine)
    UserBase.metadata.create_all(bind=engine)
