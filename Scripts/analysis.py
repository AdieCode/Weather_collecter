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



def pullution_line(df, file):
    df_new = df[(df["lon"]== 28.1878) & (df["lat"]==-25.7449)]
    df_new.plot.line(y=['no','no2','o3','so2','pm2_5','pm10','nh3'])
    plt.title("Pollutant amounts over time")
    plt.xlabel("Samples taken over (10 min) intervals.")
    plt.ylabel("Amounts (μg/m3)")
    plt.savefig(file)
    plt.show()



def pullution_bar(df):
    df_new = df[(df["lon"]== 28.1878) & (df["lat"]==-25.7449)]
    df_new = df_new[['no','no2','o3','so2','pm2_5','pm10','nh3']].mean()
    df_new.plot.bar()
    plt.title("Pollutant Amounts")
    plt.xlabel("Different Pollutant's")
    plt.ylabel("Amounts (μg/m3)")
    plt.savefig("Figures/pullution_bar.png")
    plt.show()



def pullution_scatter(df):
    df_new = df[(df["lon"]== 28.1878) & (df["lat"]==-25.7449)]
    sns.scatterplot(data=df_new,
                    x="o3",
                    y="no2")
    plt.show()
    
    sns.scatterplot(data=df_new,
                    x="pm2_5",
                    y="no2")
    plt.show()
    
    sns.scatterplot(data=df_new,
                    x="o3",
                    y="no2")
    plt.show()



def pullution_bar(df, file):
    new_df = df[['no','no2','o3','so2','pm2_5','pm10','nh3']].mean()
    new_df.plot.bar()
    plt.title("Amount of different pollutant's")
    plt.xlabel("Different Pollutant's")
    plt.ylabel("Amounts (μg/m3)")
    plt.savefig(file)
    plt.show()



def pullution_heat(df, file):
    df_new = df[(df["lon"]== 28.1878) & (df["lat"]==-25.7449)]
    df_new = df_new[['no','no2','o3','so2','pm2_5','pm10','nh3']]
    sns.heatmap(df_new.corr(),annot=True,annot_kws={"size": 7}) 
    plt.title("Correlation between pollutant's")
    plt.savefig(file)
    plt.show()



def pullution_pairplot(df, file):
    df_new = df[['no','no2','o3','so2','pm2_5','pm10','nh3']]
    # sns.pairplot(data=df_new)
    #could also use the
    sns.pairplot(data=df_new,vars=['so2','pm2_5','pm10','nh3'])
    plt.savefig(file)
    plt.show()

df = pd.read_csv("Data/pollution.csv")

pullution_line(df,"Figures/Pollution/pullution_line.png")
pullution_bar(df,"Figures/Pollution/pullution_bar.png")
pullution_heat(df, "Figures/Pollution/pullution_heat.png")
pullution_pairplot(df, "Figures/Pollution/pullution_pairplot.png")
