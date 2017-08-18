with open("Member Database\\Memberlist.txt",'r') as f:
    memlist=[x.strip('\n') for x in f.readlines()]
for regno in memlist:
    with open("Member Database\\"+regno+"\\Venues of "+regno+".txt","r") as fin:
        venues=[x.strip('\n') for x in fin.readlines()]
    for i in range(0,len(venues)):
        if len(venues[i])==4 and venues[i][len(venues[i])-1].isdigit():
            venues[i]=venues[i][0:len(venues[i])-1]
    with open("Member Database\\"+regno+"\\Venues of "+regno+".txt","w") as fout:
        for ven in venues:
            fout.write(ven+'\n')

    
