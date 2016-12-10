from . import base_analyzer

class PNA(base_analyzer.PNA):
    DEFAULT_VISA_ADDRESS = "TCPIP0::192.168.1.50::5025::SOCKET"