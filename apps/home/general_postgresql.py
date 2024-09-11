from django.db import connection

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
                    SUM("PC_NPRESUPUESTO")
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

#########################################
#########################################
#########################################
