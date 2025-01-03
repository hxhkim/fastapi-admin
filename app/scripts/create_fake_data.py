# app/scripts/create_fake_data.py
from faker import Faker
from datetime import datetime, timedelta
import random
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models import models

fake = Faker()

def create_fake_data(db: Session):
    # 템플릿 생성
    templates = []
    for i in range(5):
        template = models.Template(
            name=f"Template {i+1}",
            usage_count=random.randint(10, 100),
            is_premium=bool(random.getrandbits(1)),
            purchase_count=random.randint(0, 50)
        )
        db.add(template)
        templates.append(template)
    
    # 상품 생성
    products = []
    prices = [9900, 19900, 29900, 49900]
    for i in range(4):
        product = models.Product(
            name=f"Product {i+1}",
            type="subscription" if i % 2 == 0 else "one-time",
            price=prices[i],
            is_active=True
        )
        db.add(product)
        products.append(product)
    
    # 유저 생성
    users = []
    for i in range(50):
        user = models.User(
            email=fake.email(),
            password_hash="hashed_password",
            created_at=fake.date_time_between(start_date="-60d"),
            last_login=fake.date_time_between(start_date="-30d"),
            is_active=True
        )
        db.add(user)
        users.append(user)
    
    db.commit()
    
    # 프로젝트 생성
    for user in users:
        for _ in range(random.randint(1, 5)):
            project = models.Project(
                user_id=user.id,
                template_id=random.choice(templates).id,
                title=fake.catch_phrase(),
                created_at=fake.date_time_between(start_date="-60d"),
                avatar_url=f"https://example.com/avatar_{random.randint(1,100)}.jpg",
                motion_data="{}",
                is_active=bool(random.getrandbits(1)),
                download_count=random.randint(0, 20)
            )
            db.add(project)
    
    # 결제 생성
    for _ in range(100):
        payment = models.Payment(
            user_id=random.choice(users).id,
            product_id=random.choice(products).id,
            payment_type=random.choice(["card", "bank", "point"]),
            amount=random.choice(prices),
            created_at=fake.date_time_between(start_date="-60d")
        )
        db.add(payment)
    
    db.commit()

if __name__ == "__main__":
    db = SessionLocal()
    create_fake_data(db)
    db.close()