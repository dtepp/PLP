import pandas as pd
from CNNModel.T5 import translation
from CNNModel.Bert import predict_and_result
from Dataprepocessing import getEntity
from CNNModel.OverallSentiment import predict_review
import os

def ReviewAnalysis(input_texts):
        OverallNeg=0
        (EnText,TranslateResult,count)=translation(input_texts)
        negnum=predict_review(EnText)
        domainresult=pd.DataFrame()
        for item in EnText:
            processtext= getEntity(item)
            domainresult=pd.concat([domainresult,processtext],ignore_index=True)

        (domainsentiment,entitysentiment)=predict_and_result(domainresult)
        return TranslateResult,negnum,domainsentiment,entitysentiment

current_dir=os.getcwd()
parent_dir = os.path.dirname(current_dir)
relative_path = "Datarelated\TestReview.xlsx"
file_path = os.path.join(parent_dir, relative_path)
os.chdir(parent_dir)
df = pd.read_excel(file_path)
inputtext=df['Review Comment'].tolist()

(TranslateResult,negnum,domainsentiment,entitysentiment)=ReviewAnalysis(inputtext)

print(domainsentiment)
print(entitysentiment)
# print(TranslateResult)
# print(OverallNeg)
# print(domainresult)