import streamlit as st
import requests
import pandas as pd
import sqlite3

from bs4 import BeautifulSoup

def search():
    st.title("MovieStar")
    
    def search_movie(query):
        url = f"https://api.themoviedb.org/3/search/movie?api_key=a603e4e3f9ea9420e8aba49de87e68db&query={query}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    
    search = st.text_input("Enter Movie Name: ")
    movie_data = search_movie(search)

    data = {
        'name':[],
        'year':[],
        'genre':[],
        'tmdb':[],
        'imdb_id':[],
        'letterboxd':[],
        'imdb':[],
        'rt':[],
        'metacritic':[]
    }

    def get_imdb(id):
        url = f"https://api.themoviedb.org/3/movie/{id}/external_ids?api_key=a603e4e3f9ea9420e8aba49de87e68db"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
 
    def get_omdb(imdb_id):
        url = f'http://www.omdbapi.com/?i={imdb_id}&apikey=dc066489'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    
    def get_letterboxd(imdb_id):
        
        rating = ''
        lb_rating = None
        try:
            url = 'https://www.letterboxd.com/imdb/'+imdb_id
            page = requests.get(url)
            soup = BeautifulSoup(page.content,'html.parser')
            rating = soup.findAll('meta')[20]['content'][:4]

        except:
            
            return None
        
        else:
            if rating != 'Lett':
                lb_rating = float(rating)
            else:
                lb_rating = None

        finally:
            return lb_rating 

    if movie_data:
        for movie in movie_data['results']:
            imdb = get_imdb(movie['id'])['imdb_id']
            if imdb:
                data['name'].append(movie['title'])
                data['year'].append(movie['release_date'])
                data['genre'].append(movie['genre_ids'])
                data['tmdb'].append(movie['vote_average'])
                data['imdb_id'].append(imdb)
        

        for id in data['imdb_id']:
            # data['letterboxd'].append(get_letterboxd(id))
            result = get_omdb(id)
            if result['Ratings'] and id:
                data['imdb'].append(result['Ratings'][0]['Value'])
                data['metacritic'].append(result['Ratings'][1]['Value'])
                data['rt'].append(result['Ratings'][2]['Value'])
                
                st.write(result['Ratings'])
                st.write(result['Ratings'][0]['Source'])
   
            # conn = sqlite3.connect('movies.db')
            # cursor = conn.cursor()
            # try:
            #     cursor.execute("INSERT INTO movies (name, year, genre, tmdb, imdb_id) VALUES (?, ?, ?, ?, ?)", 
            #                     (movie['title'], movie['release_date'], str(movie['genre_ids']), movie['vote_average'], get_imdb(api_key, movie['id'])['imdb_id']))
            #     conn.commit()
            # except sqlite3.IntegrityError as e:
            #     st.error(f"Error adding movie: {e}")
            # finally:
            #     conn.close()

    st.dataframe(pd.DataFrame(data))
    
    logout_button = st.button("Logout")
    if logout_button:
        st.session_state['logged_in'] = False