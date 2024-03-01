# app.py

from flask import Flask, request, render_template,jsonify
from top_n_recommendations import get_top_n_movie_recommendations,get_movie_name_suggestions

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index_movie.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    movie_name = request.form['movie_name']
    recommendations = get_top_n_movie_recommendations(movie_name)
    return render_template('recommendations_movie.html', movie_name=movie_name, recommendations=recommendations)

@app.route('/movie_names')
def movie_names():
    
    term = request.args.get('term')
    
    suggestions = get_movie_name_suggestions(term)
    return jsonify(suggestions)

if __name__ == '__main__':
    app.run(debug=True)
