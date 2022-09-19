#!/usr/bin/python3

print('put all files and this script in the same folder')
inputname=input('Enter the SNP file name (Tab delimited file *.txt): ')
outname1=input("Enter the output file name:  ")
n=int(input("Enter the sample start column number (count start from 1, input 11 if applied on the output of ‘SNP_genotyper.py’): "))
outname2='info_'+outname1
f=open(inputname)
out1=open(outname1,'w')
out2=open(outname2,'w')
for line in f:
    headline=line
    break
f.close()
out1.write(headline)
out2.write(headline)
seq={}
judge=[]
fullinfo={}
patch={}
f=open(inputname)
good={}
for line in f:
    if "##" in line:
        continue
    elif "CHROM" not in line:
        x=line.strip('\n').strip('\t').split('\t')
        tag=str(x[0])
        fullinfo[tag]=line
        length=len(x)
        sequence=[]
        penaty=0
        for i in range(n-1,length):
            sequence.append(x[i])
            if x[i] in ['A','B','H']:
                continue
            elif x[i] in ['C','D']:
                penaty+=1
            else:
                penaty+=2
        jugname=str(penaty)+'.'+tag
        judge.append(jugname)
        seq[tag]=sequence
        patchtag=str(penaty)
        if patchtag not in patch.keys():
            patch[patchtag]=[tag]
        else:
            patch[patchtag].append(tag)
    else:
        continue

sort_tag=[]
bad={}

for i in range(1000):
    if str(i) in patch.keys():
        for x in patch[str(i)]:
            sort_tag.append(x)

for i in sort_tag:
    if i not in bad.keys():
        out2.write(fullinfo[i])
        for j in seq.keys() :
            if j not in bad.keys() and i in seq.keys():
                det=1
                if i != j:
                    length=len(seq[i])
                    for x in range(length):
                        if seq[i][x] in ['A','B','H'] and seq[j][x] in ['A','B','H']:
                            if seq[i][x]==seq[j][x]:
                                continue
                            else:
                                det=0
                                break
                        elif seq[i][x] in ['A','B','C','D','H'] and seq[j][x] in ['A','B','C','D','H']:
                            test=[seq[i][x],seq[j][x]]
                            good1=['B','H','C']
                            good2=['A','H','D']
                            if test[0] in good1 and test[1] in good1:
                                continue
                            elif test[0] in good2 and test[1] in good2:
                                continue
                            else:
                                det=0
                                break
                        else:
                            continue
                    if det==1:
                        out2.write(fullinfo[j])
                        bad[j]=1
                    else:
                        continue
                else:
                    continue
            else:
                continue
        out2.write('\n')

count=0
for i in fullinfo.keys():
    if i not in bad.keys():
        out1.write(fullinfo[i])
        count+=1
    else:
        continue
out1.close()
out2.close()

