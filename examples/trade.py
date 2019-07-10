import time
import os.path as op
from pyctp import ApiStruct, TraderApi
from cli import parse_cli


class TradeClient(TraderApi):
    def __init__(self, broker, investor, password, app_id, auth_code, front, flow_path):
        self._broker = bytes(broker, encoding='gb2312')
        self._investor = bytes(investor, encoding='gb2312')
        self._password = bytes(password, encoding='gb2312')
        self._app_id = bytes(app_id, encoding='gb2312')
        self._auth_code = bytes(auth_code, encoding='gb2312')
        self._front_id, self._session_id = None, None
        self._req_id, self._order_ref, self._ready = 0, 0, False
        self.Create(bytes(op.abspath(flow_path), encoding='gb2312'))
        self.SubscribePublicTopic(2)
        self.SubscribePrivateTopic(2)
        self.RegisterFront(bytes(front, encoding='gb2312'))
        self.Init()
        print('CTP API Version: "{}"'.format(self.GetApiVersion().decode(encoding='gb2312')))
        for i in range(5):
            time.sleep(1)
            if self.ready:
                break
            print('Waiting for CTP client connect...')
        else:
            print('*************** CTP client connect failed...')
            return
        print('Trading Date: {}'.format(self.GetTradingDay().decode(encoding='gb2312')))

    @property
    def req_id(self):
        self._req_id += 1
        return self._req_id

    @property
    def order_ref(self):
        self._order_ref += 1
        return '{:012d}'.format(self._order_ref)

    def send_order(self, code, direction, volume, price, offset_flag):
        order = ApiStruct.InputOrder(
            BrokerID=self._broker,
            InvestorID=self._investor,
            UserID=self._investor,
            OrderRef=bytes(self.order_ref, encoding='gb2312'),
            InstrumentID=bytes(code, encoding='gb2312'),
            Direction=direction,
            VolumeTotalOriginal=volume,
            LimitPrice=price,
            CombOffsetFlag=offset_flag,
            OrderPriceType=b'2',
            VolumeCondition=b'1',
            MinVolume=1,
            ForceCloseReason=b'0',
            IsAutoSuspend=0,
            UserForceClose=0,
            CombHedgeFlag=b'1',
            ContingentCondition=b'1',
            TimeCondition=b'3',
        )
        self.ReqOrderInsert(order, self.req_id)

    @property
    def ready(self):
        return self._ready

    def OnFrontConnected(self):
        print('*************** OnFrontConnected')
        self.ReqAuthenticate(
            ApiStruct.ReqAuthenticate(BrokerID=self._broker, UserID=self._investor, AppID=self._app_id, AuthCode=self._auth_code),
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

    def OnRspAuthenticate(self, pRspAuthenticate, pRspInfo, nRequestID, bIsLast):
        if pRspInfo is not None and pRspInfo.ErrorID > 0:
            print('*************** OnRspAuthenticate ERROR: {}'.format(pRspInfo.ErrorMsg.decode(encoding='gb2312')))
            return
        print('*************** OnRspAuthenticate')
        self.ReqUserLogin(
            ApiStruct.ReqUserLogin(BrokerID=self._broker, UserID=self._investor, Password=self._password),
            self.req_id,
        )

    def OnRspUserLogin(self, pRspUserLogin, pRspInfo, nRequestID, bIsLast):
        if pRspInfo.ErrorID > 0:
            print('*************** OnRspUserLogin ERROR: {}'.format(pRspInfo.ErrorMsg.decode(encoding='gb2312')))
        else:
            print('*************** OnRspUserLogin')
            self._front_id, self._session_id = pRspUserLogin.FrontID, pRspUserLogin.SessionID
            if pRspUserLogin.MaxOrderRef:
                self._order_ref = int(pRspUserLogin.MaxOrderRef.decode(encoding='gb2312'))
            self.ReqSettlementInfoConfirm(
                ApiStruct.SettlementInfoConfirm(BrokerID=self._broker, InvestorID=self._investor),
                self.req_id,
            )

    def OnRspUserLogout(self, pUserLogout, pRspInfo, nRequestID, bIsLast):
        print('*************** OnRspUserLogout')

    def OnRspSettlementInfoConfirm(self, pSettlementInfoConfirm, pRspInfo, nRequestID, bIsLast):
        if pRspInfo.ErrorID > 0:
            print('*************** OnRspSettlementInfoConfirm ERROR: {}'.format(pRspInfo.ErrorMsg.decode(encoding='gb2312')))
        else:
            print('*************** OnRspSettlementInfoConfirm')
            self._ready = True

    def OnRspQrySettlementInfo(self, pSettlementInfo, pRspInfo, nRequestID, bIsLast):
        print('*************** OnRspQrySettlementInfo')

    def OnRtnTrade(self, pTrade):
        print(pTrade)

    def OnRtnOrder(self, pOrder):
        print('*************** OnRtnOrder: {}'.format(pOrder.StatusMsg.decode(encoding='gb2312')))

    def OnErrRtnOrderInsert(self, pInputOrder, pRspInfo):
        if pRspInfo and pRspInfo.ErrorID > 0:
            print('*************** OnErrRtnOrderInsert ERROR: {}'.format(pRspInfo.ErrorMsg.decode(encoding='gb2312')))

    def OnRspQryTradingAccount(self, pTradingAccount, pRspInfo, nRequestID, bIsLast):
        if pRspInfo and pRspInfo.ErrorID > 0:
            print('*************** OnRspQryTradingAccount ERROR: {}'.format(pRspInfo.ErrorMsg.decode(encoding='gb2312')))


def main():
    args = parse_cli()
    _trade_client = TradeClient(
        args.broker,
        args.investor,
        args.password,
        args.app_id,
        args.auth_code,
        args.front_addr,
        './var/conn_',
    )
    if not _trade_client.ready:
        return

    _trade_client.send_order('rb1909', ApiStruct.D_Buy, 2, 3900, ApiStruct.OF_Open)
    time.sleep(1)


if __name__ == '__main__':
    main()
