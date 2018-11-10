from flask import Flask,render_template,request,Response,json
import json
import requests

debug = True

if not debug:
    import gensim

app = Flask(__name__,static_url_path='/static')

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/search", methods=['GET','POST'])
def search():
    if request.method == 'POST':

        org = []

        search_string = request.form.get('search_string')  # access the data inside 

        query = search_string

        cat = max(orgs.items(), key=lambda d:word2vec.similarity(search, d[1]))[0]

        #print(request.form)
        #Get top 3 similar search items
        # if not debug:
        #     queries = [item[0].replace('_', '%20') for item in word2vec.most_similar(search_string, topn=3)]
        # #print(query)
        #     queries.append(search_string) #put back the original query


        articles = set()
        forums = set()

        # for query in queries:
        article_parameters = {'search' : query, 'orderby' : 'relevance'}


        article_response = json.loads(requests.get("https://www.themix.org.uk/wp-json/wp/v2/posts?", params = article_parameters).content)
        for item in article_response:
            articles.add((item.get('title').get('rendered'), item.get('link'), item.get('featured_image_url'), item.get('excerpt').get('rendered').replace('<p>','').replace('</p>', '')))
            
        forum_response = json.loads(requests.get("https://community.themix.org.uk/search/autocomplete.json?term=" + query).content)
        for item in forum_response:
            forums.add((item.get('Title').replace('<mark>', '').replace('</mark>', ''), item.get('Url'), item.get('Summary').replace('<mark>', '').replace('</mark>', '')))

        articles=list(articles)
        forums=list(forums)
        articles = [list(elem) for elem in articles]
        forums = [list(elem) for elem in forums]

    return render_template("output.html", articles=articles, forums=forums)



if __name__ == '__main__':
    #app = create_app()

    if not debug:
        word2vec_path = "/Users/sujay/Downloads/GoogleNews-vectors-negative300.bin.gz"
        word2vec = gensim.models.KeyedVectors.load_word2vec_format(word2vec_path, binary=True)

    orgs = {1: 'abuse', 2: 'bereavement', 3: 'care', 4: 'careers', 4: 
'study', 5: 'child', 6: 'Disability', 7: 'domestic', 8: 'drugs', 8:  
'alcohol', 9: 'relationships', 10: 'health', 11: 'housing', 12: 'legal', 
13: 'mental_health', 14: 'money', 15: 'sexual', 16: 'sexuality', 17: 
'self'}

    app.run(host="0.0.0.0")
