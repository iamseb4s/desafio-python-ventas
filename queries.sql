-- Consulta para obtener los 3 productos más vendidos en función de la facturación total.
-- Esta consulta se hace a la tabla 'reporte_productos' de la base de datos 'ventas_analisis.db'.

SELECT 
    producto,
    total_facturado
FROM 
    reporte_productos
ORDER BY 
    total_facturado DESC
LIMIT 3;
