m=input('Enter the reference fasta file: ')
n=input('Enter the refernece blast file: ')

info={}
f=open(m)
tag='tag'
seq=''
for line in f:
    if '>' in line:
        tag=line.strip('\n')[1:]
    else:
        info[tag]=line
f.close()

bad={}
temp_good={}
f=open(n)
for line in f:
    x=line.split('\t')
    if x[0] not in bad.keys():
        if x[0]==x[1]:
            temp_good[x[0]]=1
        else:
            if float(x[2])>=98.00:
                bad[x[1]]=1
f.close()
out=open('r98_'+m,'w')
for j in temp_good.keys():
    out.write('>'+j+'\n'+info[j])
out.close()
