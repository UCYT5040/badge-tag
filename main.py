import badge
import utime

try:
    import gc
except ImportError:
    gc = None

from internal_os.hardware.radio import sx

pacman_melody_simple = [
    [494, 0.14285714285714285],   # B4, 16th
    [988, 0.14285714285714285],   # B5, 16th
    [740, 0.14285714285714285],   # F#5, 16th
    [622, 0.14285714285714285],   # D#5, 16th
    [988, 0.07142857142857142],   # B5, 32nd
    [740, 0.21428571428571427],   # F#5, dotted 16th
    [622, 0.2857142857142857],    # D#5, 8th
    [523, 0.14285714285714285],   # C5, 16th
    [1047, 0.14285714285714285],  # C6, 16th
    [1568, 0.14285714285714285],  # G6, 16th
    [1319, 0.14285714285714285],  # E6, 16th
    [1047, 0.07142857142857142],  # C6, 32nd
    [1568, 0.21428571428571427],  # G6, dotted 16th
    [1319, 0.2857142857142857],   # E6, 8th
    [494, 0.14285714285714285],   # B4, 16th
    [988, 0.14285714285714285],   # B5, 16th
    [740, 0.14285714285714285],   # F#5, 16th
    [622, 0.14285714285714285],   # D#5, 16th
    [988, 0.07142857142857142],   # B5, 32nd
    [740, 0.21428571428571427],   # F#5, dotted 16th
    [622, 0.2857142857142857],    # D#5, 8th
    [622, 0.07142857142857142],   # D#5, 32nd
    [659, 0.07142857142857142],   # E5, 32nd
    [698, 0.07142857142857142],   # F5, 32nd
    [698, 0.07142857142857142],   # F5, 32nd
    [740, 0.07142857142857142],   # F#5, 32nd
    [784, 0.07142857142857142],   # G5, 32nd
    [784, 0.07142857142857142],   # G5, 32nd
    [831, 0.07142857142857142],   # G#5, 32nd
    [880, 0.14285714285714285],   # A5, 16th
    [988, 0.2857142857142857],    # B5, 8th
]

class App(badge.BaseApp):
    def __init__(self) -> None:
        self.packets = []
        self.packet_data = {}
        self.role = None
        
        self._last_gc_ms = utime.ticks_ms()

    def on_open(self) -> None:
        badge.display.fill(1)
        badge.display.text("Press SW13 to be a hider", 5, 80, 0)
        badge.display.text("Press SW6 to be a seeker", 5, 160, 0)
        badge.display.show()
    
    def on_packet(self, packet: badge.radio.Packet, is_foreground: bool) -> None:
        self.packets.append([packet, sx.getRSSI()])

    def loop(self):
        if self.role:
            if badge.input.get_button(badge.input.Buttons.SW11) and self.role == "S":
                badge.radio.send_packet(dest=0xFFFF, data=self.role.encode())
                badge.buzzer.tone(600, 0.5)

            if len(self.packets):
                badge.display.fill(1)
                self.packet_data = {}
                for packet in self.packets:
                    self.packet_data[str(packet[0].source)] = [packet[1], packet[0].data.decode()]
                
                if self.role == "S": # if seeker
                    hider_rssis = []
                    for data in self.packet_data.values():
                        try:
                            if data[1] != "S":
                                hider_rssis.append(((float(data[0]) + float(data[1]))//2))
                        except ValueError: 
                            badge.display.text(f"Failed to parse int", 10, 80, 0)
                            badge.display.text(f"RSSI1:{data[0]}, RSSI2:{data[1]}", 10, 100, 0)
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
                    for packet in self.packets:
                        if packet[0].data.decode() == "S":
                    #if self.packets and self.packets[0][0].data.decode() == "S":
                            badge.radio.send_packet(dest=0xFFFF, data=str(sx.getRSSI()).encode())
                            if -sx.getRSSI() < 10:
                                self.role = "S"
                                for tone in pacman_melody_simple:
                                    badge.buzzer.tone(tone[0], tone[1] * 0.9)
                                    utime.sleep(tone[1] * 0.1)


                badge.display.text(f"Found {str(len(self.packets))} player(s)", 10, 180, 0)
                badge.display.show()
                print(self.packet_data)
                self.packets = []
                if gc:
                    gc.collect()

            utime.sleep_ms(50)
        else:
            if badge.input.get_button(badge.input.Buttons.SW13):
                self.role = "H"
                badge.display.fill(1)
                badge.display.text("You are a hider", 10, 10, 0)
                badge.display.show()
            elif badge.input.get_button(badge.input.Buttons.SW6):
                self.role = "S"
                badge.display.fill(1)
                badge.display.text("You are a seeker", 10, 10, 0)
                badge.display.show()
            utime.sleep_ms(50)

        # periodic gc
        if gc and utime.ticks_diff(utime.ticks_ms(), self._last_gc_ms) > 5000:
            gc.collect()
            self._last_gc_ms = utime.ticks_ms()