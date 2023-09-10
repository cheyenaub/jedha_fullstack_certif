import pandas as pd
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel, validator
import joblib
import uvicorn

app = FastAPI(
    title='GetAround pricing predictor API',
    description= """This API serves the purpose of estimating the daily rental price for a vehicle.
The API utilizes a dataset from GetAround

The API is based on a dataset of cars from Getaround.

The dataset contains 14 columns that are:
- `model_key`: brand of the car (Toyota, Mini, Renault, etc.)
- `mileage`: mileage of the car (in km)
- `engine_power`: engine power of the car (in horse power)
- `fuel`: fuel type of the car (includes diesel, petrol, hybrid, electric)
- `paint_color`: the color of the car
- `car_type`: the type of car (includes sedan, hatchback, suv, van, estate, convertible, coupe, subcompact)
- `private_parking_available`: whether the car has a private parking or not (boolean)
- `has_gps`: whether the car has a GPS or not (boolean)
- `has_air_conditioning`: whether the car has air conditioning or not (boolean)
- `automatic_car`: whether the car is automatic or not (boolean)
- `has_getaround_connect`: whether the car has Getaround Connect or not (boolean)
- `has_speed_regulator`: whether the car has a speed regulator or not (boolean)
- `winter_tires`: whether the car has winter tires or not (boolean)
- `rental_price_per_day`: the rental price of the car (in $)

Within this project, our objective is to fine-tune the pricing for daily rentals!
- 'rental_price_per_day': representing the rental cost of the vehicle (in $).

## Sample Cars
* '/': A **GET** request that showcases random data samples.

## Machine Learning 

This machine learning endpoint forecasts the optimal daily rental price based on your car's unique features.

Endpoints:

* '/predict'
"""
)

@app.get("/")
async def root():
    message = """Welcome to the Getaround API. This app is made to give the best price to rent your car on the GetAround app."""
    return message

# preview to get 5 random example of the data
@app.get("/preview")
async def load_sample_cars():
    """
    display some (5) random examples of the data
    """

    cars = pd.read_csv("data/get_around_pricing.csv", index_col=0)
    
    car = cars.sample(5).reset_index(drop=True)

    return car.to_dict(orient="index")

# Defining required input for the prediction endpoint
class Features(BaseModel):
    model_key: str
    mileage: int
    engine_power: int
    fuel: str
    paint_color: str
    car_type: str
    private_parking_available: bool
    has_gps: bool
    has_air_conditioning: bool
    automatic_car: bool
    has_getaround_connect: bool
    has_speed_regulator: bool
    winter_tires: bool
    
    @validator('model_key')
    def validate_model_key(cls, v):
        accepted_values = ['Citroën', 'Peugeot', 'PGO', 'Renault', 'Audi', 'BMW', 'Ford',
        'Mercedes', 'Opel', 'Porsche', 'Volkswagen', 'KIA Motors','Alfa Romeo', 'Ferrari', 'Fiat', 'Lamborghini', 'Maserati',
        'Lexus', 'Honda', 'Mazda', 'Mini', 'Mitsubishi', 'Nissan', 'SEAT','Subaru', 'Toyota', 'Suzuki', 'Yamaha']
        if v not in accepted_values:
            raise ValueError(f"Invalid model_key. Must be one of {accepted_values}")
        return v

    @validator('fuel')
    def validate_fuel(cls, v):
        accepted_values = ['diesel', 'petrol', 'hybrid_petrol', 'electro']
        if v not in accepted_values:
            raise ValueError(f"Invalid fuel. Must be one of {accepted_values}")
        return v

    @validator('mileage')
    def validate_mileage(cls, v):
        if v < 0:
            raise ValueError("Mileage must be positive")
        return v
    
    @validator('engine_power')
    def validate_engine_power(cls, v):
        if v < 0:
            raise ValueError("Engine power must be positive")
        return v
    
    @validator('paint_color')
    def validate_paint_color(cls, v):
        accepted_values = ['black', 'white', 'red', 'silver', 'grey', 'blue', 'orange','beige', 'brown', 'green']
        if v not in accepted_values:
            raise ValueError(f"Invalid color. Must be one of {accepted_values}")
        return v
    
    @validator('car_type')
    def validate_car_type(cls, v):
        accepted_values = ['sedan', 'hatchback', 'suv', 'van', 'estate', 'convertible', 'coupe', 'subcompact']
        if v not in accepted_values:
            raise ValueError(f"invalid car type. Must be one of {accepted_values}")
        
# endpoint to predict the rental price of a car
@app.post("/predict")
async def predict(features:Features):
    """ Get the predicted rental price of a car for one day.
    Let's see an example of how to use the API :
{  
    "model_key": "Peugeot",  
    "mileage" : 92000,  
    "engine_power" : 190,  
    "fuel": "diesel",  
    "paint_color": "black",  
    "car_type": "sedan",  
    "private_parking_available": false,  
    "has_gps": true,  
    "has_air_conditioning": true,  
    "automatic_car": false,  
    "has_getaround_connect": true,  
    "has_speed_regulator": true,  
    "winter_tires": false  
    }
    
Should return : "prediction" : 137.9753195 (for example)
    """
    
    features = dict(features)
    input_df = pd.DataFrame(columns=['model_key', 'mileage', 'engine_power', 'fuel', 'paint_color','car_type', 'private_parking_available', 'has_gps',
       'has_air_conditioning', 'automatic_car', 'has_getaround_connect','has_speed_regulator', 'winter_tires'])
    input_df.loc[0] = list(features.values())
    # Load the model & preprocessor
    model = joblib.load('gbr_model.pkl')
    prep = joblib.load('preprocessor.pkl')
    X = prep.transform(input_df)
    pred = model.predict(X)
    return {"prediction" : pred[0]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000, debug=True, reload=True)
