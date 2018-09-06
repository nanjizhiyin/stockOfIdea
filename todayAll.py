import tushare as ts

df = ts.get_today_all()
for row in df.iterrows():
    print(row['name'])