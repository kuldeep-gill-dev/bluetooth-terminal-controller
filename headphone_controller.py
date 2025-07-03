#!/usr/bin/env python3
import dbus
import dbus.service
import subprocess
import time
import random

class HeadphoneController:
    def __init__(self):
        self.bus = dbus.SystemBus()
        self.device_mac = None
        self.device_path = self.find_headphones()
        self.media_player = None
        
    def find_headphones(self):
        manager = dbus.Interface(
            self.bus.get_object("org.bluez", "/"),
            "org.freedesktop.DBus.ObjectManager"
        )
        
        for path, interfaces in manager.GetManagedObjects().items():
            if "org.bluez.Device1" in interfaces:
                props = interfaces["org.bluez.Device1"]
                if props.get("Connected") and "WH-CH520" in props.get("Name", ""):
                    # Extract MAC address from path (remove 'dev_' prefix)
                    mac_part = path.split("/")[-1]
                    if mac_part.startswith("dev_"):
                        self.device_mac = mac_part[4:].replace("_", ":")
                    else:
                        self.device_mac = mac_part.replace("_", ":")
                    return path
        return None
    
    def get_media_player(self):
        if not self.device_path:
            return None
            
        # Find MediaPlayer1 interface
        manager = dbus.Interface(
            self.bus.get_object("org.bluez", "/"),
            "org.freedesktop.DBus.ObjectManager"
        )
        
        for path, interfaces in manager.GetManagedObjects().items():
            if "org.bluez.MediaPlayer1" in interfaces and self.device_path in path:
                return dbus.Interface(
                    self.bus.get_object("org.bluez", path),
                    "org.bluez.MediaPlayer1"
                )
        return None
    
    def media_control(self, action):
        if not self.device_mac:
            print("No connected headphones found")
            return
            
        try:
            # Use playerctl for reliable media control (works with all players)
            if action == "play":
                subprocess.run(["playerctl", "play"], check=True)
            elif action == "pause":
                subprocess.run(["playerctl", "pause"], check=True)
            elif action == "next":
                subprocess.run(["playerctl", "next"], check=True)
            elif action == "previous":
                subprocess.run(["playerctl", "previous"], check=True)
            elif action == "stop":
                subprocess.run(["playerctl", "stop"], check=True)
            print(f"Media: {action}")
        except subprocess.CalledProcessError as e:
            print(f"Media command failed: {e}")
            print("Note: Make sure a media player (Spotify, YouTube, etc.) is active")
        except Exception as e:
            print(f"Error: {e}")
    
    def volume_control(self, action):
        if not self.device_mac:
            print("No connected headphones found")
            return
            
        try:
            # Use pactl for system volume (works with Bluetooth)
            if action == "up":
                subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "+10%"], check=True)
            elif action == "down":
                subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "-10%"], check=True)
            elif action == "mute":
                subprocess.run(["pactl", "set-sink-mute", "@DEFAULT_SINK@", "toggle"], check=True)
            print(f"Volume: {action}")
        except subprocess.CalledProcessError as e:
            print(f"Volume control failed: {e}")
        except Exception as e:
            print(f"Error: {e}")
    
    def custom_commands(self, action):
        if action == "silence":
            # Immediate pause and mute
            self.media_control("pause")
            subprocess.run(["pactl", "set-sink-mute", "@DEFAULT_SINK@", "1"])
            print("Emergency silence activated")
            
        elif action == "headphone_info":
            # Get device info
            if self.device_path:
                device = dbus.Interface(
                    self.bus.get_object("org.bluez", self.device_path),
                    "org.freedesktop.DBus.Properties"
                )
                props = device.GetAll("org.bluez.Device1")
                
                # Try to get RSSI via HCI tools
                rssi = props.get('RSSI', None)
                if rssi is None:
                    try:
                        # Use sudo hcitool for accurate RSSI
                        result = subprocess.run(["sudo", "hcitool", "rssi", self.device_mac], 
                                              capture_output=True, text=True, timeout=3)
                        if result.returncode == 0:
                            rssi = result.stdout.strip().split(':')[-1].strip()
                        else:
                            rssi = 'Permission denied'
                    except:
                        rssi = 'Failed'
                
                print(f"Device: {props.get('Name', 'Unknown')}")
                print(f"MAC: {self.device_mac}")
                print(f"Connected: {props.get('Connected')}")
                print(f"RSSI: {rssi} dBm")
                print(f"Link Quality: {self._get_link_quality()}")
                print(f"Battery: Not supported by this headphone model")
                print(f"Codec: {self._get_codec_info()}")
                
        elif action == "wireless_info":
            # Dedicated wireless engineer info
            self._show_wireless_details()
            
        elif action == "queue":
            # Show music queue/playlist
            self._show_queue()
            
        elif action == "track_info":
            # Show current track details
            self._show_track_info()
    
    def _get_link_quality(self):
        try:
            # Get HCI stats (needs sudo)
            result = subprocess.run(["sudo", "hcitool", "lq", self.device_mac], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
            return "N/A"
        except:
            return "N/A"
    
    def _get_codec_info(self):
        try:
            # Check active A2DP codec
            result = subprocess.run(["bluetoothctl", "show"], 
                                  capture_output=True, text=True)
            if "A2DP" in result.stdout:
                return "A2DP (codec details via pactl)"
            return "Unknown"
        except:
            return "Unknown"
    
    def _show_wireless_details(self):
        if not self.device_path:
            print("No device connected")
            return
            
        print("=== Wireless Engineer Details ===")
        
        # HCI info
        try:
            result = subprocess.run(["hciconfig", "-a"], capture_output=True, text=True)
            print(f"HCI Adapter Info:\n{result.stdout}")
        except:
            print("HCI info not available")
        
        # Connection info
        try:
            result = subprocess.run(["hcitool", "con"], capture_output=True, text=True)
            print(f"Active Connections:\n{result.stdout}")
        except:
            print("Connection info not available")
        
        # Signal strength monitoring
        try:
            # Get connection handle first
            con_result = subprocess.run(["hcitool", "con"], capture_output=True, text=True)
            handle = None
            for line in con_result.stdout.split('\n'):
                if self.device_mac in line and "handle" in line:
                    # Extract handle number
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part == "handle" and i+1 < len(parts):
                            handle = parts[i+1]
                            break
            
            if handle:
                # Try multiple approaches for RSSI (need sudo for some commands)
                methods = [
                    (["sudo", "hcitool", "rssi", self.device_mac], f"RSSI"),
                    (["sudo", "hcitool", "lq", self.device_mac], f"Link Quality"),
                    (["sudo", "hcitool", "lp", self.device_mac], f"Link Policy"),
                ]
                
                for cmd, desc in methods:
                    try:
                        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                        if result.returncode == 0 and result.stdout.strip():
                            print(f"{desc}: {result.stdout.strip()}")
                        else:
                            print(f"{desc}: No response")
                    except Exception as e:
                        print(f"{desc}: Error - {e}")
                        
                # Try btmon approach if available
                try:
                    result = subprocess.run(["btmon", "--time", "1"], 
                                          capture_output=True, text=True, timeout=2)
                    if "RSSI" in result.stdout:
                        lines = [line for line in result.stdout.split('\n') if 'RSSI' in line]
                        if lines:
                            print(f"Btmon RSSI: {lines[-1]}")
                except:
                    pass
            else:
                print("RSSI: Connection handle not found")
        except Exception as e:
            print(f"RSSI monitoring not available: {e}")
    
    def _show_queue(self):
        print("=== Music Queue ===")
        try:
            # Try MPRIS first (works with Spotify, browsers, etc.)
            result = subprocess.run(["playerctl", "metadata", "--format", 
                                   "{{ title }} - {{ artist }}"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Current: {result.stdout.strip()}")
                
                # Try to get queue info (limited support)
                queue_result = subprocess.run(["playerctl", "metadata", "--format", 
                                             "{{ mpris:trackid }}"], 
                                            capture_output=True, text=True)
                if queue_result.returncode == 0:
                    print(f"Track ID: {queue_result.stdout.strip()}")
                    
            # Try getting queue from common players
            players = ["spotify", "vlc", "firefox", "chromium"]
            for player in players:
                try:
                    result = subprocess.run(["playerctl", "-p", player, "metadata", 
                                           "--format", "{{ title }} - {{ artist }}"], 
                                          capture_output=True, text=True)
                    if result.returncode == 0 and result.stdout.strip():
                        print(f"{player.title()}: {result.stdout.strip()}")
                except:
                    continue
                    
        except Exception as e:
            print(f"Queue info not available: {e}")
            print("Note: Queue info depends on the media player (Spotify, VLC, etc.)")
    
    def _show_track_info(self):
        print("=== Current Track Info ===")
        try:
            # Get detailed track metadata
            metadata_fields = [
                ("title", "Title"),
                ("artist", "Artist"), 
                ("album", "Album"),
                ("length", "Duration"),
                ("position", "Position"),
                ("status", "Status"),
                ("volume", "Volume")
            ]
            
            for field, label in metadata_fields:
                try:
                    result = subprocess.run(["playerctl", "metadata", "--format", 
                                           f"{{{{ {field} }}}}"], 
                                          capture_output=True, text=True)
                    if result.returncode == 0 and result.stdout.strip():
                        value = result.stdout.strip()
                        if field == "length" and value.isdigit():
                            # Convert microseconds to MM:SS
                            seconds = int(value) // 1000000
                            value = f"{seconds//60}:{seconds%60:02d}"
                        elif field == "position" and value.isdigit():
                            seconds = int(value) // 1000000
                            value = f"{seconds//60}:{seconds%60:02d}"
                        print(f"{label}: {value}")
                except:
                    continue
                    
        except Exception as e:
            print(f"Track info not available: {e}")
            print("Note: Requires active media player with MPRIS support")