import cPickle
import datetime
import time
import shutil
import os
import sys
import pandas as pd
import networkx as nx
import random
from PIL import Image
import SendEmail
from SendEmail import SendEmail
class Node:
    def __init__(self, data,code,details):
        self.left = None
        self.right = None
        self.data = data
        self.code=code
        self.details=details
    def insert(self, data,code,details):
        if self.data:
            if data <= self.data:
                if self.left is None:
                    self.left = Node(data,code,details)
                else:
                    self.left.insert(data,code,details)
            elif data > self.data:
                if self.right is None:
                    self.right = Node(data,code,details)
                else:
                    self.right.insert(data,code,details)
        else:
            self.data = data
            self.code=code
            self.details=details
    def lookup(self, data, parent=None):
        if data < self.data:
            if self.left is None:
                return None, None
            return self.left.lookup(data, self)
        elif data > self.data:
            if self.right is None:
                return None, None
            return self.right.lookup(data, self)
        else:
            return self, parent
    def children_count(self):
        cnt = 0
        if self.left:
            cnt += 1
        if self.right:
            cnt += 1
        return cnt
    def delete(self, data):
        # get node containing data
        node, parent = self.lookup(data)
        if node is not None:
            children_count = node.children_count()
        else:
            print "Node not found?"
            return
        if children_count == 0:
        # if node has no children, just remove it
            if parent:
                if parent.left is node:
                    parent.left = None
                else:
                    parent.right = None
                del node
            else:
                self.data = None
                self.code=None
                self.details=None
        elif children_count == 1:
            # if node has 1 child
            # replace node with its child
            if node.left:
                n = node.left
            else:
                n = node.right
            if parent:
                if parent.left is node:
                    parent.left = n
                else:
                    parent.right = n
                del node
            else:
                self.left = n.left
                self.right = n.right
                self.data = n.data
                self.code=n.code
                self.details=n.details
        else:
            # if node has 2 children
            # find its successor
            parent = node
            successor = node.right
            while successor.left:
                parent = successor
                successor = successor.left
            # replace node data by its successor data
            node.data = successor.data
            node.code=successor.code
            node.details=successor.details
            # fix successor's parent's child
            if parent.left == successor:
                parent.left = successor.right
            else:
                parent.right = successor.right
    def print_tree(self):
        print str(self.data)+" "+str(self.code)+" "+str(self.details.items())+'\n',
        if self.left:
            self.left.print_tree()
     #   print self.data,
        if self.right:
            self.right.print_tree()#bst
def calstrwt(string):
    strsum=0
    for i in string:
        strsum+=ord(i)
    return strsum
def ReturnDaySlots(day):
    Dayslots={'MON':['A1','L1','F1','L2','D1','L3','TB1','L4','TG1','L5','A2','L31','F2','L32','D2','L33','TB2','L34','TG2','L35'],
              'TUE':['B1','L7','G1','L8','E1','L9','TC1','L10','TAA1','L11','B2','L37','G2','L38','E2','L39','TC2','L40','TAA2','L41'],
              'WED':['C1','L13','A1','L14','F1','L15','TD1','L16','TBB1','L17','C2','L43','A2','L44','F2','L45','TD2','L46','TBB2','L47'],
              'THU':['D1','L19','B1','L20','G1','L21','TE1','L22','TCC1','L23','D2','L49','B2','L50','G2','L51','TE2','L52','TCC2','L53'],
              'FRI':['E1','L25','C1','L26','TA1','L27','TF1','L28','TD1','L29','E2','L55','C2','L56','TA2','L57','TF2','L58','TDD2','L59']}
    return Dayslots[day]
def DeleteMember(regno):
    shutil.rmtree("Member Database\\"+regno)
    f=open("Member Database\\Memberlist.txt","r")
    details = [x.strip('\n') for x in f.readlines()]
    f.close()
    for i in range(0,len(details)):
        if regno in details[i]:
            pos=i
    del details[pos]
    f=open("Member Database\\Memberlist.txt","w")
    for i in details:
        f.write(i+'\n')
    f.close()
    print "Successfully Deleted."
    return
def PrintMemberDetails(regno):
    f=open("Member Database\\"+regno+"\Details of "+regno+".txt","r")
    details = [x.strip('\n') for x in f.readlines()]
    f.close()
    for i in details:
        print i
    return
def DisplayFreeMembersSlotwise(slot):
    if os.path.exists("SlotListFreeMembers.dat"):
        os.remove("SlotListFreeMembers.dat")
    memlist=MakeSlotNameList()
    with open("SlotListFreeMembers.dat", "rb") as input:
        lists = cPickle.load(input)
    for i in range(0,len(lists[slot-1])):
        print str(i+1)+':'
        f=open("Member Database\\"+lists[slot-1][i]+"\Details of "+lists[slot-1][i]+".txt","r")
        details = [x.strip('\n') for x in f.readlines()]
        for j in range(0,len(details)):
            print " "+details[j]
        f.close()
    return#uses hash table
def MakeSlotNameList():
     memlist=[]
     fin=open("Member Database\Memberlist.txt","r")
     memlist = [x.strip('\n') for x in fin.readlines()]
     fin.close()
     def AddMembers(memberlist):
        fulllist=[[] for i in range(0,60)]
        for regno in memberlist:
            f=open("Member Database\\"+regno+"\\Free slots of "+str(regno)+".txt",'r')
            content = [x.strip('\n') for x in f.readlines()]
            f.close()
            for i in range(0,len(content)):
                fulllist[int(content[i])-1].append(regno)
        return fulllist
       #     os.remove("Member Database\\"+regno+"\Free slots of "+regno+".txt")
     finallist=AddMembers(memlist)
     with open("SlotListFreeMembers.dat", "wb") as output:
        cPickle.dump(finallist, output, cPickle.HIGHEST_PROTOCOL)
     return memlist#uses hash table
def GetDistance(start, end):#uses djkistra's algorithm
    data = pd.read_table("GraphOfVIT.txt",
                     sep = " ",
                     header = None,
                     names = ['vx', 'vy', 'dist'])
    graph = nx.from_pandas_dataframe(data, 'vx', 'vy', 'dist')
    graph_dict = nx.to_dict_of_dicts(graph)
    distances = {}
    predecessors = {}
    to_assess = graph_dict.keys()
    for node in graph_dict:
        distances[node] = float('inf')
        predecessors[node] = None
    sp_set = []
    distances[start] = 0
    while len(sp_set) < len(to_assess):
        still_in = { node: distances[node] for node in [node for node in to_assess if node not in sp_set] }
        closest = min(still_in, key = distances.get)
        sp_set.append(closest)
        for node in graph_dict[closest]:
            if distances[node] > distances[closest] + graph[closest][node]['dist']:
                distances[node] = distances[closest] + graph[closest][node]['dist']
                predecessors[node] = closest
    path = [end]
    while start not in path:
        path.append(predecessors[path[-1]])
    return distances[end]
def VenueInterpret(venue):
    venuedict={"SJT":1,"TT":2,"SMV":3,"CBMR":4,"MB":5,"GDN":6,"CDMM":7}
    return venuedict[venue]
def TimeInterpret(slot):
    timedict={0:'08-09',1:'08-09',2:'09-10',3:'09-10',4:'10-11',5:'10-11',6:'11-12',7:'11-12',8:'12-13',9:'12-13',10:'14-15',11:'14-15',12:'15-16',13:'15-16',14:'16-17',15:'16-17',16:'17-18',17:'17-18',18:'18-19',19:'18-19'}
    return timedict[slot]
def DeskGen(memlist,DeskVen):
    Day=raw_input("Enter the day for generating desk duty(Mon/Tue/Wed/Thu/Fri):")
    slots=ReturnDaySlots(Day.upper())
    with open("SlotListFreeMembers.dat", "rb") as input:
        lists = cPickle.load(input)
    TimeDict={'08-09':[[],[]],'09-10':[[],[]],'10-11':[[],[]],'11-12':[[],[]],'12-13':[[],[]],'14-15':[[],[]],'15-16':[[],[]],'16-17':[[],[]],'17-18':[[],[]],'18-19':[[],[]]}
    for i in range(0,len(slots)):
        PriorityDict={}
        curtime=TimeInterpret(i)
        for regno in memlist:
            flag=1
            f=open("Member Database\\"+regno+"\Slots of "+regno+".txt","r")
            MemSlots = [x.strip('\n') for x in f.readlines()]
            f.close()
            f=open("Member Database\\"+regno+"\Venues of "+regno+".txt","r")
            MemVenues=[y.strip('\n') for y in f.readlines()]
            f.close()
            TslotDict={}
            LslotDict={}
            for j in range(0,len(MemSlots)):
                if 'L' in MemSlots[j]:
                    LslotDict.update({MemSlots[j]:MemVenues[j]})
                else:
                    TslotDict.update({MemSlots[j]:MemVenues[j]})
            del(MemSlots)
            del(MemVenues)
            if i%2==0:
                eqslot=int(slots[i+1].strip('L'))-1
                if regno in lists[eqslot]:
                    if i>=2 and i!=10 and i!=8  and i<=16:
                        if slots[i-2] in TslotDict.keys():
                            BefVen=VenueInterpret(TslotDict[slots[i-2]])
                        elif slots[i-1] in LslotDict.keys():
                            BefVen=VenueInterpret(LslotDict[slots[i-1]])
                        else:
                            BefVen=VenueInterpret(DeskVen)
                        if slots[i+2] in TslotDict.keys():
                            AftVen=VenueInterpret(TslotDict[slots[i+2]])
                        elif slots[i+3] in LslotDict.keys():
                            AftVen=VenueInterpret(LslotDict[slots[i+3]])
                        else:
                            AftVen=VenueInterpret(DeskVen)
                    elif i==10 or i==0:
                        BefVen=VenueInterpret(DeskVen)
                        if slots[i+2] in TslotDict.keys():
                            AftVen=VenueInterpret(TslotDict[slots[i+2]])
                        elif slots[i+3] in LslotDict.keys():
                            AftVen=VenueInterpret(LslotDict[slots[i+3]])
                        else:
                            AftVen=VenueInterpret(DeskVen)
                    else:
                        AftVen=VenueInterpret(DeskVen)
                        if slots[i-2] in TslotDict.keys():
                            BefVen=VenueInterpret(TslotDict[slots[i-2]])
                        elif slots[i-1] in LslotDict.keys():
                            BefVen=VenueInterpret(LslotDict[slots[i-1]])
                        else:
                            BefVen=VenueInterpret(DeskVen)
                else:
                    continue
            else:
                eqslot=int(slots[i].strip('L'))-1
               # print "eqslot"+str(eqslot)
                if regno in lists[eqslot]:
                    if i>=3 and i!=9 and i!=11 and i<=17:
                        if slots[i-3] in TslotDict.keys():
                            BefVen=VenueInterpret(TslotDict[slots[i-3]])
                        elif slots[i-2] in LslotDict.keys():
                            BefVen=VenueInterpret(LslotDict[slots[i-2]])
                        else:
                            BefVen=VenueInterpret(DeskVen)
                        if slots[i+1] in TslotDict.keys():
                            AftVen=VenueInterpret(TslotDict[slots[i+1]])
                        elif slots[i+2] in LslotDict.keys():
                            AftVen=VenueInterpret(LslotDict[slots[i+2]])
                        else:
                            AftVen=VenueInterpret(DeskVen)
                    elif i==11 or i==1:
                        BefVen=VenueInterpret(DeskVen)
                        if slots[i+1] in TslotDict.keys():
                            AftVen=VenueInterpret(TslotDict[slots[i+1]])
                        elif slots[i+2] in LslotDict.keys():
                            AftVen=VenueInterpret(LslotDict[slots[i+2]])
                        else:
                            AftVen=VenueInterpret(DeskVen)
                    else:
                        AftVen=VenueInterpret(DeskVen)
                        if slots[i-1] in TslotDict.keys():
                            BefVen=VenueInterpret(TslotDict[slots[i-1]])
                        elif slots[i-2] in LslotDict.keys():
                            BefVen=VenueInterpret(LslotDict[slots[i-2]])
                        else:
                            BefVen=VenueInterpret(DeskVen)
                else:
                    continue
            priotemp={regno:GetDistance(BefVen,VenueInterpret(DeskVen))+GetDistance(AftVen,VenueInterpret(DeskVen))}
            if regno not in PriorityDict.keys():
                PriorityDict.update(priotemp)
        for regno in sorted(PriorityDict,key=PriorityDict.__getitem__):
            DistValue=PriorityDict[regno]
            if regno not in TimeDict[curtime][0]:
                TimeDict[curtime][0].append(regno)
                TimeDict[curtime][1].append(DistValue)
    return TimeDict,Day
def GetName(regno):
    with open("Member Database\\"+regno+"\\Details of "+regno+".txt","r") as f:
        name=f.readline().strip('\n')
    return name.upper()       
def DeskScheduler(memlist):
    os.system('cls')
    if not os.path.exists("Desk Duty Records"):
        os.mkdir("Desk Duty Records")
    now=time.strftime("%d-%m-%y  %I-%M %p")
    ven=raw_input("Enter Venue for Desk(SJT/TT/SMV/CBMR/MB/GDN/CDMM):")
    timedict,day=DeskGen(memlist,ven)
    num=int(raw_input("Enter number of members per desk:"))
    print "\nAll the members with their point will be displayed according to the time slot.\nThe lower the point,the more likely he/she will show up for duty.\nA point greater than 30.0 is quite inconvienient"
    deskdict={}
    fulllist=[]
    for i,j in sorted(timedict.items()):
        desklist=[]
        tempregdict={}
        flag=num
        if len(j[0])==0:
            continue
        print "\n\nMembers available for time "+i+" are:"
        print i+":"
        print '\tSno\tName                     REGISTRNO\tPT\tTimes Duty Assigned'
        for k in range(0,len(j[0])):
            tempcount=0
            name=GetName(j[0][k]).upper().ljust(25)
            for m in range(0,len(fulllist)):
                if j[0][k] in fulllist[m]:
                    tempcount+=1
            if tempcount>=1:
                print '\t'+str(k+1)+'\t'+name+j[0][k]+"\t"+str(j[1][k])+"\t"+str(tempcount)
                tempregdict.update({k+1:j[0][k]})
            else:
                print '\t'+str(k+1)+'\t'+name+j[0][k]+"\t"+str(j[1][k])+'\t0'
                tempregdict.update({k+1:j[0][k]})
        print "Assign members for time "+i+":\n"
        while(flag>0):
            count=0
            sno=raw_input("\tEnter the new Sno to assign:")
            regno=tempregdict[int(sno)]
            for l in range(0,len(fulllist)):
                if regno in fulllist[l]:
                    count+=1
            if count==0:
                desklist.append(regno)
                fulllist.append(regno)
                flag-=1
            else:
                resp=raw_input( "\tReminder:\n\t"+regno+" was already assigned duty "+str(count)+" times.Still assign?(Y/N):")
                if resp=='y' or resp=='Y':
                    desklist.append(regno)
                    fulllist.append(regno)
                    flag-=1
                else:
                    continue
        deskdict.update({i:desklist})
    print "\n\n\nDesk Duties Successfully Assigned.\nRefer generated file in Desk Duty Records for details.\n\n\n"
    f=open("Desk Duty Records\\Assigned Desk Duties on ("+str(now)+").txt","w")
    for i in sorted(deskdict.keys()):
        value=deskdict[i]
        f.write(i+'\n')
        for j in value:
            f.write('\t'+j+'\n')
    f.close()
    return
def UpdateDesk(memlist):
    os.system('cls')
    if not os.path.exists("Desk Duty Records"):
        print "No files to update."
        return
    print "The Desk Duty Records will be listed.\n"
    dirlist=os.listdir("Desk Duty Records")
    dirdict={}
    sno=0
    for i in range(0,len(dirlist)):
        if "Updated" not in dirlist[i]:
            sno+=1
            print "\t"+str(sno)+":"+dirlist[i]
            dirdict.update({sno:dirlist[i]})
    path=int(raw_input("Enter the file number to update attendance"))
    fullist=[]
    with open("Desk Duty Records\\"+dirdict[path],"r") as f:
        fullist=[x.strip('\n').strip('\t') for x in f.readlines()]
    listsize=len(fullist)
    size=(listsize/10)
    for i in range(0,len(fullist),size):
        print "During "+fullist[i]+" hours,"
        fullist[i]+='\n'
        for j in range(i+1,size+i):
            status=raw_input("\t"+fullist[j]+" present?(Y/N):")
            if status == 'Y' or status == 'y':
                fullist[j]='\t'+fullist[j]+'\tPresent\n'
            else:
                fullist[j]='\t'+fullist[j]+'\tAbsent\n'
    with open("Desk Duty Records\\"+dirdict[path],"w") as f:
        for i in fullist:
            f.write(i)
    os.rename("Desk Duty Records\\"+dirdict[path],"Desk Duty Records\\"+dirdict[path][:-4]+"-Updated.txt")
    dirdict={}
    print "Attendance Successfully Updated."
    return
def DeskAttendance():
    os.system('cls')
    if not os.path.exists("Desk Duty Records"):
        print "No files to view."
        return
    print "The Desk Duty Records will be listed.\n"
    dirlist=os.listdir("Desk Duty Records")
    dirdict={}
    sno=0
    for i in range(0,len(dirlist)):
        if "Updated" in dirlist[i]:
            sno+=1
            print "\t"+str(sno)+":"+dirlist[i]
            dirdict.update({sno:dirlist[i]})
    path=int(raw_input("Enter the file number to view attendance:"))
    with open("Desk Duty Records\\"+dirdict[path],"r") as f:
        details=[x for x in f.readlines()]
    for i in details:
        print i
    dirdict={}
    return
def ProjectManager():
    os.system('cls')
    while True:
        print "\n1.Add a new Project\n2:Update Project Status\n3:Delete Completed Project\n4.View Projects\n5.Exit Project Manager\n"
        choice=raw_input("Enter Your Choice:")
        now=time.strftime("%c")
        flag=0
        if not os.path.exists("ProjectManager\\ProjectFiles.dat"):
            os.mkdir("ProjectManager")
            flag=0
        else:
            flag=1
        if flag ==1:
            f=open("ProjectManager\\Projectlist.txt","r")
            prjlist=[x.strip('\n') for x in f.readlines()]
            UpdatesValue=len(prjlist)
            f.close()
        if choice is '1':
            if flag is 1:
                Name=raw_input( "Enter the name of the Project:")
                data=calstrwt(Name)
                with open("ProjectManager\\ProjectFiles.dat", "rb") as input:
                    ProjectRecords=cPickle.load(input)
                    UpdatesString=str(now)+"  Start"
                newdict={'Name':Name,'Updates':{'0':UpdatesString}}
                ProjectRecords.insert(data,UpdatesValue,newdict)
                os.remove("ProjectManager\\ProjectFiles.dat")
                with open("ProjectManager\\ProjectFiles.dat", "wb") as output:
                    cPickle.dump(ProjectRecords, output, cPickle.HIGHEST_PROTOCOL)
                with open("ProjectManager\\Projectlist.txt","a") as fin:
                    fin.write(Name+'\n')
            else:
                Name=raw_input( "Enter the name of the Project:")
                data=calstrwt(Name)
                UpdatesString=str(now)+"  Start"
                obj=Node(data,'0',{'Name':Name,'Updates':{'0':UpdatesString}})
                with open("ProjectManager\\ProjectFiles.dat","wb") as output:
                    cPickle.dump(obj,output,cPickle.HIGHEST_PROTOCOL)
                with open("ProjectManager\\Projectlist.txt","w") as fin:
                    fin.write(Name+'\n')
        elif choice is '2':
            if flag is 1:
                prdict={}
                sno=0
                with open("ProjectManager\\ProjectFiles.dat", "rb") as input:
                   ProjectRecords=cPickle.load(input)
                print "The Projects and their respective codes will be displayed:"
                for i in prjlist:
                    sno+=1
                    print str(sno)+':'+i
                    prdict.update({str(sno):i})
                inp=raw_input("Enter the project number you want to update:")
                code=calstrwt(prdict[inp])
                node,parent=ProjectRecords.lookup(int(code))
                if node is None:
                    print "Wrong Input"
                    return
                msg=raw_input("Enter Message For latest update:")
                UpdatesString=str(now)+"  "+msg
                node,parent=ProjectRecords.lookup(int(code))
                node.details['Updates'].update({str(len(node.details['Updates'])):UpdatesString})
                os.remove("ProjectManager\\ProjectFiles.dat")
                with open("ProjectManager\\ProjectFiles.dat", "wb") as output:
                    cPickle.dump(ProjectRecords, output, cPickle.HIGHEST_PROTOCOL)
            else:
                print "No Projects Present"
                continue
        elif choice is '3':
            if flag is 1:
                with open("ProjectManager\\ProjectFiles.dat", "rb") as input:
                    ProjectRecords=cPickle.load(input)
                print "The Projects will be displayed:"
                sno=0
                prjdict={}
                for i in prjlist:
                    sno+=1
                    print str(sno)+':'+i
                    prjdict.update({str(sno):i})   
                num=raw_input("Enter the project number you want to delete:")
                inp=calstrwt(prjdict[num])
                tempflag=0
                ProjectUpdatedList=prjlist
                for i in range(0,len(prjlist)):
                    if inp == calstrwt(prjlist[i]):
                        ProjectRecords.delete(int(inp))
                        tempflag=1
                        os.remove("ProjectManager\\ProjectFiles.dat")
                        with open("ProjectManager\\ProjectFiles.dat", "wb") as output:
                            cPickle.dump(ProjectRecords, output, cPickle.HIGHEST_PROTOCOL)
                        del(ProjectUpdatedList[i])
                        break
                    else:
                        tempflag=0
                with open("ProjectManager\\Projectlist.txt","w") as fin:
                    for j in ProjectUpdatedList:
                        fin.write(str(j)+'\n')
                if tempflag==0:
                    print "Wrong input"
                    continue
                print "Successfully deleted."

            else:
                print "No Projects Present"
                continue
        elif choice is '4':
            with open("ProjectManager\\ProjectFiles.dat", "rb") as input:
                ProjectRecords=cPickle.load(input)
            print "The Projects will be displayed:"
            sno=0
            prjdict={}
            for i in prjlist:
                sno+=1
                print str(sno)+':'+i
                prjdict.update({str(sno):i})
            inp=raw_input("Enter the project number for viewing its details:")
            tcode=calstrwt(prjdict[inp])
            node,parent=ProjectRecords.lookup(int(tcode))
            if node is None:
                print "Wrong input"
                continue
            else:
                newdict=node.details
                print newdict['Name']
                newnewdict=newdict['Updates']
                for j in sorted(newnewdict.keys()):
                    print "\t"+j+"\t"+newnewdict[j]
        else:
            return
def MemberManager(memlist):
    os.system('cls')
    while True:
        ch=raw_input("\n\n1:View All Member Details\n2:View Member Details by Registration Number\n3:View Free Members according to slot\n4:Delete a member\n5:Exit\nEnter Choice:")
        if ch=='1':
            memlist=MakeSlotNameList()
            for i in memlist:
                print "\n"
                PrintMemberDetails(i)
                print "\n"
        elif ch=='2':
            memlist=MakeSlotNameList()
            for i in memlist:
                name=GetName(i).ljust(25)
                print name+" "+i
            regno=raw_input("Enter the registration number:")
            PrintMemberDetails(regno)
            print "\n"
        elif ch=='3':
            f=Image.open("VITTimetable.png")
            f.show()
            slot=raw_input("Enter the slot you want to view the free members for,you can use the image shown as reference(eg if slot is L1,type 1):")
            DisplayFreeMembersSlotwise(int(slot))
        elif ch=='4':
            regno=raw_input("Enter registration number of member to delete:")
            DeleteMember(regno)
        else:
            return
def main():
    memlist=MakeSlotNameList()
    while True:
        os.system('cls')
        print "Menu:"
        ch=raw_input("\n\n1:Member Manager\n2:Desk Duty Scheduler\n3:Project Manager\n4:Exit\n\tEnter Choice:")
        if ch=='1':
            os.system('cls')
            MemberManager(memlist)
        elif ch == '2':
            os.system('cls')
            while True:
                print "\n1.Schedule Desk Duties for a given day\n2.Update given Desk attendance status\n3.View desk attendance status\n4.Exit"
                resp=raw_input("Enter choice:")
                if resp is '1':
                    DeskScheduler(memlist)
                elif resp is '2':
                    UpdateDesk(memlist)
                elif resp is '3':
                    DeskAttendance()
                else:
                    break
        elif ch == '3':
            os.system('cls')
            ProjectManager()
        else:
            return
if __name__ == "__main__":
    main()
