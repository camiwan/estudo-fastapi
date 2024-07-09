from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from app.db.database import Base

class ClientModel(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), )
    age = Column(String(50))

    info_professional = relationship('InfoProfessionalModel', back_populates='client', cascade='all, delete-orphan')


class InfoProfessionalModel(Base):
    __tablename__ = 'info_professionals'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    training = Column(String(100))
    institution = Column(String(100))
    company_work = Column(String(100))
    client_id = Column(Integer, ForeignKey('clients.id'))
    # client_id = mapped_column(Integer, ForeignKey('clients.id'))

    client = relationship('ClientModel', back_populates='info_professional')
