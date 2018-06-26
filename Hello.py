from __future__ import print_function
import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime
import sys
global f_count, time_now, time_start, pulse_flag

file_name = 'water_flow_readings.txt'
flow_pin = 14

print('Hello!!, GPIO:{}'.format(GPIO.VERSION))
print('Python:{}'.format(sys.version))

def init_vars():
    global pulse_count, time_now, time_start, pulse_flag, time_last_pulse
    pulse_count = 0
    time_now = 0
    time_start = 0
    time_last_pulse = 0
    pulse_flag = False
    file_write('---Started:{}---'.format(datetime.now()))

def file_write(str_in):
    global file_name
    fb = open(file_name, 'a+')
    fb.write('{}\n'.format(str_in))
    fb.close()

GPIO.setmode(GPIO.BCM)
GPIO.setup(flow_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def flow_count(var):
    global pulse_count, time_start, pulse_flag, time_last_pulse
    time_last_pulse = datetime.now()
    if pulse_count == 0 : time_start = time_last_pulse
    pulse_flag = True
    pulse_count+=1

    #print('{:5d}'.format(pulse_count), end='')
    #if pulse_count%10 == 0:
    #    print('')

def sum_flow_event():
    global pulse_running, time_start, time_last_pulse, pulse_count
    str_out = ''
    pulse_running = False
    elapsed = time_last_pulse - time_start
    # print('Pulses:{}, Time:{}'.format(pulse_count, elapsed))

    if pulse_count > 2:
        str_out = 'Time:{}, Pulses:{}, elapsed:{}'.format(datetime.now(), pulse_count, elapsed)

    pulse_count = 0

    return str_out


def main():
    global pulse_count, \
        time_now, \
        time_start, \
        pulse_flag, \
        time_last_pulse, \
        pulse_running

    # i = 0
    pulse_running = False
    try:
        GPIO.add_event_detect(14, GPIO.BOTH, callback=flow_count)
        pulse_count=0
        no_pulse_count = 0
        while True:
            time_now = datetime.now()
            if pulse_flag == True:
                no_pulse_count = 0
                pulse_flag = False
                pulse_running = True
            else:
                no_pulse_count += 1

            #print('no_p_c:{}'.format(no_pulse_count))
            if no_pulse_count == 2000 and pulse_running==True:
                str_to_write = sum_flow_event()
                if not str_to_write == '':
                    print(str_to_write)
                    file_write(str_to_write)
            pass

    except KeyboardInterrupt:
        print("Bye.")

    except Exception as err:
        print('Error!:{}'.format(err))

    finally:
        GPIO.cleanup()  # this ensures a clean exit

if __name__ == '__main__':
    init_vars()
    main()
