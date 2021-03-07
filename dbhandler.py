import pymysql

config = {
    'user': 'anonymous',
    'passwd': '',
    'host': 'ensembldb.ensembl.org',
    'port': 3306,
    'database': 'ensembl_website_102',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# Connect to production database
def getConnection():
    return pymysql.connect(**config)

def suggestGeneNames(query, species, limit):
    return doQuery(query, species, limit, getConnection())
    
def doQuery(query, species, limit, connection):
    result = []
    with connection:
        with connection.cursor() as cursor:
            sql = 'SELECT `display_label` FROM `gene_autocomplete` WHERE `species`=%s AND `display_label` LIKE %s LIMIT %s;'
            num_rows = cursor.execute(sql, (species, "{}%".format(query), limit))
            if num_rows > 0:
                result = [d['display_label'] for d in cursor.fetchall()]
    return { 'result': result}
