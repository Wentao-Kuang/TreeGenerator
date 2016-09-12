# -*- coding: utf-8 -*-
"""
Created on Tue Sep 01 00:03:39 2015

Comp409 assignment2 part1 tree generator

@author: Wentao Kuang
studentId:300314565

based on the L system 
ref:http://www.bioquest.org/products/files/13157_Real-time%203D%20Plant%20Structure%20Modeling%20by%20L-System.pdf
"""
import sys
import maya.cmds as cmds
import maya.OpenMayaMPx as OpenMayaMPx
import random




kPluginCmdName = "treeG"


class Tree_Generator(OpenMayaMPx.MPxCommand):
    
    '''Initialize.'''  
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)        
        #self.createWindow()
        
    '''After loaded the pulgin and excute command of this pulgin will excute this function'''    
    def doIt(self,argList):
        self.createWindow()
        
    # I like to keep all the iportant UI elements in a dictionary.
    UIElements = {}    
    
    '''This function creates the window.''' 
    def createWindow(self):       
        self.UIElements['window'] = cmds.window()
        self.UIElements['main_layout'] = cmds.columnLayout( adjustableColumn=True )
        self.UIElements['instruction'] =cmds.button(label=('Rules Instruction'),command=self.instructionListener)        
        self.UIElements['preset1'] =cmds.button(label=('Preset Rule'),w=10,command=self.preset)
        self.UIElements['writeRule'] =cmds.button(label=('Write Random Rule'),w=50,command=self.writeRuleListener)
        self.UIElements['flowerThickness'] =cmds.intSliderGrp("flowerThickness",l="Flower Thickness:", v=1,min=0,max=10,f=True)
        self.UIElements['leafThickness'] =cmds.intSliderGrp("leafThickness",l="Leaf Thickness:", v=1,min=0,max=10,f=True)
        self.UIElements['size'] =cmds.intSliderGrp("size",l="Branch Number:", v=500,min=200,max=2000,f=True)        
        self.UIElements['rule'] = cmds.textField("rule")
        self.UIElements['angle'] = cmds.floatSliderGrp( "angle", l="Angle: ", v=25, min=0, max=100, f=True)
        self.UIElements['length'] = cmds.floatSliderGrp( "length", l="branch Length: ", v=1.5, min=0, max=10, f=True)
        self.UIElements['radius'] = cmds.floatSliderGrp( "radius", l="branch Radius: ", v=0.05, min=0, max=0.3, f=True)
        self.UIElements['cylSubdivs'] = cmds.floatSliderGrp( "subDivs", l="branch roundness: ", v=15, min=4, max=30, f=True)
        self.UIElements['length_atenuation'] = cmds.floatSliderGrp( "length_atenuation", l="Length Atenuation: ", v=75, min=0, max=100, f=True)
        self.UIElements['radius_atenuation'] = cmds.floatSliderGrp( "radius_atenuation", l="Radius Atenuation: ", v=75, min=0, max=100, f=True)  
        self.UIElements['CreateTree'] =cmds.button(label=('CreateTree'),command=self.treeGeneratorListener)
        cmds.showWindow( self.UIElements['window'] )

    '''
    This function listen the button writerule
    '''    
    def writeRuleListener(self,*args):
        size=cmds.intSliderGrp("size",q=True,v=True)
        flowerThickness=cmds.intSliderGrp("flowerThickness",q=True,v=True)
        leafThickness=cmds.intSliderGrp("leafThickness",q=True,v=True)
        rule=self.writeRule(size,flowerThickness,leafThickness)
        cmds.textField("rule", edit=True,tx=rule)
    '''
    This function listen the button preset
    '''
    def preset(self,*args):
        rule="B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F][&+B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F]]B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F][->B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F]L][&B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F]F][&+B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F][&+B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F]]B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F][->B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F]L][&B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F]F]]B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F][&+B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F]]B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F][->B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F]L][&B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F]F][->B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F][&+B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F]]B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F][->B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F]L][&B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F]F]L][&B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F][&+B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F]]B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F][->B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F]L][&B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F]F]F]"
        cmds.textField("rule", edit=True,tx=rule)
    '''
    This function listen the button instruction
    '''
    def instructionListener(self,*args):
        self.UIElements['instructionWindow'] = cmds.window()
        self.UIElements['main_layout'] = cmds.columnLayout(adjustableColumn=True )
        cmds.text( l="""        
        B    Move forward(new Branch)
        L    Leaf
        F    Flower
        +    Rotate +X (yaw right)
        -    Rotate -X (yaw left)
        ^    Rotate +Y (roll right)
        &    Rotate -Y (roll left)
        <    Rotate +Z (pitch down)
        >    Rotate -Z (pitch up)
        [    Push current state on the stack
        ]    Pop the current state from the stack(sub branch)""" )
        cmds.showWindow( self.UIElements['instructionWindow'] )
    
    '''
    This function listen the create tree
    '''   
    def treeGeneratorListener(self ,*args):
        rule=cmds.textField("rule", q=True,tx=True)
        angle=cmds.floatSliderGrp("angle",q=True,v=True)
        length=cmds.floatSliderGrp("length",q=True,v=True)
        radius=cmds.floatSliderGrp("radius",q=True,v=True)
        subDivs=cmds.floatSliderGrp("subDivs",q=True,v=True)
        length_atenuation=cmds.floatSliderGrp("length_atenuation",q=True,v=True)
        radius_atenuation=cmds.floatSliderGrp("radius_atenuation",q=True,v=True)
        #if the rule is too short or didn't create rule first, the system will use the preset rule
        if(len(rule)<=10):
            rule="B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F][&+B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F]]B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F][->B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F]L][&B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F]F][&+B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F][&+B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F]]B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F][->B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F]L][&B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F]F]]B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F][&+B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F]]B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F][->B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F]L][&B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F]F][->B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F][&+B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F]]B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F][->B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F]L][&B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F]F]L][&B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F][&+B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F]]B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F][->B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F]L][&B[&+B]B[->BL][&BF][&+B[&+B]B[->BL][&BF]]B[&+B]B[->BL][&BF][->B[&+B]B[->BL][&BF]L][&B[&+B]B[->BL][&BF]F]F]F]"
            print("rule too shot, system rule the rule automatically")
            cmds.textField("rule", edit=True,tx=rule)
        self.createTree(rule,angle,length,radius,subDivs,length_atenuation,radius_atenuation,)
   
    '''
    This function to generate random rule for the tree shape based on size, flower and leaf thickness
    Symbals from rule map to tree:
        B    Move forward(new Branch)
        L    Leaf
        F    Flower
        +    Rotate +X (yaw right)
        -    Rotate -X (yaw left)
        ^    Rotate +Y (roll right)
        &    Rotate -Y (roll left)
        <    Rotate +Z (pitch down)
        >    Rotate -Z (pitch up)
        [    Push current state on the stack
        ]    Pop the current state from the stack(sub branch)
    '''
    def writeRule(self,size,flowerThickness,leafThickness):
        #rule will start with 'BB' to stand for the tree trunk
        rule="BB"                
        combineSubRule=""
        sizeCounter=0
        while(True):                                  
            while(True):
                #50% to create a subbranch generate from the first branch in the combineSubRule
                if(random.randrange(0,2)==0 and len(combineSubRule)>0):
                    rule=rule+"["+combineSubRule+"]"
                    combineSubRule="" 
                #give a branch fisrt
                subRule="B"
                size-=1
                sizeCounter+=1
                #add flower according the flowerThickness
                if(flowerThickness!=0):
                    ranflower=random.randrange(-1,int(flowerThickness))
                    for i in range(-1,ranflower):
                        subRule+="F"
                #add leaf according the leafThickness
                if(leafThickness!=0):
                    ranLeaf=random.randrange(-1,int(leafThickness))
                    for i in range(-1,ranLeaf):
                        subRule+="L"
                #add random rotation for this branch 
                ran1=random.randrange(0,6)
                if(ran1==0):
                    subRule="+"+subRule
                elif(ran1==1):
                    subRule="-"+subRule
                elif(ran1==2):
                    subRule="^"+subRule
                elif(ran1==3):
                    subRule="&"+subRule
                elif(ran1==4):
                    subRule="<"+subRule
                elif(ran1==5):
                    subRule=">"+subRule 
                #add to combine rule or add to rule
                if(random.randrange(0,20)==0):
                    if(random.randrange(0,5)==0):
                        rule+=subRule
                    else:
                        rule+="["+subRule+"]"
                else:
                    if(random.randrange(0,5)==0):
                        subRule+=subRule
                    else:                       
                        subRule="["+subRule+"]"
                    combineSubRule=combineSubRule+subRule
                    size-=sizeCounter
                    sizeCounter=0
                    break
            if(size<=0):
                break
        return rule
                        
    #Counters
    treeCounter=0
    branchindex=0#for recording the sub level of the branch
    branchCounter=0
    leafCounter=0
    flowerCounter=0
    '''
    This function to create a tree
    '''
    def createTree(self,rule,angle,length,radius,subDivs,length_atenuation,radius_atenuation):
        treeName="tree"+str(self.treeCounter)        
        cmds.group(em=True,name=str(treeName))
        position=[0,0,0] #position x,y,z
        rotation=[0,0,0] #rotation x,y,z
        branchindex=self.branchindex
        branchCounter=self.branchCounter
        leafCounter=self.leafCounter
        flowerCounter=self.flowerCounter
        storePos={}
        storeRot={}
        for i in range(0,len(rule)):
            if(rule[i]=='+'):
                print('+')
                rotation[0]+=angle
            elif(rule[i]=='-'):
                print('-')
                rotation[0]-=angle
            elif(rule[i]=='<'):
                print('<')
                rotation[1]+=angle
            elif(rule[i]=='>'):
                print('>')
                rotation[1]-=angle
            elif(rule[i]=='&'):
                print('&')
                rotation[2]+=angle
            elif(rule[i]=='^'):
                print('^')
                rotation[2]-=angle
            elif(rule[i]=='F'):# copy the flower and put it to the right place 
                print('F')
                flowerName="flower_"+str(self.treeCounter)+"_"+str(branchCounter)+"_"+str(flowerCounter)
                try:
                    cmds.duplicate("flower")
                    cmds.rename("flower1",flowerName)
                    cmds.select(flowerName)
                    cmds.move( position[0],position[1],position[2])
                    ROT=random.randint(0,720)
                    cmds.rotate(ROT%50,ROT,ROT%30)
                    cmds.parent(flowerName, treeName)
                    cmds.scale(radius*(radius_atenuation+length_atenuation)/200,radius*(radius_atenuation+length_atenuation)/200,radius*(radius_atenuation+length_atenuation)/200)
                    for i in range(0,branchindex+1):#decrease the size of flower for upper branches
                        cmds.scale(0.95,0.95,0.95,r=True)
                    flowerCounter+=1
                except:
                    self.warning()
            elif(rule[i]=='L'):# copy the leaf and put it to the right place
                print('L')
                leafName="leaf_"+str(self.treeCounter)+"_"+str(branchCounter)+"_"+str(leafCounter)
                try:                
                    cmds.duplicate("leaf")
                    cmds.rename("leaf1",leafName)
                    cmds.select(leafName)
                    cmds.move(position[0],position[1],position[2])
                    ROT=random.randint(0,720)
                    cmds.rotate(ROT%50,ROT,ROT%30)
                    cmds.parent(leafName,treeName)
                    cmds.scale(radius*(radius_atenuation+length_atenuation)/400,radius*(radius_atenuation+length_atenuation)/400,radius*(radius_atenuation+length_atenuation)/400)
                    for i in range(0,branchindex+1):#decrease the size of leaf for upper branches
                        cmds.scale(0.85,0.85,0.85,r=True)
                    leafCounter+=1
                except:
                    self.warning()
            elif(rule[i]=='['): #save the location for the future subbranch
                print('[')
                pos=[0,0,0]
                rot=[0,0,0]
                pos[0]=position[0]
                pos[1]=position[1]
                pos[2]=position[2]
                rot[0]=rotation[0]
                rot[1]=rotation[1]
                rot[2]=rotation[2]
                storePos[str(branchindex)]=pos
                storeRot[str(branchindex)]=rot
                branchindex+=1
            elif(rule[i]==']'): #call the location to generate a subbranch
                print(']')
                branchindex-=1
                position[0]=(storePos[str(branchindex)])[0]
                position[1]=(storePos[str(branchindex)])[1]
                position[2]=(storePos[str(branchindex)])[2]
                rotation[0]=(storeRot[str(branchindex)])[0]
                rotation[1]=(storeRot[str(branchindex)])[1]
                rotation[2]=(storeRot[str(branchindex)])[2]
            else:#generate the branch and save the latest position
                print('B')
                lastPosition,branchName=self.createBranch(angle,length,radius,position,rotation,subDivs,length_atenuation,radius_atenuation,branchindex,branchCounter)
                # save the latest position of the latest vertices
                position[0]=cmds.xform(branchName+".vtx["+str(lastPosition)+"]",q=True, ws=True, t=True)[0]
                position[1]=cmds.xform(branchName+".vtx["+str(lastPosition)+"]",q=True, ws=True, t=True)[1]
                position[2]=cmds.xform(branchName+".vtx["+str(lastPosition)+"]",q=True, ws=True, t=True)[2]
                branchCounter+=1
        self.branchindex=branchindex
        self.branchCounter=branchCounter
        self.leafCounter=leafCounter
        self.flowerCounter=flowerCounter
            
            
    '''
    function to create branch
    return the last vertices and branchName for call the last position
    '''        
    def createBranch(self,angle,length,radius,position,rotation,subDivs,length_atenuation,radius_atenuation,branchindex,branchCounter):
        branchName="branch_"+str(self.treeCounter)+"_"+str(branchCounter)
        cmds.polyCylinder(n=str(branchName),r=radius,h=length,sx=subDivs,sy=1,sz=1,ax=[0,1,0])
        cmds.xform(piv=[0,-length/2,0],r=True,os=True)
        for i in range(0,branchindex+1):
            cmds.xform( scale=[radius_atenuation/100,1,radius_atenuation/100],r=True)
            cmds.xform( scale=[1,length_atenuation/100,1],r=True)
        cmds.move(0,length/2,0)
        cmds.makeIdentity( apply=True,t=1,r=1,s=1,n=0 )
        cmds.move(position[0],position[1],position[2])
        cmds.xform(ro=[rotation[0],rotation[1],rotation[2]], os=True)
        cmds.parent(branchName,"tree"+str(self.treeCounter))
        return cmds.polyEvaluate(v=True),branchName
     
    def warning(self):
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("Did't open the flower&leaf sence, so no flower or leaf generated, please open it and try again!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")      
# End of class

'''Creator'''
def cmdCreator():
    return OpenMayaMPx.asMPxPtr( Tree_Generator() )
    
'''Initialize the script plug-in'''
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerCommand( kPluginCmdName, cmdCreator )
    except:
        sys.stderr.write( "Failed to register command: %s\n" % kPluginCmdName )
        raise

'''Uninitialize the script plug-in'''
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand( kPluginCmdName )
    except:
        sys.stderr.write( "Failed to unregister command: %s\n" % kPluginCmdName )

demo = Tree_Generator()
demo.createWindow()