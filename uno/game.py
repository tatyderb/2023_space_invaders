import json

text = '''
{
    "deck": "y9 r9 y0 y1 r0 r0",
    "heap": "y1 b1 b4 r4",
    "players": [
        {
            "name": "Bob",
            "hand": "r3 r5"
        },
        {
            "name": "Charley",
            "hand": "b1 g2"
        }
    ],
    "player_index": 0
}
'''
d = json.loads(text)
print(d)

with open('data.json') as fin:
    d2 = json.load(fin)
print(d2)

