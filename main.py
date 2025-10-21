from analysis_utils import load_and_clean_data, calc_total

def main():
    # Tarea 1: Carga, limpieza y cálculo del total
    print("Iniciando el proceso de carga y limpieza de datos...")
    filepath = 'data/ventas.csv'
    clean_data = load_and_clean_data(filepath)
    final_data = calc_total(clean_data)
    
    print("Proceso completado. Se han obtenido los siguientes datos:")
    print(final_data.head())

if __name__ == "__main__":
    main()
