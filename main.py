import badge
import utime

from internal_os.hardware.radio import sx

class App(badge.BaseApp):
    def __init__(self) -> None:
        self.packets = []
        self.packet_data = {}
        self.role = None

    def on_open(self) -> None:
        badge.display.fill(1)
        badge.display.text("Press SW13 to be a hider", 5, 80, 0)
        badge.display.text("Press SW6 to be a seeker", 5, 160, 0)
        badge.display.show()
    
    def on_packet(self, packet: badge.radio.Packet, is_foreground: bool) -> None:
        self.packets.append([packet, sx.getRSSI()])

    def loop(self):
        if self.role:
            if badge.input.get_button(badge.input.Buttons.SW11):
                badge.radio.send_packet(dest=0xFFFF, data=self.role.encode())

            if len(self.packets):
                badge.display.fill(1)
                self.packet_data = {}
                for packet in self.packets:
                    self.packet_data[str(packet[0].source)] = [packet[1], packet[0].data.decode()]
                
                if self.role == "S": # if seeker
                    hider_rssis = [((int(data[0]) + int(data[1]))//2) for data in self.packet_data.values() if data[1] != "S"]
                    if hider_rssis:
                        nearest_hider_rssi = min(hider_rssis)
                        badge.buzzer.tone((-nearest_hider_rssi if -nearest_hider_rssi > 0 else 2) * 30, 0.2)
                        badge.display.text(f"Nearest hider RSSI: {nearest_hider_rssi}", 10, 60, 0)
                    else:
                        badge.display.text(f"No hiders found", 10, 60, 0)
                    #for hider in hider_rssis:
                    #    badge.display.text(f"RSSI1: {hider[0]}, RSSI2: {hider[1]}", 10, 60 + 10 * hider_rssis.index(hider), 0)
                elif self.role == "H": # if hider
                    # Ensure the packet content is "S"
                    if self.packets and self.packets[0][0].data.decode() == "S":
                        badge.radio.send_packet(dest=0xFFFF, data=str(sx.getRSSI()).encode())


                badge.display.text(f"Found {str(len(self.packets))} player(s)", 10, 180, 0)
                badge.display.show()
                print(self.packet_data)
                self.packets = []

            utime.sleep_ms(2500)
        else:
            if badge.input.get_button(badge.input.Buttons.SW13):
                self.role = "H"
                badge.display.fill(1)
                badge.display.show()
            elif badge.input.get_button(badge.input.Buttons.SW6):
                self.role = "S"
                badge.display.fill(1)
                badge.display.show()
            utime.sleep_ms(50)