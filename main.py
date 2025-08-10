import badge
import utime

from internal_os.hardware.radio import sx
from _sx126x import SX126X_CMD_GET_RSSI_INST
cmd = [SX126X_CMD_GET_RSSI_INST]

class App(badge.BaseApp):
    def __init__(self) -> None:
        self.packets = []
        self.packet_data = {}

    def on_open(self) -> None:
        badge.display.fill(1)
        # badge.display.text("Press SW11 to send", 10, 180, 0)
        badge.display.show()
    
    def on_packet(self, packet: badge.radio.Packet, is_foreground: bool) -> None:
        self.packets.append([packet, sx.getRSSI()])

    def loop(self):
        # if badge.input.get_button(badge.input.Buttons.SW11):
        badge.radio.send_packet(dest=0xFFFF, data="TBD".encode())

        if len(self.packets):
            self.packet_data = {}
            for packet in self.packets:
                self.packet_data[str(packet[0].source)] = [packet[1], packet[0].data.decode()]
            badge.buzzer.tone(800, 0.2)           
            badge.display.text(f"Got {str(len(self.packets))} packet(s)", 10, 10, 0)
            print(self.packet_data)
            badge.display.show()
            self.packets = []

        utime.sleep_ms(2500)