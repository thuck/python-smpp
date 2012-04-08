def parser_int_parameter(max_size, data):
    return data[:max_size], data[max_size:]

def parser_c_octet_string(data):
    index = data.find('00')
    return data[:index], data[index+2:]

def parser_octet_string(length, data):
    return data[:length], data[length:]

def parse_header(data):
    return 

def smpp_parser(data):
    (command_length, command_id,
    command_status, sequence_number,
    data) = data[:8], data[8:16], data[16:24], data[24:32], data[32:]


