from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
import logging

from api import models
from api import schemas
from api.database import SessionLocal, engine

logging.basicConfig(level=logging.DEBUG)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://asmaa-dashboard.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# SECRET_KEY = "your_secret_key"
SECRET_KEY = "A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0U1V2W3X4Y5Z6A7B8C9D0E1F2G3H4I5J6K7L8M9N0O1P2Q3R4S5T6U7V8W9X0Y1Z2A3B4C5D6E7F8G9H0I1J2K3L4M5N6O7P8Q9R0S1T2U3V4W5X6Y7Z8A9B0C1D2E3F4G5H6I7J8K9L0M1N2O3P4Q5R6S7T8U9V0W1X2Y3Z4A5B6C7D8E9F0G1H2I3J4K5L6M7N8O9P0Q1R2S3T4U5V6W7X8Y9Z0A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0U1V2W3X4Y5Z6A7B8C9D0E1F2G3H4I5J6K7L8M9N0O1P2Q3R4S5T6U7V8W9X0Y1Z2A3B4C5D6E7F8G9H0I1J2K3L4M5N6O7P8Q9R0S1T2U3V4W5X6Y7Z8A9B0C1D2E3F4G5H6I7J8K9L0M1N2O3P4Q5R6S7T8U9V0W1X2Y3Z4A5B6C7D8E9F0G1H2I3J4K5L6M"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# OAuth2PasswordBearer for getting the token from the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logging.debug(f"Encoded JWT: {encoded_jwt}")
    return encoded_jwt

# Add the missing imports
from api.schemas import UserLogin, Token, TokenData
from api.models import User 

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logging.debug(f"Token payload: {payload}")
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as e:
        logging.error(f"JWT Error: {e}")
        raise credentials_exception

@app.post("/")
async def create_item():
    return {"hello": "world"}

@app.post("/verify-token")
def verify_token_endpoint(token: str = Depends(oauth2_scheme)):
    logging.debug(f"Received token: {token}")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    verify_token(token, credentials_exception)
    return {"message": "Token is valid"}

# @app.post("/token", response_model=Token)
# def login(user: UserLogin, db: Session = Depends(get_db)):
#     db_user = db.query(User).filter(User.username == user.username).first()
#     if not db_user or not pwd_context.verify(user.password, db_user.password_hash):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}

# Other endpoints...

# You can also create a token endpoint for login, if needed
@app.post("/token", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not pwd_context.verify(user.password, db_user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



# Authentication endpoints
@app.post("/signup", response_model=dict)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, email=user.email, password_hash=hashed_password, full_name=user.full_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User created successfully"}


# Suivi Endpoints
@app.get("/suivi/", response_model=List[schemas.Suivi])
def read_suivis(db: Session = Depends(get_db)):
    db_suivis = db.query(models.Suivi).options(
        joinedload(models.Suivi.type_bien),
        joinedload(models.Suivi.statut),
        joinedload(models.Suivi.ville)
    ).all()
    return db_suivis

@app.get("/suivi/{suivi_id}", response_model=schemas.Suivi)
def read_suivi(suivi_id: int, db: Session = Depends(get_db)):
    db_suivi = db.query(models.Suivi).filter(models.Suivi.id == suivi_id).first()
    if db_suivi is None:
        raise HTTPException(status_code=404, detail="Suivi not found")
    return db_suivi

@app.post("/suivi/create", response_model=schemas.Suivi)
def create_suivi(suivi: schemas.SuiviCreate, db: Session = Depends(get_db)):
    logging.debug("Starting to create a new Suivi with data: %s", suivi.dict())
    try:
        db_suivi = models.Suivi(**suivi.dict(exclude={'type_accompagnement_ids'}))
        db.add(db_suivi)
        db.commit()
        db.refresh(db_suivi)
        logging.debug(f"Suivi created with ID: {db_suivi.id}")

        # Add TypeAccompagnements
        if suivi.type_accompagnement_ids:
            for ta in suivi.type_accompagnement_ids:
                logging.debug(f"Adding TypeAccompagnement with ID: {ta.id_type_accompagnement}")
                db_ta = models.SuiviTypeAccompagnement(
                    id_suivi=db_suivi.id,
                    id_type_accompagnement=ta.id_type_accompagnement
                )
                db.add(db_ta)

            db.commit()
            logging.debug("Finished creating Suivi and associated TypeAccompagnements")

        return db_suivi
    except Exception as e:
        logging.error(f"Error creating suivi: {e}")
        db.rollback()  # Rollback in case of error
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.put("/suivi/update/{suivi_id}", response_model=schemas.Suivi)
def update_suivi(suivi_id: int, suivi: schemas.SuiviBase, db: Session = Depends(get_db)):
    logging.debug(f"Starting to update Suivi with ID: {suivi_id} and data: {suivi.dict()}")

    db_suivi = db.query(models.Suivi).filter(models.Suivi.id == suivi_id).first()
    if db_suivi is None:
        raise HTTPException(status_code=404, detail="Suivi not found")

    try:
        # Update fields
        for key, value in suivi.dict(exclude={'type_accompagnement_ids'}, exclude_unset=True).items():
            setattr(db_suivi, key, value)

        # Update type_accompagnement_ids
        if suivi.type_accompagnement_ids is not None:
            # Remove existing type_accompagnement_ids
            db.query(models.SuiviTypeAccompagnement).filter(models.SuiviTypeAccompagnement.id_suivi == suivi_id).delete()

            # Add new type_accompagnement_ids
            for ta in suivi.type_accompagnement_ids:
                db_ta = models.SuiviTypeAccompagnement(
                    id_suivi=suivi_id,
                    id_type_accompagnement=ta.id_type_accompagnement
                )
                db.add(db_ta)

        db.commit()
        db.refresh(db_suivi)
        logging.debug(f"Suivi updated successfully with ID: {db_suivi.id}")
        return db_suivi
    except Exception as e:
        logging.error(f"Error updating suivi with ID {suivi_id}: {e}")
        db.rollback()  # Rollback in case of error
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.delete("/suivi/delete/{suivi_id}", response_model=dict)
def delete_suivi(suivi_id: int, db: Session = Depends(get_db)):
    db_suivi = db.query(models.Suivi).filter(models.Suivi.id == suivi_id).first()
    if db_suivi is None:
        raise HTTPException(status_code=404, detail="Suivi not found")
    
    # Delete associated type_accompagnements
    db.query(models.SuiviTypeAccompagnement).filter(models.SuiviTypeAccompagnement.id_suivi == suivi_id).delete()
    
    # Delete the suivi
    db.delete(db_suivi)
    db.commit()
    return {"message": "Suivi deleted successfully"}

# Ville Endpoints
@app.post("/ville/create", response_model=schemas.Ville)
def create_ville(ville: schemas.VilleCreate, db: Session = Depends(get_db)):
    try:
        db_ville = models.Ville(**ville.dict())
        db.add(db_ville)
        db.commit()
        db.refresh(db_ville)
        return db_ville
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=422, detail=str(e))

@app.get("/ville/", response_model=List[schemas.Ville])
def read_villes(db: Session = Depends(get_db)):
    db_villes = db.query(models.Ville).all()
    return db_villes

@app.get("/ville/{ville_id}", response_model=schemas.Ville)
def read_ville(ville_id: int, db: Session = Depends(get_db)):
    db_ville = db.query(models.Ville).filter(models.Ville.id == ville_id).first()
    if db_ville is None:
        raise HTTPException(status_code=404, detail="Ville not found")
    return db_ville

@app.put("/ville/update/{ville_id}", response_model=schemas.Ville)
def update_ville(ville_id: int, ville: schemas.VilleCreate, db: Session = Depends(get_db)):
    db_ville = db.query(models.Ville).filter(models.Ville.id == ville_id).first()
    if db_ville is None:
        raise HTTPException(status_code=404, detail="Ville not found")
    
    for key, value in ville.dict().items():
        setattr(db_ville, key, value)
    
    db.commit()
    db.refresh(db_ville)
    return db_ville

@app.delete("/ville/delete/{ville_id}", response_model=dict)
def delete_ville(ville_id: int, db: Session = Depends(get_db)):
    db_ville = db.query(models.Ville).filter(models.Ville.id == ville_id).first()
    if db_ville is None:
        raise HTTPException(status_code=404, detail="Ville not found")
    db.delete(db_ville)
    db.commit()
    return {"message": "Ville deleted successfully"}

# TypeBien Endpoints
@app.post("/typebien/create", response_model=schemas.TypeBien)
def create_typebien(typebien: schemas.TypeBienCreate, db: Session = Depends(get_db)):
    try:
        db_typebien = models.TypeBien(**typebien.dict())
        db.add(db_typebien)
        db.commit()
        db.refresh(db_typebien)
        return db_typebien
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=422, detail=str(e))

@app.get("/typebien/", response_model=List[schemas.TypeBien])
def read_typebiens(db: Session = Depends(get_db)):
    db_typebiens = db.query(models.TypeBien).all()
    logging.debug(f"Fetched TypeBien records: {db_typebiens}")
    return db_typebiens

@app.get("/typebien/{typebien_id}", response_model=schemas.TypeBien)
def read_typebien(typebien_id: int, db: Session = Depends(get_db)):
    db_typebien = db.query(models.TypeBien).filter(models.TypeBien.id == typebien_id).first()
    if db_typebien is None:
        raise HTTPException(status_code=404, detail="TypeBien not found")
    return db_typebien

@app.put("/typebien/update/{typebien_id}", response_model=schemas.TypeBien)
def update_typebien(typebien_id: int, typebien: schemas.TypeBienCreate, db: Session = Depends(get_db)):
    db_typebien = db.query(models.TypeBien).filter(models.TypeBien.id == typebien_id).first()
    if db_typebien is None:
        raise HTTPException(status_code=404, detail="TypeBien not found")
    
    for key, value in typebien.dict().items():
        setattr(db_typebien, key, value)
    
    db.commit()
    db.refresh(db_typebien)
    return db_typebien

@app.delete("/typebien/delete/{typebien_id}", response_model=dict)
def delete_typebien(typebien_id: int, db: Session = Depends(get_db)):
    db_typebien = db.query(models.TypeBien).filter(models.TypeBien.id == typebien_id).first()
    if db_typebien is None:
        raise HTTPException(status_code=404, detail="TypeBien not found")
    db.delete(db_typebien)
    db.commit()
    return {"message": "TypeBien deleted successfully"}

# Statut Endpoints
@app.post("/statut/create", response_model=schemas.Statut)
def create_statut(statut: schemas.StatutCreate, db: Session = Depends(get_db)):
    try:
        db_statut = models.Statut(**statut.dict())
        db.add(db_statut)
        db.commit()
        db.refresh(db_statut)
        return db_statut
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=422, detail=str(e))

@app.get("/statut/", response_model=List[schemas.Statut])
def read_statuts(db: Session = Depends(get_db)):
    db_statuts = db.query(models.Statut).all()
    return db_statuts

@app.get("/statut/{statut_id}", response_model=schemas.Statut)
def read_statut(statut_id: int, db: Session = Depends(get_db)):
    db_statut = db.query(models.Statut).filter(models.Statut.id == statut_id).first()
    if db_statut is None:
        raise HTTPException(status_code=404, detail="Statut not found")
    return db_statut

@app.put("/statut/update/{statut_id}", response_model=schemas.Statut)
def update_statut(statut_id: int, statut: schemas.StatutCreate, db: Session = Depends(get_db)):
    db_statut = db.query(models.Statut).filter(models.Statut.id == statut_id).first()
    if db_statut is None:
        raise HTTPException(status_code=404, detail="Statut not found")
    
    for key, value in statut.dict().items():
        setattr(db_statut, key, value)
    
    db.commit()
    db.refresh(db_statut)
    return db_statut

@app.delete("/statut/delete/{statut_id}", response_model=dict)
def delete_statut(statut_id: int, db: Session = Depends(get_db)):
    db_statut = db.query(models.Statut).filter(models.Statut.id == statut_id).first()
    if db_statut is None:
        raise HTTPException(status_code=404, detail="Statut not found")
    db.delete(db_statut)
    db.commit()
    return {"message": "Statut deleted successfully"}

# TypeAccompagnement Endpoints
@app.post("/typeaccompagnement/create", response_model=schemas.TypeAccompagnement)
def create_typeaccompagnement(typeaccompagnement: schemas.TypeAccompagnementCreate, db: Session = Depends(get_db)):
    try:
        db_typeaccompagnement = models.TypeAccompagnement(**typeaccompagnement.dict())
        db.add(db_typeaccompagnement)
        db.commit()
        db.refresh(db_typeaccompagnement)
        return db_typeaccompagnement
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=422, detail=str(e))

@app.get("/typeaccompagnement/", response_model=List[schemas.TypeAccompagnement])
def read_typeaccompagnements(db: Session = Depends(get_db)):
    db_typeaccompagnements = db.query(models.TypeAccompagnement).all()
    return db_typeaccompagnements

@app.get("/typeaccompagnement/{typeaccompagnement_id}", response_model=schemas.TypeAccompagnement)
def read_typeaccompagnement(typeaccompagnement_id: int, db: Session = Depends(get_db)):
    db_typeaccompagnement = db.query(models.TypeAccompagnement).filter(models.TypeAccompagnement.id == typeaccompagnement_id).first()
    if db_typeaccompagnement is None:
        raise HTTPException(status_code=404, detail="TypeAccompagnement not found")
    return db_typeaccompagnement

@app.put("/typeaccompagnement/update/{typeaccompagnement_id}", response_model=schemas.TypeAccompagnement)
def update_typeaccompagnement(typeaccompagnement_id: int, typeaccompagnement: schemas.TypeAccompagnementCreate, db: Session = Depends(get_db)):
    db_typeaccompagnement = db.query(models.TypeAccompagnement).filter(models.TypeAccompagnement.id == typeaccompagnement_id).first()
    if db_typeaccompagnement is None:
        raise HTTPException(status_code=404, detail="TypeAccompagnement not found")
    
    for key, value in typeaccompagnement.dict().items():
        setattr(db_typeaccompagnement, key, value)
    
    db.commit()
    db.refresh(db_typeaccompagnement)
    return db_typeaccompagnement

@app.delete("/typeaccompagnement/delete/{typeaccompagnement_id}", response_model=dict)
def delete_typeaccompagnement(typeaccompagnement_id: int, db: Session = Depends(get_db)):
    db_typeaccompagnement = db.query(models.TypeAccompagnement).filter(models.TypeAccompagnement.id == typeaccompagnement_id).first()
    if db_typeaccompagnement is None:
        raise HTTPException(status_code=404, detail="TypeAccompagnement not found")
    db.delete(db_typeaccompagnement)
    db.commit()
    return {"message": "TypeAccompagnement deleted successfully"}

# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# async def health_check():
#     return "deploimen successfully"
