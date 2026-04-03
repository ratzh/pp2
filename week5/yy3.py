from datetime import datetime , date , date, time, timedelta
d=input()
q=input()
s=datetime.strptime(d,"%Y-%m-%d %H:%M")
t=datetime.strptime(q,"%Y-%m-%d %H:%M")
diff=t-s
new=diff.total_seconds()/60
print(int(new))