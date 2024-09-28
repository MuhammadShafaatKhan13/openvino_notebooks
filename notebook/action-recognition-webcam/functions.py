import nltk
from nltk.wsd import lesk
from itertools import chain
from nltk.corpus import wordnet
import pyinflect
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
            print('here: ', j.name())
            print(j.hypernyms())
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
    most_similar_verb = ""
    max_verb_similarity =0
                    
    for terms_v in TERMS:
        # both verbs needed to be in same form as the form of verb provided in argument
        # to get better similarity result
        # print('verb: ', verb)
        doc_verb = spacy_model(verb)
        doc_tag= ""
        for token in doc_verb:
            doc_tag = token.tag_
            # print( token.tag_)
            doc_term_v = spacy_model(terms_v)
            # print(doc_term_v[0]._.inflect(doc_tag))
            verb_in_provided_form = doc_term_v[0]._.inflect(doc_tag)
            tokens_spacy = spacy_model(verb_in_provided_form + " " + verb)
            token1, token2 = tokens_spacy[0], tokens_spacy[1] 
            # print(tokens_spacy[0], tokens_spacy[1] )
            # print("Similarity:", token1.similarity(token2)) 
            if token1.similarity(token2) > max_verb_similarity:
                max_verb_similarity = token1.similarity(token2)
                most_similar_verb = verb_in_provided_form
    return most_similar_verb