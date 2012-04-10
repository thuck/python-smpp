import smpp_const
import smpp_parts as part
import asyncore
import socket
import binascii
import time

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

class BindTransmitter(object):
    __parameters = ['_command_length', '_command_id', '_command_status',
                    '_sequence_number', '_system_id', '_password',
                    '_system_type', '_interface_version', '_addr_ton',
                    '_addr_npi', '_address_range']

    __optional_parameters = []

    __slots__ = __parameters + __optional_parameters

    def __init__(self, **kargs):
        self.command_id = smpp_const.BIND_TRANSMITTER
        self.command_status = smpp_const.ESME_ROK
        self.sequence_number = kargs.get('sequence_number')
        self.system_id =  kargs.get('system_id')
        self.password = kargs.get('password')
        self.system_type = kargs.get('system_type')
        self.interface_version = kargs.get('interface_version')
        self.addr_ton = kargs.get('addr_ton')
        self.addr_npi = kargs.get('addr_npi')
        self.address_range = kargs.get('address_range')
        self.command_length = kargs.get('command_length', self.__slots__)

    command_length = property(part.get_command_length, part.set_command_length)
    command_id = property(part.get_command_id, part.set_command_id)
    command_status = property(part.get_command_status, part.set_command_status)
    sequence_number = property(part.get_sequence_number, part.set_sequence_number)
    system_id = property(part.get_system_id, part.set_system_id)
    password = property(part.get_password, part.set_password)
    system_type = property(part.get_system_type, part.set_system_type)
    interface_version = property(part.get_interface_version, part.set_interface_version)
    addr_ton = property(part.get_addr_ton, part.set_addr_ton)
    addr_npi = property(part.get_addr_npi, part.set_addr_npi)
    address_range = property(part.get_address_range, part.set_address_range)

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

class SubmitSM(object):
    _parameters = ['_command_length', '_command_id', '_command_status',
                    '_sequence_number', '_service_type', '_source_addr_ton',
                    '_source_addr_npi', '_source_addr', '_dest_addr_ton',
                    '_dest_addr_npi', '_dest_addr', '_esm_class',
                    '_protocol_id', '_priority_flag', '_schedule_delivery_time',
                    '_validity_period', '_registered_delivery',
                    '_replace_if_present_flag', '_data_coding',
                    '_sm_default_msg_id', '_sm_length', '_short_message']

    _optional_parameters = []

    __slots__ = _parameters + _optional_parameters

    def __init__(self, **kargs):
        for i in self._parameters[4:]:
            setattr(self, i[1:], kargs.get(i[1:]))
        self.command_id = smpp_const.SUBMIT_SM
        self.command_status = smpp_const.ESME_ROK
        self.sequence_number = kargs.get('sequence_number')
        self.command_length = 0

    command_length = property(part.get_command_length, part.set_command_length)
    command_id = property(part.get_command_id, part.set_command_id)
    command_status = property(part.get_command_status, part.set_command_status)
    sequence_number = property(part.get_sequence_number, part.set_sequence_number)
    service_type = property(part.get_service_type, part.set_service_type)
    source_addr_ton = property(part.get_source_addr_ton, part.set_source_addr_ton)
    source_addr_npi = property(part.get_source_addr_npi, part.set_source_addr_npi)
    source_addr = property(part.get_source_addr, part.set_source_addr)
    dest_addr_ton = property(part.get_dest_addr_ton, part.set_dest_addr_ton)
    dest_addr_npi = property(part.get_dest_addr_npi, part.set_dest_addr_npi)
    dest_addr = property(part.get_dest_addr, part.set_dest_addr)
    esm_class = property(part.get_esm_class, part.set_esm_class)
    protocol_id = property(part.get_protocol_id, part.set_protocol_id)
    priority_flag = property(part.get_priority_flag, part.set_priority_flag)
    schedule_delivery_time = property(part.get_schedule_delivery_time, part.set_schedule_delivery_time)
    validity_period = property(part.get_validity_period, part.set_validity_period)
    registered_delivery = property(part.get_registered_delivery, part.set_registered_delivery)
    replace_if_present_flag = property(part.get_replace_if_present_flag, part.set_replace_if_present_flag)
    data_coding = property(part.get_data_coding, part.set_data_coding)
    sm_default_msg_id = property(part.get_sm_default_msg_id, part.set_sm_default_msg_id)
    sm_length = property(part.get_sm_length, part.set_sm_length)
    short_message = property(part.get_short_message, part.set_short_message)


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

