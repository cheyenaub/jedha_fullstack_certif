from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union
from joblib import load


description = """This API serves the purpose of estimating the daily rental price for a vehicle.
The API utilizes a dataset derived from Getaround's extensive collection of cars.
## About GetAround:
### Key Highlights Include:

- `Ranked 2nd` globally in the peer-to-peer car-sharing industry.
- `Operates` in 950 cities spanning across 8 countries, with 1.6 million customers renting 66,000 cars from hosts. A substantial market potential unlocked through a digital framework.
- Services an addressable market valued at $155 billion, with a proven track record of profitability.
- Demonstrates a `profitability per transaction` exceeding 50%, showcasing substantial trip contribution margins.
- Boasts robust `long-term resilience` within the car-sharing model, enhanced by cutting-edge connected car technology, ensuring an exceptional user experience.
- Creates an exceptionally smooth and seamless experience for both hosts and renters.

Within this project, our objective is to fine-tune the pricing for daily rentals!
- `daily_rental_price`: representing the rental cost of the vehicle (in $).

## Sample Cars
* `/`: A **GET** request that showcases random data samples.

## Model Search
* `/search_model_key/{model_key}`: A **GET** request to retrieve data corresponding to a specific car model.

## Machine Learning 

This machine learning endpoint forecasts the optimal daily rental price based on your car's unique features.

Endpoints:

* `/predict`

For further details on each endpoint, please refer to the documentation below 👇.
"""

app = FastAPI()

# Charger le modèle de régression linéaire
model = load('modele_regression.pkl')

class CarFeatures(BaseModel):
    feature1: float
    feature2: float
    # Ajoutez d'autres caractéristiques ici selon votre modèle

@app.get("/")
async def welcome():
    message = """Bienvenue sur l'API de tarification de location de voitures ! Cette API est conçue pour estimer le prix optimal auquel vous devriez louer votre voiture. Le modèle utilisé pour la prédiction est un modèle de Gradient Boosting formé sur des données collectées par l'équipe de data scientists de Getaround."""
    return message

@app.get("/examples")
async def load_examples():
    """
    Affiche quelques exemples aléatoires des données
    """

    # Charger les données d'exemple
    examples = [
        {"feature1": 5.1, "feature2": 3.5},
        {"feature1": 4.9, "feature2": 3.0},
        {"feature1": 4.7, "feature2": 3.2},
        {"feature1": 4.6, "feature2": 3.1},
        {"feature1": 5.0, "feature2": 3.6}
    ]

    return examples

@app.get("/search/model/{model_key}")
async def search_car_model(model_key: str):
    """
    Recherche de données pour un modèle de voiture spécifique
    """

    # Chargez vos données de modèle de voiture ici
    # Remplacez cette liste par vos données réelles
    car_data = [
        {"model_key": "Toyota", "feature1": 5.1, "feature2": 3.5},
        {"model_key": "Honda", "feature1": 4.9, "feature2": 3.0},
        {"model_key": "Ford", "feature1": 4.7, "feature2": 3.2},
    ]

    # Recherchez le modèle de voiture spécifié
    result = [car for car in car_data if car["model_key"] == model_key]

    return result

class CarPrediction(BaseModel):
    feature1: float
    feature2: float
    # Ajoutez d'autres caractéristiques ici selon votre modèle

@app.post("/predict")
async def predict_price(car: CarPrediction):
    """
    Obtenez le prix de location prédit pour une voiture
    """

    # Utilisez le modèle pour faire une prédiction
    features = [car.feature1, car.feature2]  # Ajoutez d'autres caractéristiques ici selon votre modèle
    prediction = model.predict([features])

    return {"predicted_price": prediction[0]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
