import asyncio
import argparse
import time
import json
from messages import IAMAT, WHATSAT
from evaluate import evaluate_json, evaluate_info, evaluate_error
import pandas as pd
import os
import sys


'''
communicate (['Juzang', 'Bernard', 'Jaquez', 'Johnson', 'Clark'])
0 1 0 1 1
1 0 1 1 0
0 1 0 0 1
1 1 0 0 0
1 0 1 0 0
'''

TIMEOUT_MSG = "TIMEOUT"
PYTHON_VER = "3.10"

class SuperClient:
    def __init__(self, host='127.0.0.1', message_max_length=1e6, timeout=None):
        '''
        127.0.0.1 is the localhost
        port could be any port
        '''
        self.host = host
        self.message_max_length = int(message_max_length)
        self.timeout = timeout # no timeout if None

    def set_server_info(self, port_dict, server_dir):
        self.port_dict = port_dict
        self.port2server = dict(zip(port_dict.values(), port_dict.keys()))
        self.Juzang = port_dict['Juzang']
        self.Bernard = port_dict['Bernard']
        self.Jaquez = port_dict['Jaquez']
        self.Johnson = port_dict['Johnson']
        self.Clark = port_dict['Clark']
        self.server = os.path.join(server_dir, "server.py")

    async def start_server(self, server_name):
        command = 'nohup python{} {} {} &\n'.format(PYTHON_VER, self.server, server_name)
        os.system(command)
        # wait for a while so that the server has its time of setting up
        await asyncio.sleep(0.5)

    async def end_server(self, server_name):
        port = self.port_dict[server_name]
        os.system('lsof -ti:{} | xargs kill'.format(port))
        await asyncio.sleep(0.3)

    def end_all_servers(self):
        for server_name in self.port_dict.keys():
            port = self.port_dict[server_name]
            os.system('lsof -ti:{} | xargs kill'.format(port))

    async def crazy(self, port, message):
        reader, writer = await asyncio.open_connection(self.host, port, loop=self.loop)
        # write
        writer.write(str(message).encode())
        await writer.drain()
        writer.write_eof()
        # read
        if self.timeout is None:
            data =  await reader.read(self.message_max_length)
        else:
            read_func = reader.read(self.message_max_length)
            try:
                data = await asyncio.wait_for(read_func, timeout=self.timeout)
            except asyncio.TimeoutError:
                writer.close()
                print("TIME OUT")
                return TIMEOUT_MSG
        writer.close()
        return data.decode().strip()

    async def iamat(self, port, clientName, longitude, latitude):
        message = IAMAT(clientName, longitude, latitude, time.time())
        reader, writer = await asyncio.open_connection(self.host, port, loop=self.loop)
        # write
        writer.write(str(message).encode())
        await writer.drain()
        writer.write_eof()
        # read
        if self.timeout is None:
            data = await reader.read(self.message_max_length)
        else:
            read_func = reader.read(self.message_max_length)
            try:
                data = await asyncio.wait_for(read_func, timeout=self.timeout)
            except asyncio.TimeoutError:
                writer.close()
                print("TIME OUT")
                return TIMEOUT_MSG
        writer.close()
        return data.decode().strip()

    async def whatsat(self, port, clientName, radius, maxItems):
        message = WHATSAT(clientName, radius, maxItems)
        reader, writer = await asyncio.open_connection(self.host, port, loop=self.loop)
        # write
        writer.write(str(message).encode())
        await writer.drain()
        writer.write_eof()
        # read
        if self.timeout is None:
            data =  await reader.read(self.message_max_length)
        else:
            read_func = reader.read(self.message_max_length)
            try:
                data = await asyncio.wait_for(read_func, timeout=self.timeout)
            except asyncio.TimeoutError:
                writer.close()
                print("TIME OUT")
                return TIMEOUT_MSG
        writer.close()
        return data.decode()

    def run_iamat(self, port, clientName, longitude, latitude):
        # start the loop
        data = self.loop.run_until_complete(self.iamat(port, clientName, longitude, latitude))
        return data
    def safe_run_iamat(self, *args):
        try:
            return self.run_iamat(*args)
        except:
            return "CRUSH"

    def run_whatsat(self, port, clientName, radius, maxItems):
        # start the loop
        data = self.loop.run_until_complete(self.whatsat(port, clientName, radius, maxItems))
        first_line = data.split('\n')[0]
        try:
            json_part = json.loads(data[len(first_line):]) if first_line.strip()[0] != "?" else dict()
            first_line = first_line.strip()
            return first_line, json_part
        except:
            return "CRUSH", dict()

    def safe_run_whatsat(self, *args):
        try:
            return self.run_whatsat(*args)
        except:
            return "CRUSH", dict()

    async def errormsg(self, port, message):
        try:
            reader, writer = await asyncio.open_connection(self.host, port)
            # write
            writer.write(str(message).encode())
            await writer.drain()
            writer.write_eof()
            # read
            if self.timeout is None:
                data =  await reader.read(self.message_max_length)
            else:
                read_func = reader.read(self.message_max_length)
                try:
                    data = await asyncio.wait_for(read_func, timeout=self.timeout)
                except asyncio.TimeoutError:
                    writer.close()
                    print("TIME OUT")
                    return TIMEOUT_MSG
            writer.close()
            return data.decode()
        except:
            return "CRUSH"

    def run_errormsg(self, port, message):
        try:
            data = self.loop.run_until_complete(self.errormsg(port, message))
            return data
        except:
            return "CRUSH"

    def safe_run_errormsg(self, *args):
        try:
            return self.run_errormsg(*args)
        except:
            return "CRUSH"

    def run_crazy(self, port, crazy_info):
        data = self.loop.run_until_complete(self.crazy(port, crazy_info))
        return True if (len(data) and data[0] == '?') else False

    def run_startserver(self, server_name):
        self.loop.run_until_complete(self.start_server(server_name))
    def run_endserver(self, server_name):
        self.loop.run_until_complete(self.end_server(server_name))

    def start_all_servers(self):
        for server_name in self.port_dict.keys():
            self.run_startserver(server_name)

    def test(self):
        self.loop = asyncio.get_event_loop()
        # dropping the connections
        all_servers = list(self.port_dict.keys())
        for server_name in all_servers:
            self.run_endserver(server_name)
            # similarly, self.run_startserver(server_name) could be used to start a single server
        sleep(1)

        # test 1 basic: send iamat to juzang, test if all servers can respond to whatsat correctly
        print ("===============")
        print ("Test 1")
        self.start_all_servers()
        data = self.safe_run_iamat(self.Juzang, "client", 34.068931, -118.445127)
        print(evaluate_info(data, self.port2server[self.Juzang], "client", 34.068931, -118.445127))
        first_line, json_part = self.safe_run_whatsat(self.Juzang, "client", 10, 5)
        sleep(1)
        # any other server can respond with correct info
        for test_target in [self.Bernard, self.Jaquez, self.Johnson, self.Clark]:
            first_line, json_part = self.run_whatsat(test_target, "client", 10, 5)
            print(evaluate_info(first_line, self.port2server[self.Juzang], "client", 34.068931, -118.445127))
            print(evaluate_json(json_part, 5))
        self.end_all_servers()


        # test 2 for flooding: kill a server, test if all other servers can still respond correctly
        print ("===============")
        print ("Test 2")
        self.start_all_servers()
        test_case = {
            "client": "client_test",
            "latitude": +34.068930,
            "longitude": -118.445127,
            "latitude2": +34.068940,
            "longitude2": -119.445127,
            "radius": 10,
            "max_item": 5
        }

        data = self.safe_run_iamat(self.Johnson, test_case["client"], test_case["latitude"], test_case["longitude"])

        # terminate Juzang and Bernard; now Clark and Jaquez are connected, but Johnson is not
        self.run_endserver(self.Juzang)
        self.run_endserver(self.Bernard)
        data = self.safe_run_iamat(self.Clark, test_case["client"], test_case["latitude2"], test_case["longitude2"])
        sleep(0.5)

        # the record at Jaquez should be the latest copy from Clark
        first_line, json_part = self.safe_run_whatsat(self.Jaquez, test_case["client"], test_case["radius"], test_case["max_item"])
        print(evaluate_info(first_line, self.port2server[self.Clark], "client", test_case["latitude2"], test_case["longitude2"]))
        print(evaluate_json(json_part, test_case["max_item"]))

        # the record at Johnson should be its old copy, as it does not connect to Clark
        first_line, json_part = self.safe_run_whatsat(self.Jaquez, test_case["client"], test_case["radius"], test_case["max_item"])
        print(evaluate_info(first_line, self.port2server[self.Johnson], "client", test_case["latitude"], test_case["longitude"]))
        print(evaluate_json(json_part, test_case["max_item"]))
        sleep(1)

        # test 3 for exception: check if an invalid message can be correctly responded
        print ("===============")
        print ("Test 3")
        self.start_all_servers()
        messages = ["IAMAT Clark +12-118", "IAMAT Clark +12-118 160000 123", "AS Clark +0.25 testuser +12-118 1234"]
        total_tests = len(messages)
        total_correct = 0
        for message in messages:
            response_message = self.safe_run_errormsg(self.Clark, message).strip()
            print (message, response_message)
            print(evaluate_error(message, response_message))
        self.end_all_servers()

if __name__ == '__main__':
    TIMEOUT = 20
    # an example of the ports
    port_assignment = {
        'Juzang': 9991,
        'Bernard': 9992,
        'Jaquez': 9993,
        'Johnson': 9994,
        'Clark': 9995
    }
    server_dir = "./sample_submission" # the place where we can find server.py

    sys.path.append(server_dir) # this is in case we have other files to import from there

    client = SuperClient(timeout=TIMEOUT) # using the default settings
    client.set_server_info(port_dict, server_dir)
    client.test()
    
    
    
    


