#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 09:51:31 2018

@author: sayambhu
"""

from nltk.corpus import gutenberg
from nltk.corpus import brown
import random
import collections
from nltk import ngrams
import numpy as np
from sklearn.model_selection import train_test_split


#Vocab1=gutenberg.words()
Sen1=gutenberg.sents()
#Vocab2=brown.words()
Sen2=brown.sents()

def trate8020(sentences):
    sentences=list(sentences)
    for words in sentences:
        words.insert(0,'<s>')
        words.append('</s>')
# =============================================================================
#     n=len(sentences)
#     t=int((4/5)*n)
# =============================================================================
    [train,test]=train_test_split(sentences,shuffle=True,train_size=0.8)
    
    
    
    return [test,train]

def trigramcount(sentences):
    uni1=collections.Counter()
    
    
    for words in sentences:
        for j in words:
            uni1[j]+=1
    
    Count1words=[w for w in uni1.keys() if uni1[w]==1]
    np.random.shuffle(Count1words)
    Count1words=Count1words[:int(len(Count1words)/4)]
    AllWords=[]
    Countuni=collections.Counter()
    for words in sentences:
        for j in words:
            if j not in Count1words:
                AllWords.append(j)
                Countuni[j]+=1
            else:
                AllWords.append('<UNK>')
                Countuni['<UNK>']+=1
    
    Countbi=ngrams(AllWords,2)
    Countri=ngrams(AllWords,3)
    Countbi=collections.Counter(Countbi)
    Countri=collections.Counter(Countri)
    ignore=[('</s>','<s>')]
    
    for a in ignore:
        if a in Countbi:
            #print(Countbi[a])
            del Countbi[a]
    
    fi='</s>'
    en='<s>'
    
    for x in Countuni:
        if ((x,fi,en) in Countri):
            del Countri[(x,fi,en)]
        if ((fi,en,x) in Countri):
            del Countri[(fi,en,x)]
        
    
    
    return [Countbi,Countuni,Countri]
    
def ContiProb(uni,bi):
    Contunipre=collections.Counter()
    Contunifol=collections.Counter()
    for pair in bi.keys():
        Ist=pair[0]
        Tnd=pair[1]
        Contunipre[Tnd]+=1
        Contunifol[Ist]+=1
    d=0.75#Hyperparameter
    Lambda=collections.Counter()
    rej='</s>'
    for x in uni:
        #if x not in rej:
        Lambda[x]=(d*Contunifol[x])/uni[x]
    TotUnipreCount=sum(Contunipre.values())
    return [d,Lambda,TotUnipreCount,Contunipre]

def testunibi(sentences,Countunitrain):
    words=[]
    for x in sentences:
        for y in x:
            if y not in Countunitrain.keys():
                words.append('<UNK>')
            else:
                words.append(y)
    uni=collections.Counter(words)
    bi=ngrams(words,2)
    tri=ngrams(words,3)
    bi=collections.Counter(bi)
    ignore=[('</s>','<s>')]
    
    for a in ignore:
        if a in bi:
            #print(bi[a])
            del bi[a]
    tri=collections.Counter(tri)
    fi='</s>'
    en='<s>'
    for x in uni:
        if ((x,fi,en) in tri):
            del tri[(x,fi,en)]
        if ((fi,en,x) in tri):
            del tri[(fi,en,x)]
    
    return [uni,bi,tri]
    
def lambdatri(Countbitrain,Countunitrain,Countritrain):
    Contunifol=collections.Counter()
    for tri in Countritrain:
        Ist=tri[0]
        Tnd=tri[1]
        #Trd=tri[2]
        x=(Ist,Tnd)
        if Countbitrain[x] not in [0]:
            Contunifol[x]+=1
        else:
            print([x,'sh'])
    d=0.75
    Lambda=collections.Counter()
    rej='</s>'
    for x in Countbitrain:
        #if x[1] not in rej:
        Lambda[x]=(d*Contunifol[x])/Countbitrain[x]
        te=x[1]
        if te=='</s>':
            del Contunifol[x]
            del Lambda[x]
    for x in Contunifol:
        te=x[1]
        if te=='</s>':
            print(x)
        
    
    
    return [d,Lambda]

def correction(pre,Lambdat):
# =============================================================================
#     pre1=('<UNK>',pre[1])
#     pre2=(pre[0],'<UNK>')
#     pre3=('<UNK>','<UNK>')
#     c1=Lambdat[pre1]
#     c2=Lambdat[pre2]
#     c3=Lambdat[pre3]
#     m=[]
#     if (c1>c2) and (c1>c3):
#         m=pre1
#     else:
#         if (c2>c3) and (c2>c1):
#             m=pre2
#         else:
#             if (c3>c1) and (c3>c2):
#                 m=pre3
#     if (Lambdat[m]==0):
#         print(m)
# =============================================================================
    m=[]
    pre0=pre[0]
    pre1=pre[1]
    ma=0
    for x in Lambdat:
        if Lambdat[(x[0],pre1)]>Lambdat[(pre0,x[1])]:
            if Lambdat[(x[0],pre1)]>ma:
                ma=Lambdat[(x[0],pre1)]
                m=(x[0],pre1)
        else:
             if Lambdat[(pre0,x[1])]>ma:
                ma=Lambdat[(pre0,x[1])]
                m=(pre0,x[1])  
    #print((m,'co'))
    return m
        
            
            
def some(train,test):
    #[test,train]=trate8020(sentences)
    [Countbitrain,Countunitrain,Countritrain]=trigramcount(train)
    [d,Lambda,TotUnipreCount,Contunipre]=ContiProb(Countunitrain,Countbitrain)
    [unitest,bitest,tritest]=testunibi(test,Countunitrain)
    Bipr=collections.Counter()
    n=sum(bitest.values())
    [d,Lambdat]=lambdatri(Countbitrain,Countunitrain,Countritrain)
    
    perplex=1
    for x in bitest:
        times=bitest[x]
        pre=x[0]
        post=x[1]
        Bipr[x]=max((Countbitrain[x]-d),0)/(Countunitrain[pre])+((Lambda[pre])*(Contunipre[post]/TotUnipreCount))
        if (Bipr[x] > 0):
            perplex*=pow((1/Bipr[x]),(times/n))
        else:
            #print(Lambda[pre],Contunipre[pre])
            x=('<UNK>',post)
            pre=x[0]
            #times=bitest[x]
            Bipr[x]=max((Countbitrain[x]-d),0)/(Countunitrain[pre])+((Lambda[pre])*(Contunipre[pre]/TotUnipreCount))
            #if (Bipr[x] > 0):
            perplex*=pow((1/Bipr[x]),(times/n))
            #else:
            #    print(x)
    [d,Lambdat]=lambdatri(Countbitrain,Countunitrain,Countritrain)
    #print(perplex)
    return [perplex,d,Lambdat,Countbitrain,Countunitrain,Countritrain,Bipr,unitest,bitest,tritest]
    
def perlex(perplex,d,Lambdat,Countbitrain,Countunitrain,Countritrain,Bipr,unitest,bitest,tritest):
    Tripr=collections.Counter()
    n1=sum(tritest.values())
    z=[]
    more=[]
    perplex1=1
    for x in tritest:
        times=tritest[x]
        pre1=x[0]
        pre2=x[1]
        pre=(pre1,pre2)
        post=(pre2,x[2])
        if Countbitrain[pre] not in [0]:
            #print(pre)
            if Lambdat[pre]==0:
                #print((pre,'be'))
                pre=correction(pre,Lambdat)
                x=(pre[0],pre[1],x[2])
                #print((x,'af'))
            Tripr[x]=max((Countritrain[x]-d),0)/(Countbitrain[pre])+((Lambdat[pre])*(Bipr[post]))
            
            
        else:
# =============================================================================
#             if Lambdat[pre]==0:
#                 #print((pre,'be'))
#                 pre=correction(pre,Lambdat)
#                 x=(pre[0],pre[1],x[2])
#                 #print((x,'af'))
#             Tripr[x]=max((Countritrain[x]-d),0)/(Countbitrain[pre])+((Lambdat[pre])*(Bipr[post]))
#             
# =============================================================================
            more.append(pre)
            
        if (Tripr[x] > 0):
            perplex1*=pow((1/Tripr[x]),(times/n1))
        else:
            z.append([Lambdat[pre],Bipr[pre],pre])

    
    return [perplex1,d,Lambdat,unitest,bitest,tritest,Countbitrain,Countunitrain,Countritrain,z,more,Bipr,Tripr]

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
                if iter>218081952:
                    break
                if (x[2]==y[0]) and (y[2]==z[0]):
                    a=random.uniform(0,1)
                    p=Tripr[x]*Tripr[y]*Tripr[z]
                    if a<p and k2<10000:
                        ma=Tripr[x]*Tripr[y]*Tripr[z]
                        ac=[y[0],y[1],y[2],z[1],z[2]]
                        break
                    else:
                        if k1*k2*k3>=21808195200 or k2>10000:
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
    #Vocab1=gutenberg.words()
    Sen1=gutenberg.sents()
    #Vocab2=brown.words()
    Sen2=brown.sents()
    [traing,testg]=trate8020(Sen1)
    [trainb,testb]=trate8020(Sen2)
    Sf1=some(traing+testg+trainb+testb,traing+testg+trainb+testb)
    S1=perlex(Sf1[0],Sf1[1],Sf1[2],Sf1[3],Sf1[4],Sf1[5],Sf1[6],Sf1[7],Sf1[8],Sf1[9])
    Bipr=S1[11]
    Tripr=S1[12]
    print(generate_sentence(Bipr,Tripr))
    print(generate_sentence(Bipr,Tripr))
    
    
    
    
if __name__ =='__main__':
    main()    
    






