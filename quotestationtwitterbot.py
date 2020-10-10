from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import random
import time
import os
from os import environ

import tweepy
consumer_key = environ['CONSUMER_KEY']
consumer_secret =  environ['CONSUMER_SECRET']
access_token =  environ['ACCESS_TOKEN']
access_secret_token =  environ['ACCESS_SECRET_TOKEN']


auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_secret_token)
api = tweepy.API(auth)


webpages=['love','humor','life','inspirational','philosophy','inspirational-quotes',
          'truth','wisdom','poetry','romance','death','happiness','hope','faith','inspiration',
          'writing','quotes','life-lessons','success','motivational','science','life-quotes','books','time','knowledge']
used_quotes=[]
current_url=''

def random_quote_generator():
	current=random.choice(webpages)
	for i in range(1,101):
		if i==1:
			begin=time.time()
			firsturl='https://www.goodreads.com/quotes/tag/'+current
			uclient=uReq(firsturl)
			page_data=uclient.read()
			uclient.close()
			page_soup = soup(page_data, 'html.parser')
			container=page_soup.findAll("div",{"class": "quoteText"})
			for raw_data in container:
				try:
					raw=raw_data.text.split('\n')
					quote=(raw[1].strip())
					author=(raw[4].strip('", '))	
					compileddata=[quote,author]
					if compileddata in used_quotes or len(quote)<10:
						continue
					else:
						if used_quotes!=[]:
							end=time.time()
							#ts=random.randint(900,5400)-(end-begin)
							time.sleep(300)
						hashtag = "#"+current+"Quote \n"
						api.update_status(hashtag+quote+'\n                                                                -'+author)
						print('updated')
						used_quotes.append(compileddata)
						
						random_quote_generator()
				except:
					pass
		else:
			begin=time.time()
			secondurl='https://www.goodreads.com/quotes/tag/{page}?page={num}'.format(page=current,num=i)
			uclient=uReq(secondurl)
			page_data=uclient.read()
			uclient.close()
			page_soup = soup(page_data, 'html.parser')
			container=page_soup.findAll("div",{"class": "quoteText"})
			for raw_data in container:
				try:
					raw=raw_data.text.split('\n')
					quote=(raw[1].strip())
					author=(raw[4].strip('", '))
					compileddata=[quote,author]
					if compileddata in used_quotes:
						continue
					else:

						end=time.time()
						#ts=random.randint(900,5400)-(end-begin)
						time.sleep(300)
						print(quote)
						print('      -',author)
						hashtag = "#"+current+"Quote \n"
						api.update_status(hashtag+quote,'\n                                                                -',author)
						print('updated')
						used_quotes.append(compileddata)
						random_quote_generator()
				except:
					pass

random_quote_generator()
