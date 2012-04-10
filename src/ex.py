import smpp_const
import smpp_parts as part
import asyncore
import socket
import binascii
import time
import datetime
from smpp_commands import SubmitSM

submit_sm = SubmitSM(command_length='60', command_id=4, command_status=0,
            sequence_number=5, service_type='', source_addr_ton=2,
            source_addr_npi=8, source_addr='555', dest_addr_ton='1',
            dest_addr_npi=1, dest_addr='555555555', esm_class=0,
            protocol_id=0, priority_flag=0, schedule_delivery_time='',
            validity_period='', registered_delivery=0, replace_if_present_flag=0,
            data_coding=0, sm_default_msg_id=0, sm_length=14,
            short_message='Hello wikipediasdsda')

print 'Showing all the parameters: (name, external value, internal value)'
for i in submit_sm.__slots__:
    print i, '('+str(getattr(submit_sm, i[1:]))+')', '('+str(getattr(submit_sm, i))+')'

print '\nShort message update will cause an update in the sm_length automagically'
print "submit_sm.short_message = 'aaaaa'"
submit_sm.short_message = 'aaaaa'

for i in submit_sm.__slots__:
    print i, '('+str(getattr(submit_sm, i[1:]))+')', '('+str(getattr(submit_sm, i))+')'

print '\nForce hex data, and force short_message and command_length update'
print "submit_sm._short_message = 'aaaaaaaa'; submit_sm.sm_length = 0; submit_sm.command_length = 0"

submit_sm._short_message = 'aaaaaaaa'
submit_sm.sm_length = 0
submit_sm.command_length = 0

for i in submit_sm.__slots__:
    print i, '('+str(getattr(submit_sm, i[1:]))+')', '('+str(getattr(submit_sm, i))+')'
