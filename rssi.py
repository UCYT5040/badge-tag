import sx from internal_os.hardware.radio
from _sx126x import SX126X_CMD_GET_RSSI_INST
cmd = [SX126X_CMD_GET_RSSI_INST]

def print_rssi():
    print(sx.SPItransfer(cmd, 1, False, [], [], 1, True))
