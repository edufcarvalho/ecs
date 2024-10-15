from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import uuid
from pydantic import BaseModel
from models import CreditLimit, User
from datetime import datetime

Session = sessionmaker(autocommit=False, autoflush=False, bind=create_engine("postgresql://user:password@ecs-db/ecs_db"))
session = Session()

app = FastAPI()

# Database connection setup
@app.get("/credit-limit/{user_id}")
def calculate_credit_limit(user_id: str):
    try:
        user = session.query(User).filter_by(id=user_id).first()

        return user.credit_limit
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")

@app.post("/credit-limit/{user_id}")
def define_credit_limit(user_id: str, credit_limit: float):
    try:
        credit_limit = CreditLimit(
            id = uuid.uuid4(),
            user_id = user_id,
            credit_limit = credit_limit,
            updated_at = datetime.now()
        )

        session.add(credit_limit)

        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
