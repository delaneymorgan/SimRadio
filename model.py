
from threading import Lock

class Model(object):
    DEFAULT_SIGNAL_STRENGTH = -65
    DEFAULT_MAC_ADDRESS = "12:34:56:78:9a:bc"
    MIN_SIGNAL = -100
    MAX_SIGNAL = 0
    SIGNAL_INC = 5
    signal_strength:int
    mac_address:str

    def __init__(self, args):
        self.args = args
        self.signal_strength = Model.DEFAULT_SIGNAL_STRENGTH
        self.mac_address = Model.DEFAULT_MAC_ADDRESS
        self.signal_strength_lock = Lock()
        self.mac_address_lock = Lock()
        return

    def set_signal_strength(self, signal_strength:int) -> None:
        with self.signal_strength_lock:
            self.signal_strength = signal_strength
        return

    def get_signal_strength(self) -> int:
        with self.signal_strength_lock:
            return self.signal_strength

    def set_mac_address(self, mac_address:str) -> None:
        with self.mac_address_lock:
            self.mac_address = mac_address
        return

    def get_mac_address(self) -> str:
        with self.mac_address_lock:
            return self.mac_address
