from flask import Flask,render_template,request,Response,json
import json
import requests


app = Flask(__name__,static_url_path='/static')



@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/search", methods=['GET','POST'])
def search():
    if request.method == 'POST':
        search_string = request.form.get('search_string')  # access the data inside 
        #print(request.form)
        query = search_string
        print(query)
        article_parameters = {'search' : query, 'orderby' : 'relevance'}
        articles = []
        forums = []

        article_response = json.loads(requests.get("https://www.themix.org.uk/wp-json/wp/v2/posts?", params = article_parameters).content)
        for item in article_response:
            articles.append([item.get('title').get('rendered'), item.get('link')])
            
        forum_response = json.loads(requests.get("https://community.themix.org.uk/search/autocomplete.json?term=" + query).content)
        for item in forum_response:
            forums.append([item.get('Title').replace('<mark>', '').replace('</mark>', ''), item.get('Url')])

        #print("Hello")
    return render_template("output.html", articles=articles, forums=forums)



if __name__ == '__main__':
    #app = create_app()
    app.run(host="0.0.0.0")
