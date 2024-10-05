from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    video_url = None  # Initialize the video URL variable
    if request.method == 'POST':
        full_url = request.form['url']
        question_id = full_url.split('/')[-1]  # Extract question ID from the URL
        
        # Define the API URL and headers
        api_url = "https://api.doubtnut.com/v1/answers/video-resource"
        params = {
            "questionId": question_id,
            "studentId": "null",
            "page": "WEB_VIDEO"
        }
        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "origin": "https://www.doubtnut.com",
            "referer": "https://www.doubtnut.com/",
            "sec-ch-ua": '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
        }
        
        # Send the GET request to the API
        response = requests.get(api_url, headers=headers, params=params)
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            video_resource = data.get('data', {}).get('resource', None)
            if video_resource:
                # Construct the video URL
                video_url = f"https://videos.doubtnut.com/{video_resource}"
            else:
                video_url = "Video resource not found."
        else:
            video_url = f"Failed to retrieve data. Status code: {response.status_code}"

    return render_template('index.html', video_url=video_url)

if __name__ == '__main__':
    app.run(debug=True)
