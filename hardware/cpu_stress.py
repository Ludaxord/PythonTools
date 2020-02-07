import signal
from multiprocessing import cpu_count, Pool


class CPUStress:

    def __init__(self):
        self.stop_loop = 0

    def exit_child(self, x, y):
        self.stop_loop = 1

    def f(self, x):
        while not self.stop_loop:
            x * x

    def run(self):
        processes = cpu_count()
        print('-' * 20)
        print('Running load on CPU(s)')
        print('Utilizing %d cores' % processes)
        print('-' * 20)
        pool = Pool(processes)
        pool.map(self.f, range(processes))


cpu_stress = CPUStress()

signal.signal(signal.SIGINT, cpu_stress.exit_child)

cpu_stress.run()
