from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

class Ville(Base):
    __tablename__ = 'ville'
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255), nullable=False)

class TypeBien(Base):
    __tablename__ = 'type_bien'  
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255), nullable=False)

class Statut(Base):
    __tablename__ = 'statut'
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255), nullable=False)

class TypeAccompagnement(Base):
    __tablename__ = 'type_accompagnement'
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255), nullable=False)
    suivi_associations = relationship("SuiviTypeAccompagnement", back_populates="type_accompagnement")
    suivis = relationship("Suivi", secondary="suivi_type_accompagnement", back_populates="type_accompagnements")

class Suivi(Base):
    __tablename__ = 'suivi'
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255), nullable=False)
    representant = Column(String(255))
    mode_retour = Column(String(255))
    activite = Column(String(255))
    numero_de_telephone = Column(String(20))
    email = Column(String(255))
    id_type_bien = Column(Integer, ForeignKey('type_bien.id'))
    budget = Column(Float)
    superficie = Column(Float)
    zone = Column(String(255))
    prix_alloue = Column(Float)
    services_clotures = Column(String(255))  # Specify length for VARCHAR
    annexes = Column(String(255))  # Specify length for VARCHAR
    id_statut = Column(Integer, ForeignKey('statut.id'))
    id_ville = Column(Integer, ForeignKey('ville.id'))
    action = Column(Boolean)
    ca_previsionnel = Column(Float)
    ca_realise = Column(Float)
    ca_total = Column(Float)
    date_creation = Column(Date)
    date_mise_a_jour = Column(Date)

    type_bien = relationship('TypeBien')
    statut = relationship('Statut')
    ville = relationship('Ville')
    type_accompagnement_ids = relationship('SuiviTypeAccompagnement', back_populates='suivi')
    type_accompagnement_associations = relationship('SuiviTypeAccompagnement', back_populates='suivi')
    type_accompagnements = relationship("TypeAccompagnement", secondary="suivi_type_accompagnement", back_populates="suivis")    # type_accompagnements = relationship(
    #     "TypeAccompagnement",
    #     secondary="suivi_type_accompagnement",
    #     back_populates="suivis"
    # )

# class SuiviTypeAccompagnement(Base):
#     __tablename__ = 'suivi_type_accompagnement'
#     id_suivi = Column(Integer, ForeignKey('suivi.id'), primary_key=True)
#     id_type_accompagnement = Column(Integer, ForeignKey('type_accompagnement.id'), primary_key=True)

#     suivi = relationship('Suivi', back_populates='type_accompagnement_ids')
#     type_accompagnement_ids = relationship('TypeAccompagnement')
#     type_accompagnement = relationship("TypeAccompagnement", back_populates="suivis")
class SuiviTypeAccompagnement(Base):
    __tablename__ = 'suivi_type_accompagnement'
    id_suivi = Column(Integer, ForeignKey('suivi.id'), primary_key=True)
    id_type_accompagnement = Column(Integer, ForeignKey('type_accompagnement.id'), primary_key=True)

    suivi = relationship('Suivi', back_populates='type_accompagnement_associations')
    type_accompagnement = relationship('TypeAccompagnement', back_populates='suivi_associations')
    type_accompagnement_ids = relationship('TypeAccompagnement')
    