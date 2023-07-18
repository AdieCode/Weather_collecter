import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def getTempToTimeGraph(df):
    sns.lineplot(data=df,
                 x="date",
                 y="temp")
    plt.show()



def wind_speed(df):
    sns.countplot(data=df,
                 x="wind_speed")
    plt.show()



def hum_temp(df):
    sns.lmplot(x="temp",
               y="humidity",
               hue="city",
               data=df)
    plt.show()

df = pd.read_csv("Data/weather.csv")
hum_temp(df)