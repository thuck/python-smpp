import smpp_const as const
import functools

def smpp_values_validation(name, value):
    try:
        if value in getattr(const, name[1:]):
            return True

        else:
            return False

    except AttributeError:
        #if there is no validator, any value is possible
        return True

def set_string_parameter(max_size, min_size, default_value, type_, name, self, value):
    if value is None:
        value = default_value

    value = value.encode('hex')

    if len(value) > max_size - 2:
        raise ValueError('Cannot exceed %s characters' % (max_size/2))

    elif len(value) < min_size - 2:
        raise ValueError('Cannot be less than %s characters' % (min_size/2))

    elif not smpp_values_validation(name, value):
        raise ValueError('%s is not a valid value for %s' % (value, name))

    if type_ == 'c-octet_string':
        setattr(self, name, '%s00' % (value))

    elif type_ == 'octet_string':
        setattr(self, name, value)

def get_string_parameter(type_, name, self):
    value = ''

    if type_ == 'c-octet_string':
        value = getattr(self, name)[:-2].decode('hex')

    elif type_ == 'octet_string':
        value = getattr(self, name).decode('hex')

    return value

def set_int_parameter(max_size, default_value, name, self, value):

    if value is None:
        value = default_value

    if type(value) is str:
        value = value.zfill(max_size)

    else:
        value = hex(value).replace('0x', '').zfill(max_size)

    if len(value) > max_size:
        raise ValueError('Cannot exceed %s: %s' % (max_size, value))

    elif not smpp_values_validation(name, value):
        raise ValueError('%s is not a valid value for %s' % (value, name))

    setattr(self, name, value)


def get_int_parameter(name, self):
    return int(getattr(self, name),16)

def set_bit_parameter(max_size, name, self, value):
    value = value.zfill(2)
    if value not in ('00', '01', '10', '11'):
        raise ValueError('Bit mask wrong value: %s' % (value))

    setattr(self, name, value)

def get_bit_parameter(name, self):
    return getattr(self, name)

def set_command_length(self, value):
    length = 0
    for i in self._parameters[1:]:
        length += len(getattr(self, i))

    for i in self._optional_parameters:
        length += len(getattr(self, i))

    self._command_length = hex((length+8)/2).replace('0x','').zfill(8)

def get_command_length(self):
    return int(self._command_length, 16)

def set_sm_length(self, value):
    self._sm_length = hex(len(self._short_message)/2).replace('0x','').zfill(2)

def get_sm_length(self):
    return int(hex(len(self._short_message)/2).replace('0x','').zfill(2), 16)

#To be used as properties to build the top objects
#I know looks bizarre... but will avoid a lot code to be done
#I know:
#Beautiful is better than ugly.
#Explicit is better than implicit.
#Simple is better than complex.
#Complex is better than complicated.

#SMPP Header
#set_command_length = functools.partial(set_int_parameter, 8, 0, '_command_length')
set_command_id = functools.partial(set_int_parameter, 8, 0, '_command_id')
set_command_status = functools.partial(set_int_parameter, 8, 0, '_command_status')
set_sequence_number = functools.partial(set_int_parameter, 8, 0, '_sequence_number')

#SMPP mandatory parameters
set_system_id = functools.partial(set_string_parameter, 32, 0, '', 'c-octet_string', '_system_id')
set_password = functools.partial(set_string_parameter, 18, 0, '', 'c-octet_string','_password')
set_system_type = functools.partial(set_string_parameter, 26, 0, '', 'c-octet_string', '_system_type')
set_interface_version = functools.partial(set_int_parameter, 2, 52, '_interface_version')
set_addr_ton = functools.partial(set_int_parameter, 2, 0, '_addr_ton')
set_addr_npi = functools.partial(set_int_parameter, 2, 0, '_addr_npi')
set_address_range = functools.partial(set_string_parameter, 82, 0, '', 'c-octet_string', '_address_range')
set_service_type = functools.partial(set_string_parameter, 12, 0, '', 'c-octet_string', '_service_type')
set_source_addr_ton = functools.partial(set_int_parameter, 2, 0, '_source_addr_ton')
set_source_addr_npi = functools.partial(set_int_parameter, 2, 0, '_source_addr_npi')
set_source_addr = functools.partial(set_string_parameter, 42, 0, '', 'c-octet_string', '_source_addr')
set_dest_addr_ton = functools.partial(set_int_parameter, 2, 0, '_dest_addr_ton')
set_dest_addr_npi = functools.partial(set_int_parameter, 2, 0, '_dest_addr_npi')
set_dest_addr = functools.partial(set_string_parameter, 42, 0, '', 'c-octet_string', '_dest_addr')
set_esm_class = functools.partial(set_int_parameter, 2, 0, '_esm_class')
set_protocol_id = functools.partial(set_int_parameter, 2, 0, '_protocol_id')
set_priority_flag = functools.partial(set_int_parameter, 2, 0, '_priority_flag')
set_schedule_delivery_time = functools.partial(set_string_parameter, 34, 2, '', 'c-octet_string', '_schedule_delivery_time')
set_validity_period = functools.partial(set_string_parameter, 34, 2, '', 'c-octet_string', '_validity_period')
set_registered_delivery = functools.partial(set_int_parameter, 2, 0, '_registered_delivery')
set_replace_if_present_flag = functools.partial(set_int_parameter, 2, 0, '_replace_if_present_flag')
set_data_coding = functools.partial(set_int_parameter, 2, 0, '_data_coding')
set_sm_default_msg_id = functools.partial(set_int_parameter, 2, 0, '_sm_default_msg_id')
#set_sm_length = functools.partial(set_int_parameter, 2, 0, '_sm_length')
set_short_message = functools.partial(set_string_parameter, 508, 0, '', 'octet_string', '_short_message')

#SMPP Header
#get_command_length = functools.partial(get_int_parameter, '_command_length')
get_command_id = functools.partial(get_int_parameter, '_command_id')
get_command_status = functools.partial(get_int_parameter, '_command_status')
get_sequence_number = functools.partial(get_int_parameter, '_sequence_number')

#SMPP mandatory parameters
get_system_id = functools.partial(get_string_parameter, 'c-octet_string', '_system_id')
get_password = functools.partial(get_string_parameter, 'c-octet_string', '_password')
get_system_type = functools.partial(get_string_parameter,'c-octet_string', '_system_type')
get_interface_version = functools.partial(get_int_parameter,'_interface_version')
get_addr_ton = functools.partial(get_int_parameter, '_addr_ton')
get_addr_npi = functools.partial(get_int_parameter, '_addr_npi')
get_address_range = functools.partial(get_string_parameter, 'c-octet_string', '_address_range')
get_service_type = functools.partial(get_string_parameter, 'c-octet_string', '_service_type')
get_source_addr_ton = functools.partial(get_int_parameter, '_source_addr_ton')
get_source_addr_npi = functools.partial(get_int_parameter, '_source_addr_npi')
get_source_addr = functools.partial(get_string_parameter, 'c-octet_string', '_source_addr')
get_dest_addr_ton = functools.partial(get_int_parameter, '_dest_addr_ton')
get_dest_addr_npi = functools.partial(get_int_parameter, '_dest_addr_npi')
get_dest_addr = functools.partial(get_string_parameter, 'c-octet_string', '_dest_addr')
get_esm_class = functools.partial(get_int_parameter, '_esm_class')
get_protocol_id = functools.partial(get_int_parameter, '_protocol_id')
get_priority_flag = functools.partial(get_int_parameter, '_priority_flag')
get_schedule_delivery_time = functools.partial(get_string_parameter, 'c-octet_string', '_schedule_delivery_time')
get_validity_period = functools.partial(get_string_parameter, 'c-octet_string', '_validity_period')
get_registered_delivery = functools.partial(get_int_parameter, '_registered_delivery')
get_replace_if_present_flag = functools.partial(get_int_parameter, '_replace_if_present_flag')
get_data_coding = functools.partial(get_int_parameter, '_data_coding')
get_sm_default_msg_id = functools.partial(get_int_parameter, '_sm_default_msg_id')
#get_sm_length = functools.partial(get_int_parameter, '_sm_length')
get_short_message = functools.partial(get_string_parameter, 'octet_string', '_short_message')



class TLV(object):
    def __init__(self, parameter_tag, type_, value, max_size, min_size = 0):

        self.parameter_tag = parameter_tag
        if value:
            self.value = Parameter(type_, value, max_size, min_size)
            self.length = len(self.value)
        else:
            self.value = None
            self.length = 0

    def __len__(self):
        if self.value:
            return 4 + self.length
        else:
            return 0

    def __call__(self, value = None):
        if value == None:
            return '%s%s%s' % (self.parameter_tag, hex(len(self.value)).replace('0x', '').zfill(4), self.value())
        else:
            self.value(value)
            self.length = len(self.value)
        
class DestAddrSubunit(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.DEST_ADDR_SUBUNIT, 'int', value, 2)

class SourceAddrSubunit(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.SOURCE_ADDR_SUBUNIT, 'int', value, 2)

class DestNetworkType(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.DEST_NETWORK_TYPE, 'int', value, 2)
        
class SourceNetworkType(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.SOURCE_NETWORK_TYPE, 'int', value, 2)
        
        
class DestBearerType(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.DEST_BEARER_TYPE, 'int', value, 2)
        
class SourceBearerType(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.DEST_BEARER_TYPE, 'int', value, 2)


class DestTelematicsID(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.DEST_TELEMATICS_ID, 'int', value, 4)
        
        
class SourceTelematicsID(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.SOURCE_TELEMATICS_ID, 'int', value, 2)
        

class QosTimeToLive(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.QOS_TIME_TO_LIVE, 'int', value, 8)


class PayloadType(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.PAYLOAD_TYPE, 'int', value, 2)

class AdditionalStatusInfoText(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.ADDITIONAL_STATUS_INFO_TEXT, 'string', value, 512, min_size = 2)

class ReceiptMessageID(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.RECEIPTED_MESSAGE_ID, 'string', value, 130, min_size = 2)

class MsMsgWaitFacilities(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.MS_MSG_WAIT_FACILITIES, 'bit', value, 2)


class PrivacyIndicator(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.PRIVACY_INDICATOR, 'int', value, 2)

class SourceSubaddress(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.SOURCE_SUBADDRESS, 'string', value, 56, min_size = 4)
        
class DestSubaddress(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.DEST_SUBADDRESS, 'string', value, 56, min_size = 4)
        
class UserMessageReference(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.USER_MESSAGE_REFERENCE, 'int', value, 4)

class UserResponseCode(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.USER_RESPONSE_CODE, 'int', value, 2)

class LanguageIndicator(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.LANGUAGE_INDICATOR, 'int', value, 2)
        
class SourcePort(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.SOURCE_PORT, 'int', value, 4)

class DestinationPort(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.DESTINATION_PORT, 'int', value, 4)

class SarMsgRefNum(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.SAR_MSG_REF_NUM, 'int', value, 4)

class SarTotalSegments(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.SAR_TOTAL_SEGMENTS, 'int', value, 2)
        
        
class SarSegmentSeqnum(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.SAR_SEGMENT_SEQNUM, 'int', value, 2)

        
class SCInterfaceVersion(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.SC_INTERFACE_VERSION, 'int', value, 2)
        
class DisplayTime(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.DISPLAY_TIME, 'int', value, 2)
        
        
class MsTime(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.MS_VALIDITY, 'int', value, 2)
        
class DpfResult(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.DPF_RESULT, 'int', value, 2)
        
class SetDpf(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.SET_DPF, 'int', value, 2)
        
class MsAvailabilityStatus(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.MS_AVAILABILITY_STATUS, 'int', value, 2)
        
class NetworkErrorCode(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.NETWORK_ERROR_CODE, 'string', value, 6)
        
class MessagePayload(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.MESSAGE_PAYLOAD, 'string', value, 1024)
        
class DeliveryFailureReason(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.DELIVERY_FAILURE_REASON, 'int', value, 2)
        
class MoreMessagesToSend(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.MORE_MESSAGES_TO_SEND, 'int', value, 2)
        
class MessageState(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.MESSAGE_STATE, 'int', value, 2)
        
class CallbackNum(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.CALLBACK_NUM, 'string', value, 38, min_size = 8)
        
class CallbackNumPresInd(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.CALLBACK_NUM_PRES_IND, 'bit', value, 2)
        
class CallbackNumAtag(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.CALLBACK_NUM_ATAG, 'string', value, 130)  
             
class NumberOfMessages(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.NUMBER_OF_MESSAGES, 'int', value, 2)
        
class SmsSignal(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.SMS_SIGNAL, 'int', value, 4)
        
class AlertOnMessageDelivery(TLV):
    def __init__(self):
        TLV.__init__(self, smpp_const.ALERT_ON_MESSAGE_DELIVERY, 'string', '', 0)
        
class ItsReplayType(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.ITS_REPLY_TYPE, 'int', value, 2)
        
class ItsSessionInfo(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.ITS_SESSION_INFO, 'string', value, 4)
        
class UssdServiceOp(TLV):
    def __init__(self, value):
        TLV.__init__(self, smpp_const.USSD_SERVICE_OP, 'string', value, 2)
        
