import requests as rq
from bs4 import BeautifulSoup
import re
import time
import pandas as pd


def download_search_page(search_word, page):
    search_url = "https://www.youtube.com/results?search_query={}&p={}"
    url = search_url.format(search_word, page)
    url_code = rq.get(url, timeout=60)
    return url_code.text
    

def parse_search_page(page_html):
    parsed = BeautifulSoup(page_html, "html.parser")
    titles = []
    urls_videos = []
    pages_video = []
    
    #print([i.has_attr("aria-describedby") == True for i in parsed.findAll("a")].count(True))
    for link in parsed.findAll("a"):
        if link.has_attr("aria-describedby") == True:
            titles.append(link["title"])
            urlls_videos = "https://youtube.com.br" + link["href"]
            urls_videos.append(urlls_videos)
            pages_video.append(rq.get(urlls_videos, timeout=60).text)
            #try:
            #    pages_video.append(rq.get(urlls_videos, timeout=60).text)
            #except rq.exceptions.SSLError:
            #    pass
            #except rq.exceptions.ConnectionError:
            #    pass
    data = pd.DataFrame({"title": titles, "urls_videos": urls_videos, "pages": pages_video})
    return data


def download_video_page(link):
    video_page = rq.get(link, timeout=60).text
    time.sleep(1)
    return video_page


def parse_video_page(page_html):
    parsed = BeautifulSoup(page_html, "html.parser")
    
    class_watch = parsed.find_all(attrs={"class":re.compile(r"watch")})
    id_watch = parsed.find_all(attrs={"id":re.compile(r"watch")})
    channel = parsed.find_all("a", attrs={"href":re.compile(r"channel")})
    meta = parsed.find_all("meta")
    
    got_data = {}
    
    for cl in class_watch:
        colname = "_".join(cl["class"])
        if "clearfix" in colname:
            continue
        got_data[colname] = cl.text.strip()
    
    for cl in id_watch:
        colname = cl["id"]
        got_data[colname] = cl.text.strip()
        
    for cl in meta:
        colname = cl.get("property")
        if colname is not None:
            got_data[colname] = cl["content"]
    
    for n, cl in enumerate(channel):
        got_data["channel_link_{}".format(n)] = cl["href"]
    
    videos_data = pd.DataFrame(got_data, index=range(1))
    selected_columns = ["watch-title", 
                        "watch-view-count", 
                        "watch-time-text", 
                        "content_watch-info-tag-list", 
                        "watch7-headline", 
                        "watch7-user-header", 
                        "watch8-sentiment-actions", 
                        "og:image", 
                        "og:image:width", 
                        "og:image:height", 
                        "og:description", 
                        "og:video:width", 
                        "og:video:height", 
                        "og:video:url", 
                        "channel_link_0"]
    
    videos_data = videos_data.reindex(columns=selected_columns)
    return videos_data
