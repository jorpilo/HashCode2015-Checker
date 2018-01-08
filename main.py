# @Author: Jorge Pinilla López
# @Date:   12-12-2017 19:38:09
# @Last modified by:   Jorge Pinilla López
# @Version: 2
# @Last modified time: 08-01-2018 0:19:38

import datacenter as dc


def read_in_file(file) -> (int, int, int, list, list):
    with open(file, 'r') as file:
        try:
            ROWS, SLOTS, UNAVAILABLE, POOLS, SERVERS = [int(value) for value in file.readline().split(' ')]
            unavailable = [None] * UNAVAILABLE
            servers = [None] * SERVERS
            for i in range(UNAVAILABLE):
                row, slot = file.readline().split(' ')
                unavailable[i] = (int(row), int(slot))
            for i in range(SERVERS):
                size, power = file.readline().split(' ')
                servers[i] = {'size': int(size), 'power': int(power)}
            return ROWS, SLOTS, POOLS, unavailable, servers
        except Exception as e:
            print('Exception reading .in file')
            print(e)
            raise



def read_out_file(file, servers) -> list:
    servers = [None]*servers
    try:
        with open(file, 'r') as file:
            i = 0
            for line in file:
                line = line.strip().split(' ')
                if line[0] != 'x':
                    row, slot, pool = line
                    servers[i] = (int(row), int(slot), int(pool))
                    i += 1
        return servers
    except:
        print('Read file exception')
        raise


def main():
    ROWS, SLOTS, POOLS, unavailable, servers = read_in_file('files/in.example')
    datacenter = dc.Datacenter(SLOTS, POOLS, ROWS)
    for row, slot in unavailable:
        try:
            datacenter.additem(rownum=row, size=1, slot=slot)
        except Exception as e:
            print(e)
            raise

    server_pos = read_out_file('files/out.example', len(servers))
    for index, server in enumerate(server_pos):
        row, slot, pool = server
        try:
            datacenter.addserver(servers, index, row, slot, pool)
        except datacenter.DCException as e:
            print('Error adding server')
            print(e)
            raise(e)

    print('The minimun is ->' + str(datacenter.calculatescore()))
    print(datacenter)


if __name__ == "__main__":
    main()