import torch
from transformers import AutoTokenizer, MT5ForConditionalGeneration
from googletrans import Translator


def translation(input_texts):
    def encode_str(text, tokenizer, seq_len):
        """ Tokenize, pad to max length and encode to ids
          Returns tensor with token ids """
        input_ids = tokenizer.encode(
            text=text,
            return_tensors='pt',
            padding='max_length',
            truncation=True,
            max_length=seq_len)

        return input_ids[0]

    max_inp_seq_len = 40
    max_tar_seq_len = 3

    tokenizer = AutoTokenizer.from_pretrained('google/mt5-small')
    LANG_TOKEN_MAPPING = {
        'identify language': '<idf.lang>'
    }
    special_tokens_dict = {'additional_special_tokens': list(LANG_TOKEN_MAPPING.values())}

    # Adding the special tokens to the tokenizer
    tokenizer.add_special_tokens(special_tokens_dict)

    model = MT5ForConditionalGeneration.from_pretrained('google/mt5-small')
    model.resize_token_embeddings(len(tokenizer))
    model_t5 = 'Step-5623_checkpoint_lang_pred.pt'
    model.load_state_dict(torch.load(model_t5, map_location=torch.device('cpu')))
    final=[]
    i = 0
    count=len(input_texts)
    for input_text in input_texts:
        input_ids = encode_str(input_text, tokenizer, max_inp_seq_len)

        # Generate output
        output_ids = model.generate(input_ids=input_ids.unsqueeze(0),
                                    max_length=max_tar_seq_len,
                                    num_beams=10,
                                    num_return_sequences=1,
                                    length_penalty=1,
                                    no_repeat_ngram_size=2)

        # Decode output
        output_text = tokenizer.decode(output_ids.squeeze(), skip_special_tokens=True)
       
        if output_text != 'en':
            i = i + 1
            translator = Translator(service_urls=['translate.google.com'])
            trans = translator.translate(input_text, dest='en')
            # Translated text
            final.append(trans.text)
        else:
            final.append(input_text)
 
    result_text = "There are overall {} reviews in the file, {} of them are not in English.".format(count, i)
    return final,result_text,count

# Example usage with a list of input texts
# input_texts = ["你好我是Lily", "I am Chinese", "我是中国人", "このホテルはとても良いと思います"]
# translation(input_texts)
