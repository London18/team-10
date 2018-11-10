from flask import Flask,render_template,request,Response,json
import json

app = Flask(__name__,static_url_path='/static')



@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/search", methods=['GET','POST'])
def search():
    if request.method == 'POST':
        search_string = request.form.get('search_string')  # access the data inside 
        print(request.form)
    return render_template("output.html", test_output=json.dumps(search_string))



if __name__ == '__main__':
    #app = create_app()
    app.run(host="0.0.0.0")
