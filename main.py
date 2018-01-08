# @Author: Jorge Pinilla López
# @Date:   12-12-2017 19:38:09
# @Last modified by:   Jorge Pinilla López
# @Version: 2.2
# @Last modified time: 8-01-2018 23:50:00

import datacenter as dc


def read_in_file(file) -> (int, int, int, list, list):
    """
    :param file:
    :return:
    """
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


def read_out_file(file, numservers) -> list:
    """
    read the output file and transforms it into a list.
    if servers
    :param file: String poiting tyo output file
    :param numservers: Integer of servers to read, must match serverlist value
    :return: servers: Ordenated list of placement of each server with (row, slot, pool).
    """

    # Efficiency instead of using append
    servers = [None] * numservers
    try:
        with open(file, 'r') as file:
            i = 0
            for line in file:
                line = line.strip().split(' ')
                if line[0] != 'x':
                    row, slot, pool = line
                    servers[i] = (int(row), int(slot), int(pool))
                i += 1
            if i < numservers:
                raise Exception('No enough servers in output file Expected: '+str(numservers)+' Got: '+str(i))
            elif i > numservers:
                raise Exception('Too many servers in output file Expected: '+str(numservers)+' Got: '+str(i))
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
        if server is not None:
            row, slot, pool = server
            try:
                datacenter.addserver(servers, index, row, slot, pool)
            except datacenter.DCException as e:
                print('Error adding server')
                print(e)
                raise

    print('The minimun is ->' + str(datacenter.calculatescore()))

    print(datacenter)


if __name__ == "__main__":
    main()
