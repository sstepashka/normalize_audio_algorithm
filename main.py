#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wave
import numpy as np
import pylab

def flatten(l):
    return [value for sublist in l for value in sublist]

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

class Normalize(object):
    """docstring for Normalize"""
    def __init__(self, db_level = -1.0):
        super(Normalize, self).__init__()

        self.maximum = -999999
        self.minimum = 999999

        self.db_level = db_level
        self.linear_level = self._db_to_linear(self._bounded_level(db_level))

        # self.current_mean = None
        # self.values_n = 0

        self.av = 0.0
        self.n = 1.0
    
    def _calc_mean(self, chunk):
        """
            This formula cal help avoid broblem with variable overflow
            (nx + m) can be very very large number.
            But after decomposite this work greatly
            
             nx + m         n         m
            --------  =  ------- + -------
              n + 1       n + 1     n + 1
            
        """
        for sample in chunk:
            self.av = (self.n - 1) / self.n * self.av + sample / self.n
            self.n += 1.0

        return self.av

    def _bounded_level(self, level):
        level_min = -145.0
        level_max = 0.0

        current_level = level

        if current_level > level_max:
            current_level = level_max

        if current_level < level_min:
            current_level = level_min

        return current_level

    def _db_to_linear(self, db_level):
        return pow(10.0, float(db_level) / 20.0)

    # def _normalize(self, chunk):
    #     return map(lambda value: value / float(np.iinfo(np.int16).max), chunk)

    # def _de_normalize(self, chunk):
    #     return map(lambda value: int(value * np.iinfo(np.int16).max), chunk)

    def process(self, chunk):

        current_maximim, current_minimum = self._get_max_min(chunk)

        self.maximum = max(self.maximum, current_maximim)
        self.minimum = min(self.minimum, current_minimum)

        offset = self._calc_mean(chunk)

        ratio = self.linear_level * float(np.iinfo(np.int16).max)

        extent = max(abs(self.maximum), abs(self.minimum))

        mult = ratio / float(extent)

        processed = map(lambda sample: int((sample - offset) * mult), chunk)

        return processed

        # return self._de_normalize(processed)

    def _get_max_min(self, chunk):
        maximum = max(chunk)
        minimum = min(chunk)

        return (maximum, minimum)

def main():
    file_name = '1453874060289.wav'

    # data = numpy.memmap(file_name, dtype='h', mode='r')

    with open(file_name, 'rb') as f:
        content = np.fromstring(f.read(), np.int16)

    # print content
    # print content.tostring()

    # pylab.plot(content)
    # pylab.plot(content)

    # maximum = np.max(content)
    # minimum = np.min(content)

    # processed = map(lambda sample: sample * 1.5, content)

    normalize = Normalize()

    # print normalize._calc_mean([1, 2, 3, 4])
    # print normalize._calc_mean([1, 2, 3, 4])

    # return

    # print normalize.process([40, 40])

    result = flatten(map(lambda chunk: normalize.process(chunk), chunks(content, 320)))

    # # print len(content)
    # # print len(result)

    # # result = map(lambda sample: sample * 1.5, content)

    # print result

    # pylab.plot(result)
    # pylab.show()

    q = np.array(result).astype(np.int16)

    with open('res.pcm', 'wb') as f:
        # f.write((np.array(result, dtype='h')).tostring())
        f.write(q.tostring())

    # processed = map(lambda sample: sample * 1.5, data)

    # print processed

if __name__ == '__main__':
    main()