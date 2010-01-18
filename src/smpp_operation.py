import smpp_const
import smpp_parts as part
import asyncore
import socket
import binascii
import struct

class Header(object):
    def __init__(self, command_id = None, 
                       command_status = None, sequence_number = None):
        self.command_length = part.CommandLength()
        self.command_id = part.CommandID(command_id)
        self.command_status = part.CommandStatus(command_status)
        self.sequence_number = part.SequenceNumber(sequence_number)
        self.body = []
        self.optional_parameter = []
        
    def format_message(self):
        message = ''
        full_body = self.body[:]
        full_body.extend(self.optional_parameter)
        for i in self.body:
            message += i()

        message = '%s%s%s%s%s' % (self.command_length(full_body),
                                self.command_id(),
                              self.command_status(), self.sequence_number(),
                              message)
        
        for i in self.optional_parameter:
            if len(i) > 0:
                message += i()
                
        return message

        
class BindTransmitter(Header):
    def __init__(self, sequence_numb, system_id = '', password = '',
                       system_type = '', interface_version = 52,
                       addr_ton = 0, addr_npi = 0, address_range = ''):
                       
        Header.__init__(self, command_id = smpp_const.BIND_TRANSMITTER,
                               command_status = smpp_const.ESME_ROK,
                               sequence_number = sequence_numb)
                               
        self.system_id = part.SystemID(system_id)
        self.password = part.Password(password)
        self.system_type = part.SystemType(system_type)
        self.interface_version = part.InterfaceVersion(interface_version)
        self.addr_ton = part.AddrTon(addr_ton)
        self.addr_npi = part.AddrNpi(addr_npi)
        self.address_range = part.AddressRange(address_range)
        self.body = [self.system_id, self.password,
                            self.system_type, self.interface_version,
                            self.addr_ton, self.addr_npi, self.address_range]


                
class BindTransmitterResp(Header):
    def __init__(self, sequence_numb, command_stat = smpp_const.ESME_ROK,
                 system_id = '', sc_interface_version = None):
        
        Header.__init__(self, command_id = smpp_const.BIND_TRANSMITTER_RESP,
                               command_status = command_stat,
                               sequence_number = sequence_numb)
        self.system_id = part.SystemID(system_id)
        self.sc_interface_version = part.SCInterfaceVersion(sc_interface_version)
        
        self.body = [self.system_id]
        self.optional_parameter = [self.sc_interface_version]
        
    def format_message(self):
        message = ''
        full_body = self.body[:]
        full_body.extend(self.optional_parameter)

        if self.command_status() == smpp_const.ESME_ROK:
            for i in self.body:
                message += i()
            message = '%s%s%s%s%s' % (self.command_length(full_body),
                                      self.command_id(),
                                      self.command_status(),
                                      self.sequence_number(), message)
            for i in self.optional_parameter:
                if len(i) > 0:
                    message += i()

        else:
            message = '%s%s%s%s' % (self.command_length([]),
                                    self.command_id(),
                                    self.command_status(),
                                    self.sequence_number())
                
        return message

                               
class BindReceiver(Header):
    def __init__(self, sequence_numb, system_id = '', password = '',
                       system_type = '', interface_version = 52,
                       addr_ton = 0, addr_npi = 0, address_range = ''):
                       
        Header.__init__(self, command_id = smpp_const.BIND_RECEIVER,
                               command_status = smpp_const.ESME_ROK,
                               sequence_number = sequence_numb)
                               
        self.system_id = part.SystemID(system_id)
        self.password = part.Password(password)
        self.system_type = part.SystemType(system_type)
        self.interface_version = part.InterfaceVersion(interface_version)
        self.addr_ton = part.AddrTon(addr_ton)
        self.addr_npi = part.AddrNpi(addr_npi)
        self.address_range = part.AddressRange(address_range)
        self.body = [self.system_id, self.password,
                            self.system_type, self.interface_version,
                            self.addr_ton, self.addr_npi, self.address_range]


class BindReceiverResp(BindTransmitterResp):
    pass

class BindTranceiver(Header):
    def __init__(self, sequence_numb, system_id = '', password = '',
                       system_type = '', interface_version = 52,
                       addr_ton = 0, addr_npi = 0, address_range = ''):
                       
        Header.__init__(self, command_id = smpp_const.BIND_TRANSCEIVER,
                               command_status = smpp_const.ESME_ROK,
                               sequence_number = sequence_numb)
                               
        self.system_id = part.SystemID(system_id)
        self.password = part.Password(password)
        self.system_type = part.SystemType(system_type)
        self.interface_version = part.InterfaceVersion(interface_version)
        self.addr_ton = part.AddrTon(addr_ton)
        self.addr_npi = part.AddrNpi(addr_npi)
        self.address_range = part.AddressRange(address_range)
        self.body = [self.system_id, self.password,
                            self.system_type, self.interface_version,
                            self.addr_ton, self.addr_npi, self.address_range]

        
class BindTranceiverResp(Header):
    def __init__(self, sequence_numb, command_stat = smpp_const.ESME_ROK,
                 system_id = '', sc_interface_version = None):
        
        Header.__init__(self, command_id = smpp_const.BIND_TRANSCEIVER_RESP,
                               command_status = command_stat,
                               sequence_number = sequence_numb)
        self.system_id = part.SystemID(system_id)
        self.sc_interface_version = part.SCInterfaceVersion(sc_interface_version)
        
        self.body = [self.system_id]
        self.optional_parameter = [self.sc_interface_version]

class OutBind(Header):
    def __init__(self, sequence_numb, system_id = '', password = '',
                       system_type = '', interface_version = 52,
                       addr_ton = 0, addr_npi = 0, address_range = ''):
                       
        Header.__init__(self, command_id = smpp_const.OUTBIND,
                               command_status = smpp_const.ESME_ROK,
                               sequence_number = sequence_numb)
                               
        self.system_id = part.SystemID(system_id)
        self.password = part.Password(password)
        
        self.body = [self.system_id, self.password]

class UnBind(Header):
    def __init__(self, sequence_numb):
        Header.__init__(self, command_id = smpp_const.UNBIND,
                               command_status = smpp_const.ESME_ROK,
                               sequence_number = sequence_numb)        

class UnBindResp(Header):
    def __init__(self, sequence_numb):
        Header.__init__(self, command_id = smpp_const.UNBIND_RESP,
                               command_status = smpp_const.ESME_ROK,
                               sequence_number = sequence_numb)
        
class GenericNack(Header):
    def __init__(self, command_stat, sequence_numb):
        Header.__init__(self, command_id = smpp_const.GENERIC_NACK,
                               command_status = command_stat,
                               sequence_number = sequence_numb)

class SubmitSM(Header):
    def __init__(self, sequence_numb,
                 dest_addr_ton,  dest_addr_npi,
                 destination_addr, esm_class,
                 protocol_id, priority_flag,
                 registered_delivery, replace_if_present_flag,
                 data_coding, sm_length, short_message,
                 
                 service_type = smpp_const.ESME_ROK,
                 source_addr_ton = 0, source_addr_npi = 0,
                 source_addr = '', schedule_delivery_time = '',
                 validity_period = '', sm_default_msg_id = 0,
                 
                 ):
        Header.__init__(self, command_id = smpp_const.SUBMIT_SM,
                               command_status = smpp_const.ESME_ROK,
                               sequence_number = sequence_numb)
        self.service_type  = part.ServiceType(service_type)


class EnquireLink(Header):
    def __init__(self, sequence_numb):
        Header.__init__(self, command_id = smpp_const.ENQUIRE_LINK,
                                command_status = smpp_const.ESME_ROK,
                                sequence_number = sequence_numb)


class EnquireLinkResp(Header):
    def __init__(self, sequence_numb):
        Header.__init__(self, command_id = smpp_const.ENQUIRE_LINK_RESP,
                                command_status = smpp_const.ESME_ROK,
                                sequence_number = sequence_numb)


class Client(asyncore.dispatcher):
    def __init__(self, host, port, bind):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect( (host, port) )
        self.bind = bind
        self.send_buf = ''
        self.recv_buf = ''

        
    def handle_connect(self):

        self.send(binascii.unhexlify(self.bind.format_message()))


    def handle_close(self):
        self.close()

    def handle_read(self):
        data = self.recv(4)
        length = struct.unpack('>L', data)[0]
        raw_pdu = self.recv(length - 4)
        a = data+raw_pdu
        print binascii.b2a_hex(a)



    def handle_write(self):
        count = 12
        self.send(binascii.unhexlify(EnquireLink(count).format_message()))
        



        
   
if __name__ == '__main__':

    bind = BindTransmitter(10, system_id = 'denis', password = 'buga', addr_npi = 1, addr_ton = 2)
    #print BindTransmitterResp(10).format_message()
    #print BindReceiver(10, system_id = 'denis', password = 'buga', addr_npi = 1, addr_ton = 2).format_message()
    #print BindReceiverResp(10, sc_interface_version = 52).format_message()
    #print BindTranceiver(10, system_id = 'denis', password = 'buga', addr_npi = 1, addr_ton = 2).format_message()
    #print BindTranceiverResp(10, command_stat = smpp_const.ESME_RBINDFAIL, sc_interface_version = 52).format_message()
    #print OutBind(10, password = 'buga').format_message()
    #print UnBind(10).format_message()
    #print UnBindResp(10).format_message()
    #print GenericNack(smpp_const.ESME_RALYBND, 10).format_message()
    
    client = Client('localhost', 8003, bind)
    

    asyncore.loop()
