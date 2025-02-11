from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return "Video Downloader API is running!"

@app.route('/download', methods=['POST'])
def download():
    try:
        url = request.form.get('url')
        if not url:
            return jsonify({'error': 'Please provide a URL'}), 400

        ydl_opts = {
            'format': 'best[ext=mp4]',
            'quiet': True,
            'no_warnings': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
        return jsonify({
            'title': info.get('title', 'Unknown'),
            'url': info.get('url')
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Vercel serverless function entry point
def handler(request, response):
    return app(request, response)
