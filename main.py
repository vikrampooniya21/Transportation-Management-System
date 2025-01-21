from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship

# Database connection URL (Windows Authentication)
DATABASE_URL = "mssql+pyodbc://@DESKTOP-JDS8NQJ\SQLEXPRESS/master?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"

# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

# FastAPI app
app = FastAPI()

# User Model
class User(Base):
    __tablename__ = "Users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=func.now())

    shipments = relationship("Shipment", back_populates="customer", cascade="all, delete-orphan")

# Shipment Model
class Shipment(Base):
    __tablename__ = "Shipments"
    shipment_id = Column(Integer, primary_key=True, autoincrement=True)
    current_location = Column(String(255), nullable=False)
    estimated_delivery = Column(DateTime, nullable=False)
    status = Column(String(50), nullable=False)
    customer_id = Column(Integer, ForeignKey("Users.user_id", ondelete="CASCADE"), nullable=False)

    customer = relationship("User", back_populates="shipments")

# Vehicle Model
class Vehicle(Base):
    __tablename__ = "Vehicles"
    vehicle_id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_number = Column(String(50), unique=True, nullable=False)
    vehicle_type = Column(String(50), nullable=False)
    driver_name = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root Endpoint
@app.get("/")
def home():
    return {"message": "Welcome to the Shipping API"}

# Get All Users
@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# Get User by ID
@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Get All Shipments
@app.get("/shipments/")
def get_shipments(db: Session = Depends(get_db)):
    shipments = db.query(Shipment).all()
    return shipments

# Get Shipment by ID
@app.get("/shipments/{shipment_id}")
def get_shipment(shipment_id: int, db: Session = Depends(get_db)):
    shipment = db.query(Shipment).filter(Shipment.shipment_id == shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return shipment

# Get All Vehicles
@app.get("/vehicles/")
def get_vehicles(db: Session = Depends(get_db)):
    vehicles = db.query(Vehicle).all()
    return vehicles

# Get Vehicle by ID
@app.get("/vehicles/{vehicle_id}")
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle
