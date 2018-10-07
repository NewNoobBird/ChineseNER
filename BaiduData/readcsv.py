import pandas as pd
import numpy as np
import codecs

path = 'baidu_news.csv'
data = pd.read_csv(path,)
#print (data.head())

text = data['content']
print (len(text))
print (text[0])
print (list(set(data['date'])))
print (list(set(data['keyword'])))

noun_content = (data['content'].isnull()) | (data['content'].apply(lambda x: str(x).isspace()))
df_null = data[noun_content]
df_not_null = data[~noun_content]

# print (df_null.head())
# print (df_not_null.head())

print (len(df_null))
print (len(df_not_null))

test = df_not_null.head()
test.to_csv('test_news.csv',index=False,encoding = 'utf-8')

df_not_null.to_csv("news.csv",index=False, encoding = 'utf-8')
df_not_null_no_content = df_not_null
#del df_not_null_no_content['content']
df_not_null_no_content=df_not_null.drop(['content'], axis=1)
df_not_null_no_content.to_csv("news_no_content.csv",index=False, encoding='utf-8')
p =df_not_null['content']
p.to_csv("content.txt",index=False, encoding='utf-8')
