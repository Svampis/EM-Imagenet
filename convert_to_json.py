import json
import sys

features = ['mouse, computer mouse', 'grille, radiator grille', 'sunglass', 'jean, blue jean, denim', 'gown', 'plate', 'crash helmet', 'washbasin, handbasin, washbowl, lavabo, wash-hand basin', 'chainlink fence', 'suit, suit of clothes', 'notebook, notebook computer', 'lampshade, lamp shade', 'military uniform', 'pot, flowerpot', 'tabby, tabby cat', 'jersey, T-shirt, tee shirt', 'corn', 'cowboy hat, ten-gallon hat', 'bookcase', 'beagle', 'soup bowl', 'car wheel', 'cup', 'microphone, mike', 'American chameleon, anole, Anolis carolinensis', 'entertainment center', 'wing', 'flat-coated retriever', 'running shoe', 'sandbar, sand bar', 'chain', 'electric guitar', 'rule, ruler', 'cellular telephone, cellular phone, cellphone, cell, mobile phone', 'green mamba', 'tractor', 'tray', 'mixing bowl', 'minibus', 'cowboy boot', 'necklace', 'space bar', 'wool, woolen, woollen', 'ice cream, icecream', 'cornet, horn, trumpet, trump', 'cassette', 'black and gold garden spider, Argiope aurantia', 'meat loaf, meatloaf', 'church, church building', 'snorkel']

out = []
file = open(sys.argv[1])
for line in file:
    line = line.strip()
    out.append([line.split(";")[0], features[int(line.split(";")[1])]])
    
print(json.dumps(out))
