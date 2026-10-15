import matplotlib.pyplot as plt


zeiten = []
min_T = []
max_p = []

with open("log.rhoCentralFoam") as f:
    for zeile in f:
        zeile = zeile.strip()                 
        if zeile.startswith("Time ="):        
            zeiten.append(float(zeile.split()[2]))
        elif zeile.startswith("min(T)"):  
            min_T.append(float(zeile.split()[2]))
        elif zeile.startswith("max(p)"):          
            max_p.append(float(zeile.split()[2]))
            

print(len(zeiten))
print(zeiten[-1])


print(len(min_T))
print(min_T[-1])

print(len(max_p))
print(max_p[-1])


plt.plot(zeiten, min_T)
plt.xlabel("Zeiten [s]")
plt.ylabel("Temp [K]")
plt.title("Minimale Temperatur über Zeit")
plt.grid(True)
plt.savefig("Temp.png", dpi=150)
plt.show()


plt.plot(zeiten, max_p)
plt.axhline(9060, color="red", linestyle="--", label="Rayleigh-Pitot")
plt.xlabel("Zeiten [s]")
plt.ylabel("Druck [Pa]")
plt.title("Maximaler Druck über Zeit")
plt.grid(True)
plt.legend()
plt.savefig("Druck.png", dpi=150)
plt.show()