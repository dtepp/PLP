import pandas as pd
import logging
logging.getLogger("transformers.modeling_utils").setLevel(logging.ERROR)
import torch
from transformers import BertTokenizer, BertForSequenceClassification, AdamW, get_linear_schedule_with_warmup
from transformers import BertTokenizer


def predict_and_result(test_file):
    def predict_subreview(test_text):
        device = torch.device("cpu")

        # Load the model
        model = BertForSequenceClassification.from_pretrained('bert-base-uncased')
        model.load_state_dict(torch.load('checkpoints/pytorch_model.bin'))

        model.to(device)

        # Create a test dataset
        test_sentences = test_text

        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)

        # Tokenize the text
        inputs = tokenizer.encode_plus(
            test_text,
            add_special_tokens=True,
            max_length=64,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt'
        )

        # Move inputs to the device
        input_ids = inputs['input_ids'].to(device)
        attention_mask = inputs['attention_mask'].to(device)

        # Make the prediction
        with torch.no_grad():
            outputs = model(input_ids, attention_mask=attention_mask)

        logits = outputs[0]
        predicted_label = torch.argmax(logits, dim=1).item()

        p = 'positive'
        n = 'negative'
        if predicted_label == 1:
            return n
        else:
            return p

    # def predict_subreview(test_text):
    #     p = 'positive'
    #     n = 'negative'
    #     model_dp = load_model('OverallS.h5')
    #     tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
    #     text_sequence = tokenizer.encode(test_text, add_special_tokens=True)
    #     X_input = pad_sequences([text_sequence], padding='post', maxlen=715)
    #     prediction = model_dp(X_input)
    #     label = 1 if prediction[0][1] > 0.5 else 0
    #     if label == 1:
    #         return n
    #     else:
    #         return p

    df = pd.read_excel(test_file)

    sent = []
    for i in range(len(df)):
        sent.append(predict_subreview(df['sentence'][i]))
    df = df.assign(subsent=sent)
    # 根据 domain 列分组
    grouped_domain = df.groupby('domain')

    # 遍历每个 domain 分组
    for domain, group_domain in grouped_domain:
        print(f"Domain: {domain}")

        # 统计每个情感类别的数量
        sentiment_counts_domain = group_domain['subsent'].value_counts()
        print("Sentiment counts for the domain:")
        print(sentiment_counts_domain)

        print()

        # 根据 entity 列分组
        grouped_entity = group_domain.groupby('entity')

        # 遍历每个 entity 分组
        for entity, group_entity in grouped_entity:
            print(f"Entity: {entity}")

            # 统计每个情感类别的数量
            sentiment_counts_entity = group_entity['subsent'].value_counts()
            print("Sentiment counts for the entity:")
            print(sentiment_counts_entity)

            print()


test_file = 'Reviews.xlsx'
predict_and_result(test_file)
