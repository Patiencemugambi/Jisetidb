from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, database
from typing import List, Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel, ValidationError
from app.database import SessionLocal
from app.schemas import Status, Geolocation

SECRET_KEY = "bbd52edcc37bf1e12607be5859baabfdb22e3aee556d5798d7174a941aa4bd8f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

ADMIN_ROLE = "admin"
USER_ROLE = "user"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user(username: str, db: Session):
    return db.query(models.User).filter(models.User.username == username).first()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = get_user(username=token_data.username, db=db) 
    if user is None:
        raise credentials_exception
    return user



@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if the user specified "admin" as the role
    role = user.role if user.role == ADMIN_ROLE else USER_ROLE

    existing_user = get_user(user.username, db)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, email=user.email, role=role, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user(form_data.username, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for field, value in user.dict().items():
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted"}


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users


@app.get("/statuses/", response_model=List[schemas.Status])
def read_statuses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    statuses = db.query(models.Status).offset(skip).limit(limit).all()
    return statuses


@app.post("/statuses/", response_model=schemas.Status)
def create_status(status: schemas.StatusCreate, db: Session = Depends(get_db)):
    db_status = models.Status(name=status.name)
    db.add(db_status)
    db.commit()
    db.refresh(db_status)
    return db_status


@app.get("/red_flags/", response_model=List[schemas.RedFlag])
def read_red_flags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    red_flags = db.query(models.RedFlag).offset(skip).limit(limit).all()
    return red_flags


@app.get("/red_flags/{red_flag_id}", response_model=schemas.RedFlag)
def read_red_flag(red_flag_id: int, db: Session = Depends(get_db)):
    db_red_flag = db.query(models.RedFlag).filter(models.RedFlag.id == red_flag_id).first()
    if db_red_flag is None:
        raise HTTPException(status_code=404, detail="Red flag not found")
    return db_red_flag


@app.post("/red_flags/", response_model=schemas.RedFlag)
def create_red_flag(red_flag: schemas.RedFlagCreate, db: Session = Depends(get_db)):
    db_red_flag = models.RedFlag(**red_flag.dict())
    db.add(db_red_flag)
    db.commit()
    db.refresh(db_red_flag)
    return db_red_flag


@app.put("/red_flags/{red_flag_id}/update_location", response_model=schemas.RedFlag)
def update_red_flag_location(
    red_flag_id: int,
    location: Geolocation,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    db_red_flag = db.query(models.RedFlag).filter(models.RedFlag.id == red_flag_id).first()
    if db_red_flag is None:
        raise HTTPException(status_code=404, detail="Red flag not found")

    if db_red_flag.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")

    db_red_flag.county = location.county
    db_red_flag.location = location.location
    db.commit()
    db.refresh(db_red_flag)
    return db_red_flag


@app.post("/statuses/{red_flag_id}/change_status", response_model=schemas.RedFlag)
def change_red_flag_status(
    red_flag_id: int,
    new_status: Status,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    if current_user.role != ADMIN_ROLE:
        raise HTTPException(status_code=403, detail="Permission denied. Only admin can change status.")

    db_red_flag = db.query(models.RedFlag).filter(models.RedFlag.id == red_flag_id).first()
    if db_red_flag is None:
        raise HTTPException(status_code=404, detail="Red flag not found")

    db_status = db.query(models.Status).filter(models.Status.name == new_status.name).first()
    if db_status is None:
        raise HTTPException(status_code=404, detail="Status not found")

    db_red_flag.status_id = db_status.id
    db.commit()
    db.refresh(db_red_flag)
    return db_red_flag


@app.post("/interventions/{intervention_id}/change_status", response_model=schemas.Intervention)
def change_intervention_status(
    intervention_id: int,
    new_status: Status,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    if current_user.role != ADMIN_ROLE:
        raise HTTPException(status_code=403, detail="Permission denied. Only admin can change status.")

    db_intervention = db.query(models.Intervention).filter(models.Intervention.id == intervention_id).first()
    if db_intervention is None:
        raise HTTPException(status_code=404, detail="Intervention not found")

    db_status = db.query(models.Status).filter(models.Status.name == new_status.name).first()
    if db_status is None:
        raise HTTPException(status_code=404, detail="Status not found")

    db_intervention.status_id = db_status.id
    db.commit()
    db.refresh(db_intervention)
    return db_intervention


@app.get("/interventions/{intervention_id}", response_model=schemas.Intervention)
def read_intervention(intervention_id: int, db: Session = Depends(get_db)):
    db_intervention = db.query(models.Intervention).filter(models.Intervention.id == intervention_id).first()
    if db_intervention is None:
        raise HTTPException(status_code=404, detail="Intervention not found")
    return db_intervention


@app.put("/interventions/{intervention_id}", response_model=schemas.Intervention)
def update_intervention(intervention_id: int, intervention: schemas.InterventionCreate, db: Session = Depends(get_db)):
    db_intervention = db.query(models.Intervention).filter(models.Intervention.id == intervention_id).first()
    if db_intervention is None:
        raise HTTPException(status_code=404, detail="Intervention not found")
    for field, value in intervention.dict().items():
        setattr(db_intervention, field, value)
    db.commit()
    db.refresh(db_intervention)
    return db_intervention


@app.put("/interventions/{intervention_id}/update_location", response_model=schemas.Intervention)
def update_intervention_location(
    intervention_id: int,
    location: Geolocation,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    db_intervention = db.query(models.Intervention).filter(models.Intervention.id == intervention_id).first()
    if db_intervention is None:
        raise HTTPException(status_code=404, detail="Intervention not found")

    if db_intervention.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")

    db_intervention.county = location.county
    db_intervention.location = location.location
    db.commit()
    db.refresh(db_intervention)
    return db_intervention


@app.post("/interventions/", response_model=schemas.Intervention)
def create_intervention(intervention: schemas.InterventionCreate, db: Session = Depends(get_db)):
    db_intervention = models.Intervention(**intervention.dict())
    db.add(db_intervention)
    db.commit()
    db.refresh(db_intervention)
    return db_intervention


@app.get("/interventions/", response_model=List[schemas.Intervention])
def read_interventions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    interventions = db.query(models.Intervention).offset(skip).limit(limit).all()
    return interventions


@app.delete("/interventions/{intervention_id}")
def delete_intervention(intervention_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_intervention = db.query(models.Intervention).filter(models.Intervention.id == intervention_id).first()
    if db_intervention is None:
        raise HTTPException(status_code=404, detail="Intervention not found")

    if db_intervention.user_id != current_user.id and current_user.role != ADMIN_ROLE:
        raise HTTPException(status_code=403, detail="Permission denied")

    db_intervention.deleted_by = current_user.id
    db_intervention.deleted_at = datetime.utcnow()
    db.commit()

    return {"message": "Intervention deleted", "deleted_at": db_intervention.deleted_at, "deleted_by": db_intervention.deleted_by}
