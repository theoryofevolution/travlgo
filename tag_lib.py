import json
import os

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
with open('tags_data.json') as file:
    tags = json.load(file)
"""
tag_file = []
for tag in tags['tags']:
    print(tag)
    english_tag = tag['allNamesByLocale']['en']
    tag_append = {'tag': tag['tagId'],
                  'tagNameEn': english_tag}
    tag_file.append(tag_append)
with open('english_tags.json', 'w') as f:
        json.dump(tag_file, f, indent=4)
"""
with open('english_tags.json') as file:
    tags = json.load(file)
snatch_tags = []
for tag in tags:
        snatch_tags.append(tag['tagNameEn'])