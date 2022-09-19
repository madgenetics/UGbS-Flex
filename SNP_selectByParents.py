#!/usr/bin/python3
print('Put all files and this script in the same folder')
m=input('Enter SNP file name: ')
zz=input('Enter output file name: ')
n=input('Enter the sample name of parent 1: ')
l=input('Which genotyper you want for parent 1 (input A/B/H): ')
v=input('Enter the sample name of parent 2: ')
s=input('Which genotyper you want for parent 2 (input A/B/H): ')

mix={'A':['A','D'],'B':['B','C'],'H':['C','D','H']}
judge1=mix[l.upper()]
judge2=mix[s.upper()]
f=open(m)
outname=zz
out=open(outname,'w')

for line in f:
    out.write(line)
    x=line.strip('\n').strip().strip('\t').split('\t')
    for i in range(len(x)):
        if x[i]==n:
            loci1=i
        elif x[i]==v:
            loci2=i
    break

for line in f:
    x=line.strip('\n').strip().strip('\t').split('\t')
    if x[loci1] in judge1 and x[loci2] in judge2:
        out.write(line)

f.close()
out.close()
