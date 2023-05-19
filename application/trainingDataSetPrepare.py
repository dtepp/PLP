import pandas as pd
import nltk
from nltk.tokenize import WordPunctTokenizer
import numpy as np
from application.Dataprepocessing import getEntity
from nnsplit import NNSplit
from textblob import TextBlob


# read the original Excel file
df = pd.read_excel('/content/drive/MyDrive/data/Hotel_Reviews.xlsx')

# calculate the number of rows per file
num_rows = len(df)
rows_per_file = num_rows // 20  # assuming you want to split into 20 files evenly
# split the original dataframe into multiple dataframes based on rows
dfs = [df[i:i+rows_per_file] for i in range(0, num_rows, rows_per_file)]

# save each dataframe as a separate Excel file
for i, df_split in enumerate(dfs):
    filename = f'split_file_{i+1}.xlsx'
    df_split.to_excel(filename, index=False)
import shutil


src = f'split_file_21.xlsx'  # path to the split file
dst = '/content/drive/MyDrive/data/' + src  # path to the destination directory
shutil.move(src, dst)  # move the file

splitter = NNSplit.load("en")


def analyze_text_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    if sentiment > 0:
        return "positive"
    elif sentiment < 0:
        return "negative"
    else:
        return "neutral"

# Testing
text = "This is a great movie!"
result = analyze_text_sentiment(text)
print(result)

df = pd.read_excel('/content/drive/MyDrive/data/split_file_3.xlsx')
data = df.values
empty = ["No Negative", " Nothing ", "No Positive"]
result = pd.DataFrame()
for i in range(0, len(data)):
    # print(data[i][6]+data[i][9])
    print(i)
    currentDF = pd.DataFrame()
    negative = ""
    positive = ""
    noDF = pd.DataFrame()
    poDF = pd.DataFrame()
    try:
        if data[i][6] not in empty:
            negative = data[i][6]
            Nsplits = splitter.split([negative])[0]
            for sentence in Nsplits:
                Entityresult = getEntity(str(sentence))
                noDF = pd.concat([noDF, Entityresult], ignore_index=True)
                # noDF = noDF.assign(sentiment="negative")
                # print(noDF)

        if data[i][9] not in empty:
            positive = data[i][9]
            Psplits = splitter.split([positive])[0]
            for sentence in Psplits:
                Entityresult = getEntity(str(sentence))
                poDF = pd.concat([poDF, Entityresult], ignore_index=True)
                # poDF = poDF.assign(sentiment="positive")
                # print(poDF)
    except Exception:

        continue

    currentDF = pd.concat([currentDF, noDF], ignore_index=True)
    currentDF = pd.concat([currentDF, poDF], ignore_index=True)
    overallComment = negative + positive
    currentDF = currentDF.assign(comment=overallComment)
    result = pd.concat([result, currentDF], ignore_index=True)
    print(result)
result = result.assign(sentiment="")

for i in range(0, len(result)):
    sentence = result["sentence"][i]

    scores = analyze_text_sentiment(sentence)
    print(scores)
    result["sentiment"][i] = scores

result.to_excel('/content/drive/MyDrive/data/split3.xlsx', index=False)