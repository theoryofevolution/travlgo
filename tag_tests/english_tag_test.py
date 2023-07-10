import json
import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

# Example usage
def tag_finder(query):
    with open('english_tags.json') as file:
        tags = json.load(file)
    snatch_tags = []
    for tags in tags['tags']:
        snatch_tags.append(tags['tagNameEn'])

    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    embeddings = model.encode(snatch_tags)

    query_embedding = model.encode([query])[0]

    # Calculate cosine similarity between query embedding and tag embeddings
    similarities = cosine_similarity([query_embedding], embeddings)[0]

    # Find the indices of the closest tags
    closest_indices = similarities.argsort()[::-1]

    return [closest_indices[0], closest_indices[1], closest_indices[2], closest_indices[3], closest_indices[4]]
