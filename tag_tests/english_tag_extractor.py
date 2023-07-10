import json

with open('tags_data.json') as file:
    tags = json.load(file)

tag_file = []

for tag in tags['tags']:
    english_extracted = {'tagId': tag['tagId'],
                         'tagNameEn': tag['allNamesByLocale']['en']
    }
    tag_file.append(english_extracted)

output_data = {'tags': tag_file}

with open('english_tags.json', 'w') as output_file:
    json.dump(output_data, output_file, indent=4)