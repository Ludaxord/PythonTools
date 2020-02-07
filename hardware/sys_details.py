import os
import platform
import re
import subprocess
import sys

import psutil
from gpuinfo import GPUInfo


class SysDetails:

    def operating_system_info(self, with_print=False):
        operating_system = sys.platform
        if with_print:
            print(f"Operating system: {operating_system}")
        if operating_system.lower() == "darwin":
            cmd = "system_profiler SPSoftwareDataType"
            stream = os.popen(cmd)
            output = stream.read()
            if with_print:
                print(output)
        return operating_system

    def cpu_name(self):
        processor = platform.processor()
        print(f"CPU name: {processor}")
        return processor

    def usage(self):
        try:
            cpu = psutil.cpu_percent()
            memory = dict(psutil.virtual_memory()._asdict())
            memory["total_gb"] = memory["total"] / 1024 ** 3
            memory["available_gb"] = memory["available"] / 1024 ** 3
            memory["used_gb"] = memory["used"] / 1024 ** 3
            memory["free_gb"] = memory["free"] / 1024 ** 3
            memory["active_gb"] = memory["active"] / 1024 ** 3
            memory["inactive_gb"] = memory["inactive"] / 1024 ** 3
            memory["wired_gb"] = memory["wired"] / 1024 ** 3
            print(f"cpu usage {cpu}")
            print(f"memory usage {memory}")
            return cpu, memory
        except Exception as e:
            print(e)

    def gpu_info(self):
        try:
            gpu = GPUInfo.check_empty()
            print(f"GPU name: {gpu}")
            return gpu
        except Exception as e:
            print(e)

    def cpu_name_by_command(self):
        system = self.operating_system_info().lower()
        if system == "windows":
            name = self.cpu_name()
            print(name)
            return name
        elif system == "darwin":
            cmd = "sysctl -n machdep.cpu.brand_string"
            stream = os.popen(cmd)
            output = stream.read()
            print(output)
            return output
        elif system == "linux":
            cmd = "cat /proc/cpuinfo"
            info = subprocess.check_output(cmd, shell=True).strip()
            for line in info.split("\n"):
                if "model name" in line:
                    name = re.sub(".*model name.*:", "", line, 1)
                    print(name)
                    return name
        else:
            name = self.cpu_name()
            print(name)
            return name


system_details = SysDetails()
system_details.operating_system_info(with_print=True)
system_details.cpu_name()
system_details.gpu_info()
system_details.usage()
system_details.cpu_name_by_command()
