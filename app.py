from pytube import YouTube
from flask import Flask,render_template,request,redirect,session,send_file
from flask.helpers import url_for
from io import BytesIO

# link=""
app = Flask(__name__)
app.config['SECRET_KEY']='6545fgn738jdjjj3ed93kdklep'
@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        session['link']=request.form.get('inputTxt')
        try:
            url=YouTube(session['link'])
            url.check_availability()
        except:
            return render_template('error.html')
        return render_template('download.html',url=url)

    return render_template('index.html')

@app.route("/download", methods = ["GET", "POST"])
def download_video():
    if request.method == "POST":
        buffer = BytesIO()
        url = YouTube(session['link'])
        itag = request.form.get("itag")
        video = url.streams.get_by_itag(itag)
        video.stream_to_buffer(buffer)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name="myYouTube.mp4", mimetype="video/mp4")
    return redirect(url_for("index"))

  
app.run(debug=True)