import os
from analysis_utils import (
    load_and_clean_data, 
    calc_total, 
    analysis, 
    save_to_sqlite,
    monthly_graph_generator
)

def main():
    # Crear directorio de salida si no existe
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Carga y limpieza
    print("Iniciando el proceso de análisis de ventas...")
    filepath = 'data/ventas.csv'
    clean_data = load_and_clean_data(filepath)
    final_data = calc_total(clean_data)
    print("Datos cargados y limpiados.")

    # Análisis
    print("Realizando análisis...")
    resultados = analysis(final_data)
    
    print("\n--- Resultados del Análisis ---")
    print(f"Producto más vendido por cantidad: {resultados['producto_mas_vendido']}")
    print(f"Producto con mayor facturación: {resultados['producto_mayor_facturacion']}")
    
    # Persistencia
    print("\nGuardando resultados en la base de datos...")
    db_path = os.path.join(output_dir, 'ventas_analisis.db')
    save_to_sqlite(resultados, db_path)

    # Visualización
    print("\nGenerando gráfico de facturación mensual...")
    chart_path = os.path.join(output_dir, 'grafico.png')
    monthly_graph_generator(resultados['facturacion_mensual'], chart_path)

    print("\n--- Proceso Finalizado ---")


if __name__ == "__main__":
    main()
