rooms=[
    {'id':1,'name':'Lets Learn Forex'},
    {'id':2,'name':'Free Account Funding'},
    {'id':3,'name':'Traders Gist and Outing'},
]
l=1
j=None
for i in rooms:
    print(i['name'])
    if i['id']==l:
        j=i
con={'j':j}
print(con)


