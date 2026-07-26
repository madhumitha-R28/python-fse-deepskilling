# ============================================================
# Digital Nurture 5.0 | Backend HO9 | security.py
# JWT Authentication, Password Hashing, Protected Routes
# Author: Madhumitha R
# INSTALL: pip install python-jose[cryptography] passlib[bcrypt] python-multipart
# ============================================================

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session

# Import db components from main.py
import sys
sys.path.insert(0, '.')
try:
    from fastapi_main import Base, SessionLocal, engine, app, get_db
except ImportError:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, declarative_base
    engine       = create_engine("sqlite:///./auth.db", connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base         = declarative_base()
    app          = FastAPI(title="Auth Service")
    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

# ============================================================
# CONFIGURATION
# ============================================================
SECRET_KEY   = "supersecret-change-this-in-production-use-256-bit-random"
ALGORITHM    = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ============================================================
# PASSWORD HASHING (HO9 Task 1, Step 87)
# WHY bcrypt over MD5/SHA-256:
# MD5 and SHA-256 are designed to be FAST — millions of hashes/second.
# This makes brute-force attacks trivial on modern hardware.
# bcrypt has a configurable "work factor" (rounds) that intentionally
# slows hashing to ~100ms per hash. A brute-force attack that would
# take 1 minute against MD5 would take 10,000 years against bcrypt
# with work_factor=12.
# Never use MD5 or plain SHA for passwords.
# ============================================================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# ============================================================
# USER MODEL (Step 86)
# ============================================================
class UserDB(Base):
    __tablename__     = "users"
    id                = Column(Integer, primary_key=True, index=True)
    email             = Column(String(100), unique=True, nullable=False)
    hashed_password   = Column(String(200), nullable=False)
    is_active         = Column(Boolean, default=True)

Base.metadata.create_all(bind=engine)


# ============================================================
# PYDANTIC SCHEMAS
# ============================================================
class UserCreate(BaseModel):
    email:    str
    password: str

class UserResponse(BaseModel):
    id:       int
    email:    str
    is_active: bool
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type:   str


# ============================================================
# JWT HELPERS (Steps 91-92)
# ============================================================
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire    = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    # WHY: JWT payloads are BASE64-ENCODED, NOT ENCRYPTED.
    # Anyone can decode the payload — never put passwords, credit cards,
    # or sensitive PII in the payload.
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail      = "Invalid or expired token",
        headers     = {"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(UserDB).filter(UserDB.email == email).first()
    if not user:
        raise credentials_exception
    return user


# ============================================================
# AUTH ENDPOINTS (Steps 88-93)
# ============================================================
@app.post("/api/v1/auth/register/", response_model=UserResponse, status_code=201, tags=["Auth"])
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Step 89: Check duplicate email
    existing = db.query(UserDB).filter(UserDB.email == user.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    # Step 90: Hash password — NEVER store plain text
    hashed = get_password_hash(user.password)
    db_user = UserDB(email=user.email, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/api/v1/auth/login/", response_model=Token, tags=["Auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail      = "Incorrect email or password",
            headers     = {"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


"""
Step 95: OAuth2 Authorization Code Flow vs Simple JWT Login
============================================================
Simple JWT Login (what we implemented):
  Client → POST /login (email+password) → Server returns JWT
  Client stores JWT, sends in Authorization: Bearer <token> header
  Server decodes JWT on every request to identify user

OAuth2 Authorization Code Flow (used by Google/GitHub login):
  1. Client redirects user to Provider (Google) login page
  2. User authenticates with Provider
  3. Provider redirects back to our app with an authorization CODE
  4. Our app exchanges the CODE for tokens via server-to-server call
  5. We receive access_token + refresh_token + id_token

Key difference:
  Simple JWT: user gives us their password directly
  OAuth2:     user never gives us their password — only gives us permission
              via the Provider. We get a token from the Provider, not from the user.
  Use OAuth2 when: integrating with Google, GitHub, Microsoft for SSO.
  Use simple JWT when: building your own auth system without third-party providers.
"""
