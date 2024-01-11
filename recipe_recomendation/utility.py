import re
import nltk
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
#nltk.download('wordnet')
#nltk.download("stopwords")

stop_word_lst = nltk.corpus.stopwords.words("english")


additional_stop_words = ["advertisement", "advertisements",'ADVERTISEMENT'
        "teaspoon",
        "t",
        "tsp.",
        "tablespoon",
        "T",
        "tbl.",
        "tb",
        "tbsp.",
        "fluid ounce",
        "fl oz",
        "gill",
        "cup",
        "c",
        "pint",
        "p",
        "pt",
        "fl pt",
        "quart",
        "q",
        "qt",
        "fl qt",
        "gallon",
        "g",
        "gal",
        "ml",
        "milliliter",
        "millilitre",
        "cc",
        "mL",
        "l",
        "liter",
        "litre",
        "L",
        "dl",
        "deciliter",
        "decilitre",
        "dL",
        "bulb",
        "level",
        "heaped",
        "rounded",
        "whole",
        "pinch",
        "medium",
        "slice",
        "pound",
        "lb",
        "#",
        "ounce",
        "oz",
        "mg",
        "milligram",
        "milligramme",
        "g",
        "gram",
        "gramme",
        "kg",
        "kilogram",
        "kilogramme",
        "x",
        "of",
        "mm",
        "millimetre",
        "millimeter",
        "cm",
        "centimeter",
        "centimetre",
        "m",
        "meter",
        "metre",
        "inch",
        "in",
        "milli",
        "centi",
        "deci",
        "hecto",
        "kilo",

        ]

    # Extend lst of stop words
stop_word_lst.extend(additional_stop_words)

"""
    @input ->str
    @return -> list
"""
def preprocess_ingredients(input_str):
    ## clean (convert to lowercase and remove punctuations and characters and then strip)
    input_str = re.sub(r'[^\w\s]', '', str(input_str).lower().strip())
            
    ## Tokenize (convert from string to list)
    lst_str = input_str.split()

    new_str_lst=[]
    ps = nltk.stem.porter.PorterStemmer()
    lem = nltk.stem.wordnet.WordNetLemmatizer()
    for word in lst_str:
        #remove stop word
        if word not in stop_word_lst:
            # Stemming (remove -ing, -ly, ...)
            stemed_word=ps.stem(word)
            # Lemmatisation (convert the word into root word)
            lem_word=lem.lemmatize(stemed_word)
            new_str_lst.append(lem_word)

    return_text = " ".join(new_str_lst)
    ## Remove digits
    return_text= ''.join([i for i in return_text if not i.isdigit()])
    ## remove mutliple space
    return_text = re.sub(' +', ' ', return_text)
    return return_text.strip().split(" ")


def get_recommendations(pd_data,scores_vec,N):
    """
    Rank scores_vec and output a pandas data frame containing all the details of the top N recipes.
    :param scores_vec: list of cosine similarities
    """
    # load in recipe dataset
    ##pd_data = pd.read_csv(config.PARSED_PATH)
    # order the scores_vec with and filter to get the highest N scores_vec
    top = sorted(range(len(scores_vec)), key=lambda i: scores_vec[i], reverse=True)[:N]
    # create dataframe to load in recommendations
    recommendation = pd.DataFrame(columns=["id","name", "ingredients", "score", "url"])
    count = 0
    for i in top:
        recommendation.at[count,"id"]=i
        recommendation.at[count, "name"] = pd_data["recipe_name"][i]
        """recommendation.at[count, "ingredients"] = ingredient_parser_final(
            pd_data["ingredients"][i]
        )"""
        recommendation.at[count, "ingredients"]=pd_data["ingredients"][i]
        recommendation.at[count, "url"] = pd_data["recipe_urls"][i]
        recommendation.at[count, "score"] = f"{scores_vec[i]}"
        count += 1
    return recommendation


"""
    @input_str -> unprocessed user text
    @pd_data -> orginal_recipie data
    @doc_vec -> vecotized document(recipie)
    @EmbeddingAlgo -> object of fitted data (returned from vectorize_document.vectroize)
    @N-> num of iteam to be returned

    return -> list of predictred N recipies
"""
def process_input(input_str,pd_data,doc_vec,EmbeddingAlgo,N=5):
        processed_input=preprocess_ingredients(input_str)
        input_emb=EmbeddingAlgo.transform([processed_input])[0].reshape(1, -1)
        cos_sim = map(lambda x: cosine_similarity(input_emb, x)[0][0], doc_vec)
        scores_vec = list(cos_sim)
        recommendations = get_recommendations(pd_data,scores_vec,N)
        return recommendations



