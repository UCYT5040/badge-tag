import badge
import utime

from internal_os.hardware.radio import sx
from _sx126x import SX126X_CMD_GET_RSSI_INST
cmd = [SX126X_CMD_GET_RSSI_INST]

class App(badge.BaseApp):
    def __init__(self) -> None:
        self.got_packet = False
        self.packet = None

    def on_open(self) -> None:
        badge.display.fill(1)
        badge.display.text("Press SW11 to send", 10, 180, 0)
        badge.display.show()
    
    def on_packet(self, packet: badge.radio.Packet, is_foreground: bool) -> None:
        self.got_packet = True
        self.packet = packet

    def loop(self):
        if badge.input.get_button(badge.input.Buttons.SW11):
            badge.radio.send_packet(dest=0xFFFF, data="This is a test packet".encode())
            badge.buzzer.tone(600, 0.5)

        if self.got_packet:
            badge.buzzer.tone(2000, 0.5)
            badge.display.fill(1)
            rssi = sx.getRSSI()
            badge.display.text(str(rssi), 10, 10, 0)
            badge.display.text(self.packet.data.decode(), 10, 50, 0)
            self.got_packet = False
            badge.display.show()

        utime.sleep_ms(50)