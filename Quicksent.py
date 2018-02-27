#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 18:09:31 2018

@author: sayambhu
"""

import pickle
import random

def get_nth_key(dictionary,n=0):
    if n<0:
        n+=len(dictionary)
    for i,key in enumerate(dictionary.keys()):
        if i==n:
            return key
    raise IndexError("Dictionary index out of range")
def Allpo(bi,dictionary):
    c=[]
    if (bi[0]=='<UNK>' or bi[1]=='<UNK>' or not(bi[1].isalpha())):
        return 'bad'
    for x in dictionary:
        if ((x[0],x[1])==bi):
            #print(bi)
            c.append(x)
    if (len(c)<=1):
        c='bad'
        #print(c,'288')
    return c
def FirstWord(Bipr):
    c=[]
    for x in Bipr:
        if (x[0]=='<s>'):
            c.append(x)
    FirstWord=[]
    n=len(c)
    while(True):
        i=random.randint(0,n-1)
        a=random.uniform(0,1)
        if Bipr[c[i]]>a:
            FirstWord=c[i]
            break
            #print()
    
    Sent=[FirstWord[0],FirstWord[1]]
    return Sent
def LastWord(wordsl,wordl,Tripr):
    c1=[]
    fwordsc1=[]
    c2=[]
    lwordsc2=[]
    
    for x in Tripr:
        if(x[2]=='</s>') and (x[0].isalpha()) and (x[0] not in ['of','to','from']):
            c1.append(x)
            fwordsc1.append(x[0])
        if (x[0]==wordsl) and (x[1]==wordl) and x[2] not in ['<UNK>'] and x[2].isalpha():
            c2.append(x)
            lwordsc2.append(x[2])
    if len(c2)<=1:
        #print('bad','321')
        return 'bad'
    
    mid=[]
    for x in Tripr:
        if (x[0] in lwordsc2) and (x[2] in fwordsc1):
            mid.append(x)
    ma=0
    ac=[]
    k1=len(c2)
    k2=len(mid)
    k3=len(c1)
    #print(k1,k2,k3)
    iter=0
    for x in c2:
        for y in mid:
            for z in c1:
                iter+=1
                if iter>21808195:
                    break
                if (x[2]==y[0]) and (y[2]==z[0]):
                    a=random.uniform(0,1)
                    p=Tripr[x]*Tripr[y]*Tripr[z]
                    if a<p and k2<10000:
                        ma=Tripr[x]*Tripr[y]*Tripr[z]
                        ac=[y[0],y[1],y[2],z[1],z[2]]
                        break
                    else:
                        if k1*k2*k3>=2180819520 or k2>10000:
                            ma=Tripr[x]*Tripr[y]*Tripr[z]
                            ac=[y[0],y[1],y[2],z[1],z[2]]
                            break
# =============================================================================
#                     if (Tripr[x]*Tripr[y]*Tripr[z])>ma:
#                         ma=Tripr[x]*Tripr[y]*Tripr[z]
#                         ac=[y[0],y[1],y[2],z[1],z[2]]
# =============================================================================
    if ma==0:
        #print('bad','349')
        return 'bad'
    else:
        return ac
    
            
    
            
        
            
    
    
            
    
def generate_sentence(Bipr,Tripr):
# =============================================================================
#     start='<s>'
#     c=[]
#     for x in Bipr:
#         if (x[0]=='<s>'):
#             c.append(x)
#     FirstWord=[]
#     n=len(c)
#     while(True):
#         i=random.randint(0,n-1)
#         a=random.uniform(0,1)
#         if Bipr[c[i]]>a:
#             FirstWord=c[i]
#             break
#             #print()
#     k=len(Tripr)
#     Sent=[FirstWord[0],FirstWord[1]]
# =============================================================================
    Sent=FirstWord(Bipr)
    #End=LastWord(Bipr)
    i=1
    l=[]
    #tricheck=Allpo((Sent[i-1],Sent[i]),Tripr)
    #k=len(Tripr)
    while(i<=12):
        j=10
        #print(i)
        tricheck=Allpo((Sent[i-1],Sent[i]),Tripr)
        if tricheck=='bad':
            #print('bad','315')
            i=1
            j=-1
            Sent=FirstWord(Bipr)
        while(j>0):
            
            k=random.randint(0,(len(tricheck)-1))
            a=random.uniform(0,1)
            if Tripr[tricheck[k]]>a:
                c=tricheck[k]
                Sent.append(c[2])
                #print(c[2])
                j=-1
                i+=1
            if i==12:
                l=LastWord(Sent[i-1],Sent[i],Tripr)
                if l=='bad':
                    #print('bad','400')
                    i=1
                    j=-1
                    Sent=FirstWord(Bipr)
                else:
                    Sent.extend(l)
                    j=-1
                    i=13
                    break
                
                
    #End=LastWord(Sent[i-2],Sent[i-1],Bipr)
    
    return Sent

def main():
    fBi1=open("Bipr1.pickle","rb")
    Bipr1=pickle.load(fBi1)
    fBi1.close()
# =============================================================================
#     fBi2=open("Bipr2.pickle","rb")
#     Bipr2=pickle.load(fBi2)
#     fBi2.close()
#     fBi3=open("Bipr3.pickle","rb")
#     Bipr3=pickle.load(fBi3)
#     fBi3.close()
#     fBi4=open("Bipr4.pickle","rb")
#     Bipr4=pickle.load(fBi4)
#     fBi4.close()
#     fBiall=open("Biprall.pickle","rb")
#     Biprall=pickle.load(fBiall)
#     fBiall.close()
# =============================================================================
    ftri1=open("Tripr1.pickle","rb")
    Tripr1=pickle.load(ftri1)
    ftri1.close()
# =============================================================================
#     ftri2=open("Tripr2.pickle","rb")
#     Tripr2=pickle.load(ftri2)
#     ftri2.close()
#     ftri3=open("Tripr3.pickle","rb")
#     Tripr3=pickle.load(ftri3)
#     ftri3.close()
#     ftri4=open("Tripr4.pickle","rb")
#     Tripr4=pickle.load(ftri4)
#     ftri4.close()
#     ftriall=open("Triprall.pickle","rb")
#     Triprall=pickle.load(ftriall)
#     ftriall.close()
# =============================================================================
    
    print('With Gutenberg only',generate_sentence(Bipr1,Tripr1))
    
    

if __name__ =='__main__':
    main()    
    



