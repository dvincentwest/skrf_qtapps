from skrf_qtwidgets.analyzers import base_analyzer


class Analyzer(base_analyzer.Analyzer):
    DEFAULT_VISA_ADDRESS = "TCPIP0::192.168.1.50::5025::SOCKET"
    NAME = "E8363C"
