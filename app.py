# save this as app.py
from flask import Flask, flash, request, redirect, url_for, render_template
from markupsafe import escape
import re
import string
import os
from werkzeug.utils import secure_filename
import easyocr
import videototext
import chatgpt
import test
import pyrebase

config ={
    "apiKey": "AIzaSyCztwgZDKmJPfYh7KGSGtuYMknpyWzv5C4",
    "authDomain": "fndtry-fd145.firebaseapp.com",
    "projectId": "fndtry-fd145",
    "storageBucket": "fndtry-fd145.appspot.com",
    "messagingSenderId": "1074974327122",
    "appId": "1:1074974327122:web:e954c8083c55280ff77a8b",
    "serviceAccount": "serviceAccount.json",
    "databaseURL": "https://fndtry-fd145-default-rtdb.firebaseio.com"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

#vectorization = pickle.load(open("Vectorization.pkl", "rb"))
#LR = pickle.load(open("LRModel.pkl", "rb"))
#DT = pickle.load(open("DTModel.pkl", "rb"))
#GBC = pickle.load(open("GBCModel.pkl", "rb"))
#RFC = pickle.load(open("RFCModel.pkl", "rb"))
#SVC = pickle.load(open("SVCModel.pkl", "rb"))

#newsapi = NewsApiClient(api_key='0bafa3367a2d4d6286889bce3bd16e61')


app = Flask(__name__)
app.debug = True
UPLOAD_FOLDER = 'static/uploads/'
 
app.secret_key = "mlproject"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        news = str(request.form['news'])
        #strresult = manual_testing(news)
        #result = re.findall(r'\w+', news)[:10]
        #result = " ".join(result)
        #articals,links = findNewsSimilar(result)        
        #return render_template("index.html",lr = strresult[0] ,dt = strresult[1],gbc = strresult[2],rfc = strresult[3], svc = strresult[4],articals=articals,links=links)
        result,avg = test.SearchNews(news)
        return render_template("index.html",res=result,avg=avg)
    else:
        return render_template("index.html")

def wordopt(text):
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub("\\W"," ",text) 
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)    
    return text

def output_lable(n):
    if n == 0:
        return "Fake News"
    elif n == 1:
        return "True News"

def imageToText(image):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image,paragraph="False",detail = 0)
    print(result[0])
    return result[0]


#def manual_testing(news):
#    testing_news = {"text":[news]}
#    new_def_test = pd.DataFrame(testing_news)
#    new_def_test["text"] = new_def_test["text"].apply(wordopt) 
#    new_x_test = new_def_test["text"]
#    new_xv_test = vectorization.transform(new_x_test)
#    pred_LR = LR.predict(new_xv_test)
#    pred_DT = DT.predict(new_xv_test)
#    pred_GBC = GBC.predict(new_xv_test)
#    pred_RFC = RFC.predict(new_xv_test)
#    pred_SVC = SVC.predict(new_xv_test)
#    result = "\n\nLR Prediction: {} \nDT Prediction: {} \nGBC Prediction: {} \nRFC Prediction: {} \nSVC Prediction: {}".format(output_lable(pred_LR[0]), 
 #                                                                                                             output_lable(pred_DT[0]), 
 #                                                                                                             output_lable(pred_GBC[0]), 
 #                                                                                                             output_lable(pred_RFC[0]), 
 #                                                                                                             output_lable(pred_SVC[0]))
 #   print(result)
 #   arrRes=[output_lable(pred_LR[0]),output_lable(pred_DT[0]),output_lable(pred_GBC[0]),output_lable(pred_RFC[0]),output_lable(pred_SVC[0])]
 #   return arrRes

#def findNewsSimilar(news):
#    articles = newsapi.get_everything(q=news,sort_by='relevancy',language='en')
 #   list1=[]
  #  list2=[]
   # for article in articles['articles']:
    #    list1.append(article['title'])
     #   list2.append(article['url'])
      #  print(article['title'])
    #return list1,list2


@app.route('/image', methods=['GET', 'POST'])
def image():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            storage.child(filename).put(file)
            url = storage.child(filename).get_url(None)
            print(url)
            #print('upload_image filename: ' + filename)
            flash('Image successfully uploaded Waiting for results..!')
            #path = 'static/uploads/{}'.format(filename)
            text = imageToText(url)
            result,avg = test.SearchNews(text)
            return render_template("image.html",res=result,avg=avg)    
        else:
            flash('Allowed image types are - png, jpg, jpeg, gif')
            return redirect(request.url)
    else:
        return render_template('image.html')

@app.route('/video', methods=['GET', 'POST'])
def video():
    if request.method == 'POST':
        link = str(request.form['link'])
        srt = videototext.getTextFromYoutubeVideo(link)
        result,avg = test.SearchNews(srt)
        return render_template("video.html",res=result,avg=avg)
    else:
        return render_template("video.html")
    

@app.route('/factcheck', methods=['GET', 'POST'])
def factcheck():
    if request.method == 'POST':
        fact = str(request.form['fact'])
        res = chatgpt.getResultChatGPT(fact)
        return render_template("factcheck.html",result=res)
    else:
        return render_template("factcheck.html")

if __name__ == '__main__':
    app.run()
