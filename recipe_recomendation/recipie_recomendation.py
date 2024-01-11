import pandas as pd
from . import utility
from . import vectroize_document
from gensim.models import Word2Vec
import random
import os.path

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
    
word_vec_file= os.path.join(CURRENT_DIR, "./model/df_recipes_ingredients_vector.bin")
recipe_data_set_file=os.path.join(CURRENT_DIR, "./dataset/df_recipes.csv")
model = Word2Vec.load(word_vec_file)
pd_data=pd.read_csv(recipe_data_set_file)
doc_vec,EmbeddingAlgo=vectroize_document.vectroize(pd_data,model,vectroize_document.MeanEmbedding)


def get_recomendation(text,N=5,to_dict=False):
    res=utility.process_input(text,pd_data,doc_vec,EmbeddingAlgo,N)
    if to_dict:
        return res.to_dict("records")
    return res

def get_random_recomendation(N=5,to_dict=False):
    recomendation = pd.DataFrame(columns=["id","name", "ingredients","url"])
    rand_arr=random.sample(range(pd_data.shape[0]), N)
    j=0
    for i in rand_arr:
        recomendation.at[j,"id"] = i
        recomendation.at[j, "name"] = pd_data["recipe_name"][i]
        recomendation.at[j, "url"] = pd_data["recipe_urls"][i]
        recomendation.at[j, "ingredients"] = pd_data["ingredients"][i]
        j+=1
    if to_dict:
        return recomendation.to_dict("records")
    return recomendation

def get_by_id(rcp_id,to_dict=False):
    recomendation = pd.DataFrame(columns=["id","name", "ingredients","url"])
    recomendation.at[0,"id"] = rcp_id
    recomendation.at[0, "name"] = pd_data["recipe_name"][rcp_id]
    recomendation.at[0, "url"] = pd_data["recipe_urls"][rcp_id]
    recomendation.at[0, "ingredients"] = pd_data["ingredients"][rcp_id]
    if to_dict:
        return recomendation.to_dict("records")
    return recomendation



if __name__=="__main__":
    data=get_random_recomendation(10)
    for i in range(0,data.shape[0]):
        print(f"[{data.at[i,'id']}]    ->  {data.at[i,'name']}")

    exit()

    while(True):
        i=input(">> ")
        res=utility.process_input(i,pd_data,doc_vec,EmbeddingAlgo,3)
        for i in res["name"]:
            print(i)
