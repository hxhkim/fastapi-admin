# app/models/models.py
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)

    projects = relationship("Project", back_populates="user")
    payments = relationship("Payment", back_populates="user")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    template_id = Column(Integer, ForeignKey("templates.id"))
    title = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    avatar_url = Column(String)
    motion_data = Column(String)  # JSON 데이터를 문자열로 저장
    is_active = Column(Boolean, default=True)
    download_count = Column(Integer, default=0)

    user = relationship("User", back_populates="projects")
    template = relationship("Template", back_populates="projects")
    download_logs = relationship("DownloadLog", back_populates="project")

class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    usage_count = Column(Integer, default=0)
    is_premium = Column(Boolean, default=False)
    purchase_count = Column(Integer, default=0)

    projects = relationship("Project", back_populates="template")

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    payment_type = Column(String)
    amount = Column(Numeric(10, 2))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="payments")
    product = relationship("Product", back_populates="payments")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    type = Column(String)
    price = Column(Numeric(10, 2))
    is_active = Column(Boolean, default=True)

    payments = relationship("Payment", back_populates="product")

class DownloadLog(Base):
    __tablename__ = "download_logs"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    downloaded_at = Column(DateTime(timezone=True), server_default=func.now())

    project = relationship("Project", back_populates="download_logs")