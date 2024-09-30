from django.db import connection

from datetime import date, datetime
from decimal import Decimal
#########################################
########         INICIO         #########
#########################################

def get_count_projects_closed(from_date, to_date):
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    COUNT(id) 
                FROM "PROYECTO_CLIENTE"
                WHERE
                    "PC_FFECHA_FIN_REAL" BETWEEN %s AND %s AND
                    "PC_CESTADO" = 'Cerrado'
            """
            cursor.execute(query, [from_date, to_date])
            result = cursor.fetchone()
            if not result:
                return 0
            return result[0]
    except Exception as e:
        print(e)
        return []

def get_sum_costo_proyectado(from_date, to_date):
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT
                    SUM("PC_NCOSTO_ESTIMADO")
                FROM "PROYECTO_CLIENTE"
                WHERE
                    "PC_FFECHA_INICIO" BETWEEN %s AND %s
            """
            cursor.execute(query, [from_date, to_date])
            result = cursor.fetchone()
            if not result:
                return 0
            return result[0]
    except Exception as e:
        print(e)
        return 0
# funcion para obtener calcular costos en base al costo de la persona contra la cantidad de horas del proyecto
def get_costo_real(contrato_id):
    try:
        with connection.cursor() as cursor:
            query = """
            select
                SUM((
                    SELECT 
                    "CP_NVALOR"
                    FROM "COSTOS_PERSONA"
                    WHERE "CP_CNOMBRE" = USUARIO
                    AND "CP_NAÑO" = AÑO
                    AND "CP_NMES" = MES
                ) * HORAS) AS "VALOR"
            from (
                Select
                "HH_CONTROL_USER_ID" AS USUARIO,
                SUM("HH_CONTROL_HORAS") AS HORAS,
                EXTRACT(YEAR  from "HH_CONTROL_FECHA")::int AS AÑO,
                EXTRACT(MONTH  from "HH_CONTROL_FECHA")::int AS MES	
                    
                FROM "PROYECTO_CLIENTE"
                LEFT JOIN "CONTRATO_CLIENTE" ON "CONTRATO_CLIENTE"."id" = "PC_CONTRATO_CLIENTE_id"
                LEFT JOIN "HH_CONTROL" ON "CONTRATO_CLIENTE"."CC_CCODIGO" = "HH_CONTROL"."HH_CONTROL_PROY_ID"
                WHERE "PC_CONTRATO_CLIENTE_id"  = %s
                GROUP BY "HH_CONTROL_USER_ID",
                EXTRACT(YEAR  from "HH_CONTROL_FECHA")::int,
                EXTRACT(MONTH  from "HH_CONTROL_FECHA")::int
            ) AS DATOS

            """
            cursor.execute(query, [contrato_id])
            result = cursor.fetchone()
            if not result:
                return 0
            return result[0]
    except Exception as e:
        print(e)
        return 0
# funcion para obtener calcular costos en base al costo de la persona contra la cantidad de horas del proyecto
def get_costo_real_global(from_date,to_date):
    try:
        with connection.cursor() as cursor:
            query = """
                select
                    SUM((
                        SELECT 
                    "CP_NVALOR"
                    FROM "COSTOS_PERSONA"
                    WHERE "CP_CNOMBRE" = USUARIO
                    AND "CP_NAÑO" = AÑO
                    AND "CP_NMES" = MES
                ) * HORAS) AS "VALOR"
            from (
                Select
                "HH_CONTROL_USER_ID" AS USUARIO,
                SUM("HH_CONTROL_HORAS") AS HORAS,
                EXTRACT(YEAR  from "HH_CONTROL_FECHA")::int AS AÑO,
                EXTRACT(MONTH  from "HH_CONTROL_FECHA")::int AS MES	
                    
                FROM "PROYECTO_CLIENTE"
                LEFT JOIN "CONTRATO_CLIENTE" ON "CONTRATO_CLIENTE"."id" = "PC_CONTRATO_CLIENTE_id"
                LEFT JOIN "HH_CONTROL" ON "CONTRATO_CLIENTE"."CC_CCODIGO" = "HH_CONTROL"."HH_CONTROL_PROY_ID"
                WHERE
				"PC_CESTADO" != 'Cerrado'
                and "PC_FFECHA_INICIO" >= %s
				and "PC_FFECHA_INICIO" <= %s
                GROUP BY "HH_CONTROL_USER_ID",
                EXTRACT(YEAR  from "HH_CONTROL_FECHA")::int,
                EXTRACT(MONTH  from "HH_CONTROL_FECHA")::int
            ) AS DATOS

            """
            cursor.execute(query, [from_date,to_date])
            result = cursor.fetchone()
            if not result:
                return 0
            return result[0]
    except Exception as e:
        print(e)
        return 0
def get_sum_monto_pagado_tf_global(from_date,to_date):
    try:
        with connection.cursor() as cursor:
            query = """
            SELECT 
                SUM(CASE 
                    WHEN "MO_CMONEDA" = 'CLP' THEN "TF_NMONTOPAGADO"
                    ELSE "TF_NMONTOPAGADO" * COALESCE((SELECT 
                                                    "TC_NTASA" 
                                                    FROM "TIPO_CAMBIO" 
                                                    WHERE "TC_CMONEDA_id" = "MONEDA"."id"
                                                    ORDER BY "id" DESC
                                                    LIMIT 1 ), 1)
                END) AS "PAGADO",
                SUM(CASE 
                    WHEN "MO_CMONEDA" = 'CLP' THEN "TF_NMONTO"
                    ELSE "TF_NMONTO" * COALESCE((SELECT 
                                                    "TC_NTASA" 
                                                    FROM "TIPO_CAMBIO" 
                                                    WHERE "TC_CMONEDA_id" = "MONEDA"."id"
                                                    ORDER BY "id" DESC
                                                    LIMIT 1), 1)
                END) AS "MONTO_TOTAL",
                SUM(CASE 
                    WHEN "MO_CMONEDA" = 'CLP' THEN "TF_NMONTO" - "TF_NMONTOPAGADO"
                    ELSE ("TF_NMONTO" - "TF_NMONTOPAGADO") * COALESCE((SELECT 
                                                    "TC_NTASA" 
                                                    FROM "TIPO_CAMBIO" 
                                                    WHERE "TC_CMONEDA_id" = "MONEDA"."id"
                                                    ORDER BY "id" DESC
                                                    LIMIT 1
                                                                    ), 1)
                END) AS "PENDIENTE"
            FROM "TAREA_FINANCIERA"
            LEFT JOIN "MONEDA" on "MONEDA".id = "TAREA_FINANCIERA"."TF_MONEDA_id"
            LEFT JOIN "PROYECTO_CLIENTE" ON "TAREA_FINANCIERA"."TF_PROYECTO_CLIENTE_id" = "PROYECTO_CLIENTE"."id"

            WHERE "PROYECTO_CLIENTE"."PC_CESTADO" != 'Cerrado'
            and "PC_FFECHA_INICIO" >= %s
            and "PC_FFECHA_INICIO" <= %s

            """
            cursor.execute(query, [from_date,to_date])
            result = cursor.fetchone()
            if not result:
                return 0
            return result
    except Exception as e:
        print(e)
        return 0
def get_horas_costo_real(contrato_id):
    try:
        with connection.cursor() as cursor:
            query = """          
                Select
                    SUM("HH_CONTROL_HORAS") AS "HORAS"
                FROM "PROYECTO_CLIENTE"
                    LEFT JOIN "CONTRATO_CLIENTE" ON "CONTRATO_CLIENTE"."id" = "PC_CONTRATO_CLIENTE_id"
                    LEFT JOIN "HH_CONTROL" ON "CONTRATO_CLIENTE"."CC_CCODIGO" = "HH_CONTROL"."HH_CONTROL_PROY_ID"
                WHERE "PC_CONTRATO_CLIENTE_id"  = %s
            """
            cursor.execute(query, [contrato_id])
            result = cursor.fetchone()
            if not result:
                return 0
            return result[0]
    except Exception as e:
        print(e)
        return 0

def get_horas_costo_real_global(from_date,to_date):
    try:
        with connection.cursor() as cursor:
            query = """          
                Select
                    SUM("HH_CONTROL_HORAS") AS "HORAS"
                FROM "PROYECTO_CLIENTE"
                    LEFT JOIN "CONTRATO_CLIENTE" ON "CONTRATO_CLIENTE"."id" = "PC_CONTRATO_CLIENTE_id"
                    LEFT JOIN "HH_CONTROL" ON "CONTRATO_CLIENTE"."CC_CCODIGO" = "HH_CONTROL"."HH_CONTROL_PROY_ID"
                WHERE 
                "PC_CESTADO" != 'Cerrado'
                and "PC_FFECHA_INICIO" >= %s
                and "PC_FFECHA_INICIO" <= %s
            """
            cursor.execute(query, [from_date,to_date])
            result = cursor.fetchone()
            if not result:
                return 0
            return result[0]
    except Exception as e:
        print(e)
        return 0

def get_detalle_costo_real(contrato_id):
    try:
        with connection.cursor() as cursor:
            query = """
            select
                USUARIO,
                MAX((
                    SELECT 
                        "CP_CMONEDA"
                    FROM "COSTOS_PERSONA"
                    WHERE "CP_CNOMBRE" = USUARIO
                    AND "CP_NAÑO" = AÑO
                    AND "CP_NMES" = MES
                ))  AS "MONEDA",
                SUM((
                    SELECT 
                        "CP_NVALOR"
                    FROM "COSTOS_PERSONA"
                    WHERE "CP_CNOMBRE" = USUARIO
                    AND "CP_NAÑO" = AÑO
                    AND "CP_NMES" = MES
                ) * HORAS) AS "VALOR"
            from (
                Select
                "HH_CONTROL_USER_ID" AS USUARIO,
                SUM("HH_CONTROL_HORAS") AS HORAS,
                EXTRACT(YEAR  from "HH_CONTROL_FECHA")::int AS AÑO,
                EXTRACT(MONTH  from "HH_CONTROL_FECHA")::int AS MES

                    
                FROM "PROYECTO_CLIENTE"
                LEFT JOIN "CONTRATO_CLIENTE" ON "CONTRATO_CLIENTE"."id" = "PC_CONTRATO_CLIENTE_id"
                LEFT JOIN "HH_CONTROL" ON "CONTRATO_CLIENTE"."CC_CCODIGO" = "HH_CONTROL"."HH_CONTROL_PROY_ID"
                WHERE "PC_CONTRATO_CLIENTE_id"  = 2
                GROUP BY "HH_CONTROL_USER_ID",
                EXTRACT(YEAR  from "HH_CONTROL_FECHA")::int,
                EXTRACT(MONTH  from "HH_CONTROL_FECHA")::int
            ) AS DATOS
            GROUP BY USUARIO


            """
            cursor.execute(query, [contrato_id])
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(e)
        return 0
def get_detalle_apertura_costo_real(contrato_id):
    try:
        with connection.cursor() as cursor:
            query = """
                Select
                "HH_CONTROL_USER_ID",
                "HH_CONTROL_FECHA",
                "HH_CONTROL_HORAS",
                (
                    SELECT 
                    "CP_NVALOR"
                    FROM "COSTOS_PERSONA"
                    WHERE "CP_CNOMBRE" = "HH_CONTROL_USER_ID"
                    AND "CP_NAÑO" = EXTRACT(YEAR  from "HH_CONTROL_FECHA")::int
                    AND "CP_NMES" = EXTRACT(MONTH  from "HH_CONTROL_FECHA")::int
                ) AS "VALOR",
                (
                    SELECT 
                    "CP_NVALOR"
                    FROM "COSTOS_PERSONA"
                    WHERE "CP_CNOMBRE" = "HH_CONTROL_USER_ID"
                    AND "CP_NAÑO" = EXTRACT(YEAR  from "HH_CONTROL_FECHA")::int
                    AND "CP_NMES" = EXTRACT(MONTH  from "HH_CONTROL_FECHA")::int
                ) * "HH_CONTROL_HORAS" AS "VALOR_TOTAL",
                (
                    SELECT 
                    "CP_CMONEDA"
                    FROM "COSTOS_PERSONA"
                    WHERE "CP_CNOMBRE" = "HH_CONTROL_USER_ID"
                    AND "CP_NAÑO" = EXTRACT(YEAR  from "HH_CONTROL_FECHA")::int
                    AND "CP_NMES" = EXTRACT(MONTH  from "HH_CONTROL_FECHA")::int
                ) AS "MONEDA"		
                FROM "PROYECTO_CLIENTE"
                LEFT JOIN "CONTRATO_CLIENTE" ON "CONTRATO_CLIENTE"."id" = "PC_CONTRATO_CLIENTE_id"
                LEFT JOIN "HH_CONTROL" ON "CONTRATO_CLIENTE"."CC_CCODIGO" = "HH_CONTROL"."HH_CONTROL_PROY_ID"
                WHERE "PC_CONTRATO_CLIENTE_id"  = %s
                ORDER BY "HH_CONTROL_USER_ID","HH_CONTROL_FECHA"

            """
            cursor.execute(query, [contrato_id])
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(e)
        return 0

def get_sum_monto_pagado_tf(proyecto_id):
    try:
        with connection.cursor() as cursor:
            query = """
            SELECT 
                "MO_CMONEDA",
                SUM("TF_NMONTOPAGADO") 
            FROM "TAREA_FINANCIERA"
            LEFT JOIN "MONEDA" on "MONEDA".id = "TAREA_FINANCIERA"."TF_MONEDA_id"
            WHERE "TF_PROYECTO_CLIENTE_id" = %s
            GROUP BY "MO_CMONEDA"

            """
            print(query)
            cursor.execute(query, [proyecto_id])
            result = cursor.fetchone()
            if not result:
                return 0
            return result
    except Exception as e:
        print(e)
        return 0
def get_sum_monto_pendiente_tf(proyecto_id):
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    "MO_CMONEDA",
                    SUM("TF_NMONTO") 
                FROM "TAREA_FINANCIERA"
                LEFT JOIN "MONEDA" on "MONEDA".id = "TAREA_FINANCIERA"."TF_MONEDA_id"
                WHERE "TF_PROYECTO_CLIENTE_id" = %s
                GROUP BY "MO_CMONEDA"

            """
            print(query)
            cursor.execute(query, [proyecto_id])
            result = cursor.fetchone()
            if not result:
                return 0
            return result
    except Exception as e:
        print(e)
        return 0

def get_sum_costo_real(from_date, to_date):
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT
                    SUM("PC_NCOSTO_REAL")
                FROM "PROYECTO_CLIENTE"
                WHERE
                    "PC_FFECHA_INICIO" BETWEEN %s AND %s
            """
            print(query)
            cursor.execute(query, [from_date, to_date])
            result = cursor.fetchone()
            if not result:
                return 0
            return result[0]
    except Exception as e:
        print(e)
        return 0

def get_sum_horas_proyectadas(from_date, to_date):
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT
                    SUM("PC_NHORAS_ESTIMADAS")
                FROM "PROYECTO_CLIENTE"
                WHERE
                    "PC_FFECHA_INICIO" BETWEEN %s AND %s
            """
            cursor.execute(query, [from_date, to_date])
            result = cursor.fetchone()
            if not result:
                return 0
            return result[0]
    except Exception as e:
        print(e)
        return 0

def get_sum_horas_reales(from_date, to_date):
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT
                    SUM("PC_NHORAS_REALES")
                FROM "PROYECTO_CLIENTE"
                WHERE
                    "PC_FFECHA_INICIO" BETWEEN %s AND %s
            """
            cursor.execute(query, [from_date, to_date])
            result = cursor.fetchone()
            if not result:
                return 0
            return result[0]
    except Exception as e:
        print(e)
        return 0

def get_sum_presupuesto(from_date, to_date):
    try:
        with connection.cursor() as cursor:
            query = """
            SELECT
                    SUM(CASE 
                    WHEN "MO_CMONEDA" = 'CLP' THEN "PC_NPRESUPUESTO"
                    ELSE "PC_NPRESUPUESTO" * COALESCE((SELECT 
                                                    "TC_NTASA" 
                                                    FROM "TIPO_CAMBIO" 
                                                    WHERE "TC_CMONEDA_id" = "MONEDA"."id"
                                                    ORDER BY "id" DESC
                                                    LIMIT 1
                                                                    ), 1)
                END) 
            FROM "PROYECTO_CLIENTE"
            LEFT JOIN "MONEDA" on "MONEDA".id = "PROYECTO_CLIENTE"."PC_MONEDA_id"
            WHERE
            "PC_FFECHA_INICIO" >= %s
            and "PC_FFECHA_INICIO" <= %s
            """
            cursor.execute(query, [from_date, to_date])
            result = cursor.fetchone()
            if not result:
                return 0
            return result[0]
    except Exception as e:
        print(e)
        return 0
    
def get_codigo_proyecto_generico(codigo_contrato):
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT
                "PC_CCODIGO"
                FROM "PROYECTO_CLIENTE"
                LEFT JOIN "CONTRATO_CLIENTE" ON "CONTRATO_CLIENTE"."id" = "PC_CONTRATO_CLIENTE_id"
                WHERE "CC_CCODIGO" = %s
                ORDER BY "PC_CCODIGO" DESC 
            """
            cursor.execute(query, [codigo_contrato])
            result = cursor.fetchone()
            if not result:
                return 0
            return result[0]
    except Exception as e:
        print(e)
        return 0

def get_sum_edp(from_date, to_date):
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT
                    SUM("EP_NTOTAL") - SUM("EP_NMONTO_PAGADO")
                FROM "ESTADO_DE_PAGO"
                INNER JOIN 
                    "PROYECTO_CLIENTE" ON "PROYECTO_CLIENTE"."id" = "ESTADO_DE_PAGO"."EP_PROYECTO_id"
                WHERE
                    "PROYECTO_CLIENTE"."PC_FFECHA_INICIO" BETWEEN %s AND %s
            """
            cursor.execute(query, [from_date, to_date])
            result = cursor.fetchone()
            if not result:
                return 0
            return result[0]
    except Exception as e:
        print(e)

def get_projects_closed_by_date(from_date, to_date):
    try:
        with connection.cursor() as cursor:
            query = f"""
                SELECT
                    "PC_CCODIGO", 
                    "PC_CNOMBRE", 
                    "PC_FFECHA_INICIO", 
                    "PC_FFECHA_FIN_ESTIMADA", 
                    "PC_FFECHA_FIN_REAL", 
                    "PC_NPRESUPUESTO", 
                    "PC_NCOSTO_REAL", 
                    "PC_NCOSTO_ESTIMADO", 
                    "PC_NHORAS_REALES", 
                    "PC_NHORAS_ESTIMADAS", 
                    "id"
                FROM "PROYECTO_CLIENTE"
                WHERE
                    "PC_FFECHA_FIN_REAL" BETWEEN '{from_date}' AND '{to_date}' AND
                    "PC_CESTADO" = 'Cerrado'
            """
            print(query)
            cursor.execute(query)
            result = cursor.fetchall()
            if not result:
                return []
            return result
    except Exception as e:
        print(e)
        return []

def get_tipo_cambio(moneda_id, fecha):
    today = date.today()
    
    try:
        with connection.cursor() as cursor:
            # 1. Buscar el tipo de cambio exacto para la fecha dada
            cursor.execute("""
                SELECT "TC_NTASA"
                FROM "TIPO_CAMBIO"
                WHERE "TC_CMONEDA_id" = %s AND "TC_FFECHA" = %s
            """, [moneda_id, fecha])
            result = cursor.fetchone()
            
            if result:
                return Decimal(result[0])

            # 2. Buscar el tipo de cambio para la fecha actual
            cursor.execute("""
                SELECT "TC_NTASA"
                FROM "TIPO_CAMBIO"
                WHERE "TC_CMONEDA_id" = %s AND "TC_FFECHA" = %s
            """, [moneda_id, today])
            result = cursor.fetchone()
            
            if result:
                return Decimal(result[0])

            # 3. Buscar el tipo de cambio más cercano hacia el pasado desde la fecha actual
            cursor.execute("""
                SELECT "TC_NTASA"
                FROM "TIPO_CAMBIO"
                WHERE "TC_CMONEDA_id" = %s AND "TC_FFECHA" < %s
                ORDER BY "TC_FFECHA" DESC
                LIMIT 1
            """, [moneda_id, today])
            result = cursor.fetchone()
            
            if result:
                return Decimal(result[0])

    except Exception as e:
        print(e)
        return None

#########################################
#########################################
#########################################
