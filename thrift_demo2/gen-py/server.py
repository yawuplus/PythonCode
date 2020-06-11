#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
sys.path.append('gen-py')
from multiplication import MultiplicationService
from multiplication.ttypes import *
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
class MultiplicationHandler(object):
    # multiplication.thrift 文件中已对 `multiploy` 进行了定义，参数为两个整型
    # 返回值为一整型
    def multiply(self, n1, n2):
        print('multify n1 * n2, n1: %s, n2: %s, result: %s' %
              (n1, n2, n1 * n2))
        return n1 * n2
if __name__ == '__main__':
    handler = MultiplicationHandler()
    # Processor 用来从连接中读取数据，将处理授权给 handler（自己实现），
    # 最后将结果写到连接上
    processor = MultiplicationService.Processor(handler)
    # 服务端使用 9090 端口， transport 是网络读写抽象层，为到来的连接创建传输对象
    transport = TSocket.TServerSocket(port=9090)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
    print('Starting the server...')
    server.serve()
    print('done.')