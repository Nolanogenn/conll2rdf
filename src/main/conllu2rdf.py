import pprint
import argparse
import pandas as pd
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import Namespace, NamespaceManager
from rdflib.namespace import RDF

graph = Graph()


parser = argparse.ArgumentParser()

parser.add_argument('--input', help='The input TSV file')
parser.add_argument('--output', help='The output RDF file')
parser.add_argument('--columns', help='The columns defined in the TSV file (list of columns divided by a space)')
parser.add_argument('--uri', help='The basic uri of your resource')

args=parser.parse_args()

colnames = args.columns.split()
input_tsv = open(args.input).readlines()

sentences = []
sentence = []
for line in input_tsv:
    if line != '\n':
        sentence.append(line.split('\t'))
    else:
        sentences.append(sentence)
        sentence = []

#prefix_ud = f"https://github.com/UniversalDependencies/universaldependencies.github.io/{args.lan}/dep/#"



prefixes = {
    "" : f"{args.uri}",
    "conll" : "https://ufal.mff.cuni.cz/conll2009-st/task-description.html/#",
    "rdf":"http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "nif":"https://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core/nif-core.html#",
    "rdfs":"http://www.w3.org/2000/01/rdf-schema#",
}

for prefix in prefixes:
    graph.bind(prefix, prefixes[prefix])

nif_sentence = Namespace(prefixes['nif']).Sentence 
nif_word = Namespace(prefixes['nif']).Word
nif_next_word = Namespace(prefixes['nif']).nextWord

col_classes = {
        "WORD":Namespace(prefixes['conll']).WORD,
        "LEMMA":Namespace(prefixes['conll']).LEMMA,
        "UPOS":Namespace(prefixes['conll']).UPOS,
        "POS":Namespace(prefixes['conll']).POS,
        "MISC":Namespace(prefixes['conll']).MISC,
        "FEAT":Namespace(prefixes['conll']).FEAT,
        "HEAD":Namespace(prefixes['conll']).HEAD,
        "EDGE":Namespace(prefixes['conll']).EDGE,
        "DEPS":Namespace(prefixes['conll']).DEPS,
       }

for sentence_enum, sentence in enumerate(sentences):
    id_sentence = URIRef(f"{prefixes['']}{sentence_enum}_0")

    uri_sentence = f"{id_sentence}"
    
    graph.add((id_sentence, RDF.type, nif_sentence))
    for word in sentence:
        id_word = URIRef(f"{prefixes['']}s{sentence_enum}_{word[0]}")
        graph.add((id_word, RDF.type, nif_word))
        
        for index_col, col in enumerate(colnames):
            if word[index_col] != '_' and col != 'ID':
                rel = col_classes[col]
                if col != "HEAD":
                    graph.add((id_word, rel, Literal(word[index_col])))
                else:
                    id_head = URIRef(f"{prefixes['']}s{sentence_enum}_{word[index_col]}")
                    graph.add((id_word, rel, id_head))

    if sentence_enum == 5:
        break

print(graph.serialize())



