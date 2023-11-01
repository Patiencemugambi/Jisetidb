from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from typing import List
from pydantic import BaseModel
from app.schemas import Status
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(username=user.username, email=user.email, role=user.role)
    db_user.password = user.password
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

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

@app.put("/red_flags/{red_flag_id}", response_model=schemas.RedFlag)
def update_red_flag(red_flag_id: int, red_flag: schemas.RedFlagCreate, db: Session = Depends(get_db)):
    db_red_flag = db.query(models.RedFlag).filter(models.RedFlag.id == red_flag_id).first()
    if db_red_flag is None:
        raise HTTPException(status_code=404, detail="Red flag not found")
    for field, value in red_flag.dict().items():
        setattr(db_red_flag, field, value)
    db.commit()
    db.refresh(db_red_flag)
    return db_red_flag

@app.delete("/red_flags/{red_flag_id}")
def delete_red_flag(red_flag_id: int, db: Session = Depends(get_db)):
    db_red_flag = db.query(models.RedFlag).filter(models.RedFlag.id == red_flag_id).first()
    if db_red_flag is None:
        raise HTTPException(status_code=404, detail="Red flag not found")
    db.delete(db_red_flag)
    db.commit()
    return {"message": "Red flag deleted"}

class InterventionList(BaseModel):
    interventions: List[schemas.Intervention]

@app.get("/interventions/", response_model=List[schemas.Intervention])
def read_interventions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    interventions = db.query(models.Intervention).offset(skip).limit(limit).all()
    return interventions

@app.get("/interventions/{intervention_id}", response_model=schemas.Intervention)
def read_intervention(intervention_id: int, db: Session = Depends(get_db)):
    db_intervention = db.query(models.Intervention).filter(models.Intervention.id == intervention_id).first()
    if db_intervention is None:
        raise HTTPException(status_code=404, detail="Intervention not found")
    return db_intervention

@app.post("/interventions/", response_model=schemas.Intervention)
def create_intervention(intervention: schemas.InterventionCreate, db: Session = Depends(get_db)):
    db_intervention = models.Intervention(**intervention.dict())
    db.add(db_intervention)
    db.commit()
    db.refresh(db_intervention)
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

@app.delete("/interventions/{intervention_id}")
def delete_intervention(intervention_id: int, db: Session = Depends(get_db)):
    db_intervention = db.query(models.Intervention).filter
