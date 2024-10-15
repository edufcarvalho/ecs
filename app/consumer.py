from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from kafka import KafkaConsumer
import json
from models import EmotionalData
import uuid
from datetime import datetime

Session = sessionmaker(autocommit=False, autoflush=False, bind=create_engine("postgresql://user:password@ecs-db/ecs_db"))
session = Session()\

# Kafka consumer to listen to emotional data
consumer = KafkaConsumer(
    'emotions',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    api_version=(0,11,5),
    enable_auto_commit=True,
    group_id='ecs-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:
    try:
        message = message.value

        emotional_data = EmotionalData(
            id=uuid.uuid4(),
            user_id=message["user_id"],
            emotion=message["emotion"],
            thought=message["thought"],
            updated_at=datetime.now()
        )

        session.add(emotional_data)

        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")

session.close()
