from django.http import JsonResponse
from django.shortcuts import render
from .models import Question
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

dataframe = pd.read_csv('chatbot/static/csv/chatbot_data.csv')
vectorizer = TfidfVectorizer(ngram_range=(1, 3))
vec = vectorizer.fit_transform(dataframe['question'])

def home(request):
    if request.method == 'POST':
        if request.is_ajax():
            msg = request.POST.get('msg')
            my_question = vectorizer.transform([msg])
            cs = cosine_similarity(my_question, vec)
            rs = pd.Series(cs[0]).sort_values(ascending=0)
            rsi = rs.index[0]
            top = rs.iloc[0:1]
            x = top.values[0]

            if x < 0.3:
                answer = 'Sorry !!! I am not trained for that.......'
                if msg!= '':
                    question = Question(question_text=msg)
                    question.save()
            else:
                answer = dataframe.iloc[rsi]['answer']

            data = {'answer': answer}
            return JsonResponse(data)
    return render(request, 'home.html')
