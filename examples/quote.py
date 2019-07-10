import time
import argparse
import os.path as op
from pyctp import ApiStruct, MdApi


class QuoteClient(MdApi):
    def __init__(self, broker, investor, password, front, flow_path, instruments):
        self._broker = bytes(broker, encoding='gb2312')
        self._investor = bytes(investor, encoding='gb2312')
        self._password = bytes(password, encoding='gb2312')
        self._req_id, self._logged, self._ready = 0, False, False
        self.Create(bytes(op.abspath(flow_path), encoding='gb2312'))
        self.RegisterFront(bytes(front, encoding='gb2312'))
        self.Init()
        print('CTP API Version: "{}"'.format(self.GetApiVersion().decode(encoding='gb2312')))
        for i in range(5):
            time.sleep(1)
            if self._logged:
                break
            print('Waiting for CTP client connect...')
        else:
            print('*************** CTP client connect failed...')
            return
        print('Trading Date: {}'.format(self.GetTradingDay().decode(encoding='gb2312')))

        instruments = [bytes(inst, encoding='gb2312') for inst in instruments]
        self.SubscribeMarketData(instruments)
        for i in range(5):
            time.sleep(1)
            if self._logged:
                break
            print('Waiting for subscribing...')
        else:
            print('*************** Subscribe failed...')
            return

    @property
    def req_id(self):
        self._req_id += 1
        return self._req_id

    @property
    def ready(self):
        return self._ready

    def OnFrontConnected(self):
        print('*************** OnFrontConnected')
        self.ReqUserLogin(
            ApiStruct.ReqUserLogin(BrokerID=self._broker, UserID=self._investor, Password=self._password),
            self.req_id,
        )

    def OnFrontDisconnected(self, nReason):
        reasons = {
            0x1001: '网络读失败',
            0x1002: '网络写失败',
            0x2001: '接收心跳超时',
            0x2002: '发送心跳失败',
            0x2003: '收到错误报文',
        }
        print('*************** OnFrontDisconnected[{:0x}]: {}'.format(nReason, reasons[nReason]))

    def OnRspUserLogin(self, pRspUserLogin, pRspInfo, nRequestID, bIsLast):
        if pRspInfo.ErrorID > 0:
            print('*************** OnRspUserLogin ERROR: {}'.format(pRspInfo.ErrorMsg.decode(encoding='gb2312')))
        else:
            print('*************** OnRspUserLogin')
            self._logged = True

    def OnRspUserLogout(self, pUserLogout, pRspInfo, nRequestID, bIsLast):
        print('*************** OnRspUserLogout')

    def OnRspSubMarketData(self, pSpecificInstrument, pRspInfo, nRequestID, bIsLast):
        if pRspInfo.ErrorID > 0:
            print('*************** OnRspSubMarketData ERROR: {}'.format(pRspInfo.ErrorMsg.decode(encoding='gb2312')))
        else:
            print('*************** OnRspSubMarketData')
            self._ready = True

    def OnRtnDepthMarketData(self, pDepthMarketData):
        print('Quote: Instrument={}, Price={}'.format(pDepthMarketData.InstrumentID.decode(encoding='gb2312'), pDepthMarketData.LastPrice))


def parse_cli():
    parser = argparse.ArgumentParser(description='Account Monitor')
    parser.add_argument('--broker', type=str, required=True, help='BrokerID')
    parser.add_argument('--investor', type=str, required=True, help='InvestorID')
    parser.add_argument('--password', type=str, required=True, help='Password')
    parser.add_argument('--front_addr', type=str, required=True, help='Front Address')
    return parser.parse_args()


def main():
    args = parse_cli()
    _quote_client = QuoteClient(
        args.broker,
        args.investor,
        args.password,
        args.front_addr,
        './var/conn_',
        ['rb1910', 'TA909'],
    )
    if not _quote_client.ready:
        return

    while True:
        time.sleep(1)


if __name__ == '__main__':
    main()
