import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
from analysis_utils import calc_total

def test_calc_total():
    """
    Prueba que la función calc_total calcula correctamente la columna 'total'.
    """
    # Datos de prueba
    data_entrada = {
        'producto': ['A', 'B'],
        'cantidad': [10, 5],
        'precio_unitario': [100, 20]
    }
    df_entrada = pd.DataFrame(data_entrada)

    # Datos esperados
    data_esperada = {
        'producto': ['A', 'B'],
        'cantidad': [10, 5],
        'precio_unitario': [100, 20],
        'total': [1000, 100]
    }
    df_esperada = pd.DataFrame(data_esperada)

    # Aplicando cambios
    df_resultado = calc_total(df_entrada)

    # Confirmación
    assert_frame_equal(df_resultado, df_esperada)
