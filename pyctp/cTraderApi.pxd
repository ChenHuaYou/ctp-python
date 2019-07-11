# -*- coding: utf-8 -*-

from cUserApiStruct cimport *
from libcpp cimport bool as cbool
from libc.string cimport const_char

cdef extern from "Python.h":
    ctypedef struct PyObject
    ctypedef struct PyMethodDef:
        const_char *ml_name
    object PyImport_ImportModule(const_char *name)
    object PyCFunction_NewEx(PyMethodDef *ml, PyObject *self, object module)
    object XGotAttr "PyObject_GetAttr"(object o, object attr_name)
    object XGetAttr "PyObject_GetAttrString"(object o, const_char *attr_name)
    object XCGetAttr "PyObject_GetAttrString"(PyObject *o, const_char *attr_name)
    int CSetAttr "PyObject_SetAttrString"(PyObject *o, const_char *attr_name, object v) except -1

cdef extern from "ThostFtdcTraderApi.h":
    cdef cppclass CTraderApi "CThostFtdcTraderApi":
        void Release() nogil
        void Init() nogil
        int Join() nogil
        const_char *GetTradingDay() nogil
        void RegisterFront(char *pszFrontAddress) nogil
        void RegisterNameServer(char *pszNsAddress) nogil
        void RegisterFensUserInfo(CFensUserInfoField *pFensUserInfo) nogil
        void RegisterSpi(CTraderSpi *pSpi) nogil
        void SubscribePrivateTopic(TE_RESUME_TYPE nResumeType) nogil
        void SubscribePublicTopic(TE_RESUME_TYPE nResumeType) nogil
        int ReqAuthenticate(CReqAuthenticateField *pReqAuthenticate, int nRequestID) nogil
        int ReqUserLogin(CReqUserLoginField *pReqUserLogin, int nRequestID) nogil
        int ReqUserLogout(CUserLogoutField *pUserLogout, int nRequestID) nogil
        int ReqUserPasswordUpdate(CUserPasswordUpdateField *pUserPasswordUpdate, int nRequestID) nogil
        int ReqTradingAccountPasswordUpdate(CTradingAccountPasswordUpdateField *pTradingAccountPasswordUpdate, int nRequestID) nogil
        int ReqOrderInsert(CInputOrderField *pInputOrder, int nRequestID) nogil
        int ReqParkedOrderInsert(CParkedOrderField *pParkedOrder, int nRequestID) nogil
        int ReqParkedOrderAction(CParkedOrderActionField *pParkedOrderAction, int nRequestID) nogil
        int ReqOrderAction(CInputOrderActionField *pInputOrderAction, int nRequestID) nogil
        int ReqQueryMaxOrderVolume(CQueryMaxOrderVolumeField *pQueryMaxOrderVolume, int nRequestID) nogil
        int ReqSettlementInfoConfirm(CSettlementInfoConfirmField *pSettlementInfoConfirm, int nRequestID) nogil
        int ReqRemoveParkedOrder(CRemoveParkedOrderField *pRemoveParkedOrder, int nRequestID) nogil
        int ReqRemoveParkedOrderAction(CRemoveParkedOrderActionField *pRemoveParkedOrderAction, int nRequestID) nogil
        int ReqExecOrderInsert(CInputExecOrderField *pInputExecOrder, int nRequestID) nogil
        int ReqExecOrderAction(CInputExecOrderActionField *pInputExecOrderAction, int nRequestID) nogil
        int ReqForQuoteInsert(CInputForQuoteField *pInputForQuote, int nRequestID) nogil
        int ReqQuoteInsert(CInputQuoteField *pInputQuote, int nRequestID) nogil
        int ReqQuoteAction(CInputQuoteActionField *pInputQuoteAction, int nRequestID) nogil
        int ReqCombActionInsert(CInputCombActionField *pInputCombAction, int nRequestID) nogil
        int ReqQryOrder(CQryOrderField *pQryOrder, int nRequestID) nogil
        int ReqQryTrade(CQryTradeField *pQryTrade, int nRequestID) nogil
        int ReqQryInvestorPosition(CQryInvestorPositionField *pQryInvestorPosition, int nRequestID) nogil
        int ReqQryTradingAccount(CQryTradingAccountField *pQryTradingAccount, int nRequestID) nogil
        int ReqQryInvestor(CQryInvestorField *pQryInvestor, int nRequestID) nogil
        int ReqQryTradingCode(CQryTradingCodeField *pQryTradingCode, int nRequestID) nogil
        int ReqQryInstrumentMarginRate(CQryInstrumentMarginRateField *pQryInstrumentMarginRate, int nRequestID) nogil
        int ReqQryInstrumentCommissionRate(CQryInstrumentCommissionRateField *pQryInstrumentCommissionRate, int nRequestID) nogil
        int ReqQryExchange(CQryExchangeField *pQryExchange, int nRequestID) nogil
        int ReqQryProduct(CQryProductField *pQryProduct, int nRequestID) nogil
        int ReqQryInstrument(CQryInstrumentField *pQryInstrument, int nRequestID) nogil
        int ReqQryDepthMarketData(CQryDepthMarketDataField *pQryDepthMarketData, int nRequestID) nogil
        int ReqQrySettlementInfo(CQrySettlementInfoField *pQrySettlementInfo, int nRequestID) nogil
        int ReqQryTransferBank(CQryTransferBankField *pQryTransferBank, int nRequestID) nogil
        int ReqQryInvestorPositionDetail(CQryInvestorPositionDetailField *pQryInvestorPositionDetail, int nRequestID) nogil
        int ReqQryNotice(CQryNoticeField *pQryNotice, int nRequestID) nogil
        int ReqQrySettlementInfoConfirm(CQrySettlementInfoConfirmField *pQrySettlementInfoConfirm, int nRequestID) nogil
        int ReqQryInvestorPositionCombineDetail(CQryInvestorPositionCombineDetailField *pQryInvestorPositionCombineDetail, int nRequestID) nogil
        int ReqQryCFMMCTradingAccountKey(CQryCFMMCTradingAccountKeyField *pQryCFMMCTradingAccountKey, int nRequestID) nogil
        int ReqQryEWarrantOffset(CQryEWarrantOffsetField *pQryEWarrantOffset, int nRequestID) nogil
        int ReqQryInvestorProductGroupMargin(CQryInvestorProductGroupMarginField *pQryInvestorProductGroupMargin, int nRequestID) nogil
        int ReqQryExchangeMarginRate(CQryExchangeMarginRateField *pQryExchangeMarginRate, int nRequestID) nogil
        int ReqQryExchangeMarginRateAdjust(CQryExchangeMarginRateAdjustField *pQryExchangeMarginRateAdjust, int nRequestID) nogil
        int ReqQryExchangeRate(CQryExchangeRateField *pQryExchangeRate, int nRequestID) nogil
        int ReqQrySecAgentACIDMap(CQrySecAgentACIDMapField *pQrySecAgentACIDMap, int nRequestID) nogil
        int ReqQryProductExchRate(CQryProductExchRateField *pQryProductExchRate, int nRequestID) nogil
        int ReqQryOptionInstrTradeCost(CQryOptionInstrTradeCostField *pQryOptionInstrTradeCost, int nRequestID) nogil
        int ReqQryOptionInstrCommRate(CQryOptionInstrCommRateField *pQryOptionInstrCommRate, int nRequestID) nogil
        int ReqQryExecOrder(CQryExecOrderField *pQryExecOrder, int nRequestID) nogil
        int ReqQryForQuote(CQryForQuoteField *pQryForQuote, int nRequestID) nogil
        int ReqQryQuote(CQryQuoteField *pQryQuote, int nRequestID) nogil
        int ReqQryCombInstrumentGuard(CQryCombInstrumentGuardField *pQryCombInstrumentGuard, int nRequestID) nogil
        int ReqQryCombAction(CQryCombActionField *pQryCombAction, int nRequestID) nogil
        int ReqQryTransferSerial(CQryTransferSerialField *pQryTransferSerial, int nRequestID) nogil
        int ReqQryAccountregister(CQryAccountregisterField *pQryAccountregister, int nRequestID) nogil
        int ReqQryContractBank(CQryContractBankField *pQryContractBank, int nRequestID) nogil
        int ReqQryParkedOrder(CQryParkedOrderField *pQryParkedOrder, int nRequestID) nogil
        int ReqQryParkedOrderAction(CQryParkedOrderActionField *pQryParkedOrderAction, int nRequestID) nogil
        int ReqQryTradingNotice(CQryTradingNoticeField *pQryTradingNotice, int nRequestID) nogil
        int ReqQryBrokerTradingParams(CQryBrokerTradingParamsField *pQryBrokerTradingParams, int nRequestID) nogil
        int ReqQryBrokerTradingAlgos(CQryBrokerTradingAlgosField *pQryBrokerTradingAlgos, int nRequestID) nogil
        int ReqQueryCFMMCTradingAccountToken(CQueryCFMMCTradingAccountTokenField *pQueryCFMMCTradingAccountToken, int nRequestID) nogil
        int ReqFromBankToFutureByFuture(CReqTransferField *pReqTransfer, int nRequestID) nogil
        int ReqFromFutureToBankByFuture(CReqTransferField *pReqTransfer, int nRequestID) nogil
        int ReqQueryBankAccountMoneyByFuture(CReqQueryAccountField *pReqQueryAccount, int nRequestID) nogil

cdef extern from "ThostFtdcTraderApi.h" namespace "CThostFtdcTraderApi":
    CTraderApi *CreateFtdcTraderApi(const_char *pszFlowPath) nogil except +
    const_char *GetApiVersion() nogil

cdef extern from "CTraderApi.h":
    cdef cppclass CTraderSpi:
        CTraderSpi(PyObject *obj)
        long tid
    void ReleaseTraderApi(CTraderApi *api, CTraderSpi *spi)
    cdef PyObject *Xmod "__pyx_m"
    cdef PyMethodDef _init_method
    int CheckMemory(void *) except 0
    void XFixSysModules()
    object XStr(const_char *v)

    cdef const_char *S___name__
    cdef const_char *S_ctypes
    cdef const_char *S_addressof
    cdef const_char *S_from_address
    cdef const_char *S_Accountregister
    cdef const_char *S_BrokerTradingAlgos
    cdef const_char *S_BrokerTradingParams
    cdef const_char *S_CFMMCTradingAccountKey
    cdef const_char *S_CFMMCTradingAccountToken
    cdef const_char *S_CancelAccount
    cdef const_char *S_ChangeAccount
    cdef const_char *S_CombAction
    cdef const_char *S_CombInstrumentGuard
    cdef const_char *S_ContractBank
    cdef const_char *S_DepthMarketData
    cdef const_char *S_EWarrantOffset
    cdef const_char *S_ErrorConditionalOrder
    cdef const_char *S_Exchange
    cdef const_char *S_ExchangeMarginRate
    cdef const_char *S_ExchangeMarginRateAdjust
    cdef const_char *S_ExchangeRate
    cdef const_char *S_ExecOrder
    cdef const_char *S_ExecOrderAction
    cdef const_char *S_ForQuote
    cdef const_char *S_ForQuoteRsp
    cdef const_char *S_InputCombAction
    cdef const_char *S_InputExecOrder
    cdef const_char *S_InputExecOrderAction
    cdef const_char *S_InputForQuote
    cdef const_char *S_InputOrder
    cdef const_char *S_InputOrderAction
    cdef const_char *S_InputQuote
    cdef const_char *S_InputQuoteAction
    cdef const_char *S_Instrument
    cdef const_char *S_InstrumentCommissionRate
    cdef const_char *S_InstrumentMarginRate
    cdef const_char *S_InstrumentStatus
    cdef const_char *S_Investor
    cdef const_char *S_InvestorPosition
    cdef const_char *S_InvestorPositionCombineDetail
    cdef const_char *S_InvestorPositionDetail
    cdef const_char *S_InvestorProductGroupMargin
    cdef const_char *S_Notice
    cdef const_char *S_NotifyQueryAccount
    cdef const_char *S_OpenAccount
    cdef const_char *S_OptionInstrCommRate
    cdef const_char *S_OptionInstrTradeCost
    cdef const_char *S_Order
    cdef const_char *S_OrderAction
    cdef const_char *S_ParkedOrder
    cdef const_char *S_ParkedOrderAction
    cdef const_char *S_Product
    cdef const_char *S_ProductExchRate
    cdef const_char *S_QueryCFMMCTradingAccountToken
    cdef const_char *S_QueryMaxOrderVolume
    cdef const_char *S_Quote
    cdef const_char *S_QuoteAction
    cdef const_char *S_RemoveParkedOrder
    cdef const_char *S_RemoveParkedOrderAction
    cdef const_char *S_ReqQueryAccount
    cdef const_char *S_ReqRepeal
    cdef const_char *S_ReqTransfer
    cdef const_char *S_RspAuthenticate
    cdef const_char *S_RspInfo
    cdef const_char *S_RspRepeal
    cdef const_char *S_RspTransfer
    cdef const_char *S_RspUserLogin
    cdef const_char *S_SecAgentACIDMap
    cdef const_char *S_SettlementInfo
    cdef const_char *S_SettlementInfoConfirm
    cdef const_char *S_Trade
    cdef const_char *S_TradingAccount
    cdef const_char *S_TradingAccountPasswordUpdate
    cdef const_char *S_TradingCode
    cdef const_char *S_TradingNotice
    cdef const_char *S_TradingNoticeInfo
    cdef const_char *S_TransferBank
    cdef const_char *S_TransferSerial
    cdef const_char *S_UserLogout
    cdef const_char *S_UserPasswordUpdate
