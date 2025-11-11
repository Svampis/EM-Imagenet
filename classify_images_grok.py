from xai_sdk import Client  # type: ignore
import sys
import os
import base64

from xai_sdk.chat import user, image
client = Client(api_key=os.getenv('XAI_API_KEY'))

classes = """
0: mouse, computer mouse
1: grille, radiator grille
2: sunglass
3: jean, blue jean, denim
4: gown
5: plate
6: crash helmet
7: washbasin, handbasin, washbowl, lavabo, wash-hand basin
8: chainlink fence
9: suit, suit of clothes
10: notebook, notebook computer
11: lampshade, lamp shade
12: military uniform
13: pot, flowerpot
14: tabby, tabby cat
15: jersey, T-shirt, tee shirt
16: corn
17: cowboy hat, ten-gallon hat
18: bookcase
19: beagle
20: soup bowl
21: car wheel
22: cup
23: microphone, mike
24: American chameleon, anole, Anolis carolinensis
25: entertainment center
26: wing
27: flat-coated retriever
28: running shoe
29: sandbar, sand bar
30: chain
31: electric guitar
32: rule, ruler
33: cellular telephone, cellular phone, cellphone, cell, mobile phone
34: green mamba
35: tractor
36: tray
37: mixing bowl
38: minibus
39: cowboy boot
40: necklace
41: space bar
42: wool, woolen, woollen
43: ice cream, icecream
44: cornet, horn, trumpet, trump
45: cassette
46: black and gold garden spider, Argiope aurantia
47: meat loaf, meatloaf
48: church, church building
49: snorkel
"""

paths = open(sys.argv[1])

i = 0

for fpath in paths:
    # Replace this with the URL of wherever you're hosting the images
    image_url = "https://thinkcenter.ddns.me/" + fpath

    chat = client.chat.create(model="grok-2-vision-1212")
    chat.append(
        user(
            "Classify this image as one of the following. Print only the number, provide no other text, always stick to a number even if it's a guess\n" + classes,
            image(image_url=image_url, detail="low"),
        )
    )

    response = chat.sample()
    out = response.content

    fileout = open(sys.argv[2], "a")
    print(fpath.strip() + ";" + chat.sample().content, file=fileout)
    fileout.close()
    print(i, file=sys.stderr)
    i += 1

paths.close()
