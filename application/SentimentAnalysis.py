import pandas as pd
from .CNNModel.T5 import translation
from .CNNModel.Bert import predict_and_result
from .Dataprepocessing import getEntity
from .CNNModel.OverallSentiment import predict_review
import os
import re


def extract_sentiment_counts(input_string):
    # Extract the positive number using regular expressions
    positive_match = re.search(r'positive\s+(\d+)', input_string)

    # Retrieve the positive number if match was found
    if positive_match:
        positive = int(positive_match.group(1))
    else:
        positive = 0

    # Extract the negative number using regular expressions
    negative_match = re.search(r'negative\s+(\d+)', input_string)

    # Retrieve the negative number if match was found
    if negative_match:
        negative = int(negative_match.group(1))
    else:
        negative = 0

    return positive, negative



def ReviewAnalysis(input_texts):
        (EnText,TranslateResult,count)=translation(input_texts)
        negnum=predict_review(EnText)
        OverallResult="Among all these reviews, "+str(negnum)+" of them is negative. So the rate of negative reviews is "+str(round(negnum/count * 100, 2))+"%."
        domainresult=pd.DataFrame()
        for item in EnText:
            processtext= getEntity(item)
            domainresult=pd.concat([domainresult,processtext],ignore_index=True)

        (entitysentiment,domainsentiment)=predict_and_result(domainresult)
        Newdomainsentiment=[]
        Newentitysentiment=[]
        dfentity = pd.DataFrame(columns=['Entity','Domain','Total amount', 'Negative sentences'])
        for text in domainsentiment:
            spiltdomain=text.split(',')
            domainname=spiltdomain[0]
            domainPos,domainNeg=extract_sentiment_counts(spiltdomain[1])
            total=domainPos+domainNeg
            domainresult="For the domain of "+domainname+", there are "+str(total)+" sentences related and the rate of negative feedback is "+str(round(domainNeg/total * 100, 2))+"%."
            Newdomainsentiment.append(domainresult)
            
        for text in entitysentiment:
            spiltentity=text.split(',')
            entityname=spiltentity[0]
            domainname=spiltentity[1]
            entityPos,entityNeg=extract_sentiment_counts(spiltentity[2])
            total=entityPos+entityNeg
            new_row = {'Entity': entityname, 'Domain':domainname,  'Total amount':total, 'Negative sentences':entityNeg}
            dfentity = pd.concat([dfentity, pd.DataFrame(new_row, index=[0])], ignore_index=True)
            
        df_sorted = dfentity.sort_values(by='Negative sentences', ascending=False)
            
        return TranslateResult,OverallResult,Newdomainsentiment,df_sorted

# current_dir=os.getcwd()
# parent_dir = os.path.dirname(current_dir)
# relative_path = "Datarelated\TestReview.xlsx"
# file_path = os.path.join(parent_dir, relative_path)
# os.chdir(parent_dir)
# df = pd.read_excel(file_path)
# inputtext=df.iloc[:, 0].values[1:].tolist()
# (TranslateResult,OverallResult,Newdomainsentiment,df_sorted)=ReviewAnalysis(inputtext)
# print(TranslateResult)
# print(OverallResult)
# print(Newdomainsentiment)
# print(df_sorted)
