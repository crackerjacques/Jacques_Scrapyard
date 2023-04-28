import sys
import argparse
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib


# Receive AES67 Streaming with sdp file
# The sdp file format is Merging Technology compliant since it was created for use with the Merging Technology interface.
#


def on_message(bus, message, loop):
    mtype = message.type
    if mtype == Gst.MessageType.EOS:
        print("End of stream")
        loop.quit()
    elif mtype == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        print("Error: %s" % err, debug)
        loop.quit()
    return True

def main(args):
    Gst.init(None)
    Gst.debug_set_active(True)
    Gst.debug_set_default_threshold(4)
    
    parser = argparse.ArgumentParser(description='AES67 audio receiver')
    parser.add_argument('--sdp', type=str, help='Path to the SDP file')
    parser.add_argument('--clock-rate', type=int, default=48000, help='Audio clock rate in Hz (default: 48000)')
    parser.add_argument('--channels', type=int, default=2, help='Number of audio channels (default: 2)')
    parser.add_argument('--port', type=int, default=5004, help='RTP port (default: 5004)')
    parser.add_argument('--interface', type=str, help='Network interface to bind (default: all available interfaces)')
    args = parser.parse_args()

    if args.sdp:
        with open(args.sdp, 'r') as sdp_file:
            sdp = sdp_file.read()
    else:
        sdp = None

    caps = f"application/x-rtp,media=(string)audio,clock-rate=(int){args.clock_rate},encoding-name=(string)L24,encoding-params=(string){args.channels},channels=(int){args.channels},payload=(int)98"

    if sdp:
        pipeline = Gst.parse_launch(f"appsrc name=appsrc0 format=GST_FORMAT_TIME ! sdpdemux ! rtpL24depay ! audioconvert ! autoaudiosink")
        appsrc_elem = pipeline.get_by_name("appsrc0")
        appsrc_caps = Gst.Caps.from_string(f"application/sdp,media=(string)application")
        appsrc_elem.set_property("caps", appsrc_caps)
        buffer = Gst.Buffer.new_wrapped(bytes(sdp, 'utf-8'))
        appsrc_elem.emit("push-buffer", buffer)
        appsrc_elem.emit("end-of-stream")
    else:
        pipeline = Gst.parse_launch(f"udpsrc name=udpsrc0 port={args.port} ! rtpL24depay ! audioconvert ! autoaudiosink")
        udpsrc_elem = pipeline.get_by_name("udpsrc0")
        udpsrc_elem.set_property("caps", Gst.Caps.from_string(caps))
        if args.interface:
            udpsrc_elem.set_property("multicast_iface", args.interface)

    print(f"Using network interface: {args.interface}")

    bus = pipeline.get_bus()
    bus.add_signal_watch()
    loop = GLib.MainLoop()
    bus.connect("message", on_message, loop)

    pipeline.set_state(Gst.State.PLAYING)

    try:
        loop.run()
    except Exception as e:
        print("Error:", e)
    finally:
        pipeline.set_state(Gst.State.NULL)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
