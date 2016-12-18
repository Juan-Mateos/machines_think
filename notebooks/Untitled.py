
# coding: utf-8

# In[382]:

import pickle
import os
from itertools import islice

import numpy as np
import pandas as pd

import ratelim
import json
import requests
import scholarly

from nltk.sentiment.vader import SentimentIntensityAnalyzer

#We use scholarly to extract author data from GS. We will focus on the top 5 results and check matches on
    #institution

@ratelim.patient(10,30)
def gimme_scholar(auth_name):
    '''
    Takes an author name and returns the profiles of the top 5 academics
    
    '''
    returned = scholarly.search_author(auth_name)
    
    #Tries to append the 5 first results to an out-list
    #out = next(returned)
    
    out=[]
    #return(returned)
    
    it = 0
    while it<5:
        it +=1
        try:
            out.append(next(returned))
        except:
            return(out)
    return(out)


#We obtain genders using genderise, a web API

@ratelim.patient(10,30)
def gimme_gender(auth_name):
    '''
    Takes an author name and returns the gender based on https://genderize.io/
    
    '''
    
    first_name = auth_name.split(" ")[0]
    
    result = requests.get("https://api.genderize.io/?name={x}".format(x=first_name))
    return(json.loads(result.content.decode('utf-8')))


# In[50]:

data_dir = os.path.join(os.path.dirname(os.getcwd()),'data/interim')


# In[51]:

with open(data_dir + '/parsed_pickle.p','rb') as infile:
    parsed = pickle.load(infile)


# In[294]:

#Use only those entries for which we have the author's name
selected_outputs = [x for x in parsed if len(x[0])>0]

#Create a df with author metadata
author_metadata_df = pd.DataFrame([[x[0][0].strip(),x[1][0],x[2][0]] for x in selected_outputs],
                                 columns=['name','url','bio'])

#We want to focus on entries with an academic profile and a likely presence in Google scholar
names = ['university','college','school','mit','institute','professor']

#Academic keyword in bio
has_university = [any(n in x[2][0].lower() for n in names) for x in selected_outputs]

print("We have {x} academics".format(x=np.sum(has_university)))

#Add a variable in the df
author_metadata_df['is_academic'] = has_university


# In[298]:

#Extract affiliations and genders
author_metadata_external = []

it = 0
for a in author_metadata_df.name:
    it +=1
    
    #Running...
    if(it%20==0):
        print('running with author {au}'.format(au=a))
    
    #Extract scholar results
    scholar_results = gimme_scholar(a)
    
    #Extract gender
    gender_results = gimme_gender(a)['gender']
    
    author_metadata_external.append([scholar_results,gender_results])


# In[379]:

#Extract affiliations and interests of first match. How can we be sure that's the right one?

#First extract a list of affiliations for each author
academic_info=[]
for x in author_metadata_external:
    #print(num)
    
    try:
        affs = x[0][0].affiliation
    except:
        affs = 'no_info'
    
    try:
        ints = x[0][0].interests
    except:
        ints = ['no_info']
        
    academic_info.append([affs,ints])


# In[380]:

#Need to find a way of lumping these subjects into disciplines
pd.Series([x.lower() for el in academic_info for x in el[1]]).value_counts()


# In[386]:

#Need to perform the sentiment analysis (sentence level and average?) and the topic modelling (document level)


# In[ ]:



