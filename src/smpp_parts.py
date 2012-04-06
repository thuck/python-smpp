import smpp_const
import functools

        
def command_length(param_order):
    return hex(sum([len(i) for i in param_order])+16).replace('0x', '').zfill(8)

def generic_value_check(values, value):
    if value in values:
        return value

    else:
        raise ValueError

command_id = functools.partial(generic_value_check, part.command_id)
command_status = functools.partial(generic_value_check, part.command_status)

def sequence_number(value):
    return hex(value).replace('0x', '').zfill(8)
            
def set_string_parameter(max_size, min_size, name, self, value):
    value = value.encode('hex')

    if len(value) > max_size:
            raise ValueError('Cannot exceed %s characters' % (max_size))

    elif len(value) < min_size:
            raise ValueError('Cannot be less than %s characters' % (min_size))

    setattr(self, name, '%s00' % (value))

def get_string_parameter(name, self):
    return getattr(self, name).decode('hex')

def set_int_parameter(max_size, name, self, value):
    value = hex(value).replace('0x', '').zfill(2)
    if len(value) > max_size:
        raise ValueError('Cannot exceed 255 as value (00 - ff): %s' % (value))

    setattr(self, name, value)

def get_int_parameter(name, self):
    return int(getattr(self, name), 16)


def set_bit_parameter(max_size, name, self, value):
    value = value.zfill(2)
    if value not in ('00', '01', '10', '11'):
        raise ValueError('Bit mask wrong value: %s' % (value))

    setattr(self, name, value)

def get_bit_parameter(name, self):
    return getattr(self, name)


class IntParameter(Parameter):
    def __init__(self, value):
        Parameter.__init__(self, 'int', value, 2)
    
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

#To be used as properties to build the top objects
#I know looks bizarre... but will avoid a lot code to be done
#I know:
#Beautiful is better than ugly.
#Explicit is better than implicit.
#Simple is better than complex.
#Complex is better than complicated.
set_system_id = functools.partial(set_string_parameter, 32, 0, '_system_id')
set_password = functools.partial(set_string_parameter, 18, 0, '_password')
set_system_type = functools.partial(set_string_parameter, 26, 0, '_system_type')
set_interface_version = functools.partial(set_int_parameter, 2, '_interface_version')
set_addr_ton = functools.partial(set_int_parameter, 2, '_addr_ton')
set_addr_npi = functools.partial(set_int_parameter, 2, '_addr_npi')
set_address_range = functools.partial(set_string_parameter, 82, 0, '_address_range')
set_service_type = functools.partial(set_string_parameter, 12, 0, '_service_type')
set_source_addr_ton = functools.partial(set_int_parameter, 2, '_source_addr_ton')
set_source_addr_npi = functools.partial(set_int_parameter, 2, '_source_addr_npi')
set_source_addr = functools.partial(set_string_parameter, 42, 0, '_source_addr')
set_dest_addr_ton = functools.partial(set_int_parameter, 2, '_dest_addr_ton')
set_dest_addr_npi = functools.partial(set_int_parameter, 2, '_dest_addr_npi')
set_dest_addr = functools.partial(set_string_parameter, 42, 0, '_dest_add')
set_esm_class = functools.partial(set_int_parameter, 2, '_esm_class')
set_protocol_id = functools.partial(set_int_parameter, 2, '_protocol_id')
set_priority_flag = functools.partial(set_int_parameter, 2, '_priority_flag')
set_schedule_delivery_time = functools.partial(set_string_parameter, 34, 2, '_schedule_delivery_time')
set_validity_period = functools.partial(set_string_parameter, 34, 2, '_validity_period')
set_registered_delivery = functools.partial(set_int_parameter, 2, '_registered_delivery')
set_replace_if_present_flag = functools.partial(set_int_parameter, 2, '_replace_if_present_flag')
set_data_coding = functools.partial(set_int_parameter, 2, '_data_coding')
set_sm_default_msg_id = functools.partial(set_int_parameter, 2, '_sm_default_msg_id')
set_sm_length = functools.partial(set_int_parameter, 2, '_sm_length')
set_short_message = functools.partial(set_string_parameter, 508, 0, '_short_message')

get_system_id = functools.partial(get_string_parameter, '_system_id')
get_password = functools.partial(get_string_parameter, '_password')
get_system_type = functools.partial(get_string_parameter,'_system_type')
get_interface_version = functools.partial(get_int_parameter,'_interface_version')
get_addr_ton = functools.partial(get_int_parameter, '_addr_ton')
get_addr_npi = functools.partial(get_int_parameter, '_addr_npi')
get_address_range = functools.partial(get_string_parameter, '_address_range')
get_service_type = functools.partial(get_string_parameter, '_service_type')
get_source_addr_ton = functools.partial(get_int_parameter, '_source_addr_ton')
get_source_addr_npi = functools.partial(get_int_parameter, '_source_addr_npi')
get_source_addr = functools.partial(get_string_parameter, '_source_addr')
get_dest_addr_ton = functools.partial(get_int_parameter, '_dest_addr_ton')
get_dest_addr_npi = functools.partial(get_int_parameter, '_dest_addr_npi')
get_dest_addr = functools.partial(get_string_parameter, '_dest_add')
get_esm_class = functools.partial(get_int_parameter, '_esm_class')
get_protocol_id = functools.partial(get_int_parameter, '_protocol_id')
get_priority_flag = functools.partial(get_int_parameter, '_priority_flag')
get_schedule_delivery_time = functools.partial(get_string_parameter, '_schedule_delivery_time')
get_validity_period = functools.partial(get_string_parameter, '_validity_period')
get_registered_delivery = functools.partial(get_int_parameter, '_registered_delivery')
get_replace_if_present_flag = functools.partial(get_int_parameter, '_replace_if_present_flag')
get_data_coding = functools.partial(get_int_parameter, '_data_coding')
get_sm_default_msg_id = functools.partial(get_int_parameter, '_sm_default_msg_id')
get_sm_length = functools.partial(get_int_parameter, '_sm_length')
get_short_message = functools.partial(get_string_parameter, '_short_message')


        
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
        
