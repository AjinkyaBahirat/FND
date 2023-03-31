from youtube_transcript_api import YouTubeTranscriptApi

def getTextFromYoutubeVideo(link):
    linkall = str(link)
    url = linkall.split("=")
    #print(url[1])
    srt = YouTubeTranscriptApi.get_transcript(url[1])
    #print(srt)
    #return srt;
    txt = ""
    for item in srt:
        txt = " ".join([txt,item["text"]])
    print(txt)
    return txt    
#getTextFromYoutubeVideo("https://www.youtube.com/watch?v=vosFtc4Jse8")
