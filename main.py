import requests

API_URL = 'https://www.googleapis.com/youtube/v3/videos'
KEY = 'SECRET_KEY'

class VideoInfo:
    def __init__(self, id, title, duration):
        self.id = id
        self.title = title

        duration = duration[2:]
        self.duration = parse_duration(duration)
    
    def __str__(self):
        return f"Title: {self.title}\nDuration: {self.duration}s\n"

# duration_str in XXHXXMXXS
def parse_duration(duration_str):
    curr = duration_str
    duration = 0

    if not duration_str: return duration

    # split by H
    tmp1 = curr.split("H")
    if(len(tmp1) == 1): # no H
        curr = tmp1[0]
    else:
        curr = tmp1[1]
        duration += int(tmp1[0]) * 60 * 60

    # split by M
    tmp1 = curr.split("M")
    if(len(tmp1) == 1): # no M
        curr = tmp1[0]
    else:
        curr = tmp1[1]
        duration += int(tmp1[0]) * 60

    # split by S
    tmp1 = curr.split("S")
    if(len(tmp1) == 1): # no S
        curr = tmp1[0]
    else:
        duration += int(tmp1[0])
    
    return duration

def get_id(url:str):
    start_idx = url.index("?v=") + 3
    
    if '&' in url:
        end_idx = url.index("&")
    else:
        end_idx = len(url)
    
    return url[start_idx:end_idx]

def get_list_of_urls():
    with open("url.txt", "r") as f:
        return f.readlines()

def process_response(id):
    response = requests.get(API_URL, params={"key": KEY, "part": "contentDetails, snippet", "id": id})
    res = response.json()

    info = []
    for item in res["items"]:
        info.append(VideoInfo(item["id"], item["snippet"]["title"], item["contentDetails"]["duration"]))

    return info


def run():
    list_of_urls = get_list_of_urls()
    
    ids = []
    for url in list_of_urls:
        ids.append(get_id(url).strip())
    id_str = ",".join(ids)

    info = process_response(id_str)
    total_duration = sum([i.duration for i in info])

    for i in info:
        print(i)

    print(f"Total duration: {total_duration / 60 :.2f} min(s)")

    if total_duration / 3600 > 1: # if more than 1h, show in hours too
        print(f"Total duration: {total_duration / 3600 :.2f} hour(s)")

run()