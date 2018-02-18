import random
from flask_cors import CORS
from flask import Flask, request, jsonify, redirect, render_template
from lib542.user import *
from lib542.cache import *

app = Flask(__name__, static_url_path='')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
CORS(app)


@app.route('/')
def main():
    return redirect('index.html')


@app.route('/profile', methods=['GET'])
def profile():
    user_session = request.cookies.get('session')
    return jsonify(extract_profile(user_session))


@app.route('/login', methods=['POST', 'GET'])
def req_ajax():
    username = request.form.get('username')
    password = request.form.get('password')
    a_result = authentication(username, password)

    # return redirect("/page", code=302)
    return jsonify(result=a_result)


@app.route('/register', methods=['POST', 'GET'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == '' or password == '':
        return jsonify([False])
    else:
        return jsonify([True, create_account(username, password)])


@app.route('/name/<name>', methods=['GET'])
def name_redirect(name):
    return redirect('http://www.imdb.com' + request.full_path)


@app.route('/title/<title>', methods=['GET'])
def title_redirect(title):
    return redirect('http://www.imdb.com' + request.full_path)


# /mainPage
@app.route('/getMovieList', methods=['POST', 'GET'])
def get_movie_list():
    # Request parameters via request.args
    # Prevent None type.

    # get title
    title = request.args.get('title')
    # title = '' if request.args.get('title') is None else request.args.get('title')

    # genres
    genres = request.args.get('genres')
    if genres == 'All':
        genres = ''

    # years
    years = request.args.get('years')

    if years == 'All':
        min_year, max_year = 0, 9999
    elif years == 'Earlier':
        min_year, max_year = 0, 1979
    elif len(years) == 4:
        min_year, max_year = int(years), int(years)
    elif len(years) == 9:
        min_year, max_year = years[5:], years[:4]
    else:
        min_year, max_year = 0, 9999

    # rating
    rating = request.args.get('rating')
    if rating == 'All':
        min_rating, max_rating = 0, 9999
    elif len(rating) == 3:
        min_rating, max_rating = int(rating), int(rating)
    elif len(rating) == 7:
        min_rating, max_rating = rating[4:], rating[:3]
    else:
        min_rating, max_rating = 0, 9999

    # sort
    sort = request.args.get('sort')
    if sort == 'rating':
        sort = 'r.`avg(Rating)`'
    elif sort == 'years':
        sort = 'm.Years'
    else:
        sort = 'm.MID'

    print('---> Incoming Request')
    print("title: " + title)
    print("genres: " + genres)
    print('years:' + years)
    print('rating:' + rating)

    # Compose Statement
    statement = "SELECT m.Title, m.Genres, r.`avg(Rating)`, m.Years, l.imdbId " + \
                "FROM Links l, Movies m, Avg_Rating r " + \
                "WHERE m.MID=r.MID " + \
                "AND m.MID=l.MID " + \
                "AND m.Title Like \'%" + title + "%\' " + \
                "AND m.Genres Like \'%" + genres + "%\' " + \
                "AND m.Years <= " + str(max_year) + " " + \
                "AND m.Years >= " + str(min_year) + " " + \
                "AND r.`avg(Rating)` <= " + str(max_rating) + " " + \
                "AND r.`avg(Rating)` >= " + str(min_rating) + " " + \
                "ORDER BY " + sort + " DESC " + \
                "LIMIT 0, 10;"

    # statement = "select m.Title from Movies m"
    # Make some log will be useful for debugging
    print('---> Executing SQL Statement')
    print(statement)

    # Raw result of SQL output
    result = sql_execute(statement)

    # Checking poster
    for index, item in enumerate(result):
        result[index] = item + (summary_cache(item[4]),)

    return jsonify(result)


# /getMovieCover
@app.route('/getMovieCover', methods=['GET'])
def get_movie_cover():
    imdb_id = request.args.get('id')
    image_url = '/img/poster/%s.jpg' % imdb_id

    if not os.path.exists('./static/img/poster/%s.jpg' % imdb_id):
        try:
            d = pq(url='http://www.imdb.com/title/tt%s/' % imdb_id)
            image_url = d('div.poster > a > img').attr('src')
            image_res = requests.get(image_url)
            with open('./static/img/poster/%s.jpg' % imdb_id, 'wb') as file:
                file.write(image_res.content)
                image_url = '/img/poster/%s.jpg' % imdb_id
        except:
            image_url = 'https://coden.hk/img/github.png'

    return redirect(image_url, code=302)


@app.route('/getBannerMovie', methods=['GET'])
def get_banner_moive():
    random_start = random.randint(0, 100)

    statement = "SELECT * " + \
                "FROM Movies, Avg_Rating, Links " + \
                "WHERE Movies.MID=Avg_Rating.MID " + \
                "AND Movies.MID=Links.MID " + \
                "ORDER BY `avg(Rating)` DESC LIMIT %d, %d;" % (random_start, 8)
    print('---> Executing SQL Statement')
    print(statement)
    result = sql_execute(statement)
    return jsonify(result)


@app.route('/details', methods=['GET'])
def detail_page():
    imdb_id = request.args.get('id')

    statement = "SELECT Movies.Title, Movies.Genres, `avg(Rating)`, Movies.MID " + \
                "FROM Movies, Links, Avg_Rating " + \
                "WHERE Links.imdbId='%s' " % imdb_id + \
                "AND Movies.MID=Links.MID " + \
                "AND Movies.MID=Avg_Rating.MID;"

    print('---> Executing SQL Statement')
    print(statement)
    movie_result = sql_execute(statement)[0]

    # TODO: Add history recording system
    # Random based recommend system
    # random_start = random.randint(0, 100)
    # statement = "SELECT * " + \
    #             "FROM Movies, Avg_Rating, Links " + \
    #             "WHERE Movies.MID=Avg_Rating.MID " + \
    #             "AND Movies.MID=Links.MID " + \
    #             "ORDER BY `avg(Rating)` DESC LIMIT %d, %d;" % (random_start, 4)
    # print('---> Executing SQL Statement')
    # print(statement)
    # recommend_result = sql_execute(statement)

    image_url = poster_cache(imdb_id)
    summary_text = summary_cache(imdb_id)
    rec_info = recommend_cache(imdb_id)
    print(rec_info)

    render_data = {
        "movie_name": movie_result[0],
        "movie_genres": movie_result[1],
        "movie_rating": round(movie_result[2], 1),
        "poster": image_url,
        "summary_text": summary_text,
        # "recommends": recommend_result,
        "rec_info": rec_info
    }
    return render_template('details.html', data=render_data)


if __name__ == "__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))
