#!/usr/bin/env python3

import time
import argparse

from api import yi


def main():
    parser = argparse.ArgumentParser(description="yiac")
    parser.add_argument(
        "-i", "--ip", help="Yi IP (default: 192.168.42.1)", default="192.168.42.1",
    )
    parser.add_argument(
        "-p", "--port", type=int, help="Yi Port (default: 7878)", default=7878
    )
    parser.add_argument("--stream", action="store_true", default=False)
    args = parser.parse_args()

    y = yi(args.ip, args.port, "ERROR")
    y.connect()

    if args.stream:
        y.stream.start()
        print("RTSP stream enabled: rtsp://%s/live" % args.ip)


if __name__ == "__main__":
    main()
