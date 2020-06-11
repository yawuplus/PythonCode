#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
sys.path.append('gen-py')
from multiplication import MultiplicationService
from multiplication.ttypes import *
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
try:
    # 同样使用 9090 端口，使用阻塞式 I/O 进行传输，是最常见的模式
    transport = TSocket.TSocket('localhost', 9090)
    transport = TTransport.TBufferedTransport(transport)
    # 封装协议，使用二进制编码格式进行传输
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    # 创建一个 client
    client = MultiplicationService.Client(protocol)
    # 打开连接
    transport.open()
    n1 = 5
    n2 = 7
    product = client.multiply(n1, n2)
    print '%s * %s = %s' % (n1, n2, product)
    # 关闭连接
    transport.close()
except Thrift.TException, tx:
    print '%s' % (tx.message)