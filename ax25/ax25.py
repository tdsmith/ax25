from enum import Enum, auto

import attr

# http://www.ax25.net/AX25.2.2-Jul%2098-2.pdf


class FrameType(Enum):
    I = auto()
    S = auto()
    U = auto()


@attr.s(repr=False)
class StationIdentifier:
    callsign = attr.ib()
    ssid = attr.ib(validator=attr.validators.instance_of(int))

    @classmethod
    def from_bytes(cls, s):
        if len(s) != 7:
            raise ValueError("len(s) != 7")
        call = ''.join(chr(i >> 1) for i in s[:6]).rstrip()
        ssid = (s[6] >> 1) & 0b1111
        return cls(call, ssid)

    @classmethod
    def from_text(cls, s):
        call, ssid = s.split("-")
        return cls(call, int(ssid))

    @classmethod
    def from_object(cls, obj):
        if isinstance(obj, cls):
            return obj
        else:
            return cls.from_text(obj)

    def __repr__(self):
        return "'%s-%d'" % (self.callsign, self.ssid)


@attr.s
class Frame:
    destination = attr.ib(convert=StationIdentifier.from_object)
    source = attr.ib(convert=StationIdentifier.from_object)
    path = attr.ib(validator=attr.validators.instance_of(list))
    frame_type = attr.ib(validator=attr.validators.instance_of(FrameType))
    control = attr.ib()
    pid = attr.ib()
    info = attr.ib()

    @classmethod
    def from_bytes(cls, s, modulus=8):
        if modulus not in (8, 128):
            raise ValueError("Modulus must be 8 or 128")

        destination = StationIdentifier.from_bytes(s[:7])
        # dest_cmdresp = s[7] & 0b10000000
        source = StationIdentifier.from_bytes(s[7:14])

        i = 14
        path = []
        while s[i-1] & 1 == 0:
            hop_node = StationIdentifier.from_bytes(s[i:i+7])
            seen = s[i+6] & 0b10000000
            path.append(RepeaterHop(hop_node, seen))
            i += 7

        pid = None
        control_size = 1 if modulus == 8 else 2

        if s[i] & 0b01 == 0:
            frame_type = FrameType.I
            control = s[i:i+control_size]
            i += control_size
            pid = s[i]
            i += 1
        elif s[i] & 0b11 == 0b01:
            frame_type = FrameType.S
            control = s[i:i+control_size]
            i += control_size
        elif s[i] & 0b11 == 0b11:
            frame_type = FrameType.U
            control = s[i]
            i += 1
            if control & 0b11101100 == 0:
                pid = s[i]
                i += 1
        else:
            raise ValueError("Unknown frame type at field %r" % s[i])

        info = s[i:]

        return cls(
            destination=destination,
            source=source,
            path=path,
            frame_type=frame_type,
            control=control,
            pid=pid,
            info=info,
        )


@attr.s
class RepeaterHop:
    station = attr.ib(validator=attr.validators.instance_of(StationIdentifier))
    seen = attr.ib(default=False, convert=bool)
