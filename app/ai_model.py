import random
from models import User

# Function to simulate machine learning model prediction
def predict_credit_limit(user: User):
    return random.randint(500, 5000)
