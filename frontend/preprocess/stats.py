import csv
import json
import math
import statistics
import dateutil.parser
from datetime import datetime
# Aggregate thingspeak exports to history similar to victron app history
# python3 stats.py | sed 's/^/var feeds=/' > feeds.json

with open('feeds.csv', newline='') as feeds:
    reader = csv.DictReader(feeds)
    vals=[]
    ys=[]
    prevdt=None
    state={'0':0,'3':0,'4':0,'5':0}
    result=[]
    
    for row in reader:
        tz=dateutil.parser.parse(row['created_at'])
        dt=datetime.combine(tz,datetime.min.time())
        
        try:
            vals.append(int(row['field1']))
            state[row['field3']] +=1
            ys.append(int(row['field7']))
        except:
            continue       
        
        if prevdt is None:
            prevdt=dt
        if prevdt!=dt:
            totals=sum(state.values())       
            minV=min(vals)
            maxV=max(vals)
            yieldToday=max(ys);
            div = maxV - minV
            div0= math.floor(div*(state["0"]/totals))+minV
            div3= math.floor(div*(state["3"]/totals))+div0
            div4= math.floor(div*(state["4"]/totals))+div3
            div5= math.floor(div*(state["5"]/totals))+div4
            result.append({"dt":prevdt.timestamp()*1000,
                           "minV":minV,
                            "maxV":maxV,
                            "medianV":statistics.median(vals),
                           "div0":div0,
                           "div3":div3,
                           "div4":div4,
                           "div5":div5,
                           "yieldToday":yieldToday})   
            vals.clear()
            ys.clear()
            state={'0':0,'3':0,'4':0,'5':0}
    
            prevdt=dt
print (json.dumps(result))
