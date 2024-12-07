from blinker import Signal

from snmp_agent import SNMPAgent

from model import Model

class SimRadio(SNMPAgent):
    model:Model

    def __init__(self, args, model:Model):
        config = {
            "enterprise_mib": ".1.3.6.1.4.1.28097.7.9.1",
            "mib_modules": {
                "6.1": {"handler": self.handle_get_signal_strength},
                "2.1": {"handler": self.handle_get_mac_address}
            }
        }
        super().__init__(args, config)
        self.model = model
        return

    def handle_get_signal_strength(self):
        return str(self.model.get_signal_strength())

    def handle_get_mac_address(self):
        return str(self.model.get_mac_address())
