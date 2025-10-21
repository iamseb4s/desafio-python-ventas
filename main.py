from analysis_utils import (
    load_and_clean_data, 
    calc_total, 
    analysis, 
    save_to_sqlite
)

def main():
    # Tarea 1: Carga y limpieza
    print("Iniciando el proceso de análisis de ventas...")
    filepath = 'data/ventas.csv'
    clean_data = load_and_clean_data(filepath)
    final_data = calc_total(clean_data)
    print("Datos cargados y limpiados.")

    # Tarea 2: Análisis
    print("Realizando análisis...")
    resultados = analysis(final_data)
    
    print("\n--- Resultados del Análisis ---")
    print(f"Producto más vendido por cantidad: {resultados['producto_mas_vendido']}")
    print(f"Producto con mayor facturación: {resultados['producto_mayor_facturacion']}")
    
    # Tarea 3: Persistencia
    print("\nGuardando resultados en la base de datos...")
    db_path = 'output/ventas_analisis.db'
    save_to_sqlite(resultados, db_path)

    print("\n--- Proceso Finalizado ---")


if __name__ == "__main__":
    main()
