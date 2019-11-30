#!/usr/bin/env python3

import time
import argparse

from yiac.api import yi


def print_settings(y, filter_name):
    settings = y.settings.get()
    if filter_name in settings:
        options = y.settings.options(filter_name)
        print(filter_name)
        print("   value: %s" % settings[filter_name])
        print("   permission: %s" % options["permission"])
        print("   options: %s" % ", ".join(options["options"]))
    else:
        for s in settings:
            options = y.settings.options(s)
            if filter_name == 'all' or filter_name == options["permission"]:
                print(s)
                print("   value: %s" % settings[s])
                print("   permission: %s" % options["permission"])
                print("   options: %s" % ", ".join(options["options"]))


def main():
    parser = argparse.ArgumentParser(description="yiac")
    parser.add_argument(
        "-i", "--ip", help="Yi IP (default: 192.168.42.1)", default="192.168.42.1",
    )
    parser.add_argument(
        "-p", "--port", type=int, help="Yi Port (default: 7878)", default=7878
    )
    parser.add_argument("--stream", action="store_true", default=False, help="Enable RTSP stream")
    parser.add_argument("-s", "--setting", help="Get and set setting options, e.g. all, settable, readonly or any settingname") 
    parser.add_argument("--set")
    parser.add_argument("--record-start", action="store_true", default=False, help="start video recording")
    parser.add_argument("--record-stop", action="store_true", default=False, help="stop video recording")
    parser.add_argument("--proxy", default=554, help="proxy stream to localhost")

    args = parser.parse_args()

    y = yi(args.ip, args.port, "DEBUG")
    y.connect()

    if args.stream:
        y.stream.start()
        print("RTSP stream enabled: rtsp://%s/live" % args.ip)

    if args.setting:
        print_settings(y, args.setting)

        if args.set:
            y.settings.set(args.setting, args.set)
            print_settings(y, args.setting)

    if args.record_start:
        y.video.start()

    if args.record_stop:
        y.video.stop()

    y.close()

if __name__ == "__main__":
    main()
