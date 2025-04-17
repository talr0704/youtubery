from flask import Flask, render_template, request, send_file
import yt_dlp, os, uuid

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    uid = str(uuid.uuid4())
    output = os.path.join(DOWNLOAD_FOLDER, f"{uid}.%(ext)s")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        filepath = output.replace("%(ext)s", "mp3")
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return f"שגיאה: {e}", 500
