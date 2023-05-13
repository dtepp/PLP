# pip install transformers
import torch
from transformers import BertTokenizer
from keras.utils import pad_sequences

def predict_review(text):
    model_dp = torch.load('model_dp.pt')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
    text_sequence = tokenizer.encode(text, add_special_tokens=True)
    X_input = pad_sequences([text_sequence], padding='post', maxlen=715)
    prediction = model_dp(X_input)
    label = 1 if prediction[0][1] > 0.5 else 0
    if label == 1:
        print("The text is classified as: Negative")
    else:
        print("The text is classified as: Positive")

# test_data = ["This hotel was amazing! The staff was friendly and the room was clean and comfortable.",
#              "I had a terrible experience at this hotel. The room was dirty and the staff was unhelpful.",
#              "The food at the restaurant was delicious and the service was excellent.",
#              "The location of the hotel was perfect for my needs and the room was spacious and well-appointed."]
#
# for text in test_data:
#     predict_review(text)