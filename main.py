from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from textblob import TextBlob
import syllables
import textstat


global l
l = []

def read_input(filename):
    links = pd.read_csv(filename)
    for (i, j) in links.iterrows():
        url = j.to_string()
        url = url.split()
        #print(url)
        l.append(url[3])
        #extract_text(url[1],url[3])


def extract_text(id,link):
    txt = '.txt'
    filename = str(id) + txt
    driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
    driver.get(link)
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    text = soup.find_all("p")
    f = open(filename, "w")
    output = ''
    for para in text:
        output += para.text
    f.writelines(output)
    f.close()
    print(output)
    return (output)

def avg_sentence_len(text):
    sentences = text.split(".")  # split the text into a list of sentences.
    words = text.split(" ")  # split the input text into a list of separate words
    if (sentences[len(sentences) - 1] == ""):  # if the last value in sentences is an empty string
        average_sentence_length = len(words) / len(sentences) - 1
    else:
        average_sentence_length = len(words) / len(sentences)
    return average_sentence_length  # returning avg length of sentence



def text_analysis():
    path = 'D:\ML Class\HonorsCourse'
    dir_list = os.listdir(path)
    ps = []         #polarity score
    ss = []         #subjectivity score
    fn = []         #file id
    pos = []        #positive score
    neg = []        #negative score
    w = []          #word count
    ww = []         #syllables list
    fog = []        #fog index
    asl = []        #average sentence length
    #print(output.columns)
    for files in dir_list:
        if '.txt' in files:
            #print(files)
            f = open(files, "r")
            files = files.split(".")
            fn.append(files[0])
            text = f.read()
            a = avg_sentence_len(text)
            asl.append(a)
            fog_index = textstat.gunning_fog(text)
            fog.append(fog_index)
            words = text.split()
            word_count = len(words)
            w.append(word_count)
            s = syllables.estimate(text)
            ww.append(s)
            lower_case = text.lower()
            cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))
            tokenized_words = word_tokenize(cleaned_text, "english")

            final_words = []
            for word in tokenized_words:
                if word not in stopwords.words('english'):
                    final_words.append(word)

            #print(cleaned_text)
            blob = TextBlob(cleaned_text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            ps.append(polarity)
            ss.append(subjectivity)
            obj = SentimentIntensityAnalyzer()
            sent_score = obj.polarity_scores(cleaned_text)
            negative = sent_score.get('neg')
            neg.append(negative)
            positive = sent_score.get('pos')
            pos.append(positive)
            #print(negative)
            #print(type(sent_score))

    # print(ss)
    fn = [int(x) for x in fn]
    fn.sort()
    write_output(fn, pos, neg, ps,ss, asl, w, fog, ww)


def write_output(f, pos, neg, p, s, asl, w, fog, ww):
    output = pd.DataFrame(
        {'URL_ID': f,
         'URL': l,
         'POSITIVE SCORE': pos,
         'NEGATIVE SCORE': neg,
         'POLARITY SCORE': p,
         'SUBJECTIVITY SCORE': s,
         'AVG SENTENCE LENGTH': asl,
         'WORD COUNT': w,
         'FOG INDEX': fog,
         'SYLLABLE PER WORD': ww
         })
    print(output.iloc[0:7, 2:9])
    output.to_excel("output.xlsx")



read_input('Input.csv')
text_analysis()

