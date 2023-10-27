#!/usr/bin/python3

# KAIST CS341 SDN Lab Test script

import time
import argparse
import sys

from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel

from task_topology import Topology
from graph import gen_graph
from dump import dump_clear, dump_net

if __name__ == '__main__':
    # Uncomment below to see verbose log
    #setLogLevel('debug')
    
    parser = argparse.ArgumentParser(prog='CS341 SDN Lab Tester')
    parser.add_argument('--task', metavar='T', type=int, nargs='?', default=1,
                        help='task to test', required=True, choices=range(1,6))
    args = parser.parse_args()
    
    switches, hosts, links = gen_graph(args.task)
    if args.task == 1:
        t = Topology(switches, hosts, links)
        net = Mininet(topo=t)
    elif args.task in range(2, 6):
        t = Topology(switches, hosts, links)
        net = Mininet(topo=t, controller=RemoteController, listenPort=6633)
        dump_net(net, links)
    else:
        raise NotImplementedError('Supported Task number: 1-5')
    
    net.start()
    net.waitConnected()
    if args.task == 4 or args.task == 5:
        # Launch DNS and HTTP server, then run client
        time.sleep(1)
        hosts = net.host

        h1 = net.get('h1')
        serverp = h1.popen('./server.py', shell=True)
        # In order to write output to console: append argument (stdout=sys.stdout, stderr=sys.stderr)
        # serverp = h1.popen('./server.py', shell=True, stdout=sys.stdout, stderr=sys.stderr)
        h2 = net.get('h2')
        dnsp = h2.popen('./dns -a cs341dangerous.com=10.0.0.1 -a cs341safe.com=10.0.0.1', shell=True)
        # In order to write output to console: append argument (stdout=sys.stdout, stderr=sys.stderr)
        # dnsp = h2.popen('./dns', shell=True, stdout=sys.stdout, stderr=sys.stderr)
        CLI(net)
        serverp.kill()
        dnsp.kill()
    else:
        CLI(net)
    net.stop()

