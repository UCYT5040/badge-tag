# badge-tag
Play tag with Shipwrecked PCBs

## Installation
1. Install **mpremote**.
2. Run the following command to install the app:
```bash
mpremote connect /dev/ttyACM0 mkdir :/apps/badge-tag + cp -r main.py manifest.json badge-tag.pbm :/apps/badge-tag
```

## Usage
1. Open the app.
2. Choose whether you want to be a hider or a seeker.
3. If you are the seeker, press **SW11** to search for nearby hiders.
4. If any hiders are detected, the seeker will see the RSSI of the closest one, which can be used to estimate the distance to them.
