from mage_ai.data_cleaner.transformer_actions.base import BaseAction
from mage_ai.data_cleaner.transformer_actions.constants import ActionType, Axis
from mage_ai.data_cleaner.transformer_actions.utils import build_transformer_action
from pandas import DataFrame

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def execute_transformer_action(df_merged: DataFrame, *args, **kwargs) -> DataFrame:
    """
    Transformer Action: update column names

    Docs: https://docs.mage.ai/guides/transformer-blocks#clean-column-names
    """
    df_merged = df_merged.rename(columns={
    '_date' : 'date',
    'name' : 'nom', 
    'absolute_magnitude_h': 'magnitude_absolue', 
    'estimated_diameter_min_meters' : 'diametre_estime_min_m', 
    'estimated_diameter_max_meters' : 'diametre_estime_max_m',
    'is_potentially_hazardous_asteroid' : 'potentiellement_dangeureux',
    'is_sentry_object' : 'sentry_surveillance_collisions',
    'close_approach_date': 'date_approche',
    'close_approach_date_full' : 'date_approche_complete',
    'relative_velocity_km_per_second' : 'vitesse_relative_km_par_seconde', 
    'relative_velocity_km_per_hour' : 'vitesse_relative_km_par_heure',
    'miss_distance_kilometers' : 'distance_de_la_terre',
    'orbiting_body' : 'orbite'})

    return df_merged


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
