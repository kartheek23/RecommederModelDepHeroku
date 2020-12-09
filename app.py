# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 14:44:33 2020

@author: Kartheek
"""

import pandas as pd
from flask import Flask,render_template, request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def create_sim():
    data = pd.read_csv('data.csv')
    cv = CountVectorizer()
    count_matrix=cv.fit_transform(data['comb'])
    #Create a similarity score matrix
    sim = cosine_similarity(count_matrix)
    return data,sim

#Defining a function that recommends 10 similar movies
def rcmd(m):
    m = m.lower()
    data,sim = create_sim()
    #Check if the movie is in our database or not
    if m not in data['movie_title'].unique():
        return('This movie is not in our database.\n Please spell check or enter a different movie name')
    else:
        #getting the index of the movie in the dataframe
        i = data.loc[data['movie_title']==m].index[0]
        #fetching the row containing the similarity score of the movie
        # from similarity matrix and enumerating over it.
        lst = list(enumerate(sim[i]))
        #Sorting the list in decreasing order based on similarity score
        lst = sorted(lst,key=lambda x:x[1],reverse=True)
        #Taking top 10 movies
        #Ignoring the first index as it is the original movie
        lst = lst[1:11]
        #Making an empty list containing all 10 movie recommendations
        l= []
        for i in range(len(lst)):
            a = lst[i][0]
            l = l.append(data['movie_title'][a])
        return l

app = Flask(__name__)
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/recommend")
def recommend():
    movie = request.args.get('movie')
    r = rcmd(movie)
    movie = movie.upper()
    if type(r) == type('string'):
        return render_template('recommend.html',movie=movie,r=r,t='s')
    else:
        return render_template('recommend.html',movie=movie,r=r,t='l')
    
if __name__ == '__main__':
    app.run()
            
        
        



        
        
    