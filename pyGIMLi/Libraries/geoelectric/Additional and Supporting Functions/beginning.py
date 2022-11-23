import geoelectric as gelt
file = "abemDD (resistance in res2dinv format).dat"
data = gelt.beginning(file)
data.save("abemDD.dat")  #Saved in unified data format
