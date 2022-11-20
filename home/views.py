from django.shortcuts import render
import random
import pandas as pd
import pickle
import statistics
from statistics import mode
from sklearn.feature_extraction.text import TfidfVectorizer
so_vectorizer = pickle.load(open("models/so_vectorizer.pickle", "rb"))
red_vectorizer = pickle.load(open("models/red_vectorizer.pickle", "rb"))
quora_vectorizer = pickle.load(open("models/quora_vectorizer.pickle", "rb"))

model1 = pickle.load(open("models/naive.sav", 'rb'))
model2 = pickle.load(open("models/mlp.sav", 'rb'))
model3 = pickle.load(open("models/svc.sav", 'rb'))
model4 = pickle.load(open("models/rfc.sav", 'rb'))
model5= pickle.load(open("models/qda.sav", 'rb'))

# Create your views here.
def landing(request):
    return render(request, "home.html")

def home(request):
     return render(request, "home.html")

def dashboard(request):
    if request.method == "POST":
        question = request.POST.get("question")
        platform = request.POST.get("platform")
        model = request.POST.get("model")
    
    if platform=="StackOverflow":
        ques_array = so_vectorizer.transform(pd.Series(question)).toarray()
    elif platform=="Quora":
        ques_array = quora_vectorizer.transform(pd.Series(question)).toarray()
    elif platform=="Reddit":
        ques_array = red_vectorizer.transform(pd.Series(question)).toarray()

    models = {"Model1":"Gaussian Naive Bayes", "Model2":"MLP Classifier", "Model3":"SVC Classifier","Model4":"Random Forest Classifier", "Model5":"Quadratic Discriminant Analysis", "Ensemble1":"Ensemble 1","Ensemble2":"Ensemble 2"}
    categories = {0:'open', 1:'close'}
    model_lst = [model1,model2,model3,model4,model5]

    if model =="Model1":
        ans_cat = model1.predict(ques_array)
        if ans_cat[0]!=0:
            ans_cat[0]=1
        final_ans = categories[ans_cat[0]]
        final_model = models[model]
    elif model =="Model2":
        ans_cat = model2.predict(ques_array)
        if ans_cat[0]!=0:
            ans_cat[0]=1
        final_ans = categories[ans_cat[0]]
        final_model = models[model]
    elif model =="Model3":
        ans_cat = model3.predict(ques_array)
        if ans_cat[0]!=0:
            ans_cat[0]=1
        final_ans = categories[ans_cat[0]]
        final_model = models[model]
    elif model =="Model4":
        ans_cat = model4.predict(ques_array)
        if ans_cat[0]!=0:
            ans_cat[0]=1
        final_ans = categories[ans_cat[0]]
        final_model = models[model]
    elif model =="Model5":
        ans_cat = model5.predict(ques_array)
        if ans_cat[0]!=0:
            ans_cat[0]=1
        final_ans = categories[ans_cat[0]]
        final_model = models[model]

    elif model =="Ensemble1":        # simple max voting
        ans_cat_lst = []
        for model in model_lst:
            ans_cat = model1.predict(ques_array)
            if ans_cat[0]!=0:
                ans_cat[0]=1
            ans_cat_lst.append(ans_cat)

        ans_cat_final = mode(ans_cat_lst)
        final_ans = categories[ans_cat_final]
        final_model = models[model]

    
    elif model =="Ensemble2":          # weighted sum voting
        wts = [1,0,0,0,0]            # sum should be 1
        ans_cat_lst = []
        wt_cnt = 0
        for model in model_lst:
            ans_cat = model1.predict(ques_array)
            if ans_cat[0]!=0:
                ans_cat[0]=1
            ans_cat = ans_cat*wts[wt_cnt]
            wt_cnt+=1
            ans_cat_lst.append(ans_cat)

        ans_cat_final = sum(ans_cat_lst)
        if ans_cat_final >= 0.5:
            final_ans = "close"
        else:
            final_ans = "open"
        final_model = models[model]

    context = {"question": question, "platform":platform ,"model":final_model, "ans_catog":final_ans}       
    
    return render(request, "dashboard.html",context)
