import unittest
from itertools import permutations
from QuasiEncrypt import QuasiAON

class TestQuasiAON(unittest.TestCase):
    """
    This class tests the QuasiAON class methods to ensure that they
    work properly.
    """
    def setUp(self):
        self.aon_instance = QuasiAON()
    
    def test_random_construct_latin_square(self):
        """
        Test construct_latin_square() to make sure that a true latin
        square is created by running the construct function a specified
        number of times.
        """
        #Test the matrix construction as many times as is specified.
        for each_test in range(50):
            matrix = self.aon_instance.construct_latin_square()

            #Check to make sure that the resulting matrix is square.
            self.assertTrue(len(matrix[0]) == len(matrix))

            #Check the rows to make sure that no duplicates values exist.
            for each_row in matrix:

                #Create a unique set of values.
                unique_list = set(each_row)

                #Check that the length of the unique set matches the length of
                #the original row.
                self.assertTrue(len(unique_list) == len(each_row))

            #Check the columns to make sure that no duplicates exist.
            for each_column in range(len(matrix)):

                #Get the column of values.
                column = map(lambda row: row[each_column], matrix)

                #Get the unique set of values in the column.
                unique_column = set(column)

                #Check that the length of the unique set matches the length of
                #the original column.                
                self.assertTrue(len(unique_column) == len(column))

    def test_all_latin_squares_for_set_dimension(self):
        """
        Test all possible combinations of a latin square based on the
        specified dimensions.
        """
        #Test the matrix construction for all combinations of a range.
        number_range = range(1, self.aon_instance.last_num)
        for each_test in permutations(number_range):
            matrix = self.aon_instance.construct_latin_square(each_test)

            #Check to make sure that the resulting matrix is square.
            self.assertTrue(len(matrix[0]) == len(matrix))

            #Check the rows to make sure that no duplicates values exist.
            for each_row in matrix:

                #Create a unique set of values.
                unique_list = set(each_row)

                #Check that the length of the unique set matches the length of
                #the original row.
                self.assertTrue(len(unique_list) == len(each_row))

            #Check the columns to make sure that no duplicates exist.
            for each_column in range(len(matrix)):

                #Get the column of values.
                column = map(lambda row: row[each_column], matrix)

                #Get the unique set of values in the column.
                unique_column = set(column)

                #Check that the length of the unique set matches the length of
                #the original column.                
                self.assertTrue(len(unique_column) == len(column))

if __name__ == '__main__':
    unittest.main()
