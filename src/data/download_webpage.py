#Script to scrape data from 'what to think about thinking machines' page

#Imports
import os
from urllib.request import urlopen

#Scrape
target_page = "https://www.edge.org/responses/what-do-you-think-about-machines-that-think"
accessed = urlopen(target_page)
accessed_html = accessed.read()

#Write
with open("../../data/raw/source.txt",'wb') as file:
     file.write(accessed_html)




