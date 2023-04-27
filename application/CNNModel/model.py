import pandas as pd
import numpy as np
from keras.utils import pad_sequences
from flask import Flask, request, jsonify
from keras.models import load_model
import pickle

maxlen = 689  # 限制文本长度

def load_trained_model(model_path):
    model = load_model(model_path)
    return model

def load_tokenizer(tokenizer_path):
    with open(tokenizer_path, 'rb') as handle:
        tokenizer = pickle.load(handle)
    return tokenizer

model=load_trained_model("./application/CNNModel/model.h5")
tokenizer=load_tokenizer("./application/CNNModel/tokenizer.pickle")

def predict_review(text):
    tokenizer.fit_on_texts(text)
    text_sequence = tokenizer.texts_to_sequences([text])
    X_input = pad_sequences(text_sequence, padding='post', maxlen=689)
    prediction = model.predict(X_input)
    label = 1 if prediction[0][1] > 0.5 else 0
    if label == 1:
        #print("The text is classified as: Negative")
        return 0
    else:
        #print("The text is classified as: Positive")
        return 1

