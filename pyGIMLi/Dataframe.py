import pandas as pd
 
filename = "DD-MargentoJune2019Line1.dat"
dataset = pg.physics.ert.load(filename)

surface_position = gelt.surfacePosition(dataset, full=True)
depth_of_investigation = gelt.depthOfInvestigation(dataset, full=True)
apparent_resistivity = np.array(dataset["rhoa"])

matrix = np.vstack((surface_position, 
                    depth_of_investigation, 
                    apparent_resistivity)).T

matrix = pd.DataFrame(matrix, 
                      columns=["Surface Position", 
                               "Depth of Investigation", 
                               "Apparent Resistivity"])

matrix = matrix.sort_values(["Depth of Investigation", "Surface Position"])
data = matrix[data.columns[2]]

columns = []
for i in range(1, 39):
    columns.append(f"Lay1_Pos{i}")
for i in range(1, 37):
    columns.append(f"Lay2_Pos{i}")
for i in range(1, 36):
    columns.append(f"Lay3_Pos{i}")
for i in range(1, 35):
    columns.append(f"Lay4_Pos{i}")
for i in range(1, 33):
    columns.append(f"Lay5_Pos{i}")
for i in range(1, 33):
    columns.append(f"Lay6_Pos{i}")
for i in range(1, 32):
    columns.append(f"Lay7_Pos{i}")
for i in range(1, 28):
    columns.append(f"Lay8_Pos{i}")
for i in range(1, 27):
    columns.append(f"Lay9_Pos{i}")
for i in range(1, 24):
    columns.append(f"Lay10_Pos{i}")
for i in range(1, 21):
    columns.append(f"Lay11_Pos{i}")
for i in range(1, 15):
    columns.append(f"Lay12_Pos{i}")

# Create the pandas DataFrame with column name is provided explicitly
df = pd.DataFrame(data, 
                  columns)
 
print(df)