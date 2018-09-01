#!/usr/bin/env python

import flicklib
import time
import RPi.GPIO as GPIO
import curses
import pyautogui
from curses import wrapper

some_value = 5000


@flicklib.move()
def move(x, y, z):
    global xyztxt
    xyztxt = '{:5.3f} {:5.3f} {:5.3f}'.format(x,y,z)


@flicklib.flick()
def flick(start, finish):
    global flicktxt
    flicktxt = start + finish


@flicklib.airwheel()
def spinny(delta):
    global some_value
    global airwheeltxt
    some_value += delta
    if some_value < 0:
        some_value = 0
    if some_value > 10000:
        some_value = 10000
    airwheeltxt = str(some_value/100)


@flicklib.double_tap()
def doubletap(position):
    global doubletaptxt
    doubletaptxt = position


@flicklib.tap()
def tap(position):
    global taptxt
    taptxt = position


@flicklib.touch()
def touch(position):
    global touchtxt
    touchtxt = position

#
# Main display using curses
#


def main(stdscr):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(22, GPIO.OUT)
    GPIO.output(22, False)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.OUT)
    GPIO.output(4, True)

    global xyztxt
    global flicktxt
    global airwheeltxt
    global touchtxt
    global taptxt
    global doubletaptxt

    xyztxt = ''
    flicktxt = ''
    flickcount = 0
    airwheeltxt = ''
    airwheelcount = 0
    touchtxt = ''
    touchcount = 0
    taptxt = ''
    tapcount = 0
    doubletaptxt = ''
    doubletapcount = 0

    # Clear screen and hide cursor
    stdscr.clear()

    # Add title and footer

    title = '**** MozoSoft Flick check ****'
    stdscr.addstr( title)
    stdscr.refresh()

    datawin = curses.newwin(8, curses.COLS - 6,  2, 3)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(22, GPIO.OUT)
    GPIO.output(22, True)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.OUT)
    GPIO.output(4, False)

    # Update data window continuously until Control-C
    while True:
        datawin.erase()
        datawin.border()
        datawin.addstr(1, 2, 'X Y Z     : ' + xyztxt)

        datawin.addstr(2, 2, 'Flick     : ' + flicktxt)
        datawin.addstr(3, 2, 'Airwheel  : ' + airwheeltxt)
        datawin.addstr(4, 2, 'Touch     : ' + touchtxt)
        datawin.addstr(5, 2, 'Tap       : ' + taptxt)
        datawin.addstr(6, 2, 'Doubletap : ' + doubletaptxt)
        datawin.refresh()

        xyztxt = ''

        if len(flicktxt) > 0 and flickcount == 0:
            if 'westeast' == flicktxt:
                pyautogui.typewrite('a')
                time.sleep(1.1)
                flicktxt = ''
                flickcount = 5
            elif 'eastwest' == flicktxt:
                pyautogui.typewrite('d')
                time.sleep(1.1)
                flicktxt = ''
                flickcount = 5
            elif 'northsouth' == flicktxt:
                pyautogui.typewrite('s')
                time.sleep(1.1)
                flicktxt = ''
                flickcount = 5
            elif 'southnorth' == flicktxt:
                pyautogui.typewrite('w')
                time.sleep(1.1)
                flicktxt = ''
                flickcount = 5
            else:
                continue

        if len(flicktxt) > 0 and flickcount < 5:
            flickcount += 1
        else:
            flicktxt = ''
            flickcount = 0

        if len(airwheeltxt) > 0 and airwheelcount < 5:
            airwheelcount += 1
        else:
            airwheeltxt = ''
            airwheelcount = 0

        if len(touchtxt) > 0 and touchcount < 5:
            touchcount += 1
        else:
            touchtxt = ''
            touchcount = 0

        if len(taptxt) > 0 and tapcount < 5:
            tapcount += 1
        else:
            taptxt = ''
            tapcount = 0

        if len(doubletaptxt) > 0 and doubletapcount < 5:
            doubletapcount += 1
        else:
            doubletaptxt = ''
            doubletapcount = 0

        time.sleep(0.1)


wrapper(main)
