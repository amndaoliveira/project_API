from fastapi import APIRouter, HTTPException
from app.db import get_session
from app.models.Usuario import Usuario
from sqlmodel import SQLModel, Field, Session, create_engine, select

