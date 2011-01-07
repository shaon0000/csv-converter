import unittest
from csv_converter import CSVdata

class CSVdataTest(unittest.TestCase):
    def setUp(self):
        self.files = []
        self.new_data = CSVdata(['january', 'february', 'march'])
        
        """ first data source is a typical ideal case.
            All of the mandatory columns are in perfect order.
        """
        self.test_csv_file_nice = [['address1','city','name','zip','country','lol_factor','bigs'],
                               ['random', 'SF', 'shaon', '12351', 'USA', '23523', '2352324'],
                               ['even', 'SF', 'shaon', '54632', 'USA', '12', '141']]
        
        """ Test data has a random column in between two mandatory columns """
        self.test_csv_file_column_swap = [['city','random_column','address1','name','zip','country','lol_factor','bigs'],
                               ['SF','', 'random', 'shaon', '12351', 'USA', '23523', '2352324'],
                               ['SF','', 'even', 'shaon', '54632', 'USA', '12', '141']]
        
        """ Test data is missing 'city' column, should produce error! """
        self.test_csv_file_missing_must_have = [['address1','name','zip','country','lol_factor','bigs'],
                               ['random', 'shaon', '12351', 'USA', '23523', '2352324'],
                               ['even', 'shaon', '54632', 'USA', '12', '141']]
    
    def test_new_csv_file_nice(self):
        self.assertEqual(self.new_data.new_csv_file(self.test_csv_file_nice[0], 'january'), None, 'ideal csv file format was not accepted, serious error!')
        self.assertEqual(self.new_data.must_have_locations, [0,1,2,3,4], 'ideal data did not create a must_have index list properly '+str(self.new_data.must_have_locations))

    def test_new_csv_file_column_swap(self):
        self.assertEqual(self.new_data.new_csv_file(self.test_csv_file_column_swap[0], 'january'), None, 'swapped csv could not be created')
        self.assertEqual(self.new_data.must_have_locations, [0,2,3,4,5], 'improper column order did not induce a change in must_have_location order '+str(self.new_data.must_have_locations))
    
    def test_new_csv_file_error(self):
        try:
            self.new_data.new_csv_file(self.test_csv_file_missing_must_have[0], 'january')
            raise Exception('did not error on trying to push columns with missing mandatory columns!')
        except:
            assert True
    
    def test_creating_table(self):
        self.new_data.get_or_create_table('awesome') 
    
    def test_row_loading(self):
        """ try to load in a row from original csv structure """
    
        self.new_data.new_csv_file(self.test_csv_file_nice[0], 'january')
        for row in self.test_csv_file_nice[1:]:
            self.new_data.load_csv_line_list(row)
        self.assertEqual(set(self.new_data.tables.keys()), set(['lol_factor','bigs']), str(self.new_data.tables.keys()))
        self.assertEqual(self.new_data.tables['lol_factor']['rows'][('random','SF','shaon','12351','USA')]['january'],'23523', 'did not get expected value, got instead: '+str(self.new_data.tables['lol_factor']['rows'][('random','SF','shaon','12351','USA')]['january']))
    
    def test_row_loading_out_of_order(self):
        """ try to load in a row from original csv structure """
    
        self.new_data.new_csv_file(self.test_csv_file_column_swap[0], 'january')
        for row in self.test_csv_file_column_swap[1:]:
            self.new_data.load_csv_line_list(row)
        self.assertEqual(set(self.new_data.tables.keys()), set(['lol_factor','bigs', 'random_column']), str(self.new_data.tables.keys()))
        self.assertEqual(self.new_data.tables['lol_factor']['rows'][('random','SF','shaon','12351','USA')]['january'],'23523', 'did not get expected value, got instead: '+str(self.new_data.tables['lol_factor']['rows'][('random','SF','shaon','12351','USA')]['january']))
    

    def tearDown(self):
        self.files = []
        self.new_data = None
        self.test_csv_file_nice =[]
        self.test_csv_file_column_swap = []
        self.test_csv_file_missing_must_have = []

if __name__ == '__main__':
    unittest.main()
