import os.path
from flask import Flask
import os
import run_backend
import time
import pandas as pd
import codecs

app = Flask(__name__)

queries = ['Data+Science', 'Machine+Learning']
limit_page = 2

def get_predictions():
    
    new_videos_csv = "new_videos.csv"
    if not os.path.exists(new_videos_csv):
        print("inicio update db")
        run_backend.update_db(queries, limit_page)
    
    last_update = os.path.getmtime(new_videos_csv) * 1e9
    
            
    predictions = []
    new_videos = pd.read_csv("new_videos.csv", sep=";")
    for row in new_videos.iterrows():
        predictions.append((row[1]["video_id"], row[1]["title"], float(row[1]["score"]), row[1]["thumb"]))
        
    predictions = sorted(predictions, key=lambda x: x[2], reverse=True)[:30]
        
    predictions_formatted = []
    carrousel_formatted = []
    for n, e in enumerate(predictions):
        if n == 0:
            carrousel_formatted.append("""<div class="carousel-item active">
            <iframe width="600" height="337" class="iframe-video" src=\"{embed}\" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
            <div>
                <p>Score: <b>{score}</b></p>
            </div>
            </div>""".format(embed=e[0], score=e[2]))
        elif n !=0 and n <= 4:
            carrousel_formatted.append("""<div class="carousel-item">
            <iframe width="600" height="337" class="iframe-video" src=\"{embed}\" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
            <div>
                <p>Score: <b>{score}</b></p>
            </div>
            </div>""".format(embed=e[0], score=e[2]))
            
        
        predictions_formatted.append("""<tr>
                                            <th><a href=\"{link}\">{title}</a></th>
                                            <th>{score}</th>
                                        </tr>""".format(title=e[1], link=e[0], score=e[2]))
        
    return "\n".join(predictions_formatted), "\n".join(carrousel_formatted), last_update

@app.route('/')
def main_page():
    preds, carrousel, last_update = get_predictions()
<<<<<<< HEAD:App/.ipynb_checkpoints/app-checkpoint.py
    base_html = codecs.open("base_view.html", "r", "utf-8").read().format((time.time() - last_update) / 1e9, carrousel)
    final_html = codecs.open("final_view.html", "r", "utf-8").read()
    result = base_html + """
            <table class="table-videos">{}</table>""".format(preds) + final_html
    view = open("view_complete.html", "wb")
    view.write(result.encode())
    view.close()
    return result
=======
    base_html = codecs.open("base_view.html", "r", "utf-8").read().replace("\n", "").format((time.time() - last_update) / 1e9, carrousel)
    final_html = codecs.open("final_view.html", "r", "utf-8").read().replace("\n", "")
    return base_html + """
            <table class="table-videos">{}""".format(preds) + final_html
>>>>>>> parent of 7369c88... update8:.ipynb_checkpoints/app-checkpoint.py


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
