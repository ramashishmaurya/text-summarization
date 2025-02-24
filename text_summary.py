import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import pandas  as pd 
import numpy

text = """Learning is a lifelong journey that expands our knowledge 
and skills. It helps us adapt to changing environments and stay relevant in a fast paced world.
With continuous learning, we develop problem-solving abilities and critical thinking skills.
Education opens doors to better opportunities, career growth, and personal fulfillment. Reading books, taking online courses,
or engaging in discussions all contribute to intellectual growth.
The ability to learn keeps our minds sharp and active. Ultimately, knowledge empowers us to make informed decisions and shape a better future."""



def summarizer(rowdocs):
    stopwords = list(STOP_WORDS)

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(rowdocs)
    # print(type(doc))

    #  convert into tokens 
    tokens = [ token.text for token in doc ]
    # print(tokens)


    # there will not be any functuation and stopwords 
    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text]+=1
    # print(word_freq)
                
    max_freq =max(word_freq.values())

    # print(max_freq)


    # normalized data by dividing the frequency of entire data
    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq

    # print(word_freq)
    sent_tokens = [ sent for sent in  doc.sents]

    # print(sent_tokens)

    sent_score = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_score.keys():
                    sent_score[sent] =word_freq[word.text]
                else:
                    sent_score[sent]+=word_freq[word.text]

    # print(sent_score)
    # print(sent_score.keys())
    # print(sent)

    select_len = int(len(sent_score)*0.3)

    summary =nlargest(select_len ,sent_score ,key=sent_score.get )

    # print all the values of top 3 order 
    # print(summary)

    df = pd.DataFrame(sent_score.items() , columns=['sentences' , 'score'])
    # print(df)

    final_summary = [word.text for word in summary]
    summary = " ".join(final_summary)

    # print(summary)/
    # print(len(text.split(' ')))
    # print(len(summary.split(' ')))
    return summary , doc , len(rowdocs.split(' ')) , len(summary.split(' '))

# n ="hi my name is ashish what is your name"
# print(summarizer(n))



    



