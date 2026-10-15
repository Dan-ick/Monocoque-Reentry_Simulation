import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv("Data/data.csv")
höhe = df["Altitude"] / 1000 
time = df["Time"]

plt.plot(time, höhe)
plt.xlabel("Zeit in s")
plt.ylabel("Höhe in km")
plt.title("Höhe über Zeit")
plt.grid(True)
plt.savefig("Hoehe_ueber_zeit.png", dpi=150)
plt.show()


df = pd.read_csv("Data/data_assembly.csv")
temperature = df["Temperature"]


plt.plot(time, temperature)
plt.axhline(906, color="red", linestyle="--", label="Schmelzpunkt")
plt.xlabel("Zeiten [s]")
plt.xlabel("Zeit in s")
plt.ylabel("Temp in K")
plt.title("temp über Zeit")
plt.grid(True)
plt.legend()
plt.savefig("Temperature_of_the_Monocoque_over_time.png", dpi=150)
plt.show()

print(df["Mass"].iloc[0])
print(df["Mass"].iloc[-1])
