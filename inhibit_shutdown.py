#!/usr/bin/python

import xbmc
import subprocess

# Set of (protocol, local port) tuples.
watched = {
    ('tcp', 22), # SSH
    ('tcp', 445), # samba
    }
sleep_time = 60 * 1000 # sleep time between checks in miliseconds
service_name = 'service.inhibit_shutdown'

def check_services():
    """ Check if any of the watched services is running. """

    netstat = subprocess.check_output(['/bin/netstat', '--protocol=inet', '-n'], universal_newlines=True)

    for line in netstat.split('\n')[2:]:
        items = line.split()

        proto = items[0]
        port = int(items[3].split(':')[-1])

        if (proto, port) in watched:
            print("{}: Found {} connection from {} to port {}".format(service_name, proto, items[4], port))
            return True

    print("{} No connection found.".format(service_name))
    return False

while not xbmc.abortRequested:
    if check_services():
        print("{}: Inhibiting idle shutdown".format(service_name))
        xbmc.executebuiltin('InhibitIdleShutdown')
    else:
        print("{}: Allowing idle shutdown".format(service_name))
        xbmc.executebuiltin('AllowIdleShutdown')
    xbmc.sleep(sleep_time)
