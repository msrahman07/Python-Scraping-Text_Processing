from crypt import methods
from flask import Flask, render_template, request
from flask import jsonify
import requests
from word_count import word_count_json, scrape_for_all_links, create_wordcloud
import json

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
url = []

@app.route("/", methods=["POST", "GET"])
def home():
    result = jsonify({"":"Happy Scraping!"})
    urlinput = ""
    result_len = 0
    errors = False
    wordcloud = False
    urls = []
    if(request.method == "POST"):
        print(request.form['url'])
        urlinput = request.form['url']
        if(request.form['links'] == "oneLink"):  
            try:
                # print (word_count_json(url))
                result, texts = word_count_json(urlinput)
                print(texts)
                create_wordcloud(texts)
                wordcloud = True
                result_len = len(result)
                result = jsonify(result)
                # print(result.json)
            except:
                urlinput = ""
                errors = True
                result = jsonify({"Error":" Make sure it's a valid URL and starts with https://"})
        
        elif(request.form['links'] == "allLinks"):
            try:
                print ("Scraping all links")
                result1, texts, urls = scrape_for_all_links(urlinput)
                create_wordcloud(texts)
                wordcloud = True
                result_len = len(result1)
                result = jsonify(result1)
                # print(result.json)
            except:
                errors = True
                urlinput = ""
                result = jsonify({"Error":" Make sure it's a valid URL and starts with https://"})
    # print(url)
    return render_template("index.html", result=result, 
                        formUrl=urlinput, result_len=result_len, 
                        errors=errors, cloud=wordcloud, urls=urls)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('index.html'), 404

# @app.route("/words", methods=['POST'])
# def post_url():
#     if request.method == 'POST':
#         print("request: ", request.content_type)
#         print("blah blah:", request)
#         raw_data = request.get_data()
#         data = json.loads(raw_data.decode("utf-8"))
#         print("here's the data:", data)
#         url = []
#         try:
#             # print (word_count_json(url))
#             value = word_count_json(data)
#             url.append(value)
#             return value
#         except:
#             return jsonify({"message":"invalid url"})
    
#     return data
#     # try:
#     #         # print (word_count_json(url))
#     #     return jsonify(word_count_json(url))
#     # except:
#     #     return jsonify({"message":"invalid url"})
    
#     # return jsonify({'message': 'it\'s a get request'})

# @app.route("/words")
# def wordcount():
#     print(url)
#     # url.append() 
#     return jsonify({'message': 'it\'s a get request'})


if __name__ == "__main__":
    app.run(debug=True)