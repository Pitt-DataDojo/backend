from flask import Flask, request
from flask_cors import CORS
import os
import seaborn as sns
# import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

app = Flask(__name__)
CORS(app)


@app.route('/api/wordcloud', methods=['GET'])
def word_cloud():
    medicine = request.args.get('medicine')
    path = "static/" + medicine + ".png"
    if os.path.isfile(path):
        return "/"+path
    dataDepression = pd.read_csv('static/data_depr_CLEAN_sideEffectReviews.csv', encoding="gbk")
    drug1data = dataDepression.loc[dataDepression['urlDrugName'] == medicine]
    mpl.rcParams['font.size'] = 12
    mpl.rcParams['savefig.dpi'] = 900
    mpl.rcParams['figure.subplot.bottom'] = .1
    stopwords = set(STOPWORDS)
    wordcloud = WordCloud(
        background_color='white',
        stopwords=stopwords,
        max_words=200,
        max_font_size=40,
        random_state=42
    ).generate(str(drug1data['sideEffectsReview']))
    fig = plt.figure(1)
    plt.imshow(wordcloud)
    plt.axis('off')
    fig.savefig(path, dpi=900)
    return "/"+path


@app.route('/api/dataviz', methods=['GET'])
def data_viz():
    medicine = request.args.get('medicine')
    path = "static/" + medicine + "viz.svg"
    if os.path.isfile(path):
        return "/" + path
    df = pd.read_csv("static/data_depr.csv", encoding="gbk")
    asd = df[df.urlDrugName == medicine]
    cp = sns.catplot(x="rating", hue="urlDrugName", col="effectiveness", data=asd, kind="count", palette="Set3", col_wrap=2, height=5, aspect=1)
    (cp.set_axis_labels("", "Counting the number of ratings")
     .despine(left=True))
    cp.savefig(path, format='svg', dpi=900)
    return "/" + path


@app.route('/api/comments', methods=['GET'])
def comment():
    medicine = request.args.get('medicine')
    df = pd.read_csv("static/data_depr.csv", encoding="gbk")
    comments = df[df.urlDrugName == medicine]['commentsReview'].sample(3)
    return comments.to_json()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8000)), debug=True)
