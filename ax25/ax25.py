import attr

# http://www.ax25.net/AX25.2.2-Jul%2098-2.pdf


@attr.s
class Frame:
    destination = attr.ib()
    source = attr.ib()
    path = attr.ib(validator=attr.validators.instance_of(list))
    control = attr.ib()
    info = attr.ib()
    fcs = attr.ib()

    @classmethod
    def from_bytes(cls, s):
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

        return cls(
            destination=destination,
            source=source,
            path=path,
            control=None,
            info=None,
            fcs=None,
        )


@attr.s
class InformationFrame(Frame):
    pid = attr.ib()


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

    def __repr__(self):
        return "'%s-%d'" % (self.callsign, self.ssid)


@attr.s
class RepeaterHop:
    station = attr.ib(validator=attr.validators.instance_of(StationIdentifier))
    seen = attr.ib(default=False, convert=bool)
