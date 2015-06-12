import random

class QuasiAON(object):
    """
    This class is designed to handle the encoding and decoding of a message
    by using the All-or-Nothing approach and applying Quasigroups.  It is
    not intended as a full encryption method, but rather as an addition
    to another encryption method to increase security.
    """
    def __init__(self):
        #This must always be a prime number to get a true latin square.
        self.last_num = 7

    def construct_latin_square(self, first_row = []):
        """
        Construct the matrix needed to encode and decode the pseudomessage.
        """
        matrix = []

        #If the first row is passed to the function then use it, otherwise make
        #a random first row.
        if len(first_row) == 0:
            first_row = range(1, self.last_num)
            random.shuffle(first_row)

        #Add the first row to the matrix
        matrix.append(first_row)

        #Get the remaining rows.
        for each_num in range(2, self.last_num):
            each_row = []

            #Loop over each column in the first row to calculate the
            #appropriate values for the following rows.
            for each_column in matrix[0]:
                #Calculate the value.
                new_value = (each_num * each_column) % (self.last_num)

                #Add the value to the new row.
                each_row.append(new_value)

            #Add the row to the matrix
            matrix.append(each_row)

        return matrix

    def construct_latin_square_match(self, old_latin_square):
        """
        Construct a latin square that is the alternate match to another
        latin square.  This allows for the creation of a quasigroup that
        is used for decoding a message.
        """
        new_latin_square = []

        for each_row in old_latin_square:
            #Prepare all the elements of the row for appending.
            new_row = [None for each_column in each_row]

            for index, each_column in enumerate(each_row):
                #Put the column value of the old latin square into the matching
                #column in the new latin square.
                new_row[each_column - 1] = index + 1

            #Add the row to the new matching latin square.
            new_latin_square.append(new_row)

        return new_latin_square

    def encode_message(self, number_message, latin_square, leader):
        """
        Encode the message using the AON methodology.
        """
        #Initialize the encoded message and previous number variables.
        previous_number = 0
        encoded_message = ''

        for index, each_number in enumerate(number_message):
            number_as_integer = int(each_number)
            
            #Start the encoded message by mapping the first number in the number
            #message.
            if index == 0:
                previous_number = latin_square[leader - 1][number_as_integer - 1]

            #If it isn't the start, then use the previously mapped quasigroup
            #instead of the leader.
            else:
                previous_number = latin_square[previous_number - 1][number_as_integer - 1]

            encoded_message += str(previous_number)

        return encoded_message

    def decode_message(self, number_message, latin_square, leader):
        """
        Decode the message using the AON methodology.
        """
        new_value = 0
        decoded_message = ''
        
        for index, each_number in enumerate(number_message):
            number_as_integer = int(each_number)

            #If the first item in the message is evaluated, then use the leader.
            if index == 0:
                new_value = latin_square[leader - 1][number_as_integer - 1]

            #Otherwise, use the current item with the next item.
            else:
                previous_number = int(number_message[index - 1])
                print previous_number
                new_value = latin_square[previous_number - 1][number_as_integer - 1]

            decoded_message += str(new_value)

        return decoded_message

    def package_message(self, encoded_message, matrix, leader):
        """
        Prepare the message for sending.
        """
        pass

    def unpackage_message(self, packet):
        """
        Unpack the message after it is received.
        """
        pass

    def convert_message_to_number_string(self, message):
        """
        Convert the binary representing the characters into a string of
        numbers  for the encoding.
        """
        #Get the value of each character and format it in terms of bits.
        number_list = [str(ord(character)) for character in message]
        return ''.join(number_list)

    def print_matrix(self, matrix):
        for each_row in matrix:
            print each_row
        
