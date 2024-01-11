import pandas as pd
from . import utility
from gensim.models import Word2Vec

def vectroize(pd_data,out_file):
    #pd_data=>keys: name, ingredients etc...
    # preprocess ingridants
    pd_data["processed_ingredients"]=pd_data.ingredients.apply(utility.preprocess_ingredients)
    ## !!! still existens of wordss like teassopene tablesopne

    # sort the ingridient list ()
    sorted_ingredients_lst=pd_data.processed_ingredients.apply(lambda x:x.sort())
    sorted_ingredients_lst=pd_data.processed_ingredients
    print(f"Processed ingredients: {len(sorted_ingredients_lst)}")
    #get average len of ingridident list
    lengths = [len(i) for i in sorted_ingredients_lst]
    avg_len = float(sum(lengths)) / len(lengths)
    window_size=round(avg_len)
    # train and save CBOW Word2Vec model
    model_cbow = Word2Vec(
      sorted_ingredients_lst, sg=0, workers=8, window=window_size, min_count=1, vector_size=100
    )
    model_cbow.save(out_file)
    print("Word2Vec model successfully trained")
    
 

if __name__=="__main__" :
    pd_data=pd.read_csv("dataset/df_recipes.csv")
    vectroize(pd_data,"model/df_recipes_ingredients_vector.bin")