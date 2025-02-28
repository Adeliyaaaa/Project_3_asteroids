import io
import pandas as pd
import requests
from pandas import DataFrame

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def merge_data(df1: pd.DataFrame, df2: pd.DataFrame, *args, **kwargs):
    """
    Merge both DataFrames
    """
    if df1.empty:
        print("ERREUR : Le DataFrame df1 reçu est vide !")
    elif df2.empty:
        print("ERREUR : Le DataFrame df2 reçu est vide !")
    else:
        print("Nombre de lignes :", df1.shape[0], ",", df2.shape[0])

    df_merged = pd.merge(df2, df1, how='left', on='name')

    
    return df_merged



@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'