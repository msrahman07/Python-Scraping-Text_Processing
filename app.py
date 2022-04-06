from crypt import methods
from flask import Flask, render_template, request
from flask import jsonify
import requests
from word_count import word_count_json
import json

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
url = []

@app.route("/", methods=["POST", "GET"])
def home():
    result = jsonify({"Read":"Input any website link to find out the wordcounts"})
    urlinput = ""
    if(request.method == "POST"):
        print(request.form['url'])
        urlinput = request.form['url']
        try:
            # print (word_count_json(url))
            result = jsonify(word_count_json(urlinput))
            # print(result.json)
        except:
            urlinput = ""
            result = jsonify({"Error":" Make sure it's a valid URL and starts with https://"})
    # print(url)
    return render_template("index.html", result=result, formUrl=urlinput)

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