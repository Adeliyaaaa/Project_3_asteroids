import pandas as pd
from pandas import DataFrame
from datetime import datetime
from datetime import date
import re

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(df_merged: DataFrame, *args, **kwargs):
    """
    Template code for a transformer block.
    """
    # Cleaning words : 
    dirty_list = ["Masse estimée: NULL", "Lieu d'impact terrestre: Aucun", "Aucun", 
            "Mission d'exploration spatiale: Aucun", 'Aucun à ce jour', "Aucun à ce jour.", 
            "Phénomènes observés: Aucun à ce jour"]

    def cleaning(word : str) -> str: 
        if word in dirty_list and isinstance(word, str): 
            word = None
        else : word = word
        return word

    df_merged['masse_estimee_kg'] = df_merged['masse_estimee_kg'].apply(cleaning)
    df_merged['lieu_impact'] = df_merged['lieu_impact'].apply(cleaning)
    df_merged['mission'] = df_merged['mission'].apply(cleaning)
    df_merged['phenomene_observee'] = df_merged['phenomene_observee'].apply(cleaning)

    # Column masse 
    def exposant_unicode(match):
        exposants = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
        return match.group(1) + match.group(2).translate(exposants)

    def transform_masse (masse : str) -> str:
        if isinstance (masse, str): 
            masse = masse.replace(",", ".").replace('</sup>', '').replace('\u202f', ' ')
            pattern = r"(\d+)(?:\^|<sup>)(\d+)(?:</sup>)?"
            formatted_masse = re.sub(pattern, exposant_unicode, masse)
            return formatted_masse

    df_merged['masse_estimee_kg'] = df_merged['masse_estimee_kg'].apply(lambda x : transform_masse(x) if isinstance(x, str) else x)

    # Column type  
    df_merged['type'] = df_merged['type'].astype(str).apply(
    lambda x : re.sub(r'^(Type Apollo|Type Inconnu|Type: Inconnu|Type X).*', 'Inconnu', x, flags=re.IGNORECASE))

    df_merged['type'] = df_merged['type'].astype(str).apply(
        lambda x : re.sub(r'^Type S.*', 'Type S (silicatés)', x, flags=re.IGNORECASE))

    df_merged['type'] = df_merged['type'].astype(str).apply(
        lambda x : re.sub(r'^Type M.*', 'Type M (métalliques)', x, flags=re.IGNORECASE))

    df_merged['type'] = df_merged['type'].astype(str).apply(
        lambda x : re.sub(r'^Type C.*', 'Type C (carbonés)', x, flags=re.IGNORECASE))

    df_merged['type'] = df_merged['type'].astype(str).apply(
        lambda x : re.sub(r'^Type B.*', 'Type B (sous-type de C)', x, flags=re.IGNORECASE))

    df_merged['type'] = df_merged['type'].astype(str).apply(
        lambda x : re.sub(r'^Type L.*', 'Type L (entre S (silicatés) et C (carbonés))', x, flags=re.IGNORECASE))

    df_merged['type'] = df_merged['type'].astype(str).apply(
        lambda x : re.sub(r'^Type V.*', 'Type V (basaltique)', x, flags=re.IGNORECASE))

    df_merged['type'] = df_merged['type'].astype(str).apply(
        lambda x : re.sub(r'^Type Q.*', 'Type Q (Olivine, Pyroxène, Métaux (fer-nickel), Silicates non altérés)', x, flags=re.IGNORECASE))


    return df_merged


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'