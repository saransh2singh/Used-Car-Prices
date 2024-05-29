from flask import Flask, render_template, request
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        data = request.form
        year = int(data['Year'])
        present_price = float(data['Present_Price'])
        kms_driven = int(data['Kms_Driven'])
        owner = int(data['Owner'])
        fuel_type = data['Fuel_Type_Petrol']
        if fuel_type == 'Petrol':
            fuel_type_petrol = 1
            fuel_type_diesel = 0
        else:
            fuel_type_petrol = 0
            fuel_type_diesel = 1
        year = 2024 - year
        seller_type = data['Seller_Type_Individual']
        if seller_type == 'Individual':
            seller_type_individual = 1
        else:
            seller_type_individual = 0
        transmission_manual = data['Transmission_Mannual']
        if transmission_manual == 'Mannual':
            transmission_manual = 1
        else:
            transmission_manual = 0
        prediction = model.predict([[present_price, kms_driven, owner, year, fuel_type_diesel, fuel_type_petrol, seller_type_individual, transmission_manual]])
        output = round(prediction[0], 2)
        if output < 0:
            prediction_text = "Sorry, you cannot sell this car."
        else:
            prediction_text = "You can sell the car at {}".format(output)
        return render_template('index.html', prediction_text=prediction_text)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
