# -*- coding: utf-8 -*-
import time


class Timer(object):
    '''
    Created on 2 feb. 2017

    Clase para cronometrar a lo churri

    @author: F. Javier Ortega
    '''

    '''
    Map para sacar los tiempos "en bonito"
    '''
    intervals = (
        ('weeks', 604800),  # 60 * 60 * 24 * 7
        ('days', 86400),    # 60 * 60 * 24
        ('hours', 3600),    # 60 * 60
        ('minutes', 60),
        ('seconds', 1)
        )

    def __init__(self):
        self.start = 0
        self.end = 0

    '''
    Función para sacar un número de segundos "en bonito"
    '''
    def display_time(self, seconds, granularity=2):
        result = []
        for name, count in self.intervals:
            value = seconds // count
            if value:
                seconds -= value * count
                if value == 1:
                    name = name.rstrip('s')
                result.append("{} {}".format(value, name))
        return ', '.join(result[:granularity])

    '''
    Función para sacar el número de segundos medidos "en bonito"
    '''
    def display_time(self, granularity=2):
        return self.display_time(self.elapsed_time())

    '''
    Comienzo del cronómetro
    '''
    def start_timer(self):
        self.start = time.time()

    '''
    Parar el cronómetro
    '''
    def stop_timer(self):
        self.end = time.time()

    '''
    Cálculo del tiempo empleado
    '''
    def elapsed_time(self):
        return self.start - self.end