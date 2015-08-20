from QuasiEncrypt import QuasiAON

class Sender(QuasiAON):
    def encode(self, message, first_row = [], leader = 4, algorithm = None):
        # Get the number list representing the message.
        number_list = self.message_to_number_list(message)

        # Get the encoding square and get the encoded message.
        encoding_square = self.construct_encoding_square(first_row, algorithm)
        encoded_message = self.encode_message(number_list, encoding_square, leader)

        # Package the message and return it.
        packaged_message = self.package_message(encoded_message, encoding_square, leader)

        return packaged_message

class Receiver(QuasiAON):
    def decode(self, packaged_message, algorithm = None):
        # Unpackage the message.
        leader, first_row, encoded_message = self.unpackage_message(packaged_message)

        # Get the decoding square to decode the message.
        encoding_square = self.construct_encoding_square(first_row, algorithm)
        decoding_square = self.construct_decoding_square(encoding_square)

        # Turn the encoded message into the list of integers representing it.
        encoded_number_list = self.message_to_number_list(encoded_message)

        # Convert the encoded integer list into a decoded integer list.
        decoded_number_list = self.decode_message(encoded_number_list, decoding_square, leader)

        # Get the message related to the decoded number list.
        message = self.number_list_to_message(decoded_number_list)

        return message

if __name__ == '__main__':
    sender = Sender()
    receiver = Receiver()

    messages = ['hello world!', 'this is a test of the messaging', 'blah 13941d031@#d94J$(%)#']

    for message in messages:
        packaged_message = sender.encode(message)
        if message == receiver.decode(packaged_message):
            print 'Successful message:', message
        else:
            print 'Unsuccessful message:', message
    
