import threading, socket
from client import Client

class Server:
    def __init__(self,host, port):
        self.host = host
        self.port = port
        self.__is_running = True
        self.__connection_addr_dict = {}
        self.__lock = threading.Lock()

    @property
    def connections(self):
        return self.__connection_addr_dict

    def send(self, addr, data):
        with self.__lock:
            if addr in self.__connection_addr_dict:
                self.__connection_addr_dict[addr]['send'] = data
            else:
                raise Exception('Connection does not exist')

    def __run(self):
        print('starting server on ', (self.host,self.port))
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            while self.__is_running:
                connection, address = s.accept()
                print('accepted connection from ', address)
                self.__connection_addr_dict[address] = dict(send=b'',get=b'')
                connection_thread = threading.Thread(target=self.__listen_new_connection, args=(connection, address))
                connection_thread.start()
        self.__connection_addr_dict.clear()
        print('server stopping... ', (self.host, self.port))

    def close_connection(self, addr):
        with self.__lock:
            if addr in self.__connection_addr_dict:
                self.__connection_addr_dict.pop(addr)

    def start(self):
        server_tread = threading.Thread(target=self.__run)
        server_tread.start()

    def stop(self):
        self.__is_running = False
        client = Client(self.host,self.port)
        try:
            client.connect()
            client.send(b'Bye!')
            client.disconnect()
        except ConnectionResetError as e:
            print(e)
        except Exception as e:
            print(e)

    def get_data(self, addr):
        with self.__lock:
            if addr in self.__connection_addr_dict:
                return self.__connection_addr_dict[addr]['get']
        raise Exception('Connection does not exist')

    def __listen_new_connection(self, connection, address):
        with connection:
            print('connected by', address)
            while address in self.__connection_addr_dict:
                try:
                    data = connection.recv(1024)
                    with self.__lock:
                        if data:
                            self.__connection_addr_dict[address]['get'] = data
                            if self.__connection_addr_dict[address]['send'] != b'':
                                connection.sendall(self.__connection_addr_dict[address]['send'])
                                self.__connection_addr_dict[address]['send'] = b''
                            else:
                                connection.sendall(b' ')
                except Exception as e:
                    print(e)
                    break
        self.close_connection(address)
        print('closing connection to', address)