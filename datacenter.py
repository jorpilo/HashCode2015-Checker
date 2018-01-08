# @Author: Jorge Pinilla López
# @Date:   8-01-2018 00:38:09
# @Last modified by:   Jorge Pinilla López
# @Version: 2.2
# @Last modified time: 8-01-2018 23:37:00

import numpy as np


class Datacenter(object):

    def __init__(self, SLOTS, POOLS, ROWS):
        self.datacenter = {
            'Slots': SLOTS,
            'Power': [0] * POOLS,
            'Rows': [
                {
                    'Power': [0] * POOLS,
                    'Slots': [{
                        'Start': 0,
                        'End': SLOTS - 1,
                    }]
                }for i in range(ROWS)]
        }

    def addserver(self, serverlist, servernumber, row, slot, pool):
        server = serverlist[servernumber]
        if pool < 0 or pool > len(self.datacenter['Power']):
            raise self.DCException('No pool ' + str(pool))
        if server is None:
            raise self.DCException('Server ' + str(servernumber) + ' already used')
        try:
            self.additem(row, slot, server['size'])
        except self.DCException as e:
            raise self.DCException("Couldn't add server "+ str(servernumber)+" to datacenter").with_traceback(e.__traceback__)
        serverlist[servernumber] = None
        self.datacenter['Power'][pool] += server['power']
        self.datacenter['Rows'][row]['Power'][pool] += server['power']

    def additem(self, rownum, slot, size):
        row = self.datacenter['Rows'][rownum]
        found = False
        i = 0
        while not found and i < len(row['Slots']):
            freeblock = row['Slots'][i]
            if slot >= freeblock['Start'] and slot + size - 1 <= freeblock['End']:
                if freeblock['Start'] == slot and freeblock['End'] == slot + size - 1:
                    row['Slots'].remove(freeblock)
                elif freeblock['Start'] == slot:
                    freeblock['Start'] += size
                elif freeblock['End'] == slot + size - 1:
                    freeblock['End'] -= size
                else:
                    row['Slots'].append({'Start': freeblock['Start'], 'End': slot - 1})
                    row['Slots'].append({'Start': slot + size, 'End': freeblock['End']})
                    row['Slots'].remove(freeblock)
                found = True
            else:
                i += 1
        if not found and i >= len(row['Slots']):
            raise self.DCException('No free space on row ' + str(rownum) + ' slot ' + str(slot))

    def calculatescore(self):
        minOfRows = [[a_i - b_i for a_i, b_i in zip(self.datacenter['Power'], row['Power'])] for row in
                     self.datacenter['Rows']]
        return np.minimum(*minOfRows)

    def __str__(self) -> str:
        rows = []
        result = ""
        for i in range(len(self.datacenter['Rows'])):
            rows.append(np.array(['X'] * self.datacenter['Slots']))
        i = 0
        for Row in self.datacenter['Rows']:
            for freeSlot in Row['Slots']:
                rows[i][range(freeSlot['Start'], freeSlot['End'] + 1)] = [' ']
            result += str(rows[i]) + '--->' + str(Row['Power']) + '\n'
            i += 1
        return result

    def __repr__(self) -> str:
        return str(self)

    class DCException(Exception):
        def __init__(self, message):
            super().__init__(message)
