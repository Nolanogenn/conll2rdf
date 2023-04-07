# ConllU2RDF
__

Python script to convert tsv files in CONLLU format to rdf. An example of how it is used can be found in src/run\_example.sh.  

To run the script, you invoke **main/conllu2rdf.py** with the following arguments:
- **--input** :  the path to the input file
- **--output** : the path where you want to output file to be stored
- **--columns** : a string of space-divided names of the columns present in your input file. Currently the script accepts the following columns: \[ID WORD LEMMA UPOS POS FEAT HEAD EDGE DEPS MISC LABEL\]
- **--uri** :  the uri of your resource.


__

## Contacts
email: genn@gnolano.xyz
