import tkinter as tk
import requests
import json
from newspaper import Article
import pyttsx3 as tts
from tkinter import HORIZONTAL, VERTICAL, BOTTOM, X, RIGHT, Y, LEFT, BOTH, ALL
import webbrowser
import urllib
import os
from PIL import ImageTk, Image

from keys import *

title_list = {}
description_list = {}
author_list = {}
date_list = {}
url_list = {}
title_button = {}



BG = "black"
FG = "white"
CLICKED = "blue"
CURR_CLICKED = 0


class myApp:
	def __init__(self, master):
		
		# HEADERS MENU DESIGN
		self.menu_frame = tk.Frame(master)
		self.menu_frame.pack(padx=10, pady=10)

		self.top_ten_button = tk.Button(self.menu_frame, text="TOP 10", font=('helvetica', 25 , 'bold'), bg=BG, fg=CLICKED, borderwidth=0)
		self.top_ten_button.config(command = self.show_top_ten)
		self.top_ten_button.grid(row=0, column=0, padx=10, pady=10)

		self.technology_button = tk.Button(self.menu_frame, text="TECH", font=('helvetica', 25 , 'bold'), bg=BG, fg=FG, borderwidth=0)
		self.technology_button.config(command = self.show_tech)
		self.technology_button.grid(row=0, column=1, padx=10, pady=10)

		self.science_button = tk.Button(self.menu_frame, text="SCIENCE", font=('helvetica', 25 , 'bold'), bg=BG, fg=FG, borderwidth=0)
		self.science_button.config(command = self.show_science)
		self.science_button.grid(row=0, column=2, padx=10, pady=10)

		self.business_button = tk.Button(self.menu_frame, text="BUSINESS", font=('helvetica', 25 , 'bold'), bg=BG, fg=FG, borderwidth=0)
		self.business_button.config(command = self.show_business)
		self.business_button.grid(row=0, column=3, padx=10, pady=10)

		self.sports_button = tk.Button(self.menu_frame, text="SPORTS", font=('helvetica', 25 , 'bold'), bg=BG, fg=FG , borderwidth=0)
		self.sports_button.config(command = self.show_sports)
		self.sports_button.grid(row=0, column=4, padx=10, pady=10)

		self.weather_button = tk.Button(self.menu_frame, text="WEATHER", font=('helvetica', 25 , 'bold'), bg=BG, fg=FG , borderwidth=0)
		self.weather_button.config(command = self.show_weather)
		self.weather_button.grid(row=0, column=5, padx=10, pady=10)


		# ARTICLES DISPLAY DESIGN 
		self.parent_frame = tk.Frame(master)
		self.parent_frame.pack()
		
		self.main_canvas = tk.Canvas(self.parent_frame)
		self.main_canvas.config(bg=BG, borderwidth=0, highlightthickness=0)
		self.main_canvas.pack()

		self.article_frame = tk.Frame(self.main_canvas)
		self.article_frame.config(bg=BG,borderwidth=0, highlightthickness=0)
		self.article_frame.pack()


		self.show_top_ten()



	def show_article(self, article_number):
		
		global title_list
		global description_list
		global author_list
		global date_list
		global url_list
		global title_button


		article_overlay = tk.Toplevel()
		article_overlay.config(bg=BG)
		article_overlay.title(title_list[article_number])

		title_label = tk.Label(article_overlay, text=title_list[article_number], font=('Helvetica', 20, 'bold'), bg=BG, fg=FG)
		title_label.grid(row=0, column=0, columnspan=2, sticky="n")

		byline_label = tk.Label(article_overlay, text=author_list[article_number], font=('Helvetica', 10, 'bold'), bg=BG, fg=FG)
		byline_label.grid(row=1, column=0, columnspan=2, sticky="n")

		filler = tk.Label(article_overlay, text="                    ", bg=BG)
		filler.grid(row=2, column=0, columnspan=1)

		tts_button = tk.Button(article_overlay, text="READ OUT!", command=lambda: self.text_to_speech(article), bg=BG, fg=FG, font=('helvetica', 10, 'bold'))
		tts_button.grid(row=3, column=0)

		article_url = url_list[article_number]

		problem_button = tk.Button(article_overlay, text="PROBLEM WITH ARTICLE? open in browser", command=lambda: self.open_in_browser(article_url))
		problem_button.config(bg=BG, fg=FG, font=('helvetica', 10, 'bold'))
		problem_button.grid(row=3, column=1, padx=15)

		article = self.parse_article(article_url)

		content = tk.Message(article_overlay, text=article, font=('Helvetica', 15), bg=BG, fg=FG)
		content.grid(row=4,column=0, columnspan=2)


		article_overlay.mainloop()


	def text_to_speech(self, txt):
		# reads out the text passed to it.

		engine = tts.init()
		engine.say(txt)
		engine.runAndWait()


	def parse_article(self, url) -> str:
		
		article = Article(url, language="en")
		article.download()
		article.parse()
		# article.nlp()

		return article.text


	def show_top_ten(self):
		# UPDATING HEADER COLOUR
		self.update_headers(0)

		# CLEARING OUT ARTICLE FRAME
		self.article_frame.destroy()

		# FOR CREATING THE ARTICLE FRAME
		self.create_article_frame()

		# PUSHING ARTICLES ON THE ARTICLE FRAME
		self.fill_article_frame("cnn")


	def show_tech(self):
		# UPDATING HEADER COLOUR
		self.update_headers(1)

		# CLEARING OUT THE ARTICLE FRAME
		self.article_frame.destroy()

		# FOR CREATING THE ARTICLE FRAME
		self.create_article_frame()

		# PUSHING ARTICLES ON THE ARTICLE FRAME
		self.fill_article_frame("techcrunch")


	def show_science(self):
		# UPDATING HEADER COLOUR
		self.update_headers(2)

		# CLEARING OUT ARTICLE FRAME
		self.article_frame.destroy()

		# FOR CREATING THE ARTICLE FRAME
		self.create_article_frame()

		# PUSHING ARTICLES ON THE ARTICLE FRAME
		self.fill_article_frame("national-geographic")


	def show_business(self):
		# UPDATING HEADER COLOUR
		self.update_headers(3)

		# CLEARING OUT ARTICLE FRAME
		self.article_frame.destroy()

		# FOR CREATING THE ARTICLE FRAME
		self.create_article_frame()

		# PUSHING ARTICLES ON THE ARTICLE FRAME
		self.fill_article_frame("business-insider")


	def show_sports(self):
		# UPDATING HEADER COLOUR
		self.update_headers(4)

		# CLEARING OUT ARTICLE FRAME
		self.article_frame.destroy()

		# FOR CREATING THE ARTICLE FRAME
		self.create_article_frame()

		# PUSHING ARTICLES ON THE ARTICLE FRAME
		self.fill_article_frame("espn")


	def show_weather(self):
		# UPDATING HEADER COLOUR
		self.update_headers(5)

		# CLEARING OUT ARTICLE FRAME
		self.article_frame.destroy()

		# FOR CREATING THE ARTICLE FRAME
		self.create_article_frame()

		# SHOWING THE WEATHER

		FONT = ('Helvetica', 15, 'bold')
		UNIT = 'metric'

		response = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&units=%s&appid=%s" %(LAT, LON , UNIT , WEATHER_API_KEY)).json()

		icon_id = response['current']['weather'][0]['icon']
		icon_url = "http://openweathermap.org/img/wn/%s@2x.png" %(icon_id)

		urllib.request.urlretrieve(icon_url, icon_id)
		ICON_PATH = os.getcwd() + "\\" + "TEMP\\" + "\\" + icon_id
		OPEN_ICON = ImageTk.PhotoImage(Image.open(icon_id))

		timezone = response['timezone']

		timezone_label = tk.Label(self.article_frame, text="SHOWING WEATHER FOR TIMEZONE  %s" %(timezone), font=FONT, bg=BG, fg=FG)
		timezone_label.grid(row=0, column=0, padx=20, pady=20)


		icon = tk.Label(self.article_frame, image=OPEN_ICON, bg=BG, fg=FG)
		icon.image = OPEN_ICON
		icon.grid(row=1, column=1, padx=10, pady=10, rowspan=3)


		current_temp = response['current']['temp']
		feels_like = response['current']['feels_like']
		current_weather = response['current']['weather'][0]['main']
		weather_description = response['current']['weather'][0]['description']

		curr_temp_label = tk.Label(self.article_frame, text="CURRENT TEMPERATURE 	: 	%s C" %(current_temp), font=FONT, bg=BG, fg=FG)
		curr_temp_label.grid(row=1, column=0, padx=10, pady=10)

		feels_like_label = tk.Label(self.article_frame, text="FEELS LIKE 	: 	%s C" %(feels_like), font=FONT, bg=BG, fg=FG)
		feels_like_label.grid(row=2, column=0, padx=10, pady=10)

		curr_weather_label = tk.Label(self.article_frame, text="CURRENT WEATHER 	: 	%s" %(current_weather), font=FONT, bg=BG, fg=FG)
		curr_weather_label.grid(row=3, column=0, padx=10, pady=10)

		description_label = tk.Label(self.article_frame, text="DESCRIPTION 		: 	%s" %(weather_description), font=FONT, bg=BG, fg=FG)
		description_label.grid(row=4, column=0, padx=10, pady=10)



	def create_article_frame(self):
		self.article_frame = tk.Frame(self.main_canvas)
		self.article_frame.config(bg=BG,borderwidth=0, highlightthickness=0)
		self.article_frame.pack()


	def fill_article_frame(self, endpoint):
		RESPONSE = requests.get("https://newsapi.org/v2/top-headlines?sources=%s&apiKey=%s" %(endpoint, API_KEY)).json()
		TOTAL_ARTICLES = RESPONSE['totalResults']


		# dictionaries for storing various types of information for articles
		self.clear_lists()

		global title_list
		global description_list
		global author_list
		global date_list
		global url_list
		global title_button


		# for fetching info of all the articles and storing them in dictionaries declared above
		for i in range(0, TOTAL_ARTICLES):
			title_list[i] = RESPONSE['articles'][i]['title']
			description_list[i] = RESPONSE['articles'][i]['description']
			author_list[i] = RESPONSE['articles'][i]['author']
			date_list[i] = RESPONSE['articles'][i]['publishedAt']
			url_list[i] = RESPONSE['articles'][i]['url']


		# FOR PUSHING STUFF ONTO THE MAIN UI
		for i in range(0, TOTAL_ARTICLES):
			title = title_list[i]
			author = author_list[i]
			date = date_list[i]
			description = description_list[i]

			title_button[i] = tk.Button(self.article_frame, text=title, font=('Helvtica', 15 , 'bold'), command= lambda i=i: self.show_article(i), bg=BG, fg=FG)
			title_button[i].config(borderwidth=0)
			title_button[i].pack()
			filler = tk.Label(self.article_frame, bg=BG, fg=FG)
			filler.pack()
			filler.pack()


	def clear_lists(self):
		global title_list
		global description_list
		global author_list
		global date_list
		global url_list
		global title_button

		title_list.clear()
		description_list.clear()
		author_list.clear()
		date_list.clear()
		url_list.clear()
		title_button.clear()


	def open_in_browser(self, url):
		webbrowser.open(url, new=2)


	def update_headers(self, new_clicked):

		global CURR_CLICKED

		if CURR_CLICKED == new_clicked:
			pass

		# CHANGING COLOUR OF CURRENTLY CLICKED
		if CURR_CLICKED == 0:
			self.top_ten_button.config(fg=FG)

		elif CURR_CLICKED == 1:
			self.technology_button.config(fg=FG)

		elif CURR_CLICKED == 2:
			self.science_button.config(fg=FG)

		elif CURR_CLICKED == 3:
			self.business_button.config(fg=FG)

		elif CURR_CLICKED == 4:
			self.sports_button.config(fg=FG)

		elif CURR_CLICKED == 5:
			self.weather_button.config(fg=FG)


		# CHANGING COLOUR OF NEW CLICKED
		if new_clicked == 0:
			self.top_ten_button.config(fg=CLICKED)

		elif new_clicked == 1:
			self.technology_button.config(fg=CLICKED)

		elif new_clicked == 2:
			self.science_button.config(fg=CLICKED)

		elif new_clicked == 3:
			self.business_button.config(fg=CLICKED)

		elif new_clicked == 4:
			self.sports_button.config(fg=CLICKED)

		elif new_clicked == 5:
			self.weather_button.config(fg=CLICKED)



		CURR_CLICKED = new_clicked




root = tk.Tk()
root.title("Daily Digest!")
root.config(bg=BG)
root.geometry("1200x750")

app = myApp(root)


root.columnconfigure(0, weight=1)
root.mainloop()