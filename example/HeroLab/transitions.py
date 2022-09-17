from typing import Dict as aDict
import os
import pickle

transitions: aDict
references: aDict
# Load scraped target data
    
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, './target.data')
with open(file_path, 'rb') as datafile:
    transitions, references = pickle.load(datafile)

transition_set = set()
reference_set = set()

for subDict in transitions.values():
    for transition in subDict.keys():
        transition_set.add(transition)

for subDict in references.values():
    for reference in subDict.keys():
        reference_set.add(reference)