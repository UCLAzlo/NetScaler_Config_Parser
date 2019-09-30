'''
Author: Daniel Meirovitch
Description: Reads a NetScaler Conf file, and outputs following documentation
             details into a CSV file:
             V-Server Name/IP/Protocol/Port
             Service Group Name/Port/Member Names/IP Names
'''

#Modules to import
import sys

#Global Constants
ADD_COL = 0
BIND_COL = 0

LB_COL = 1
VSERVER_COL = 2
SG_COL = 1
SERVER_COL = 1
MONITOR_COL = 3
POLICY_COL = 4

NAME_VSERVER_COL = 3
PROTOCOL_VSERVER_COL = 4
IP_VSERVER_COL = 5
PORT_VSERVER_COL = 6

NAME_SG_COL = 2
PROTOCOL_SG_COL = 3
MATCH_SG_COL = 4

NAME_SERVER_COL = 2
IP_SERVER_COL = 3
MATCH_SERVER_COL = 3

# add lb vservers to dict

def add_vServers(conf):
    details = {}
    for line in conf:
        if ( line[ADD_COL] == "add" and line[LB_COL] == "lb" and line[VSERVER_COL] == "vserver" ):
            vServer_object = {'name': line[NAME_VSERVER_COL], 'IP': line[IP_VSERVER_COL],
             'Protocol': line[PROTOCOL_VSERVER_COL], 'Port': line[PORT_VSERVER_COL]}
            details[line[NAME_VSERVER_COL]] = vServer_object
    return details

# add service groups to dict


def add_ServiceGroups(conf):
    details = {}
    for line in conf:
        if line[ADD_COL] == "add" and line[SG_COL] == "serviceGroup":
            sg_object = {'name': line[NAME_SG_COL], 'Protocol': line[PROTOCOL_SG_COL]}
            details[line[NAME_SG_COL]] = sg_object
    return details

# add servers to dict


def add_Servers(conf):
    details = {}
    for line in conf:
        if line[ADD_COL] == "add" and line[SERVER_COL] == "server":
            server_object = {'name': line[NAME_SERVER_COL], 'IP': line[IP_SERVER_COL]}
            details[line[NAME_SERVER_COL]] = server_object
    return details

# Bind server objects to service group dict object


def bind_ServiceGroups(conf, serviceGroups, servers):
    base = "Server"
    server_count = 0
    for line in conf:
        if ( line[BIND_COL] == "bind" and line[SG_COL] == "serviceGroup"
            and line[MONITOR_COL] != "-monitorName" ):
            server_object = servers[line[MATCH_SERVER_COL]]
            serviceGroups[line[NAME_SG_COL]][base + str(server_count)] = server_object
            server_count += 1
    return serviceGroups

# Bind service group objects to vServer dict object


def bind_vServers(conf, vServers, serviceGroups):
    base = "ServiceGroup"
    sg_count = 0
    for line in conf:
        if (line[BIND_COL] == "bind" and line[LB_COL] == "lb" and
            line[VSERVER_COL] == "vserver" and line[POLICY_COL] != "-policyName") :
            if line[MATCH_SG_COL] in serviceGroups:
                sg_object = serviceGroups[line[MATCH_SG_COL]]
                vServers[line[NAME_VSERVER_COL]][base + str(sg_count)] = sg_object
                sg_count += 1
    return vServers

# Print results


def printConfDoc(vServers):
    print("vServer Name, vServer IP, vServer Protocol, vServer Port, SG Name,"
          "SG Protocol, Server 1 Name, Server 1 IP, Server 2 Name, Server 2 IP,"
          "Server 3 Name, Server 3 IP, Server 4 Name, Server 4 IP,"
          "Server 5 Name, Server 5 IP")
    for vs_key in vServers:
        print(
            f"{vServers[vs_key]['name']}, {vServers[vs_key]['IP']},"
            f"{vServers[vs_key]['Protocol']}, {vServers[vs_key]['Port']}",
            end=", ")
        for sg_key in vServers[vs_key]:
            if "ServiceGroup" in sg_key:
                sg_object = vServers[vs_key][sg_key]
                print(
                    f"{sg_object['name']}, {sg_object['Protocol']}", end=", ")
                for svr_key in sg_object:
                    if "Server" in svr_key:
                        svr_object = sg_object[svr_key]
                        print(
                            f"{svr_object['name']}, {svr_object['IP']}", end=", ")

        print("")


# Read file and process
orig_conf = sys.argv[1]
conf = [[n for n in line.split()] for line in orig_conf.split('\n')]

vServers = add_vServers(conf)
serviceGroups = add_ServiceGroups(conf)
servers = add_Servers(conf)

serviceGroups = bind_ServiceGroups(conf, serviceGroups, servers)
vServers = bind_vServers(conf, vServers, serviceGroups)

printConfDoc(vServers)