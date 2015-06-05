import random

class QuasiAON(object):
    """
    This class is designed to handle the encoding and decoding of a message
    by using the All-or-Nothing approach and applying Quasigroups.  It is
    not intended as a full encryption method, but rather as an addition
    to another encryption method to increase security.
    """
    def __init__(self):
        pass

    def construct_latin_square(self):
        """
        Construct the matrix needed to encode and decode the pseudomessage.
        """
        matrix = []
        last_num = 256

        #Get the first row of integers in a random order.
        first_row = range(1, last_num)
        random.shuffle(first_row)

        #Add the first row to the matrix
        matrix.append(first_row)

        #Get the remaining rows.
        for each_num in range(2, last_num):
            each_row = []

            #Loop over each column in the first row to calculate the
            #appropriate values for the following rows.
            for each_column in matrix[0]:
                #Calculate the value.
                new_value = (each_num * each_column) % (last_num + 1)

                #Add the value to the new row.
                each_row.append(new_value)

            #Add the row to the matrix
            matrix.append(each_row)

        return matrix
        
