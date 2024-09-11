from django.db import connection

#########################################
########         INICIO         #########
#########################################

def get_projects_closed(from_date, to_date):
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
#########################################
#########################################
#########################################
