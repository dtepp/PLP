import pandas as pd
import logging

logging.getLogger("transformers.modeling_utils").setLevel(logging.ERROR)
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import BertTokenizer
from keras.utils import pad_sequences
from keras.models import load_model
from concurrent.futures import ThreadPoolExecutor


def load_bert_model(device):
    model = BertForSequenceClassification.from_pretrained('bert-base-uncased')
    model.load_state_dict(torch.load('checkpoints/pytorch_model.bin'))
    model.to(device)
    return model


def load_cnn_model():
    return load_model('OverallS.h5')


def predict_bert(device, model, test_text):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
    inputs = tokenizer.encode_plus(
        test_text,
        add_special_tokens=True,
        max_length=64,
        padding='max_length',
        truncation=True,
        return_attention_mask=True,
        return_tensors='pt'
    )

    input_ids = inputs['input_ids'].to(device)
    attention_mask = inputs['attention_mask'].to(device)

    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)

    logits = outputs[0]
    predicted_label = torch.argmax(logits, dim=1).item()

    if predicted_label == 1:
        return 'negative'
    else:
        return 'positive'


def predict_cnn(model, test_text):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
    text_sequence = tokenizer.encode(test_text, add_special_tokens=True)
    X_input = pad_sequences([text_sequence], padding='post', maxlen=715)
    prediction = model(X_input)
    label = 1 if prediction[0][1] > 0.5 else 0
    if label == 1:
        return 'negative'
    else:
        return 'positive'


def predict_and_result(test_file):
    # If there's a GPU available...
    if torch.cuda.is_available():
        device = torch.device("cuda")
        print('There are %d GPU(s) available.' % torch.cuda.device_count())
        print('We will use the GPU:', torch.cuda.get_device_name(0))
    else:
        print('No GPU available, using the CPU instead.')
        device = torch.device("cpu")

    df = pd.read_excel(test_file)

    if device == torch.device("cpu"):
        cnn_model = load_cnn_model()
        with ThreadPoolExecutor() as executor:
            sent = list(executor.map(lambda x: predict_cnn(cnn_model, x), df['sentence']))
    else:
        bert_model = load_bert_model(device)
        with ThreadPoolExecutor() as executor:
            sent = list(executor.map(lambda x: predict_bert(bert_model, device, x), df['sentence']))

    df = df.assign(subsent=sent)

    # group by domain
    grouped_domain = df.groupby('domain')

    # look at each domain
    for domain, group_domain in grouped_domain:
        print(f"Domain: {domain}")

        # summarize the sentiment counts
        sentiment_counts_domain = group_domain['subsent'].value_counts()
        print("Sentiment counts for the domain:")
        print(sentiment_counts_domain)

        print()

        # group by entity
        grouped_entity = group_domain.groupby('entity')

        # look at each entity in this domain
        for entity, group_entity in grouped_entity:
            print(f"Entity: {entity}")

            # summarize the sentiment counts
            sentiment_counts_entity = group_entity['subsent'].value_counts()
            print("Sentiment counts for the entity:")
            print(sentiment_counts_entity)

            print()


test_file = 'Reviews.xlsx'
predict_and_result(test_file)
