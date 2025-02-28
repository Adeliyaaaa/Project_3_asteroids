import io
import pandas as pd
import requests
from datetime import datetime
import time
from pandas import DataFrame
import google.generativeai as genai
from mage_ai.data_preparation.shared.secrets import get_secret_value

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def transform_data(df1: pd.DataFrame, *args, **kwargs):
    """
    Data from GoogleAI
    """
    GOOGLE_API_KEY=get_secret_value('google_api_key')
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

    if df1.empty: 
        print("Le DataFrame est vide!")
        return df1

    data_dict = {}
    for i in range(0, len(df1)): 
        response = model.generate_content(f"""Tu es un Astrophysicien spécialisé dans les astéroïdes. Réponds aux questions et donne moi uniquement les réponses sous forme de liste []:
                - décrit l'astéroïde {df1.loc[i, 'name']} en moins de 600 caractères
                - date de découverte sous format année-mois-date
                - masse estimée en kg ou None
                - choisis une réponse de la liste: type C (carbonés), type S (silicatés), type M (métalliques), Inconnu
                - date d'entrée atmosphérique : date ou None
                - choisis une ou des réponses de la liste: Boules de feu ou bolides, Traînées de fumée ou de plasma, Tremblements de terre aériens (Bang supersonique), Éclats de lumière ou explosions atmosphériques, Chutes de météorites, Phénomènes observés lors de survols proches (Near-Earth Flybys), Impacts terrestres, Aucun à ce jour
                - Lieu d'impact terrestre : ville, région, pays, continent ou None
                - décrit la mission d'exploration spatiale en moins de 600 caractères ou None
                - longitude du lieu d'impact terrestre ou None
                - latitude du lieu d'impact terrestre ou None""")
        

        name = df1.loc[i, "name"]
        response = response.text
        r = response.replace("```\n[\n", "").replace("]\n```\n", "").replace("* ", "").replace("[", "").replace("]", "").replace("\n\n", "\n").replace("```", "").replace("- ", "").split("\n")
        test = [item for item in r if item]
        data_dict[name] = test
        time.sleep(7)

    df2 = pd.DataFrame.from_dict(data_dict, orient='index', columns=['description', 'date_decouverte', 'masse_estimee_kg', 
                                'type', 'date_entree_athmospherique', 'phenomene_observee', 'lieu_impact', 'mission', 'latitude', 'longitude']).reset_index().rename(columns={'index' : 'name'})
    
    print(df2.shape)

    return df2

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'

