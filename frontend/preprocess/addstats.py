import subprocess as cmd
import requests
import json
import math
import statistics
import dateutil.parser
from datetime import datetime

## stats aggregator
## intended to be run on a daily basis in order to avoid full exports from thinsgspeak
## Todo error retry limit, overall errorhandling
## calculate how much data we need to get from thingsspeak
## improve file handling survive missing files

def getDate():
    date=datetime.combine(datetime.now(),datetime.min.time())
    return math.floor(datetime.timestamp(date))

def getLastRunDate(dt):
    try:
        with open('last_run.json') as json_file:
            data = json.load(json_file)
            if dt > int(data['lastRun']):
                return True
            else:
                return False
    except FileNotFoundError:
        return True


def git_push_hist():
    try: 
        cmd.run('git add ./hist.json', check=True, shell=True) 
        cmd.run('git commit -m "refresh hist"', check=True, shell=True)
        cmd.run("git push -u origin master -f", check=True, shell=True)
        print("hist refreshed")
        return True
    except:
        print("computer says no")
        return False

def loadHist(fileName):
    print("processing hist")
    result=[]
    lastFulldt=0
    with open(fileName) as json_file:
        data = json.load(json_file)
        lastFulldt = data[-2]['dt']

        for p in data:
            if  p['dt'] > lastFulldt:
                continue
            print('h',p['dt'])
            result.append({"dt":p['dt'],"minV":p['minV'],"maxV":p['maxV'],
                           "medianV":p['medianV'],"div0":p['div0'],"div3":p['div3'],
                           "div4":p['div4'],"div5":p['div5'],"yieldToday":p['yieldToday']})
        json_file.close()
    return result

#appends newer history..
def refresh():
    result = loadHist('hist.json')
    lastFulldt = result[-1]['dt']
    print("adding new data")
    r = requests.get('https://api.thingspeak.com/channels/1095413/feeds.json?results=8000')
    res=r.json().get('feeds')
    vals=[]
    ys=[]
    prevdt=None
    state={'0':0,'3':0,'4':0,'5':0}
    for row in res:
        created_at = row.get('created_at')
        field1 = row.get('field1')
        field3 = row.get('field3')
        field7 = row.get('field7')
        tz=dateutil.parser.parse(created_at)
        dt=datetime.combine(tz,datetime.min.time())
       
        try:
            vals.append(int(field1))
            state[field3] +=1
            ys.append(int(field7))
        except:
            continue       
        
        if prevdt is None:
            prevdt=dt
        if prevdt!=dt:
            totals=sum(state.values())       
            minV=min(vals)
            maxV=max(vals)
            yieldToday=max(ys)
            div = maxV - minV
            div0= math.floor(div*(state["0"]/totals))+minV
            div3= math.floor(div*(state["3"]/totals))+div0
            div4= math.floor(div*(state["4"]/totals))+div3
            div5= math.floor(div*(state["5"]/totals))+div4
            mydt = math.floor(prevdt.timestamp()*1000)
            if lastFulldt < mydt:
                print("adding rec dt:",mydt)        
                result.append({"dt":mydt,
                                "minV":minV,"maxV":maxV,"medianV":statistics.median(vals),
                                "div0":div0,"div3":div3,"div4":div4,
                                "div5":div5,"yieldToday":yieldToday})   
            vals.clear()
            ys.clear()
            state={'0':0,'3':0,'4':0,'5':0}
            prevdt=dt

    truncedHist = result[-70:]
    print("saving hist")
    with open('hist.json', 'w') as outfile:       
        json.dump(truncedHist, outfile)
    outfile.close()    

### main 
ts=getDate()
if getLastRunDate(ts):
    try:
        refresh()
        git_push_hist()
        ## use returncode from git to tell whether lastru was succesfull
        with open('last_run.json', 'w') as outfile:       
            json.dump({"lastRun":ts}, outfile)
        print("hist successfully updated")    
    except:
        print("something bad appened")
else:
    print("data is still fresh - no need to do anything")        
