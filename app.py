from flask import Flask,render_template,request 
import newspaper

from newspaper import Article
import random
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings
warnings.filterwarnings('ignore')


app = Flask(__name__)
@app.route('/')

def index():
	return render_template("index.html")

@app.route('/about')
def about():
	return render_template("about.html")

@app.route('/bot', methods = ["GET","POST"])
def bot():
	# Download the punkt package
	nltk.download('punkt', quiet=True)


	# get the article
	article = Article('https://www.who.int/india/emergencies/coronavirus-disease-(covid-19)')
	article.download()
	article.parse()
	article.nlp()
	corpus = article.text
	#print fetched data
	#print(corpus)
	#tokenization
	text = corpus
	sens_lst = nltk.sent_tokenize(text) #sentense list


	a1 = Article('https://www.who.int/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19#:~:text=symptoms')
	a1.download()
	a1.parse()
	a1.nlp()
	corpus = a1.text
	text = corpus
	sens_lst.append(text)

	a2 = Article('https://www.who.int/news-room/q-a-detail/coronavirus-disease-(covid-19)-vaccines?adgroupsurvey={adgroupsurvey}&gclid=CjwKCAiAgc-ABhA7EiwAjev-j0k-0vsnLgrDYYbw2YD3MyEeT-szPs_WUbi2G_EvwfxNk1gDeCpvABoC5WAQAvD_BwE')
	a2.download()
	a2.parse()
	a2.nlp()
	corpus = a2.text
	text = corpus
	sens_lst.append(text)


	a5 = Article('https://pune.gov.in/corona-virus-updates/')
	a5.download()
	a5.parse()
	a5.nlp()
	corpus = a5.text
	text = corpus
	sens_lst.append(text)

	a6 = Article('https://www.business-standard.com/article/current-affairs/maharashtra-covid-19-vaccination-resumes-in-mumbai-pune-after-two-days-121011900468_1.html')
	a6.download()
	a6.parse()
	a6.nlp()
	corpus = a6.text
	text = corpus
	sens_lst.append(text)

	a7 = Article('https://www.who.int/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-schools')
	a7.download()
	a7.parse()
	a7.nlp()
	corpus = a7.text
	text = corpus
	sens_lst.append(text)

	# returns a random greeting response
	def greeting_resp(text):
		text = text.lower()
		b_greetings = ['howdy','hi','hello','hey','namaste','ciao'] 
		u_greeting = ['hi','hello','hey','greetings','wassup','ciao','namaste']
		for wrd in text.split():
			if wrd in u_greeting:
			  return random.choice(b_greetings)

	def idx_sort(list_var):
		leng = len(list_var)
		list_idx = list(range(0, leng))
		x = list_var
		for i in range(leng):
		   for j in range(leng):
		     if x[list_idx[i]] > x[list_idx[j]]:
		       #swap
		       temp = list_idx[i]
		       list_idx[i] = list_idx[j]
		       list_idx[j] = temp
		return list_idx

	#Create bot response
	def b_response(u_ip):
		u_ip = u_ip.lower()
		sens_lst.append(u_ip)
		b_response = ''
		cm = CountVectorizer().fit_transform(sens_lst)
		similarity_scores = cosine_similarity(cm[-1], cm)
		similarity_scores_list = similarity_scores.flatten()
		idx = idx_sort(similarity_scores_list)
		idx = idx[1:]
		resp_flag = 0

		j = 0  #give top two similar sentences
		for i in range(len(idx)):
			if similarity_scores_list[idx[i]] > 0.0:
			  b_response = b_response+' '+sens_lst[idx[i]]
			  resp_flag = 1
			  j = j + 1
			if j > 2:
			  break
			if resp_flag == 0:
				b_response = b_response+' '+"I apoligize, I don't understand"
				break

			#sens_lst.remove(u_ip)
		return b_response

	ex_ls = ['exit','see you later','bye','quit','break','terminate','adios']

	if request.method == 'GET':
		return render_template("bot.html")

	
	
	if request.method == 'POST':
		text1 = request.form.get('textbox')
		while(True):
		    u_ip = text1
		    if u_ip.lower() in ex_ls:
		      ans = str('MIT Bot: See you later!')
		      break
		    else:
		      if greeting_resp(u_ip) != None:
		        ans = str(greeting_resp(u_ip))
		        break
		      else:
		        ans = str(b_response(u_ip))
		        break
		return render_template("bot.html",output=ans,user_text=text1)





		
	

				  

if __name__=="__main__":
	app.run()

