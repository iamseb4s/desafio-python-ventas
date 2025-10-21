import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker

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

def analysis(df: pd.DataFrame) -> dict:
    # (a) Producto más vendido (en cantidad de unidades)
    top_product_quantity = df.groupby('producto')['cantidad'].sum().sort_values(ascending=False).idxmax()

    # (b) Producto más vendido (en valor total)
    top_product_sales = df.groupby('producto')['total'].sum().sort_values(ascending=False).idxmax()

    # (c) Facturación total por mes
    monthly_revenue = df.groupby(df['fecha'].dt.to_period('M'))['total'].sum().reset_index()
    monthly_revenue['month_str'] = monthly_revenue['fecha'].dt.strftime('%B %Y')
    monthly_revenue['fecha'] = monthly_revenue['fecha'].astype(str)

    # DataFrame agregado para el reporte de productos
    product_report = df.groupby('producto').agg(
        total_quantity=('cantidad', 'sum'),
        total_revenue=('total', 'sum')
    ).sort_values(by='total_revenue', ascending=False).reset_index()

    results = {
        'producto_mas_vendido': top_product_quantity,
        'producto_mayor_facturacion': top_product_sales,
        'facturacion_mensual': monthly_revenue,
        'reporte_productos': product_report
    }

    return results

def save_to_sqlite(results: dict, db_path: str):
    try:
        # Conexión a la base de datos
        conn = sqlite3.connect(db_path)

        # Guardando el dataframe en la base de datos
        results['reporte_productos'].to_sql('reporte_productos', conn, if_exists='replace', index=False)

        # Guardar la facturación mensual
        results['facturacion_mensual'].to_sql('facturacion_mensual', conn, if_exists='replace', index=True)

        print(f"Resultados guardados exitosamente en la base de datos '{db_path}'")
        conn.close()
    except Exception as e:
        print(f"Error al guardar en la base de datos: {e}")

def monthly_graph_generator(monthly_revenue: pd.DataFrame, output_path: str):
    plt.figure(figsize=(12, 7))
    ax = sns.barplot(data=monthly_revenue, x='month_str', y='total', palette='viridis')

    # Formato del gráfico
    # Etiquetas de datos sobre las barras
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(f'{height:,.0f}',
                    (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='center',
                    xytext=(0, 9),
                    textcoords='offset points')

    # Formato de números en miles y millones
    def format_millions(y, _):
        if y >= 1e6:
            return f'{y/1e6:,.1f}M'
        elif y >= 1e3:
            return f'{y/1e3:,.0f}K'
        else:
            return f'{y:,.0f}'

    formatter = ticker.FuncFormatter(format_millions)
    ax.yaxis.set_major_formatter(formatter)

    # Etiquetas y título
    plt.title("Facturación Total Mensual", fontsize=24, weight='bold', pad=20)
    plt.xlabel("Mes", fontsize=16)
    plt.ylabel("Facturación Total", fontsize=16)

    sns.despine(left=True)
    ax.tick_params(axis='y', which='both', left=False)
    plt.tight_layout()
    
    try:
        plt.savefig(output_path)
        print(f"Gráfico guardado exitosamente en '{output_path}'")
    except Exception as e:
        print(f"Error al guardar el gráfico: {e}")
