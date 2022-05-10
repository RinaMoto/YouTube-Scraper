import scrapetube
from flask import Flask, request
import json 

app = Flask(__name__)

@app.route('/videos', methods=['POST'])
def get_vids():
    artist = request.get_json()
    urls = []
    try:
        channels = scrapetube.get_search(
            query=artist['name'],
            limit=1,
            results_type="channel"
        )

        for channel in channels:
            channel_id = channel['channelId']
            videos = scrapetube.get_channel(
                channel_id=f"{channel_id}", 
                limit=3
            )
            for video in videos:
                urls.append({'url': 'https://www.youtube.com/watch?v=' + video['videoId']})
            break
    except:
        return "Could not get Youtube channel of artist", 400
    
    print(json.dumps(urls))
    return json.dumps(urls), 200, {'ContentType':'application/json'}

if __name__=="__main__":
    app.run(threaded=True, port=5000)