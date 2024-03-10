from flask import Flask, jsonify
from flask_cors import CORS
from summarizer.summarizer import get_news_summaries

app = Flask(__name__)
CORS(app)

@app.route('/news', methods=['GET'])
def get_news():
  news_summaries = get_news_summaries()
  return jsonify(news_summaries)

if  __name__ == '__main__':
  app.run(debug=True)