#Process scraped data using beautiful soup

from bs4 import BeautifulSoup
import pickle

#Load raw data
with open("../../data/raw/source.txt",'r') as in_file:
     raw_file = in_file.read()

#Make soup
soup = BeautifulSoup(raw_file,'html.parser')

#Extract content
#1. Authorship / author metadata

article_metadata = soup.find_all('div',class_='views-field views-field-php')

#NB in some cases there is more than 1 author
auth_names = [[x.get_text() for x in el.find_all('div',
                                                 class_='views-field views-field-field-last-name')] 
              for el in article_metadata]

auth_urls = [[x.find('a').get('href') for x in el.find_all('div',
                                                 class_='views-field views-field-field-last-name')] 
              for el in article_metadata]

auth_bios = [[x.find('div').get_text() for x in el.find_all('div',
                                                 class_='views-field views-field-field-user-title')] 
              for el in article_metadata]


#2. Text of contribution
text = soup.find_all('div',
                     class_='views-field views-field-body')

contr_text = [x.find('div').get_text() for x in text]

#This is everything
#Put them in a list where every element has 5 elements (author, url, bio, title, text)

outputs = [[a,u,b,tx] for a,u,b,tx in zip(auth_names,
                                            auth_urls,auth_bios,contr_text)]

#Pickle
with open('../../data/interim/parsed_pickle.p','wb') as outfile:
     pickle.dump(outputs,outfile)





