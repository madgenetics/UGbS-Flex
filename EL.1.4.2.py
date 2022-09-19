#! /usr/bin/env python3

m=input('Enter comb reads file full name: ')
m1=input('Enter Solo 1 reads file full name: ')
m2=input('Enter Solo 2 reads file full name: ')
m3=int(input('enter the read length standard for Solo 1: '))
m4=int(input('enter the read length standard for Solo 2: '))
n=input('enter output file full name: ')

def trans(x):
    code={'A':'T','T':'A','G':'C','C':'G'}
    r=''
    for i in x[::-1]:
        if i in code.keys():
            r+=code[i]
        else:
            r+=i
    return r

final={}

out=open(n,'w')
f=open(m)
out1=open('dump_'+n,'w')

tag=[]

for line in f:
    if line[0]=='@':
        if len(tag)>1:
            for i in tag:
                if i[0]=='@':
                    out.write(i)
                elif i[0]=='+':
                    out.write(i)
                else:
                    out.write(i.strip('\n').strip()+(m3+m4-len(i.strip('\n').strip()))*"A"+'\n')
        tag=[]
        tag.append(line)
    else:
        tag.append(line)
for i in tag:
    if i[0]=='@':
        out.write(i)
    elif i[0]=='+':
        out.write(i)
    else:
        out.write(i.strip('\n').strip()+(m3+m4-len(i.strip('\n').strip()))*"A"+'\n') 
f.close()

info={}# info[tag]=[[read1,qc],[read2,qc]]
bad={}
tag='tag'
bad['tag']=1
f=open(m1)
temp=[]
for line in f:
    if line[0]=='@':
        if len(temp)>1:
            if len(temp[1].strip('\n').strip()) != m3:
                bad[tag] = 1
            info[tag]=[[temp[1],temp[3]]]
        tag=line.strip('\n').strip()[1:-1]
        temp=[]
        temp.append(line)
    else:
        temp.append(line)
f.close()
if len(temp[1].strip('\n').strip())!=m3:
    bad[tag]=1
info[tag]=[[temp[1],temp[3]]]

f=open(m2)
temp=[]
tag='tag'
for line in f:
    if line[0]=='@':
        if len(temp) > 1:
            if len(temp[1].strip('\n').strip()) != m4:
                bad[tag] = 1
            if tag in info.keys():
                info[tag].append([temp[1], temp[3]])
        tag = line.strip('\n').strip()[1:-1]
        temp=[]
        temp.append(line)
    else:
        temp.append(line)
f.close()
if len(temp[1].strip('\n').strip()) != m4:
    bad[tag] = 1
info[tag].append([temp[1], temp[3]])

for i in info.keys():
    if i not in bad.keys():
        if len(info[i])==2:
            out.write('@'+i+'1\n'+info[i][0][0].strip('\n')+trans(info[i][1][0].strip('\n'))+'\n'+'+\n'+info[i][0][1].strip('\n')+info[i][1][1].strip('\n')[::-1]+'\n')
    else:
        if len(info[i])==2:
            out1.write('@'+i+'1\n'+info[i][0][0].strip('\n')+trans(info[i][1][0].strip('\n'))+'\n'+'+\n'+info[i][0][1].strip('\n')+info[i][1][1].strip('\n')[::-1]+'\n')
out.close()
out1.close()



