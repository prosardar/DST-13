import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations
from scipy.stats import ttest_ind
   
pd.set_option('display.max_rows', 50) # показывать больше строк
pd.set_option('display.max_columns', 50) # показывать больше колонок

stud_db = pd.read_csv('C:\\Users\\prosa\\source\\repos\\skillfactory_rds\\project 2\\stud_math.xls')

def get_boxplot(yColumn, column):
    fig, ax = plt.subplots(figsize = (14, 4))
    sns.boxplot(x=column, y=yColumn, 
                data=stud_db.loc[stud_db.loc[:, column].isin(stud_db.loc[:, column].value_counts())],
               ax=ax)
    plt.xticks(rotation=45)
    ax.set_title('Boxplot for ' + column)
    plt.show()

def get_stat_dif(yColumn, column):
    cols = stud_db.loc[:, column].value_counts()
    display(cols)
    combinations_all = list(combinations(cols, 2))
    for comb in combinations_all:
        if ttest_ind(stud_db.loc[stud_db.loc[:, column] == comb[0], yColumn], 
                        stud_db.loc[stud_db.loc[:, column] == comb[1], yColumn]).pvalue \
            <= 0.05/len(combinations_all): # Учли поправку Бонферони
            print('Найдены статистически значимые различия для колонки', column)
            break
    #print('Статистически значимые различия НЕ найдены для колонки', column) 
