from pygooglenews import GoogleNews
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import difflib

gn = GoogleNews()

#s = gn.search(query="Parliament Budget Session updates | Logjam continues in Parliament, both Houses adjourned till 2 p.m. today")

def SearchNews(news):
    s = gn.search(query=news)
    stories=[]
    score=[]
    newsitem = s["entries"]
    for item in newsitem:
        story={
            'title': item.title,
            'link': item.link
        }
        #print(item.title)
        per = scoreFinder(news,item.title)
        score.append(per)
        stories.append(story)
    if(len(score)!=0):
        avg = sum(score)/len(score)
    else:
        avg = 0.00
    #print(round(avg,2))
    return stories,round(avg,2)

def scoreFinder(text1,text2):
    # Convert the texts into TF-IDF vectors
    #vectorizer = TfidfVectorizer()
    #vectors = vectorizer.fit_transform([text1, text2])

    # Calculate the cosine similarity between the vectors
    #similarity = cosine_similarity(vectors)
    #print(similarity[0][0])
    res = len(set(text1) and set(text2)) / float(len(set(text1) or set(text2))) * 100
    return res
    #result =  difflib.SequenceMatcher(a=text1.lower(), b=text2.lower())
    #print(result.ratio())
    #return result.ratio()

#SearchNews("Joe Biden’s options on TikTok narrow after Beijing pushes back")