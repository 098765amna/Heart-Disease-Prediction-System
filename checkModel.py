import pandas as pd
import pickle as pk
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler

def Predictions(inputData):
    model = pk.load(open("HeartModel.pkl", "rb"))

    prediction = model.predict(inputData)

    return prediction

data = pd.read_csv("C:/Users/heart disease prediction system dataset_.csv")
label_encoders = {}
for column in ['ChestPain', 'Thal']:
    le = LabelEncoder()
    data[column] = le.fit_transform(data[column])
    label_encoders[column] = le

    # Define features and target variable
X = data.drop('Num', axis=1)

prediction = Predictions(X[0:1])

if prediction == 1:
    print("Heart Disease!!!")
elif prediction == 0:
    print("Not...") 