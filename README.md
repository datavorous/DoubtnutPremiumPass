# Doubtnut-Premium Crack
Won't pay 5 rupees/day. Reverse engineered Doubtnut's API

https://doubtnut-dxdm.onrender.com/

<img src="https://preview.redd.it/literally-me-ll-alakh-pandey-edition-v0-32vc64u5p6rd1.jpg?width=447&format=pjpg&auto=webp&s=ea8c4bad57417ca255904963c5e0830072de039b">

## 1. Imports and Setup

```python
from flask import Flask, request, render_template
import requests
from googlesearch import search

app = Flask(__name__)
```

This section imports necessary libraries:
- Flask for web application development
- requests for making HTTP requests
- googlesearch for performing Google searches

It also initializes the Flask application.

## 2. Doubtnut Link Retrieval

```python
def get_doubtnut_links(query):
    dork = f"doubtnut {query}"
    search_results = search(dork)
    doubtnut_links = [result for result in search_results if 'doubtnut.com' in result]
    return doubtnut_links
```

This function:
- Takes a user query
- Performs a Google search with "doubtnut" prepended to the query
- Filters the results to include only Doubtnut links
- Returns the list of Doubtnut links

## 3. Video Link Extraction

```python
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
```

This function:
- Extracts the question ID from the Doubtnut URL
- Sends a GET request to Doubtnut's API with specific parameters and headers
- Parses the JSON response to extract the video resource
- Constructs and returns the full video URL if available

## 4. Flask Route Handler

```python
@app.route('/', methods=['GET', 'POST'])
def index():
    video_url = None
    search_results = None
    if request.method == 'POST':
        query = request.form['url']
        
        if 'doubtnut.com' in query:
            video_url = get_doubtnut_video_link(query)
        else:
            doubtnut_links = get_doubtnut_links(query)
            search_results = []
            for index, link in enumerate(doubtnut_links, start=1):
                video_url = get_doubtnut_video_link(link)
                search_results.append({
                    'link': link,
                    'video_url': video_url
                })
    return render_template('index.html', video_url=video_url, search_results=search_results)
```

This route handler:
- Processes both GET and POST requests
- For POST requests:
  - If the query is a Doubtnut link, it directly fetches the video URL
  - If not, it searches for Doubtnut links and fetches video URLs for each
- Renders the 'index.html' template with the results

## 5. Application Execution

```python
if __name__ == '__main__':
    app.run(debug=True)
```

This snippet runs the Flask application in debug mode when the script is executed directly.
