import smpp_const

class CommandLength(object):
        
    def __call__(self, param_order):
        return hex(sum([len(i) for i in param_order])+16).replace('0x', '').zfill(8)

class CommandID(object):
    #Must check if is a valid command_id
    def __init__(self, value):
        self._value = value
        
    def __call__(self, value = None):
        if value == None:
            return self._value
        else:
            self._value = value
            
class CommandStatus(object):
    #Must check if is a valid command_status
    def __init__(self, value):
        self._value = value
        
    def __call__(self, value = None):
        if value == None:
            return self._value
        else:
            self._value = value
            
class SequenceNumber(object):
    def __init__(self, value):
        self._value = hex(value).replace('0x', '').zfill(8)
        
    def __call__(self, value = None):
        if value == None:
            return self._value
        else:
            self._value = hex(value).replace('0x', '').zfill(8)

class Parameter(object):
    def __init__(self, type_, value, max_size, min_size = 0):
        self.type = type_
        self.max_size = max_size
        self.min_size = min_size
        self.set_value = {'string':self._string_parser,
                          'int':self._int_parser,
                          'bit':self._bit_parser}.get(type_)
        self.set_value(value)
    
    def _string_parser(self, value):
        self._value = value.encode('hex')

        if len(self._value) > self.max_size:
            raise ValueError(self.__class__.__name__+' cannot exceed '+str(self.max_size)+' characters')
        elif len(self._value) < self.min_size:
            raise ValueError(self.__class__.__name__+' cannot be less than '+str(self.max_size)+' characters')
        self._value = '%s00' % (self._value)        
        
    def _int_parser(self, value):
        self._value = hex(value).replace('0x', '').zfill(2)
        if len(self._value) > self.max_size:
            raise ValueError(self.__class__.__name__+' cannot exceed 255 as value (00 - ff)')
        
    def _bit_parser(self, value):
        self._value = value.zfill(2)
        if self._value not in ('00', '01', '10', '11'):
            raise ValueError(self.__class__.__name__+' Bit mask wrong value')
    
    def __len__(self):
        return len(self._value)/2
        
    def __call__(self, value = None):
        if value == None:
            return self._value
        else:
            self.set_value(value)

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

            
class SystemID(Parameter):
    def __init__(self, value):
        Parameter.__init__(self, 'string', value, 32)
    
class Password(Parameter):
    def __init__(self, value):
        Parameter.__init__(self, 'string', value, 18)
    
class SystemType(Parameter):
    def __init__(self, value):
        Parameter.__init__(self, 'string', value, 26)
        
class InterfaceVersion(IntParameter):
    pass

class AddrTon(IntParameter):
    pass

class AddrNpi(IntParameter):
    pass       
        
class AddressRange(Parameter):
    def __init__(self, value):
        Parameter.__init__(self, 'string', value, 82)

class ServiceType(Parameter):
    def __init__(self, value):
        Parameter.__init__(self, 'string', value, 12)
        
class SourceAddrTon(IntParameter):
    pass
        
class SourceAddrNpi(IntParameter):
    pass
        
class SourceAddr(Parameter):
    def __init__(self, value):
        Parameter.__init__(self, 'string', value, 42)

class DestAddrTon(IntParameter):
    pass
        
class DestAddrNpi(IntParameter):
    pass

class DestinationAddr(Parameter):
    def __init__(self, value):
        Parameter.__init__(self, 'string', value, 42)

class EsmClass(IntParameter):
    pass
        
class ProtocolID(IntParameter):
    pass
        
class PriorityFlag(IntParameter):
    pass

class ScheduleDeliveryTime(Parameter):
    def __init__(self, value):
        Parameter.__init__(self, 'string', value, 34, min_size = 2)

class ValidityPeriod(Parameter):
    def __init__(self, value):
        Parameter.__init__(self, 'string', value, 34, min_size = 2)

class RegisteredDelivery(IntParameter):
    pass
        
class ReplaceIfPresentFlag(IntParameter):
    pass

class DataCoding(IntParameter):
    pass

class SmDefaultMsgID(IntParameter):
    pass
        
class SmLength(IntParameter):
    pass

class ShortMessage(Parameter):
    def __init__(self, value):
        Parameter.__init__(self, 'string', value, 508)
        
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
        
