import numpy as np
import pandas as pd
import pickle as pk
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier

def createModel(data):
    label_encoders = {}
    for column in ['ChestPain', 'Thal']:
        le = LabelEncoder()
        data[column] = le.fit_transform(data[column])
        label_encoders[column] = le

    # Define features and target variable
    X = data.drop('Num', axis=1)
    y = data['Num']


    # split the data
    xTrain, xTest, yTrain, yTest = train_test_split(X, y, 
                                                    test_size=0.2)
    # train
    model = RandomForestClassifier(random_state=42)
    model.fit(xTrain, yTrain)

    # test the model
    yPred = model.predict(xTest)

    print("Accuracy:", accuracy_score(yTest, yPred)*100)
    print("Classification Report: \n", classification_report(yTest, yPred))

    return model

def main():

    data = pd.read_csv("C:/Users/heart disease prediction system dataset_.csv")

    model = createModel(data)

    with open('HeartModel.pkl', 'wb') as f:
        pk.dump(model, f)
        
if __name__ == '__main__':
    main()