import pymysql
import testing.mysqld
import unittest

import dbhandler

def handler(mysqld):
    conn = pymysql.connect(**mysqld.dsn())
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE `gene_autocomplete` (`species` VARCHAR(50), `display_label` VARCHAR(50))""")
    cursor.execute("""INSERT INTO  `gene_autocomplete` (`species`, `display_label`) 
        VALUES ('S1','G1'),('S1','G2'), ('S2','G3'), ('S2','G4')""")
    cursor.close()
    conn.commit()
    conn.close()

Mysqld = testing.mysqld.MysqldFactory(cache_initialized_db=True, on_initialized=handler, port=7531)
    
def tearDownModule():
    Mysqld.clear_cache()

class TestGeneSuggestQuery(unittest.TestCase):
    def setUp(self):
        self.mysql = Mysqld()
        self.connection = pymysql.connect(**self.mysql.dsn(),cursorclass=pymysql.cursors.DictCursor)

    def tearDown(self):
        self.mysql.stop()
    
    def test_No_results(self):
        result = dbhandler.doQuery('X', 'Y', 10, self.connection)
        self.assertTrue(result == {'result': []})
        
    def test_S1_G(self):
        result = dbhandler.doQuery('G', 'S1', 2, self.connection)
        self.assertTrue(result == {'result': ['G1', 'G2']})
    
    def test_S2_G(self):
        result = dbhandler.doQuery('G', 'S2', 2, self.connection)
        self.assertTrue(result == {'result': ['G3', 'G4']})


if __name__ == '__main__':
    unittest.main()
