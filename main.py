#!/usr/bin/env python3
import argparse
import sys
from headphone_controller import HeadphoneController

def main():
    parser = argparse.ArgumentParser(description="Bluetooth Term Controller")
    parser.add_argument("action", choices=[
        "play", "pause", "stop", "next", "previous",
        "vol_up", "vol_down", "mute",
        "silence", "info", "wireless_info", "queue", "track_info"
    ], help="Action to perform")
    
    args = parser.parse_args()
    controller = HeadphoneController()
    
    # Media controls
    if args.action in ["play", "pause", "stop", "next", "previous"]:
        controller.media_control(args.action)
    
    # Volume controls
    elif args.action in ["vol_up", "vol_down"]:
        controller.volume_control(args.action.split("_")[1])
    elif args.action == "mute":
        controller.volume_control("mute")
    
    # Custom commands
    elif args.action == "silence":
        controller.custom_commands(args.action)
    
    elif args.action == "info":
        controller.custom_commands("headphone_info")
    
    elif args.action == "wireless_info":
        controller.custom_commands("wireless_info")
    
    elif args.action == "queue":
        controller.custom_commands("queue")
    
    elif args.action == "track_info":
        controller.custom_commands("track_info")

if __name__ == "__main__":
    main()
