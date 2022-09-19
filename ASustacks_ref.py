m=input('Enter Ustacks output tags.tsv file name: ')
n=input('Enter output reference fasta file name: ')
p=int(input('Enter the threshold number for reference (for example, if you want the reference tags should at least exist in 4 different samples, enter 4): '))

f=open(m)
out=open(n,'w')
for line in f:
    break


seq=''
temp=[]
count=0
head=m.split('.tags.')[0]
for line in f:
    if 'consensus' in line:
        if len(temp)>=p:
            out.write('>'+head+'_'+str(count)+'\n'+seq+'\n')
        x=line.split('\t')
        count+=1
        seq=x[9]
        temp=[]
    else:
        if 'model' not in line:
            x=line.split('\t')[8].split('_')[0]
            if x not in temp:
                temp.append(x)
if len(temp)>=p:
    out.write('>'+head+'_'+str(count)+'\n'+seq+'\n')
f.close()
out.close()
