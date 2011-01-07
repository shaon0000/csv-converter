# author: Shaon Bhuiyan
# description: a CSV data extractor that lets us generate another CSV file
# TODO: create testsamples of CSV lines
# TODO: build a testing system to test this code
# TODO: check with viv to see what he thinks of this idea

import csv
import os
import sys
import fnmatch

DEBUG = True # does more printing and checks if this is set to True

def print_debug( *args):
    print_objs = []
    for i in range(0, len(args)):
        print_objs.append(str(args[i]))
    print ' '.join(print_objs)

class CSVdata:
    def __init__(self, months):
        """
        table----------- column_names
            |
            |
            |
    (name, address1, cit, state, zip) <-- identity set
                    |
                    |
                    |------|------|------|
                   jan    feb    mar    apr
                    |
                    |
                    |
                  VALUE
        the whole point of this is that this scheme prioritizes data-elements such as ad_clicks first.
        It then prioritizes months because our initial CSV emphasized months so this lets us place items by months easily,
        but lets us later create tables based on data-elements later.
        """
        self.tables = {}
        self.months = months # this takes whatever months it can find!
        self.must_have = ('address1','city','name','zip','country') # this are defining columns
        self.ignore = ('package','impression_limit') # ignore these columns
    
    def new_csv_file(self, columns, month):
        # called to prepare structure for new csv file
        self.original_csv_columns = columns
        self.current_month = month
        self.column_integrity_check()
        self.create_row_rule()

    def column_integrity_check(self):
        # check to make sure the csv columns have must-have columns
        print_debug("insuring column integrity!", 
                    (set(self.original_csv_columns) & set(self.must_have)), 
                    self.must_have
                    )
        assert (set(self.original_csv_columns) & set(self.must_have)) == set(self.must_have)
    
    def create_row_rule(self):
        """makes a list that relates to self.original_csv_columns"""
        if DEBUG: # this is incase create_row_rule is called during coding stage improperly
            self.column_integrity_check() # check here before hand to make sure it works
        
        # define where must_have values are located in the original csv columns
        self.must_have_locations = [] 
        
        self.table_locations = [] # definitions for tables are located
        for i in range(0, len(self.original_csv_columns)):
            element = self.original_csv_columns[i]
            if element in self.must_have:
                self.must_have_locations.append(i)
            elif element in self.ignore:
                pass
            else:
                self.table_locations.append(i)
        
    def load_csv_line_list(self, line_list): 
        """ loads the row from the csv into our data structure """
        row_elements = list(self.must_have[0:]) 
        for i in self.must_have_locations: 
            #TODO: not sure if this algorithim can handle a csv swap with different 
            #      column formats
            column_name = self.original_csv_columns[i] # pull out original column name
            location = row_elements.index(column_name) # locate this data goes in identity columns
            row_elements[location] = line_list[i] 
        # disable any possibility of making changes to row_elements
        # it will now work as an identification tag
        row_elements = tuple(row_elements)
        
        for i in self.table_locations:
            table_name = self.original_csv_columns[i]
            identity_tuple_row = self.get_or_create_identity_tuple(table_name, row_elements)
            identity_tuple_row[self.current_month] = line_list[i]
            
    def check_row_has_no_NULLS(self, row):
        # check to make sure the row doesn't have any None elements
        assert [x for x in row if x is None] is []

    def get_or_create_identity_tuple(self, table_name, identity_tuple):
        """ return a generated or pre-existing row with the given identity_tuple """
        # do some asserts to insure structure was properly prepared
        # not too many asserts now, but it might get bigger along the way
        assert self.months is not None
        table = self.get_or_create_table(table_name) # attempt to get the table
        if identity_tuple in table['rows']:
            pass
        else:
            table['rows'][identity_tuple] = {}
            for month in self.months:
                table['rows'][identity_tuple][month] = None
        return table['rows'][identity_tuple]

    def get_or_create_table(self, name):
        """ return a generated or pre-existing table """
        #TODO: create some assertions to insure that tables are made after proper configuration
        #TODO: define a proper configuration
        if name in self.tables:
            pass
        else:
            self.tables[name] = { 'column_names': self.must_have, 'rows': {}}
        return self.tables[name]

def find_year(word): # return the year found in a word
    # this basically finds the first sequence of four integers
    nums = '0123456789'
    year = ''
    for i in word:
        if i in nums:
            year += i
            
        else:
            if len(year) == 4:
                return year
            year = ''
    if len(year) == 4:
        return year
    return None

args = sys.argv

def find_year_test():
    tests = [('a0',None), ('a01',None), ('a00000', None), ('13523425234', None), ('135235234',None), ('!@$@#3241@@#"','3241'), ('ABCD4567', '4567'), ('1234ABC','1234')]
    correct_expected = len(tests)
    correct_recieved = 0
    for test in tests:
        try:
            assert find_year(test[0]) == test[1]
            print "test:",test[0],"PASSED!"
            correct_recieved += 1
        except AssertionError:
            print "---- FAILED TEST CASE -----"
            print "test:",test[0],"FAILED!"
            print "expected:",test[1],"got:",find_year(test[0])
            print "---------------------------"
    print "%s/%s" % (correct_recieved, correct_expected), "passed"
    return None

""" first check if find_year is to be tested """
if len(args) >= 2:
    if args[1] == 'find_year-test':
        find_year_test()
        exit()

print "looking through these files..."
potential_files = os.listdir(os.getcwd())
for i in potential_files:
    print i

print "NOTE: only considering these files! files must have a year and must of .csv type to be considered!!"
potential_files = [x for x in potential_files if find_year(x) is not None and fnmatch.fnmatch(x, '*.csv')]

for i in potential_files:
    print "--->",i

print "---"
print "3) generating years to show"

mode = "YEAR_PICK"
year = None

while mode == "YEAR_PICK":
    possible_years = list(set([find_year(x) for x in potential_files]))
    for i in range(0, len(possible_years)):
        print "<",i,">", possible_years[i]

    print "select a year from above (give the entry number, NOT the year!)"
    
    year_index = input()
    
    if year_index >= 0 and year_index < len(possible_years):
        year = possible_years[year_index]
        mode = "CSV_LOAD"

potential_files = [x for x in potential_files if find_year(x) == year]    
match_checks = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul','aug','sep','oct', 'nov', 'dec']










