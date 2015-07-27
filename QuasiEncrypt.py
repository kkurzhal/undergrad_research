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
        self.last_num = 257
        self.wrap_num = self.last_num - 1
        self.block_size = 8

    def run_through_example(self, message='hello world', first_row=[], leader=4, algorithm = None):
        """
        Take a message and run through the entire encoding/decoding
        process, printing out the information along the way.
        """
        print 'Initial message:', '"' + message + '"'
        print 'Initial first row:', first_row
        print 'Initial leader:', leader, '\n'
        
##        bits = self.message_to_bit_list(message)
##        print 'Bit list:', bits
        
##        numbers = self.bit_list_to_number_list(bits)
##        print 'Number list:', numbers, '\n'

        numbers = self.message_to_number_list(message)

        encode_square = self.construct_encoding_square(first_row, algorithm)
        print 'Encoding latin square:'
##        self.print_matrix(encode_square), '\n'
        print len(encode_square), 'x', len(encode_square[-1])

        encoded_message = self.encode_message(numbers, encode_square, leader)
        print 'Encoded message length:', len(encoded_message)
        print 'Encoded message:'
        print encoded_message

        print 'First row:', encode_square[0]

        packaged_message = self.package_message(encoded_message, encode_square, leader)
        print 'Packaged message:', packaged_message, '\n'

        leader, first_row, de_encoded_message = self.unpackage_message(packaged_message)
        print 'Unpackaged leader:', leader
        print 'Unpackaged first row:', first_row
        print 'Unpackaged encoded message:', encoded_message

        print 'Encoded == De-encoded:', encoded_message == de_encoded_message
        print 'De-encoded message length:', len(de_encoded_message)

        encode_square = self.construct_encoding_square(first_row)
        print 'Unpackaged encoding square:'
##        self.print_matrix(encode_square)

        decode_square = self.construct_decoding_square(encode_square)
        print 'Decoding latin square:'
##        self.print_matrix(deacode_square)

##        encoded_message = self.message_to_bit_list(encoded_message)
##        encoded_message = self.bit_list_to_number_list(encoded_message)
        unpackaged_number_list = self.message_to_number_list(de_encoded_message)
        print 'De-encoded number list == Encoded number list:', numbers == unpackaged_number_list
        print 'Unpackaged number list:', unpackaged_number_list

        numbers = self.decode_message(unpackaged_number_list, decode_square, leader)
        print 'Decoded message/number list:', numbers

##        bits = self.number_list_to_bit_list(numbers)
##        print 'Decoded bit list:', bits

##        message = self.bit_list_to_message(bits)
##        print 'Decoded message:', message

        final_message = self.number_list_to_message(numbers)
        print 'Decoded message:', '"' + final_message + '"'
        print 'Decoded message == Original message:', final_message == message

    def wrap_value(self, value):
        """
        Get the wrapped value that results when a number is too high.
        """
        if value == self.wrap_num:
            return 0
        else:
            return value

    def unwrap_value(self, value):
        """
        Get the unwrapped value that results when a number is 0.
        """
        if value == 0:
            return self.wrap_num
        else:
            return value

    def custom_encoding_algorithm(self, x, y):
        return (x + y + (3 * (((x**2) * y) % 9)))

    def default_encoding_algorithm(self, x, y):
        return x * y

    def construct_encoding_square(self, first_row = [], algorithm = None):
        """
        Construct the matrix needed to encode and decode the pseudomessage.
        """
        matrix = []

        #If the first row is passed to the function then use it, otherwise make
        #a random first row.
        if len(first_row) == 0:
            first_row = range(1, self.last_num)
##            first_row = map(lambda value: chr(value), first_row)
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
                try:
                    algorithm_result = 0
                    
                    if algorithm == None:
                        algorithm_result = self.default_encoding_algorithm(each_num, each_column)
                    else:
                        algorithm_result = algorithm(each_num, each_column)
                        
                    new_value = algorithm_result % (self.last_num)

                    #Add the value to the new row.
                    each_row.append(new_value)
                except Exception as err:
                    print err
                    print 'each_num type:', type(each_num)
                    print 'each_column type:', type(each_column)
                    print 'each_column value:"' + each_column + '"'
                    print 'last_num type:', type(self.last_num)
                    print 'Value:', new_value
                    print 'First Row:', first_row
                    exit(1)

            #Add the row to the matrix
            matrix.append(each_row)

        return matrix

    def construct_decoding_square(self, encoding_latin_square):
        """
        Construct a latin square that is the alternate match to another
        latin square.  This allows for the creation of a quasigroup that
        is used for decoding a message.
        """
        new_latin_square = []

        for each_row in encoding_latin_square:
            #Prepare all the elements of the row for appending.
            new_row = [None for each_column in each_row]

            for index, each_column in enumerate(each_row):
                #Put the column value of the old latin square into the matching
                #column in the new latin square.
                try:
                    new_row[each_column - 1] = index + 1
                except Exception as err:
                    print err
                    print each_column
                    exit(1)
                

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
            number_as_integer = each_number
            
            #Start the encoded message by mapping the first number in the number
            #message.
            if index == 0:
                previous_number = latin_square[leader - 1][number_as_integer - 1]

            #If it isn't the start, then use the previously mapped quasigroup
            #instead of the leader.
            else:
                previous_number = latin_square[previous_number - 1][number_as_integer - 1]

            encoded_message += chr(self.wrap_value(previous_number))

        return encoded_message

    def decode_message(self, number_message, latin_square, leader):
        """
        Decode the message using the AON methodology.
        """
        new_value = 0
        decoded_number_list = []
        
        for index, each_number in enumerate(number_message):
            number_as_integer = each_number

            #If the first item in the message is evaluated, then use the leader.
            if index == 0:
                new_value = latin_square[leader - 1][number_as_integer - 1]

            #Otherwise, use the current item with the next item.
            else:
                previous_number = number_message[index - 1]
##                print previous_number
                new_value = latin_square[previous_number - 1][number_as_integer - 1]

            decoded_number_list.append(self.unwrap_value(new_value))

        return decoded_number_list

    def bit_list_to_number_list(self, bit_list):
        """
        Take a bit list and turn it into a number list to map the values
        for encoding.
        """
        #Convert each set of bits to the proper integer and add it to the number
        #list.
        number_list = map(lambda bit_string: int(bit_string, 2), bit_list)

        return number_list

    def number_list_to_bit_list(self, number_list):
        """
        Take a number list and turn it into a bit list to map the values
        for decoding.
        """
        bit_list = map(lambda each_number: bin(each_number), number_list)

        return bit_list

    def package_message(self, encoded_message, matrix, leader):
        """
        Package the encoded message with the the chosen leader and first
        row of the matrix.
        """
        row = map(lambda each_number: chr(self.wrap_value(each_number)), matrix[0])
        packaged_message = chr(self.wrap_value(leader)) + ''.join(row) + encoded_message
        return packaged_message

    def unpackage_message(self, packaged_message):
        """
        Unpack the message after it is received and return the leader,
        first row of the matrix, and encoded message in a tuple.
        """
        leader = self.unwrap_value(ord(packaged_message[0]))
        first_row = map(lambda each_number: self.unwrap_value(ord(each_number)), packaged_message[1:self.last_num])
        encoded_message = packaged_message[self.last_num:]
        return (leader, first_row, encoded_message)

    def convert_message_to_number_string(self, message):
        """
        Convert the binary representing the characters into a string of
        numbers  for the encoding.
        """
        #Get the value of each character and format it in terms of bits.
        number_list = [str(ord(character)) for character in message]
        return ''.join(number_list)

    def message_to_number_list(self, message):
        return map(lambda each_character: self.unwrap_value(ord(each_character)), message)

    def number_list_to_message(self, number_list):
        return ''.join(map(lambda each_number: chr(self.wrap_value(each_number)), number_list))

    def message_to_bit_list(self, message):
        """
        Get a list of bit strings representing the message, where the
        number of bits is determined by the set block size for the
        class.
        """
        bit_list = []

        #Loop through each character in the message.
        for each_character in message:
            character_value = ord(each_character)
            
            #Get the binary string represented for the interger representation
            #of the character.
            bit_string = bin(character_value)[2:]

            #Get the padding that might possibly be needed.
            needed_padding = self.block_size - (len(bit_string) % self.block_size)
            padding = '0' * needed_padding
            bit_string = padding + bit_string

            #Handle any cases where the remaining bit string is larger than
            #the block size by splitting up the bit string into that block size.
            block_split_count = len(bit_string) / self.block_size
            for each_block in range(block_split_count):
                #Get the block of bits from the bit string.
                string_position = (each_block + 1) * self.block_size
                bits = bit_string[:string_position]

                #Add the block bits to the bit list and throw away those bits
                #from the bit string.
                bit_list.append(bits)
                bit_string = bit_string[string_position:]
            
        return bit_list

    def bit_list_to_message(self, bit_list):
        """
        Take a bit list and convert it back into the appropriate
        message.  The resulting message depends on the set block size
        of the class.
        """
        message = ''

        #Join the bits together into a single string.
        bit_string = ''.join(bit_list)

        #Unpack all blocks of bits into a message.
        while len(bit_string) > 0:
            
            #Get the value of the block of bits and the matching character.
            bit_value = int(bit_string[:self.block_size], 2)
            character = chr(bit_value)

            #Get the character and clear the bits from the original bit string.
            message += character
            bit_string = bit_string[self.block_size:]

        return message

    def print_matrix(self, matrix):
        for each_row in matrix:
            print each_row
        
