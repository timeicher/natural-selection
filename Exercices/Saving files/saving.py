import pandas as pd


data = pd.DataFrame({"Cheese": [[0,1,2],[2,2,3],[7,7,3]]})

datatoexcel = pd.ExcelWriter("FromPython.xlsx",engine="xlsxwriter")

data.to_excel(datatoexcel, sheet_name="sheet1")

datatoexcel.save()