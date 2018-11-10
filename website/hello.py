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

        # if w2v:

        #     ##### word2vec ######

        #     #Get top 3 similar search items
        #     queries = [item[0].replace('_', '%20') for item in word2vec.most_similar(search_string, topn=3)]
        #     queries.append(search_string) #put back the original query


        #     articles = set()
        #     forums = set()



        #     for query in queries:
        #         article_parameters = {'search' : query, 'orderby' : 'relevance'}

        #         article_response = json.loads(requests.get("https://www.themix.org.uk/wp-json/wp/v2/posts?", params = article_parameters).content)
        #         for item in article_response:
        #             articles.add((item.get('title').get('rendered'), item.get('link'), item.get('featured_image_url'), item.get('excerpt').get('rendered').replace('<p>','').replace('</p>', '')))
                    
        #         forum_response = json.loads(requests.get("https://community.themix.org.uk/search/autocomplete.json?term=" + query).content)
        #         for item in forum_response:
        #             forums.add((item.get('Title').replace('<mark>', '').replace('</mark>', ''), item.get('Url'), item.get('Summary').replace('<mark>', '').replace('</mark>', '')))

        #     articles=list(articles)
        #     forums=list(forums)
        #     articles = [list(elem) for elem in articles]
        #     forums = [list(elem) for elem in forums]
        
        # else:

        ###### non-word2vec ######

        query=search_string
        orgs = {1: 'abuse', 2: 'bereavement', 3: 'care', 4: 'careers', 4: 'study', 5: 'child', 6: 'Disability', 7: 'domestic', 8: 'drugs', 8: 'alcohol', 9: 'relationships', 10: 'health', 11: 'housing', 12: 'legal', 13: 'mental_health', 14: 'money', 15: 'sexual', 16: 'sexuality', 17: 'self'}
        org = []
        for key, value in orgs.items():
            print(key,value)
            if value == query:
                
                org_response = json.loads(requests.get('https://tyt992fym8.execute-api.eu-west-2.amazonaws.com/prod/organisations?norg=1&lat=51.507351&long=-0.127758&distance=500&unit=m&>&cat=' + str(key) + '&limit=3').content).get('results')
                for item in org_response:
                    spec_org = json.loads(requests.get('https://tyt992fym8.execute-api.eu-west-2.amazonaws.com/prod/organisations/' + str(item.get('orgid'))).content)
                    org.append([spec_org.get('name'), spec_org.get('website'), spec_org.get('serviceoffered')])
                break

        print(org)

        
        articles = []
        forums = []
        


        article_parameters = {'search' : query, 'orderby' : 'relevance'}

        
        article_response = json.loads(requests.get("https://www.themix.org.uk/wp-json/wp/v2/posts?", params = article_parameters).content.decode('utf-8'))
        for item in article_response:
            articles.append([item.get('title').get('rendered'), item.get('link'), item.get('featured_image_url'), item.get('excerpt').get('rendered').replace('<p>','').replace('</p>', '')])   
        forum_response = json.loads(requests.get("https://community.themix.org.uk/search/autocomplete.json?term=" + query).content.decode('utf-8'))
        for item in forum_response:
            forums.append([item.get('Title').replace('<mark>', '').replace('</mark>', ''), item.get('Url'), item.get('Summary').replace('<mark>', '').replace('</mark>', '')])


    return render_template("output.html", articles=articles, forums=forums, org=org)



if __name__ == '__main__':
    #app = create_app()

    #w2v=False
    # if w2v:
    #     word2vec_path = "/Users/sujay/Downloads/GoogleNews-vectors-negative300.bin.gz"
    #     word2vec = gensim.models.KeyedVectors.load_word2vec_format(word2vec_path, binary=True)


    orgs = {1: 'abuse', 2: 'bereavement', 3: 'care', 4: 'careers', 4: 
'study', 5: 'child', 6: 'Disability', 7: 'domestic', 8: 'drugs', 8:  
'alcohol', 9: 'relationships', 10: 'health', 11: 'housing', 12: 'legal', 
13: 'mental_health', 14: 'money', 15: 'sexual', 16: 'sexuality', 17: 
'self'}

    app.run(host="0.0.0.0")
