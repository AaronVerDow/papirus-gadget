#!/usr/bin/python

from __future__ import print_function

import os
import sys
import string
from papirus import PapirusTextPos

from time import sleep
import RPi.GPIO as GPIO

import re

def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(l, key = alphanum_key)

# Check EPD_SIZE is defined
EPD_SIZE=0.0
if os.path.exists('/etc/default/epd-fuse'):
    exec(open('/etc/default/epd-fuse').read())
if EPD_SIZE == 0.0:
    print("Please select your screen size by running 'papirus-config'.")
    sys.exit()

# Running as root only needed for older Raspbians without /dev/gpiomem
if not (os.path.exists('/dev/gpiomem') and os.access('/dev/gpiomem', os.R_OK | os.W_OK)):
    user = os.getuid()
    if user != 0:
        print('Please run script as root')
        sys.exit()

# Command line usage
# papirus-buttons

hatdir = '/proc/device-tree/hat'

WHITE = 1
BLACK = 0

SIZE = 27

# Assume Papirus Zero
SW1 = 21
SW2 = 16
SW3 = 20 
SW4 = 19
SW5 = 26

# Check for HAT, and if detected redefine SW1 .. SW5
if (os.path.exists(hatdir + '/product')) and (os.path.exists(hatdir + '/vendor')) :
   with open(hatdir + '/product') as f :
      prod = f.read()
   with open(hatdir + '/vendor') as f :
      vend = f.read()
   if (prod.find('PaPiRus ePaper HAT') == 0) and (vend.find('Pi Supply') == 0) :
       # Papirus HAT detected
       SW1 = 16
       SW2 = 26
       SW3 = 20
       SW4 = 21
       SW5 = -1

SELECT = SW1
DOWN = SW2
UP = SW3

iso_dir="/gadget_disks"


def safe_index(list, number):
    try: 
        return list[number]
    except IndexError:
        pass
    if number > 0:
        number = number - len(list)
    else:
        number = number + len(list)
    try: 
        return list[number]
    except IndexError:
        return ''


def main(argv):
    global SIZE

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(SW1, GPIO.IN)
    GPIO.setup(SW2, GPIO.IN)
    GPIO.setup(SW3, GPIO.IN)
    GPIO.setup(SW4, GPIO.IN)
    if SW5 != -1:
        GPIO.setup(SW5, GPIO.IN)

    papirus = PapirusTextPos(False, rotation = int(argv[0]) if len(sys.argv) > 1 else 0)

    cdrom=''
    i = 0
    files = []

    papirus.AddText('USB Gadget ISO Loader\n\nREDRAW CDROM UP DOWN SELECT', 0, 0, Id='browser',size=12)
    papirus.AddText('Status Unknown', 0, 55, Id='status', size=20)
    papirus.AddText('', 160, 55, Id='cdrom', size=12)
    papirus.AddText('Please select a disk.', 0, 80, Id='selected', size=12)
    papirus.WriteAll()
    while True:
        press = False

        if GPIO.input(SW5) == False:
            papirus.WriteAll()

        if GPIO.input(SW4) == False:
            if not cdrom:
                cdrom=' cdrom=y'
                papirus.UpdateText('cdrom', 'cdrom')
            else:
                cdrom=''
                papirus.UpdateText('cdrom', '')
            press = True

        if GPIO.input(UP) == False:
            press = True
            i = i - 1

        if GPIO.input(DOWN) == False:
            press = True
            i = i + 1

        if GPIO.input(SELECT) == False:
            os.system('rmmod g_mass_storage')
            status = os.system('modprobe g_mass_storage file="%s" stall=0 %s' % ('/'.join((iso_dir, file)), cdrom))
            papirus.UpdateText('selected', file)
            if cdrom:
                type = 'CDROM '
            else:
                type = 'DISK '
            cdrom=''
            papirus.UpdateText('cdrom', '')
            
            if (status == 0):
                papirus.UpdateText('status', type + 'OK')
            else:
                papirus.UpdateText('status', type + 'Fail!')
            papirus.WriteAll(True)

        if press is False:
            sleep(0.1)
            continue

        try:
            file=files[i]
        except IndexError:
            files=natural_sort(os.listdir(iso_dir))
            if( i > 0 ):
                i = 0
            else:
                i = -1 
            if not files:
                papirus.UpdateText('browser', 'No files found')
            file=files[i]

        papirus.UpdateText('browser', '%s\n%s\n%s\n%s' % (
            safe_index(files, i),
            safe_index(files, i+1),
            safe_index(files, i+2),
            safe_index(files, i+3)
        ))
        papirus.WriteAll(True)

        sleep(0.1)

if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.exit('interrupted')

