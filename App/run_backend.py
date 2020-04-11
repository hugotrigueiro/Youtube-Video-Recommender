from get_data import *
from ml_utils import *
import time
import pandas as pd


def update_db(queries, limit_page):
    dfs = []
    for query in queries:
        for page in range(1, limit_page):
            search_page = download_search_page(query, page)
            video_list = parse_search_page(search_page)["urls_videos"]
            
            video_page = video_list.apply(download_video_page)
            video_data = video_page.apply(parse_video_page)
            video_data = video_data[video_data.apply(lambda x: x["watch-title"].notnull().values[0])]
            video_data_predict = video_data.apply(compute_prediction)
            
            df = pd.DataFrame({})
            df["title"] = video_data_predict.apply(lambda x: x["watch-title"].values[0])
            df["score"] = video_data_predict.apply(lambda x: x["score"].values[0])
            df["video_id"] = video_data_predict.apply(lambda x: x["og:video:url"].values[0])
            df["thumb"] = video_data_predict.apply(lambda x: x["og:image"].values[0])
            df = df[df["video_id"].notnull()]
            dfs.append(df)
    df = pd.concat(dfs)
    df.to_csv("new_videos.csv", sep=";", index=False)
    print("Arquivo salvo!")
    return True
