from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class VilleBase(BaseModel):
    nom: str

class VilleCreate(VilleBase):
    pass

class Ville(VilleBase):
    id: int

    class Config:
        orm_mode = True

class TypeBienBase(BaseModel):
    nom: str

class TypeBienCreate(TypeBienBase):
    pass

class TypeBien(TypeBienBase):
    id: int

    class Config:
        orm_mode = True

class StatutBase(BaseModel):
    nom: str

class StatutCreate(StatutBase):
    pass

class Statut(StatutBase):
    id: int

    class Config:
        orm_mode = True

class TypeAccompagnementBase(BaseModel):
    nom: str

class TypeAccompagnementCreate(TypeAccompagnementBase):
    pass

class TypeAccompagnement(TypeAccompagnementBase):
    id: int

    class Config:
        orm_mode = True

class SuiviTypeAccompagnementBase(BaseModel):
    id_type_accompagnement: int
    statut_suivi_type_accompagnement: str

class SuiviTypeAccompagnementCreate(SuiviTypeAccompagnementBase):
    pass

class SuiviTypeAccompagnement(SuiviTypeAccompagnementBase):
    id_suivi: int

    class Config:
        orm_mode = True

class SuiviBase(BaseModel):
    nom: str
    representant: Optional[str]
    mode_retour: Optional[str]
    activite: Optional[str]
    numero_de_telephone: Optional[str]
    email: Optional[str]
    budget: Optional[float]
    superficie: Optional[float]
    zone: Optional[str]
    prix_alloue: Optional[float]
    services_clotures: Optional[str]
    annexes: Optional[str]
    action: Optional[bool]
    ca_previsionnel: Optional[float]
    ca_realise: Optional[float]
    ca_total: Optional[float]
    date_creation: Optional[date]
    date_mise_a_jour: Optional[date]
    id_type_bien: Optional[int]
    id_statut: Optional[int]
    id_ville: Optional[int]
    type_accompagnement_ids: List[SuiviTypeAccompagnementCreate] = []

class SuiviWithTypes(SuiviBase):
    id: int
    type_bien: TypeBien
    statut: Statut
    ville: Ville
    type_accompagnements: List[TypeAccompagnement]
    type_accompagnement_associations: List[SuiviTypeAccompagnement]

    class Config:
        orm_mode = True
class SuiviCreate(SuiviBase):
    pass

class Suivi(SuiviBase):
    id: int
    type_bien: Optional[TypeBien]
    statut: Optional[Statut]
    ville: Optional[Ville]
    type_accompagnement_ids: List[SuiviTypeAccompagnement] = []
    type_accompagnements: List[TypeAccompagnement] = []

    class Config:
        orm_mode = True

class SuiviUpdate(SuiviBase):
    pass

    class Config:
        orm_mode = True

# authentication 

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str