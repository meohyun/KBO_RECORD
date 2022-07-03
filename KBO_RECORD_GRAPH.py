from tokenize import String
from matplotlib import font_manager,rc
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

teamname = input("Team: ")
font_path = "C:/Windows/Fonts/NGULIM.TTF"

font = font_manager.FontProperties(fname=font_path).get_name()
rc('font',family=font)

df= pd.read_excel(f"{teamname}_기록.xlsx",sheet_name='포수')
df1 = pd.read_excel(f"{teamname}_기록.xlsx",sheet_name='내야수')
df2 = pd.read_excel(f"{teamname}_기록.xlsx",sheet_name='외야수')

data_concat= pd.concat([df,df1,df2],ignore_index=True)

for i in range(len(data_concat['AVG'])):
    if type(data_concat['AVG'][i]) == str:
        data_concat['AVG'][i] = 0.0

data_concat = data_concat.drop(['Unnamed: 0'],axis=1)
data_concat = data_concat.sort_values(by=['AVG'],axis=0)


x = data_concat['AVG'].values
y = data_concat['선수명'].values


plt.figure(figsize=(5,5))
plt.barh(y,x,height=0.5)
plt.title(f"{teamname} 야수 AVG")

for i, v in enumerate(x):
    plt.text(v, y[i], x[i],                 # 좌표 (x축 = v, y축 = y[0]..y[1], 표시 = y[0]..y[1])
             fontsize = 9, 
             color='blue',
             horizontalalignment='left',  # horizontalalignment (left, center, right)
             verticalalignment='center')    # verticalalignment (top, center, bottom)
plt.show()


