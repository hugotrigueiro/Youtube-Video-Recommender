import pandas as pd
import re
import joblib as jb
from scipy.sparse import hstack, csr_matrix
import numpy as np

mdl_lgbm = jb.load("lgbm_20200408.pkl.z")
title_vec = jb.load("titlevec_20200408.pkl.z")

def clean_date(data):
    df = data
    date_clean = df["watch-time-text"].str.extract(r"(\d+) de ([a-z]+)\. de (\d+)")
    date_clean[0] = date_clean[0].apply(lambda x: "0" + str(x) if len(str(x)) == 1 else x)

    months_replace = {"jan": "01", 
                      "fev": "02",
                      "mar": "03",
                      "abr": "04",
                      "mai": "05",
                      "jun": "06",
                      "jul": "07",
                      "ago": "08",
                      "set": "09",
                      "out": "10",
                      "nov": "11",
                      "dez": "12"}

    date_clean[1] = date_clean[1].replace(months_replace)
    return pd.to_datetime(date_clean[0] + "/" + date_clean[1] + "/" + date_clean[2], format="%d/%m/%Y")



def clean_views(data):
    df = data
    result = df["watch-view-count"].str.extract(r"(\d+\.?\d+)", expand=False).str.replace(".", "").fillna(0).astype(int).values[0]
    return result



def compute_features(data):
    df = data
    if df["watch-view-count"].isnull().values[0] == True:
        return np.nan
    
    publish_date = clean_date(data)
    if publish_date is None:
        return None
    
    views = clean_views(data)
    title = df["watch-title"].values[0]
    features = pd.DataFrame(index=range(1))
    
    features["tempo_desde_pub"] = (pd.Timestamp.today() - publish_date) / np.timedelta64(1, 'D')
    features["views"] = views
    features["views_por_dia"] = features["views"] / features["tempo_desde_pub"]
    features = features.drop("tempo_desde_pub", axis=1)
    
    vectorized_title = title_vec.transform([title])
    
    num_features = csr_matrix(np.array([features["views"].values[0], features["views_por_dia"].values[0]]))
    feature_array = hstack([num_features, vectorized_title])
    return feature_array



def compute_prediction(data):
    df = data
    feature_array = compute_features(df)
    
    if feature_array is None:
        return 0
    
    p = mdl_lgbm.predict_proba(feature_array)[0][1]
    df["score"] = p
    return df