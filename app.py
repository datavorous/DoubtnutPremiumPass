from flask import Flask, request, render_template
import requests
from googlesearch import search

app = Flask(__name__)

# Function to get Doubtnut links using Google search dork
def get_doubtnut_links(query):
    dork = f"doubtnut {query}"
    search_results = search(dork)
    doubtnut_links = [result for result in search_results if 'doubtnut.com' in result]
    return doubtnut_links

# Function to fetch video link from a Doubtnut URL
def get_doubtnut_video_link(full_url):
    question_id = full_url.split('/')[-1]
    url = "https://api.doubtnut.com/v1/answers/video-resource"
    params = {
        "questionId": question_id,
        "studentId": "-37",
        "page": "WEB_VIDEO"
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": "https://www.doubtnut.com",
        "referer": "https://www.doubtnut.com/",
        "user-agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        video_resource = data.get('data', {}).get('resource', None)
        if video_resource:
            video_url = f"https://videos.doubtnut.com/{video_resource}"
            return video_url
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    video_url = None
    search_results = None

    if request.method == 'POST':
        query = request.form['url']
        
        # Check if the query is a Doubtnut link
        if 'doubtnut.com' in query:
            # Get video solution if it's a direct Doubtnut link
            video_url = get_doubtnut_video_link(query)
        else:
            # Fetch Doubtnut links for search queries
            doubtnut_links = get_doubtnut_links(query)
            search_results = []
            for index, link in enumerate(doubtnut_links, start=1):
                video_url = get_doubtnut_video_link(link)
                search_results.append({
                    'link': link,
                    'video_url': video_url
                })

    return render_template('index.html', video_url=video_url, search_results=search_results)

if __name__ == '__main__':
    app.run(debug=True)
