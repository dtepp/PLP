import nltk
nltk.download('wordnet')
nltk.download('punkt')
import spacy
#nlp = spacy.load('en_core_web_sm')
from nltk.corpus import wordnet as wn
import pandas as pd


def get_all_hyponyms(synset, hyponyms_list):
    hyponyms = synset.hyponyms()
    if not hyponyms:
        return
    hyponyms_list.extend(hyponyms)
    for hyponym in hyponyms:
        get_all_hyponyms(hyponym, hyponyms_list)


extra_food_words = ["noodle"]
extra_env_words = ["floor","toilet","facility"]
food_synset = wn.synset('food.n.01')
hyponyms_list = []
get_all_hyponyms(food_synset, hyponyms_list)

# 将所有下位词存储在一个列表中
all_food_words = [synset.name().split('.')[0] for synset in [food_synset] + hyponyms_list]
all_food_words.extend(extra_food_words)
cost_synset = wn.synset('cost.n.01')
hyponyms_list = []
get_all_hyponyms(cost_synset, hyponyms_list)

all_cost_words = [synset.name().split('.')[0] for synset in [cost_synset] + hyponyms_list]
acc_synset = wn.synset('furniture.n.01')
hyponyms_list = []
get_all_hyponyms(acc_synset, hyponyms_list)

all_env_words = [synset.name().split('.')[0] for synset in [acc_synset] + hyponyms_list]
all_env_words.extend(extra_env_words)
aspect = {
    "food":all_food_words,
    "service": ["staff", "service", "attendant", "cleaning", "guide", "instruction", "bookings"],
    "environment": all_env_words,
    "price": all_cost_words,
}

def aspectCat(sentence):
    category = []
    keywords = []
    for tok in sentence:
        tok = tok.lower()
        for key, val in aspect.items():
            if tok in val:
                keywords.append(tok)
                category.append(key)
    if len(category) == 0:
        category.append("overall")
    return category,keywords



def getEntity(text):
    text = text.replace(",", ".")
    sentences = nltk.sent_tokenize(text)
    df = pd.DataFrame(columns=["entity", "domain", "sentence"])
    for sent in sentences:

        tokens = nltk.word_tokenize(sent)
        categories, keywords = aspectCat(tokens)
        print(sent, categories, keywords)
        data_dict = {"entity": keywords, "domain": categories, "sentence": sent}
        df = df.append(data_dict, ignore_index=True)
    return  df