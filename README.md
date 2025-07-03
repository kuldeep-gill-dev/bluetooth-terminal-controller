# 🎧 Bluetooth Term Controller

Control your Bluetooth headphones, speakers, and devices directly from the terminal!

## Features

🎵 **Media Controls**
- Play, pause, stop, next, previous
- Works with any AVRCP-compatible Bluetooth device

🔊 **Volume Control** 
- Volume up/down, mute toggle
- System-level audio control

📡 **Wireless Diagnostics**
- Real-time RSSI monitoring  
- Link quality metrics
- Connection diagnostics
- HCI adapter information


📱 **Track Information**
- Current song details
- Artist, album, duration
- Playback status

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Basic controls
python3 main.py play
python3 main.py next
python3 main.py vol_up
python3 main.py mute

# Get device info
python3 main.py info
python3 main.py wireless_info
python3 main.py track_info
```

## All Commands

| Command | Description |
|---------|-------------|
| `play` | Start playback |
| `pause` | Pause playback |
| `stop` | Stop playback |
| `next` | Next track |
| `previous` | Previous track |
| `vol_up` | Volume up |
| `vol_down` | Volume down |
| `mute` | Toggle mute |
| `info` | Device information |
| `wireless_info` | Detailed wireless diagnostics |
| `track_info` | Current track details |
| `queue` | Show current track/player info |
| `party_mode` | Fun volume oscillation |
| `random_skip` | Skip random number of songs |
| `silence` | Emergency pause + mute |
| `bass_boost` | Toggle audio enhancement |

## Compatibility

- ✅ Bluetooth headphones with AVRCP support
- ✅ Gaming controllers (Xbox, PlayStation, Switch Pro)
- ✅ Bluetooth speakers
- ✅ Car audio systems
- ✅ Any device supporting Audio/Video Remote Control Profile

## Requirements

- Linux with BlueZ stack
- PulseAudio
- Python 3.6+
- Paired Bluetooth device

## Installation

```bash
git clone <repo-url>
cd bluetooth-term-controller
pip install -r requirements.txt

# For RSSI monitoring (optional)
sudo apt install bluez-tools
```

## Why Terminal Control?

Perfect for:
- ⌨️ Terminal enthusiasts who never want to leave the shell
- 🎮 Gaming setups where GUI switching breaks flow  
- 🖥️ Headless systems and remote servers
- 🔧 Automation and scripting workflows
- 📡 Wireless diagnostics and monitoring

## Contributing

Found a bug or want to add device support? Open an issue or PR!

Built for terminal lovers who refuse to touch the mouse! 🚀
