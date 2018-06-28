
#TODO = change name to main.py!
import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime
import sys
import os
from peewee import *

db = SqliteDatabase('Readings.db', check_same_thread=False)


class Pulse_data(Model):
    Date = DateField()
    Time = TimeField()
    Pulses = IntegerField()
    elapsed = TimeField()

    class Meta:
        database = db

#global pulse_count, time_now, time_start, pulse_flag

script_path = os.path.dirname(os.path.realpath(__file__))
file_name = 'water_flow_readings.txt'
full_file_name = '{}/{}'.format(script_path, file_name)
flow_pin = 14

print('Main running, GPIO:{}'.format(GPIO.VERSION))
print('Python:{}'.format(sys.version))
print('Script:{}, file:{}'.format(script_path, full_file_name))

def init_db():
    db.connect()

def init_vars():
    global pulse_count, time_now, time_start, pulse_flag, time_last_pulse
    pulse_count = 0
    time_now = 0
    time_start = 0
    time_last_pulse = 0
    pulse_flag = False
    file_write('---Started:{}---'.format(datetime.now()))

def init_GPIO():
    global flow_pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(flow_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def first_db_write():
    db.create_tables([Pulse_data])
    exam = Pulse_data(Date='25/06/2018', Time='23:43:00', Pulses=610, elapsed='00:02:12')
    exam1 = Pulse_data(Date='26/06/2018', Time='18:43:56', Pulses=6210, elapsed='00:20:10')
    exam2 = Pulse_data(Date='29/06/2018', Time='11:43:10', Pulses=1222, elapsed='00:00:53')
    exam.save()
    exam1.save()
    exam2.save()
    print('examples saved!')
    pass

def file_write(str_in):
    global full_file_name
    fb = open(full_file_name, 'a+')
    fb.write('{}\n'.format(str_in))
    fb.close()

def db_pulse_write(_date, _time, _count, _elapsed):
    db.create_tables([Pulse_data])
    pulse = Pulse_data(Date=_date, Time=_time, Pulses=_count, elapsed=_elapsed)
    pulse.save()
    pass

def db_read_all():
    pass
#    for pulse in Pulse_data.select():
#        print(pulse.Date, pulse.Time, pulse.Pulses, pulse.elapsed)

def flow_count(var):
    global pulse_count, time_start, pulse_flag, time_last_pulse
    time_last_pulse = datetime.now()
    if pulse_count == 0 : time_start = time_last_pulse
    pulse_flag = True
    pulse_count += 1

    #print('{:5d}'.format(pulse_count), end='')
    #if pulse_count%10 == 0:
    #    print('')

def sum_flow_event():
    global pulse_running, time_start, time_last_pulse, pulse_count
    pulse_running = False
    elapsed = time_last_pulse - time_start
    # print('Pulses:{}, Time:{}'.format(pulse_count, elapsed))
    _time_now = datetime.now()
    time_date = _time_now.date()
    time_time = _time_now.time().strftime('%H:%M:%S')

    tmp_pulse_count = pulse_count
    pulse_count = 0

    return time_date, time_time, tmp_pulse_count, elapsed


def main():
    global pulse_count, \
        time_now, \
        time_start, \
        pulse_flag, \
        time_last_pulse, \
        pulse_running

    db_read_all()
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
                p_date, p_time, p_count, p_elpd = sum_flow_event()

                if p_count > 2:
                    str_to_write = 'Time:{} {}, Pulses:{}, elapsed:{}'.format(
                        p_date, p_time, p_count, p_elpd)
                    print(str_to_write)

                    file_write(str_to_write)
                    db_pulse_write(p_date, p_time, p_count, p_elpd)

            sleep(1.0/1000.0)   #1mS
            pass

    except KeyboardInterrupt:
        print("Bye.")

    except Exception as err:
        print('Error!:{}'.format(err))

    finally:
        GPIO.cleanup()  # this ensures a clean exit
        db.close()

if __name__ == '__main__':
    init_vars()
    init_GPIO()
    init_db()
    main()
