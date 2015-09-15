#!/usr/bin/python2
#coding: utf-8

import Gnuplot

class gnuplot:
    def __init__(self, x, y, title):
        self.x = x
        self.y = y
        self.title = title
        self.plot()

    def plot(self):
        self.g = Gnuplot.Gnuplot(debug=0)
        d = Gnuplot.Data(self.x, self.y, with_='lines')
        self.g.title(self.title)
        self.g.xlabel('times')
        self.g.ylabel('%s' % self.title)
        self.g.plot(d)
        self.g.hardcopy('./%s.ps' % self.title, enhanced=1, color=1)
