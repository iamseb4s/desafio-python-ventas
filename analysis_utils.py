import pandas as pd

def load_and_clean_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath, encoding='utf-8', sep=',')
    df['fecha'] = pd.to_datetime(df['fecha'], format='%Y-%m-%d')
    df = df[(df['cantidad'] > 0) & (df['precio_unitario'] > 0)].copy()
    df.dropna(inplace=True)
    df.sort_values(by='fecha', inplace=True)
    return df

def calc_total(df: pd.DataFrame) -> pd.DataFrame:
    if 'cantidad' in df.columns and 'precio_unitario' in df.columns:
        df['total'] = df['cantidad'] * df['precio_unitario']
    return df
