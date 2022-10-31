import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import LocalOutlierFactor
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


def read_and_clean_data():

    df = pd.read_csv('Data_Base/echocardiogram.data', sep=",", header=None , on_bad_lines='skip')
    df.columns = ["survival", "still-alive", "age-at-heart-attack", "pericardial-effusion", "fractional-shortening",
                "epss", "lvdd", "wall-motion-score", "wall-motion-index", "mult", "name", "group", "alive-at-1"]
                
    df.replace('?', np.nan, inplace=True)
    df.head()   

    df.columns[df.isna().any()].tolist()


    df.drop(['alive-at-1', 'mult', 'group', 'name','wall-motion-score'], axis = 1, inplace = True)
    df.columns


    for column in df:
        df[column] = pd.to_numeric(df[column])

    for column in df:
        if column in ['still-alive', 'pericardial-effusion']: continue
        df[column].fillna(df[column].mean().round(1), inplace = True)

    df.columns[df.isna().any()].tolist()

    df.rename(columns = {'still-alive': 'alive'}, inplace = True)

    df.to_csv('Data_Base/clean_data.csv', index = False)







#machine learning

#reading and cleaning data only once
if (os.path.isfile('Data_Base/clean_data.csv')) == False: 
    read_and_clean_data()

df = pd.read_csv('Data_Base/clean_data.csv')
lof = LocalOutlierFactor()
outliers_rows = lof.fit_predict(df)
mask = outliers_rows != -1
df = df[mask]

X_train, X_test, y_train, y_test = train_test_split(df.drop(['alive'], 1), df['alive'], test_size=0.25, random_state=42)
X_train.shape, X_test.shape

random_forest = RandomForestClassifier(max_depth=1,n_estimators=11, random_state=42).fit(X_train, y_train)



risk_desctiption = [
    "According to our predictions the profile that alligns with the input data is that of one in a critical condition, Please seek help immediately.",
    "According to our predictions the profile that alligns with the input data is that of one in a medium level risk, it is advised to see a health professional as soon as possible.",
    "According to our predictions the profile that alligns with the input data is that of one in a Low level risk. You can report the lab results when needed."
]



def predict(input_):
    values = [float(x) for x in input_]
    prediction = random_forest.predict_proba([values])
    prediction = prediction[0][0]
    if prediction < 0.4:
        return ["Low level Risk",risk_desctiption[2]]
    if prediction < 0.6:
        return ["Medium Risk",risk_desctiption[1]]
    if prediction < 1:
        return ["High Risk",risk_desctiption[0]]
    


####################  functions for getting rows and columns for graphs   ####################

#getting list of tuples as points (x,y) for graph plotting
def treat_data(column):
    data = df[column].value_counts()
    data = list(zip(data,data.index))
    sorted_data = sorted(data, key=lambda tup: tup[1])
    return sorted_data

#getting data for the graphs
def get_graph_data():
    age = treat_data('age-at-heart-attack')
    pericardial_effusion = treat_data('pericardial-effusion')
    fractional_shortening = treat_data('fractional-shortening')
    epss = treat_data('epss')
    lvdd = treat_data('lvdd')
    wall_motion_index = treat_data('wall-motion-index')
    return [age,pericardial_effusion,fractional_shortening,epss,lvdd,wall_motion_index]