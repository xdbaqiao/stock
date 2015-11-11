#!/usr/bin/env python2
# coding: utf-8

import re
import csv

def common_re(str_re, html):
    m = re.compile(str_re).search(html)
    if m:
        return m.groups()[0]
    return ''

class UnicodeWriter:
    def __init__(self, file, encoding='utf-8', mode='wb', quoting=csv.QUOTE_ALL, utf8_bom=False, auto_repair=False, **argv):
        self.encoding = encoding
        self.unique = False 
        self.unique_by = None
        if hasattr(file, 'write'):
            self.fp = file
        else:
            if auto_repair:
                self._remove_invalid_rows(file=file, quoting=quoting, **argv)
            if utf8_bom:
                self.fp = open(file, 'wb')
                self.fp.write('\xef\xbb\xbf')
                self.fp.close()
                self.fp = open(file, mode=mode.replace('w', 'a'))
            else:
                self.fp = open(file, mode)
        if self.unique:
            self.rows = adt.HashDict() # cache the rows that have already been written
            for row in csv.reader(open(self.fp.name, 'rb')):
                self.rows[self._unique_key(row)] = True
        self.writer = csv.writer(self.fp, quoting=quoting, **argv)

    def _unique_key(self, row):
        return '_'.join([str(row[i]) for i in self.unique_by]) if self.unique_by else str(row)

    def _remove_invalid_rows(self, file, **argv):
        if os.path.exists(file):
            file_obj = open(file)
            tmp_file = file + '.tmp'
            tmp_file_obj = open(tmp_file, 'wb')
            writer = csv.writer(tmp_file_obj, **argv)
            try:
                for row in csv.reader(file_obj):
                    writer.writerow(row)
            except Exception, e:
                pass
            file_obj.close()
            tmp_file_obj.close()
            os.remove(file)
            os.rename(tmp_file, file)

    def _cell(self, s):
        """Normalize the content for this cell
        """
        if isinstance(s, basestring):
            if isinstance(s, unicode):
                s = s.encode(self.encoding, 'ignore')
        elif s is None:
            s = ''
        else:
            s = str(s)
        return s

    def writerow(self, row):
        row = [self._cell(col) for col in row]
        if self.unique:
            if self._unique_key(row) not in self.rows:
                self.writer.writerow(row)
                self.rows[self._unique_key(row)] = True
        else:
            self.writer.writerow(row)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

    def flush(self):
        self.fp.flush()
        if hasattr(self.fp, 'fileno'):
            # this is a real file
            os.fsync(self.fp.fileno())

    def close(self):
        self.fp.close()
