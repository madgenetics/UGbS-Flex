m=input('Enter the Ustacks output tags.tsv file: ')
n=input('Enter the output fastq filename: ')
count=0
f=open(m)
out=open(n,'w')
for line in f:
    if 'consensus' in line:
        count+=1
        x=line.split('\t')
        out.write('@'+m.split('.tags.')[0]+"_"+str(count)+'\n')
        out.write(x[9]+'\n+\n'+len(x[9])*'E'+'\n')
f.close()
out.close()
