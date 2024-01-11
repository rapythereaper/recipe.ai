import pandas as pd
from . import utility
from gensim.models import Word2Vec
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity



"""
    to call transform()
"""
class MeanEmbedding(object):
    def __init__(self, model_cbow):
        self.model_cbow = model_cbow
        self.vector_size = model_cbow.wv.vector_size

    def fit(self):  
        return self

    def transform(self, docs): 
        doc_vector = self.doc_average_list(docs)
        return doc_vector
        ##doc_vec = [doc.reshape(1, -1) for doc in doc_vector]
        ##return doc_vec  ####

    def doc_average(self, doc):
        mean = []
        for word in doc:
            if word in self.model_cbow.wv.index_to_key:
                mean.append(self.model_cbow.wv.get_vector(word))

        if not mean: 
            return np.zeros(self.vector_size)
        else:
            mean = np.array(mean).mean(axis=0)
            return mean

    def doc_average_list(self, docs):
        return np.vstack([self.doc_average(doc) for doc in docs])

""" @pd_data->data set of recipies; opend via pands
    @model-> vecotrize ingrodients data
    @EmbeddingAlgo-> algo to vectorize document

    return -> docuemtn_vector, objec to Embeding algo (to be passed to utility.process_input) 
"""
def vectroize(pd_data,model,EmbeddingAlgo=MeanEmbedding):
    algo_emb=EmbeddingAlgo(model)
    pd_data["processed_ingredients"]=pd_data.ingredients.apply(utility.preprocess_ingredients)
    sorted_ingredients_lst=pd_data.processed_ingredients.apply(lambda x:x.sort())
    sorted_ingredients_lst=pd_data.processed_ingredients
    doc_vec = algo_emb.transform(sorted_ingredients_lst)
    doc_vec = [doc.reshape(1, -1) for doc in doc_vec]

    assert len(doc_vec) == len(sorted_ingredients_lst)
    return doc_vec,algo_emb




if __name__=="__main__" :
    model = Word2Vec.load("model/df_recipes_ingredients_vector.bin")
    mean_emb=MeanEmbedding(model)

    pd_data = pd.read_csv("dataset/df_recipes.csv")
    pd_data["processed_ingredients"]=pd_data.ingredients.apply(utility.preprocess_ingredients)
    sorted_ingredients_lst=pd_data.processed_ingredients.apply(lambda x:x.sort())
    sorted_ingredients_lst=pd_data.processed_ingredients

    doc_vec = mean_emb.transform(sorted_ingredients_lst)
    doc_vec = [doc.reshape(1, -1) for doc in doc_vec]

    assert len(doc_vec) == len(sorted_ingredients_lst)
    while True:
        inp=input(">> ")
        inp=utility.preprocess_ingredients(inp)
        input_emb=mean_emb.transform([inp])[0].reshape(1, -1)
        cos_sim = map(lambda x: cosine_similarity(input_emb, x)[0][0], doc_vec)
        scores_vec = list(cos_sim)
        recommendations = utility.get_recommendations(pd_data,scores_vec,5)
        print(recommendations)