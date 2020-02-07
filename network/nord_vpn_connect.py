#!/usr/bin/env python3

import io
import random
import sched
import time
from subprocess import Popen, PIPE

import psutil

from utils.arg_class import ArgClass
from utils.parser import Parser


class NordVpnConnect(ArgClass):
    pid = -1
    country_code = None
    s = sched.scheduler(time.time, time.sleep)

    def __init__(self, countrycode=None):
        self.country_code = countrycode

    def __args(self):
        return Parser(args=[
            {"command": "--country_code", "type": str, "help": "set initial country code to connect"},
            {"command": "--change_time", "type": int, "help": "set time to change connection server"}
        ]).get_args()

    def get_args(self):
        args = self.__args()
        countrycode = args.country_code
        change_time = args.change_time
        return countrycode, change_time

    def connect_to_open_pyn(self):
        print("-------------- connecting to open pyn --------------")
        openpyn_init = Popen(['sudo', 'openpyn', '--init'], shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        openpyn_init.communicate()
        time.sleep(2)

    def get_country_code(self, file_name=None):
        if file_name is None:
            file_name = f"{self.get_current_dir_path()}/country.txt"
        l = list()
        with io.open(file_name, 'r', encoding='utf-8') as f:
            for line in f:
                if line != '\n':
                    l.append(line.replace("\n", ""))
        return l

    def get_random_country_code(self):
        random_list = self.get_country_code()
        random_code = random.choice(random_list)
        return random_code

    def connect_to_nord_vpn(self, command='openpyn', country='pl'):
        print("-------------- connecting to nord vpn --------------")
        openpyn_output = Popen([command, country])
        pid = openpyn_output.pid
        openpyn_output.communicate()

    def run(self):
        self.kill_nord_vpn()
        if self.country_code is None:
            random_value = self.get_random_country_code()
        else:
            random_value = self.country_code
        print(random_value)
        self.connect_to_nord_vpn(country=random_value)

    def main(self, countrycode=None):
        if self.country_code is None:
            self.country_code = countrycode
        self.run()

    def kill_nord_vpn(self):
        if self.pid != -1:
            print(f"killing process on pid {self.pid}")
            p = psutil.Process(self.pid)
            p.kill()
        else:
            print(f"there are no running process on pid {self.pid}")


nord_vpn = NordVpnConnect()

country_code, change_time = nord_vpn.get_args()


def run_hourly(sc):
    nord_vpn.main(country_code)
    print("running nordvpn hourly")
    s.enter(60, 1, run_hourly, (sc,))


print(f"-------------- country code => {country_code} --------------")
print(f"-------------- change time => {change_time} --------------")

if change_time is not None:
    s = sched.scheduler(time.time, time.sleep)
    s.enter(change_time, 1, run_hourly, (s,))
    s.run()
else:
    nord_vpn.main(country_code)
