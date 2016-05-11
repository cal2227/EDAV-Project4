#!/usr/bin/env python

from datetime import datetime
import json

import nltk
from nltk import word_tokenize as nltk_word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import inaugural

from readability import Readability

suas_fname = "../data/State_of_the_Union_Addresses_1790-2016.txt"
enriched_suas_fname = "../data/enriched_suas.json"
reading_levels_fname = "../data/suas_with_reading_levels.json"
with_presidents_fname = "../data/suas_with_presidents.json"
with_elections_fname = "../data/suas_with_elections.json"
with_word_sets_fname = "../data/suas_with_word_sets.json"

inaugurals_fname = "../data/inaugural.json"
enriched_inaugurals = "../data/enriched_inaugurals.json"
inaugurals_reading_levels_fname = "../data/inaugurals_with_reading_levels.json"

sua_delim = "***"

def split_by_sua(fname):
    
    def without_intro(fname):
        with open(fname, 'r') as f:
            in_intro = True
            for line in f:
                if in_intro:
                    if line.strip() == sua_delim:
                        in_intro = False
                else:
                    yield line
    
    def sua_lines(lines):
        sua = []
        for line in lines:
            if line.strip() == sua_delim:
                yield sua
                sua = []
            elif line:
                sua.append(line)
        yield sua
        
    
    for j, sua in enumerate(sua_lines(without_intro(fname))):
        metadata_offset = 0
        for i, line in enumerate(sua):
            if "State of the Union" in line or "Address Before a Joint Session" in line:
                metadata_offset = i
                break        
        
        president = sua[metadata_offset+1].strip()
        dt = datetime.strptime(sua[metadata_offset+2].strip(), '%B %d, %Y')
        year = dt.year     
        
        yield {
            'president': president, 
            'year': int(year),
            'text': ''.join(sua[metadata_offset+3:]).replace('\n', ' ').strip()
        }

def get_suas():
    return [sua for sua in split_by_sua(suas_fname)]

def get_suas_1970():
    return [sua for sua in split_by_sua(suas_fname) if sua['year'] >= 1970]

def get_years(suas):
    return [sua['year'] for sua in suas]

def get_presidents(suas):
    return [sua['president'] for sua in suas]

def get_texts(suas):
    return [sua['text'] for sua in suas]

reading_level_keys = ['GunningFogIndex', 'ColemanLiauIndex', 'LIX', 'SMOGIndex', \
                      'FleschKincaidGradeLevel', 'ARI', 'FleschReadingEase', 'RIX']

def all_reading_levels(text):
    rd = Readability(text)
    return {
        'ARI': rd.ARI(),
        'FleschReadingEase': rd.FleschReadingEase(),
        'FleschKincaidGradeLevel': rd.FleschKincaidGradeLevel(),
        'GunningFogIndex': rd.GunningFogIndex(),
        'SMOGIndex': rd.SMOGIndex(),
        'ColemanLiauIndex': rd.ColemanLiauIndex(),
        'LIX': rd.LIX(),
        'RIX': rd.RIX(),
    }

def get_reading_levels(suas):
    return [all_reading_levels(sua['text']) for sua in suas]

def enrich_collection(collection, auxiliary):
    for c, aux in zip(collection, auxiliary):
        c.update(aux)

def save_as_json(fname, data):
    with open(fname, 'w') as outfile:
        json.dump(data, outfile)

def load_json_as_dict(fname):
    with open(fname, 'r') as infile:
        return json.loads(infile.read())

def unique_words_len(text):
    return len(set(text.lower().split()))

def basic_tokenizer(text):
    tokens = nltk_word_tokenize(text)
    return tokens

def stem_tokenizer(text):
    tokens = nltk_word_tokenize(text)
    stemmer = PorterStemmer()
    stems = list(set([stemmer.stem(word) for word in tokens]))
    return stems

def gen_inaugurals():
    for fileid in inaugural.fileids():
        yield { 
            'year': fileid[:4],
            'text': ' '.join(inaugural.words(fileid))
        }

def get_inaugurals():
    return [ia for ia in gen_inaugurals()]

def gen_ConditionalFreqDist(suas, words):
    return nltk.ConditionalFreqDist(
        (target, sua['year'])    
        for sua in suas    
        for w in nltk.word_tokenize(sua['text'])
        for target in words
        if w.lower().startswith(target))

if __name__ == '__main__':
    with open(suas_fname, 'r') as f:
        print (len(f.readlines()))
