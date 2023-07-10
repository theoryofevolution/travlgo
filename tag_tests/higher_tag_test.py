import fasttext
import numpy as np
import fasttext.util

# download English pretrained model
#fasttext.util.download_model('en', if_exists='ignore')
ft = fasttext.load_model('cc.en.300.bin')

def cos_sim(a, b):
    """Takes 2 vectors a, b and returns the cosine similarity according 
    to the definition of the dot product
    (https://masongallo.github.io/machine/learning,/python/2016/07/29/cosine-similarity.html)
    """
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return dot_product / (norm_a * norm_b)

def compare_word(w, words_vectors):
    """
    Compares new word with those in the words vectors dictionary
    """
    vec=ft.get_sentence_vector(w)
    return {w1:cos_sim(vec,vec1) for w1,vec1 in words_vectors.items()}

# define your word list
words_list=[ "metal", "st. patrick", "health"]

# compute words vectors and save them into a dictionary.
# since there are multiwords expressions, we use get_sentence_vector method
# instead, you can use  get_word_vector method
words_vectors={w:ft.get_sentence_vector(w) for  w in words_list}

# try compare_word function!

compare_word('saint patrick', words_vectors)
# output: {'metal': 0.13774191, 'st. patrick': 0.78390956, 'health': 0.10316559}

compare_word('copper', words_vectors)
# output: {'metal': 0.6028242, 'st. patrick': 0.16589196, 'health': 0.10199054}

compare_word('ireland', words_vectors)
# output: {'metal': 0.092361264, 'st. patrick': 0.3721483, 'health': 0.118174866}
