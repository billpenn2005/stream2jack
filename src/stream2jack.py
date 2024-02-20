import json
import sys
import numpy as np

file_name=str('')
try:
    file_name=sys.argv[1]
except IndexError:
    print('no file inputed')
    exit(0)
with open(file_name, 'r') as file:
    data = json.load(file)
leng=0;
for i in data['note']:
    d=i['beat'][0]
    leng=max(leng,i['beat'][0])
    if(d==0):
        continue
    if(not 'column' in i):
        continue
    a=i['beat'][1]
    b=i['beat'][2]
    c=a/b
    if(a==b-1 and b>4):
        i['beat'][0]+=1
        i['beat'][1]=0
        i['beat'][2]=2
        continue
    if((b-(2*a))<=b/32):
        i['beat'][1]=1
        i['beat'][2]=2
    elif(c<0.5):
        i['beat'][1]=0
        i['beat'][2]=2
    else:
        i['beat'][1]=1
        i['beat'][2]=2
rec_map=np.zeros((leng+10,10,10),dtype=int)
del_map=[-1]
cntr=-1
lncnt=0
for i in data['note']:
    cntr+=1
    if(i['beat'][0]==0):
        continue
    if(not 'column' in i):
        continue
    if('endbeat' in i):
        del data['note'][cntr]['endbeat']
        lncnt+=1
    chk=rec_map[i['beat'][0]][i['beat'][1]][i['column']]
    if(chk==1):
        #print('checked a error')
        if(i['beat'][1]==0):
            if(rec_map[i['beat'][0]][1][i['column']]==0):
                rec_map[i['beat'][0]][1][i['column']]=1
                data['note'][cntr]['beat'][1]=1
                #print(rec_map[i['beat'][0]][1][i['column']])
            else:
                #print('to be removed')
                del_map.append(cntr)
        else:
            if(rec_map[(i['beat'][0])+1][0][i['column']]==0):
                rec_map[(i['beat'][0])+1][0][i['column']]=1
                #print(rec_map[(i['beat'][0])+1][0][i['column']])
                data['note'][cntr]['beat'][0]+=1
                data['note'][cntr]['beat'][1]=0
            else:
                #print('to be removed')
                del_map.append(cntr)
    else:
        rec_map[i['beat'][0]][i['beat'][1]][i['column']]=1
del_num=len(del_map)-1
del_str=' note'
if(del_num>1):
    del_str+='s'
print("Removed "+str(del_num)+del_str)
for i in del_map:
    if(i==-1):
        continue
    del data['note'][i]
data['meta']['version']+=' program generated jack'
#print(data)
json_data=json.dumps(data)
file_name_head=file_name.split('.')[0]
new_file_name=file_name_head+'_program_generated_jack.mc'
with open(new_file_name, "w") as file:
    file.write(json_data)