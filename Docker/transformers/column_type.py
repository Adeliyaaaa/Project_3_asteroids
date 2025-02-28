import pandas as pd
from pandas import DataFrame
from datetime import datetime
from datetime import date

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def update_types(df_merged: DataFrame, *args, **kwargs):
    """
    Update column types

    """
    # Transformer la date stockée au format str en datetime

    df_merged['date'] = pd.to_datetime(df_merged['date'])
    df_merged['date_approche'] = pd.to_datetime(df_merged['date_approche'])
    df_merged['date_approche_complete'] = df_merged['date_approche_complete'].apply(lambda x : datetime.strptime(x, '%Y-%b-%d %H:%M'))

    def transform_to_date(x) -> date| None: 
        try:
            var_date = datetime.strptime(x, '%Y-%m-%d')
        except: 
            var_date = None
        return var_date

    df_merged['date_entree_athmospherique'] = df_merged['date_entree_athmospherique'].apply(transform_to_date)
    df_merged['date_decouverte'] = df_merged['date_decouverte'].apply(transform_to_date)

    # Transformer les colonnes numériques en float
    df_merged[['vitesse_relative_km_par_seconde','vitesse_relative_km_par_heure', 
    'distance_de_la_terre']] = df_merged[['vitesse_relative_km_par_seconde',
    'vitesse_relative_km_par_heure', 'distance_de_la_terre']].astype('float64')

    # Remplacer les Nones en str par None
    df_merged[['description', 'date_decouverte', 'masse_estimee_kg', 'type',
       'date_entree_athmospherique', 'phenomene_observee', 'lieu_impact',
       'mission', 'latitude', 'longitude']] = df_merged[['description', 'date_decouverte', 'masse_estimee_kg', 'type',
       'date_entree_athmospherique', 'phenomene_observee', 'lieu_impact',
       'mission', 'latitude', 'longitude']].apply(lambda x : x.replace('None', None))
    

    print(df_merged.dtypes)

    return df_merged


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
