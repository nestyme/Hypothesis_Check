

import pandas as pd
import numpy as np
import scipy as sp
import scipy.stats as st

data = pd.read_csv('log.txt', sep=",", header=None)

data.columns=['Number','Request Type','Response time']


data['Number'] = data.index

data_Type = data['Request Type'].unique()
print 'Различные типы запросов:',data_Type


# Выведем **средние времена отклика** для каждого  типа запроса, предварительно сгруппировав по названиям запросов
average_request_time=data.groupby(['Request Type']).mean().drop(['Number'],axis=1)


print(data.columns)
#data = data.drop(['Number'],axis=1)
data_index = data.index
data=data.sort_values(by='Request Type',ascending=False)
data.index = [i for i in range(len(data))]
data_Type= np.sort(data_Type)
data_Type = data_Type[::-1]
d = dict.fromkeys(data_Type,[])


# Так как сейчас массив данных у нас *игрушечный*, то положим в словарь в явном виде значения.
# Если мы намерены работать с `1 ТБ` данных, то следует использовать функции библиотеки `pandas`. Кроме того, для ускорения вычислений можно использовать параллельные или распределенные системы для вычислений.

d = {'/test':[0.03,0.045],'/index':[0.06,1.020],'/home':[0.561,0.870]}


# ## Подсчет доверительного интервала
# найдем 95%-ый доверительный интервал для каждого среднего значения в группах

def calculate_confidence_interval (a, percent = 0.95):
    return st.t.interval(percent, len(a)-1, loc=np.mean(a), scale=st.sem(a))
for Type in data_Type:
    a = d[Type]
    print a
    print 'Доверительный интервал 95% для ', Type, calculate_confidence_interval(a)


# ##  Проверка гипотезы 
# о равенстве средних времен отклика для типов запроса `/index` и `/test` на уровне значимости 5%.

# 1. Гипотеза $H_0$: время откликов запросов типа `/index` и `/test`  
# 2. Гипотеза $H_1$: альтернатива
av_index=average_request_time['Response time']['/index']
av_test=average_request_time['Response time']['/test']

print av_index,av_test 

def check_hypothesis (test,check,alpha=0.05):
    test = st.ttest_1samp(test, check)[1]
    if test < alpha:
        print 'Гипотеза не отвергается','\np-value:',test
    else:
        print 'Гипотеза отвергается','\np-value:',test


check_hypothesis(d['/test'],av_index)


check_hypothesis(d['/index'],av_test)


# Видим, что в одном случае гипотеза -- отвеграется, а в другом -- нет. 
# В данном случае это говорит лишь о том, что данных катастрофически мало
