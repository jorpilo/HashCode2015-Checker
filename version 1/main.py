# @Author: Jorge Pinilla López
# @Date:   12-12-2017 19:38:09
# @Last modified by:   Jorge Pinilla López
# @Version: 1
# @Last modified time: 08-01-2018 0:19:38


import numpy as np
""" DataReader and parser: """

def addServer(datacenter, serverlist, servernumber, row, slot, pool):
    server = serverlist[servernumber]
    if pool < 0 or pool > len(datacenter['Power']):
        raise Exception('No pool '+str(pool))
    if server is None:
        raise Exception('Server '+str(servernumber)+' already used')
    try:
        addItem(datacenter,row, slot, server['size'])
    except Exception as e:
        raise Exception(str(e) + ' for serverNumber '+str(servernumber))
    serverlist[servernumber] = None
    datacenter['Power'][pool] += server['power']
    datacenter['Rows'][row]['Power'][pool] += server['power']


def addItem(datacenter, rownum, slot, size):
    row = datacenter['Rows'][rownum]
    found = False
    i = 0
    while not found and i < len(row['Slots']):
        freeblock = row['Slots'][i]
        if slot >= freeblock['Start'] and slot+size-1 <= freeblock['End']:
            if freeblock['Start'] == slot and freeblock['End'] == slot+size-1:
                row['Slots'].remove(freeblock)
            elif freeblock['Start'] == slot:
                freeblock['Start'] += size
            elif freeblock['End'] == slot+size-1:
                freeblock['End'] -= size
            else:
                row['Slots'].append({'Start': freeblock['Start'], 'End': slot-1})
                row['Slots'].append({'Start': slot+size, 'End': freeblock['End']})
                row['Slots'].remove(freeblock)
            found = True
        else:
            i += 1
    if not found and i >= len(row['Slots']):
        raise Exception('No free space on row '+str(rownum)+' slot '+str(slot))


def printdc(datacenter):
    rows = []
    for i in range(len(datacenter['Rows'])):
        rows.append(np.array(['X']*datacenter['Slots']))
    i = 0
    for Row in datacenter['Rows']:
        for freeSlot in Row['Slots']:
            rows[i][range(freeSlot['Start'], freeSlot['End']+1)] = [' ']
        print(str(rows[i])+'--->'+str(Row['Power']))
        i += 1


def calculateScore(datacenter):
    minOfRows = [[a_i - b_i for a_i, b_i in zip(datacenter['Power'], row['Power'])] for row in datacenter['Rows']]
    return np.minimum(*minOfRows)


def main():
    with open('in.example','r') as file:
        try:
            ROWS, SLOTS, UNAVAILABLE, POOLS, SERVERS = [int(value) for value in file.readline().split(' ')]
            unavailable = [None]*UNAVAILABLE
            servers = [None]*SERVERS
            for i in range(UNAVAILABLE):
                row, slot = file.readline().split(' ')
                unavailable[i] = (int(row), int(slot))
            for i in range(SERVERS):
                size, power = file.readline().split(' ')
                servers[i] = {'size': int(size), 'power': int(power)}
        except Exception as e:
            print('Exception reading .in file')
            print(e)
            exit(1)
    datacenter = {
        'Slots': SLOTS,
        'Power': [0] * POOLS,
        'Rows': [
            {
                'Power': [0] * POOLS,
                'Slots': [{
                    'Start': 0,
                    'End': SLOTS-1,
                }]
            } for i in range(ROWS)]
    }
    for row, slot in unavailable:
        try:
            addItem(datacenter, rownum=row, size=1, slot=slot)
        except Exception as e:
            print(e)
            exit(1)
    with open('out.example', 'r') as file:
        try:
            i = 0
            for line in file:
                line = line.strip().split(' ')
                if line[0] != 'x':
                    row, slot, pool = line
                    addServer(datacenter, servers, i, int(row), int(slot), int(pool))
                i += 1
        except Exception as e:
            print('Error reading output file')
            print(e)
            exit(1)

    print('The minimun is ->' + str(calculateScore(datacenter)))
    printdc(datacenter)


if __name__ == "__main__":
    main()