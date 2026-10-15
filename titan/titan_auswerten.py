import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv("Data/data.csv")
höhe = df["Altitude"] / 1000 
time = df["Time"]

plt.plot(time, höhe)
plt.xlabel("time in s")
plt.ylabel("altitude in km")
plt.title("altitude over time")
plt.grid(True)
plt.savefig("altitude_over_time.png", dpi=150)
plt.show()


df = pd.read_csv("Data/data_assembly.csv")
temperature = df["Temperature"]


plt.plot(time, temperature)
plt.axhline(906, color="red", linestyle="--", label="Melting Point")
plt.xlabel("time in s")
plt.ylabel("temp in K")
plt.title("temp over time")
plt.grid(True)
plt.legend()
plt.savefig("Temperature_of_the_Monocoque_over_time.png", dpi=150)
plt.show()

print(df["Mass"].iloc[0])
print(df["Mass"].iloc[-1])
