import nltk
from nltk.wsd import lesk
from itertools import chain
from nltk.corpus import wordnet
nltk.download('wordnet')

# will check if any element of list1 exists in list2
def list_element_in_another_list(list1, list2):
    for i in list1:
        if i in list2:
            return True
    return False

# will return the Word Sense Disambiguation of word present in a sentence
def get_word_sense_disambiguation(sentence, word):
    wsd_dict = {"synset":"", "word":""}
    print('Word Sense Disambiguation of word: ')
    print(lesk(sentence.split(),str(word)))
    wsd_dict["synset"] = str(lesk(sentence.split(), str(word))).replace('Synset(\'', '').replace('\')', '')
    wsd_dict["word"] = str(lesk(sentence.split(), str(word)).lemmas()[0].name())
    return wsd_dict

# will return hypernyms of a word
def get_word_hypernyms(synset, word):
    word_hypernyms = []
    # Reference: https://stackoverflow.com/a/50983529/16185710
    for i,j in enumerate(wordnet.synsets(word)):
        if synset == j.name():
            # print('here: ', j.name())
            # print(j.hypernyms())
            print('Hypernyms:', ', '.join(list(chain(*[l.lemma_names() for l in j.hypernyms()]))))
            word_hypernyms = list(chain(*[l.lemma_names() for l in j.hypernyms()])).copy()
    print('word hypernyms: ', word_hypernyms)
    return word_hypernyms
        
# will return generelised words for a given word according to given TERMS
def get_generelised_words(word, hypernyms, TERMS):
    generelised_words = []
    if str(word) in TERMS:
        generelised_words.append(str(word))
    elif list_element_in_another_list(hypernyms,TERMS):
        for v in hypernyms:
            if v in TERMS:
                generelised_words.append(v)
    return generelised_words

# wil return most similar verb for a given verb according to given TERMS using given spacy's model
def get_most_similar_verb(verb, TERMS, spacy_model):
    print('getting most similar verb for: ', verb)
    most_similar_verb = ""
    max_verb_similarity =0
    doc_verb = spacy_model(verb)    
    for terms_v in TERMS:
        # print('verb in term: ', terms_v)
        for token in doc_verb:
            tokens_spacy = spacy_model(terms_v + " " + verb)
            token1, token2 = tokens_spacy[0], tokens_spacy[1] 
            # print(tokens_spacy[0], tokens_spacy[1] )
            # print("Similarity:", token1.similarity(token2)) 
            if token1.similarity(token2) > max_verb_similarity:
                max_verb_similarity = token1.similarity(token2)
                most_similar_verb = terms_v
    return most_similar_verb