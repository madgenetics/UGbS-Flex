#!/usr/bin/python3

print('put all files and this script in the same folder')

import os

def geno(x,y):
    if x=='.':
        return '-'
    else:
        i=x.split(',')
        a=int(i[0])+0.01
        b=int(i[1])+0.01
        v=a/b
        if (a+b)<y:
            return '-'
        else:
            if v<0.1 or v==0.1:
                return 'B'
            elif v>10 or v==10:
                return 'A'
            elif v>0.1 and v <0.25:
                return 'C'
            elif v >4  and v<10:
                return 'D'
            else:
                return 'H'

def score(x):
    z=list(set(x))
    if len(z)==1:
        return z[0]
    else:
        if 'A' in z:
            if 'B' in z: return '-'
            elif 'H' in z: return '-'
            elif 'C' in z: return '-'
            else: return 'A'
        elif 'B' in z:
            if 'A' in z: return '-'
            elif 'H' in z: return '-'
            elif 'D' in z: return '-'
            else: return 'B'
        elif 'H' in z:
            if 'A' in z: return '-'
            elif 'B' in z: return '-'
            else: return 'H'
        elif 'C' in z: return 'C'
        elif 'D' in z: return 'D'
        else: return z[0]


m=input('Enter the GATK vcf file name: ')
n=input('Did you apply any GATK filters (AF/QD/..) on your results? If yes, enter ‘y’, else, enter ‘n’ (use lower case only):  ')
q=int(input('Enter the percentage of missing data you want to remove, integer only:  '))
w=int(input('Enter the threshold for H (2/3/4? check instruction for detail): '))
v=int(input('Enter the threshold for sequence depth for robust SNP scoring (e.g. 8), integer only:  '))

f=open(m)
outname='temp_'+m.split('.vcf')[0]+'.txt'
out=open(outname,'w')


##remove headlines and remove bad SNPs

for line in f:
    if '##' not in line:
        if n=='y':
            if 'CHROM' in line or 'PASS' in line:
                out.write(line)
        elif n=='n':
            out.write(line)
        else:
            print('error, did you do filter from GATK? rerun program and enter the answer')
            os._exit()
f.close()
out.close()

##genotype

outname2='temp2_'+m.split('.vcf')[0]+'.txt'
out=open(outname2,'w')

f=open(outname)
for line in f:
    headline=line
    break
out.write(headline)


sample_number=len(headline.strip('\n').strip().strip('\t').split('\t'))-9
miss_judge=sample_number*q/100

for line in f:
    result=''
    temp=[]
    x=line.strip('\n').strip().split('\t')
    for i in range(9):
        result+=x[i]+'\t'
    for i in range(9,len(x)):
        if x[i]=='./.':
            result+='-'+'\t'
            temp.append('-')
        else:
            abh=geno(x[i].split(':')[1],v)
            result+=abh+'\t'
            temp.append(abh)
    result+='\n'
    if temp.count('-')<miss_judge:
        out.write(result)
out.close()
f.close()
os.remove(outname)

## Add Tag
f=open(outname2)
outname3='temp3_'+m.split('.vcf')[0]+'.txt'
out=open(outname3,'w')
start=0
chro_start=''
count=0
for line in f:
    if '#' in line:
        out.write('Tag'+'\t'+line)
    else:
        x=line.split('\t')
        chro=x[0]
        pos=int(x[1])
        if chro==chro_start:
            if abs(pos-start)<501:
                tagname='Tag_'+str(count)
            else:
                count+=1
                start=pos
                tagname='Tag_'+str(count)
        else:
            chro_start=chro
            count+=1
            start=pos
            tagname='Tag_'+str(count)
        out.write(tagname+'\t'+line)
f.close()
out.close()
os.remove(outname2)

f=open(outname3)
outname4='consolidated_H_as_'+str(w)+'_'+m.split('.vcf')[0]+'.txt'
out=open(outname4,'w')

tag=''
group={}
combine={}
seq=[]

for line in f:
    x=line.strip('\n').split('\t')
    tagname=x[0]
    length=len(x)
    if tagname!=tag:
        tag=tagname
        seq.append(tag)
        group[tagname]=[[x[i] for i in range(1,11)],[x[j] for j in range(11,length)]]
    else:
        group[tagname].append([x[j] for j in range(11,length)])


for i in group.keys():
    combine[i]=[group[i][0]]
    sampleNum=len(group[i])
    lociNum=len(group[i][1])
    for j in range(lociNum):
        cup=[]
        for k in range(1,sampleNum):
            cup.append(group[i][k][j])
        geno=score(cup)
        combine[i].append(geno)

for k in seq:
    head=k+'\t'
    for i in range(10):
        head+=combine[k][0][i]+'\t'
    for j in range(1,len(combine[k])):
        head+=combine[k][j]+'\t'
    head+='\n'
    if combine[k].count('-')<miss_judge:
        out.write(head)
out.close()
f.close()
os.remove(outname3)
        

