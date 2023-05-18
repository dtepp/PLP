import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
import spacy
# nlp = spacy.load('en_core_web_sm')
from nltk.corpus import wordnet as wn
import pandas as pd


def get_all_hyponyms(synset, hyponyms_list):
    hyponyms = synset.hyponyms()
    if not hyponyms:
        return
    hyponyms_list.extend(hyponyms)
    for hyponym in hyponyms:
        get_all_hyponyms(hyponym, hyponyms_list)


def constructAsp():
    extra_food_words = ["noodle","seafood"]
    extra_env_words = ["floor", "toilet", "facility", "far", "near", "room", "location", "environment","pool"]
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
    all_env_words.remove("buffet")
    all_food_words.remove("special")
    all_cost_words.remove("fine")
    aspect = {
        "food": all_food_words,
        "service": ["staff", "service", "attendant", "cleaning", "guide", "instruction", "bookings", "manager","Housekeeping"],
        "environment": all_env_words,
        "price": all_cost_words,
    }
    return aspect


def aspectCat(sentence):
    aspect = constructAsp()
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
    return category, keywords


def sentenceProcess(originSentence):
    lemmatizer = WordNetLemmatizer()
    # Tokenize the sentence into words and determine their POS tags
    words = word_tokenize(originSentence)
    pos_tags = nltk.pos_tag(words)
    # Lemmatize each word based on its POS
    lemmatized_words = []
    for word, pos in pos_tags:
        if pos.startswith('N'):  # Noun
            lemma = lemmatizer.lemmatize(word)
            lemmatized_words.append(lemma)
        '''
        if pos.startswith('V'):  # Verb
            lemma = lemmatizer.lemmatize(word, pos='v')
        else:
            lemma = lemmatizer.lemmatize(word)
        lemmatized_words.append(lemma)
        '''

    # Join the lemmatized words back into a sentence
    lemmatized_sentence = " ".join(lemmatized_words)
    # print(type(lemmatized_sentence))

    return (lemmatized_sentence)


def divideIntoSentence(para):  # use to divide sentence
    words = nltk.word_tokenize(para)

    # Use the PunktSentenceTokenizer to perform sentence segmentation
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = sent_detector.tokenize(para)

    return sentences


def getEntity(text):
    text = text.replace(",", ".")
    sentences = nltk.sent_tokenize(text)
    df = pd.DataFrame(columns=["entity", "domain", "sentence"])
    for sent in sentences:
        processSentence = sentenceProcess(sent)
        tokens = nltk.word_tokenize(processSentence)

        categories, keywords = aspectCat(tokens)
        # print(sent, categories, keywords)
        for i in range(0, len(categories)):
            if categories[i] != "overall":
                data_dict = {"entity": keywords[i], "domain": categories[i], "sentence": sent}
                df = pd.concat([df, pd.DataFrame([data_dict])], ignore_index=True)

    return df
