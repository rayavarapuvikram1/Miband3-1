import sys
from auth import MiBand3
from cursesmenu import *
from cursesmenu.items import *
from constants import ALERT_TYPES
import time
import os
def call_immediate():
    print ('Sending Call Alert')
    time.sleep(1)
    band.send_alert(ALERT_TYPES.PHONE)
def msg_immediate():
    print ('Sending Message Alert')
    time.sleep(1)
    band.send_alert(ALERT_TYPES.MESSAGE)
def detail_info():
    print ('MiBand')
    print ('Soft revision:',band.get_revision())
    print ('Hardware revision:',band.get_hrdw_revision())
    print ('Battery:', band.get_battery_info())
    print ('Steps:', band.get_steps())
    input('Press Enter to continue')
def custom_message():
    band.send_custom_alert(5)
def custom_call():
    # custom_call
    band.send_custom_alert(3)
def custom_missed_call():
    band.send_custom_alert(4)
'''
when setting the alarm write __value__ to 00000003-0000-3512-2118-0009af100700

You can get the value from the following

The value has 5 parts :
    1 | 02 for alarm
    
    2 | 00/c0/80 --> 
        c0 represent to turn on 1st alarm without snooze and 80 represent with snooze
        c1 represent 02nd alarm
        c2 represent 03rd alarm
        c3 represent 04th alarm
        c4 represent 05th alarm
        c5 represent 06th alarm
        c6 represent 07th alarm
        c7 represent 08th alarm
        c8 represent 09th alarm
        c8 represent 10th alarm

    3 | 06 # 
        Hour of alarm time

    4 | 1e # 
        minutes of alarm time
        
    5 | 0x01 - 0b00000001 - Monday
        0x02 - 0b00000010 - Tuesday
        0x04 - 0b00000100 - Wednesday
        0x08 - 0b00001000 - Thursday
        0x10 - 0b00010000 - Friday
        0x20 - 0b00100000 - Saturday
        0x40 - 0b01000000 - Sunday
        
        If you want multiple days add the hexes of those days.
'''
def change_date():
    band.change_date()

def f(g):
    print 'Raw accel :', g

def acceleration_values():
    band.start_raw_data_realtime(accel_raw_callback=f, duration=80)


def slider_mi_band_3():
    setup_data = b'\x03\x01'
    band.change_slide()

    while True:
        band.button_chars.write(setup_data)
        if band.waitForNotifications(0.4):
            # print(button_chars.supportsRead())
            # print(button_chars.propertiesToString())
            # print(band.waitForNotifications(0.4))
            # print(button_chars.read())
            pass        


    time.sleep(5)
    print("END")

def but_click():
    print(band.subscribeNotifications())
    while True:
        if band.waitForNotifications(1):
            print("Notification")
# sudo gatttool -b FE:1D:5C:3B:50:61 -I -t random
# handle: 0x004c, char properties: 0x10, char value handle: 0x004d, uuid: 00000010-0000-3512-2118-0009af100700

MAC_ADDR = "FB:FB:11:96:CD:EE"
print ('Attempting to connect to ', MAC_ADDR)

band = MiBand3(MAC_ADDR, debug=True)
band.setSecurityLevel(level = "medium")
band.authenticate()

menu = CursesMenu("MiBand MAC: " + MAC_ADDR, "Select an option")
detail_menu = FunctionItem("View Band Detail info", detail_info)
msg_alert = FunctionItem("Send a Message Notification", custom_message)
call_alert = FunctionItem("Send a Call Notification", custom_call)
miss_call_alert = FunctionItem("Send a Missed Call Notification", custom_missed_call)
change_date_time = FunctionItem("acceleration", acceleration_values)
click_menu = FunctionItem("Remote",but_click)
band3_remote = FunctionItem("band3", slider_mi_band_3)

menu.append_item(band3_remote)
menu.append_item(change_date_time)
menu.append_item(click_menu)
menu.append_item(detail_menu)
menu.append_item(msg_alert)
menu.append_item(call_alert)
menu.append_item(miss_call_alert)
menu.show()