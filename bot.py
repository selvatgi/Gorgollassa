#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tweepy
from time import sleep
from datetime import *
from random import randint,choice
import credencials
import sys

try:
	usuari_principal = sys.argv[1]
except IndexError:
	print "No hi ha usuari"

auth = tweepy.OAuthHandler(credencials.usuaris[usuari_principal][0], credencials.usuaris[usuari_principal][1])
auth.set_access_token(credencials.usuaris[usuari_principal][2], credencials.usuaris[usuari_principal][3])

api = tweepy.API(auth)

arxiu_log = open("log_tuits.txt", 'w')

class tuit:	
	def __init__(self, entrada):
		self.id = 0
		self.es_retuit = False
		self.es_de_avui = False
		self.autor = entrada.user.screen_name
		self.text = entrada.text
		self.reply = entrada.in_reply_to_status_id
		self.status = entrada
		self.data = entrada.created_at
		arxiu_log.write(str(entrada))
		arxiu_log.write("\n\n\n\n")
		if not (datetime.today() - timedelta(days=1)) > self.data:
			self.es_de_avui = True
		try:
			self.id = entrada._json['retweeted_status']['id']
			self.es_retuit = True
		except KeyError:
			self.id = entrada.id

class usuari:
	def __init__(self, nom, veure_ids = 0): 
		self.nom = nom
		self.veure_ids = veure_ids
		self.tuits = self.darrers_tuits()
		self.llista_id = []
		for i in self.tuits:
			self.llista_id.append(i.id)

	def darrers_tuits(self): #fa llista des darrers tuits
		llista = []
		public_tweets = api.user_timeline(self.nom)
		i = 0
		for tweet in public_tweets: #afegeix a llista ses id reals des darrers 20 tuits
			x = tuit(tweet)
			llista.append(x)
		return llista

def fer_retuit(identificador):
	#api.retweet(identificador)
	print "RT de " + str(identificador) + " fet.\n"
	sleep(randint(3,9))
	#api.create_favorite(identificador)
	print "Fav de " + str(identificador) + " fet.\n"
	print "RT i fav fet"


secundari = usuari(choice(credencials.usuaris[usuari_principal][4]))
principal = usuari(usuari_principal,1)
print "Usuari principal es: " + principal.nom
print "Usuari secundari es: " + secundari.nom
print "llista de usuaris secundaris: " + str(credencials.usuaris[usuari_principal][4])

frase_log = str(datetime.now()) + " " + principal.nom + ": "

if secundari.tuits[0].id not in principal.llista_id: 
	if not secundari.tuits[0].es_retuit:
		print "Fer rt"
		espera = randint(0,10)
		print "Esperant " + str(espera) + " segons per fer RT de " + str(secundari.tuits[0].id)
		sleep(espera)
		fer_retuit(secundari.tuits[0].id)
	
		try: 
			print "Fet RT de usuari " + secundari.tuits[0].autor + ": " + secundari.tuits[0].text
			frase_log += "Fet RT de usuari @" + secundari.tuits[0].autor + ": " + secundari.tuits[0].text.encode('utf-8')
		except UnicodeDecodeError:
			print "Fet RT de usuari " + secundari.tuits[0].autor + ": " + str(secundari.tuits[0].id)
			frase_log += "Fet RT de usuari @" + secundari.tuits[0].autor + ": " + str(secundari.tuits[0].id)
		except UnicodeEncodeError:
			print "Fet RT de usuari " + secundari.tuits[0].autor + ": " + str(secundari.tuits[0].id)
			frase_log += "Fet RT de usuari @" + secundari.tuits[0].autor + ": " + str(secundari.tuits[0].id)

else:
	print "Ja estava fet"
	frase_log += "Retuit de " + secundari.nom + " " + str(secundari.tuits[0].autor) + " ja estava fet"

frase_log += "\n"
arxiu_log.write(frase_log)
arxiu_log.close()
