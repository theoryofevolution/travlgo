import json
import os

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
with open('english_tags.json') as file:
    tags = json.load(file)
snatch_tags = []
for tags in tags['tags']:
        snatch_tags.append(tags['tagNameEn'])
