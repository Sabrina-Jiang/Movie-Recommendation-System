import os
from pyquery import PyQuery as pq
import requests
import json

FAILED_IMAGE = 'https://coden.hk/img/github.png'


def summary_cache(imdb_id):
    if not os.path.exists('./static/descriptions/%s.txt' % imdb_id):
        d = pq(url='http://www.imdb.com/title/tt%s/' % imdb_id)
        try:
            summary_text = d('.plot_summary').html()
            with open('./static/descriptions/%s.txt' % imdb_id, 'w') as file:
                file.write(summary_text)
        except:
            summary_text = "Server Error"
    else:
        summary_text = open('./static/descriptions/%s.txt' % imdb_id, 'r').read()

    return summary_text


def recommend_cache(imdb_id):
    if not os.path.exists('./static/recommends/%s.txt' % imdb_id):
        d = pq(url='http://www.imdb.com/title/tt%s/' % imdb_id)
        try:
            rec_raw = d('.rec_item')
            rec_item = []
            for item in rec_raw[:6]:
                img_id = d(item).attr('data-tconst')[2:]
                rec_item.append([img_id, {
                    'title': d(
                        '.rec_overview[data-tconst=tt%s] > .rec_details > .rec-info > .rec-jaw-upper > .rec-title' % img_id).text(),
                    'des': d(
                        '.rec_overview[data-tconst=tt%s] > .rec_details > .rec-info > .rec-jaw-upper > .rec-rating' % img_id).text()[32:]
                }])

            rec_json = json.dumps(rec_item)
            with open('./static/recommends/%s.txt' % imdb_id, 'w') as file:
                file.write(rec_json)
        except:
            rec_item = "Server Error"
    else:
        rec_item = json.loads(open('./static/recommends/%s.txt' % imdb_id, 'r').read())

    return rec_item


def poster_cache(imdb_id):
    image_url = '/img/poster/%s.jpg' % imdb_id

    if not os.path.exists('./static/img/poster/%s.jpg' % imdb_id):
        d = pq(url='http://www.imdb.com/title/tt%s/' % imdb_id)
        try:
            image_url = d('div.poster > a > img').attr('src')
            image_res = requests.get(image_url)
            with open('./static/img/poster/%s.jpg' % imdb_id, 'wb') as file:
                file.write(image_res.content)
                image_url = '/img/poster/%s.jpg' % imdb_id
        except:
            image_url = FAILED_IMAGE

    return image_url
