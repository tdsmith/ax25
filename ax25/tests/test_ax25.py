from ax25.ax25 import Frame, StationIdentifier, FrameType


class TestStationIdentifier:
    def test_parse_bytes(self):
        b = bytes([0x9c, 0x94, 0x6e, 0xa0, 0x40, 0x40, 0xe0])
        p = StationIdentifier.from_bytes(b)
        assert p.callsign == "NJ7P"
        assert p.ssid == 0


class TestParsing:
    def test_simplex(self):
        b = bytes([
            # 0x7e,  # flag
            0x9c, 0x94, 0x6e, 0xa0, 0x40, 0x40, 0xe0,  # dest
            0x9c, 0x6e, 0x98, 0x8a, 0x9a, 0x40, 0x61,  # source
            0x3e, 0xf0, 0x00, 0x00,  # body
            # 0x7e  # flag
        ])
        p = Frame.from_bytes(b)
        assert p.destination.callsign == "NJ7P"
        assert p.destination.ssid == 0
        assert p.source.callsign == "N7LEM"
        assert p.source.ssid == 0
        assert len(p.path) == 0
        assert p.frame_type == FrameType.I

    def test_repeater(self):
        b = bytes([
            # 0x7e,  # flag
            0x9c, 0x94, 0x6e, 0xa0, 0x40, 0x40, 0xe0,  # dest
            0x9c, 0x6e, 0x98, 0x8a, 0x9a, 0x40, 0x60,  # source
            0x9c, 0x6e, 0x9e, 0x9e, 0x40, 0x40, 0xe3,  # repeater
            0x3e, 0xf0, 0x00, 0x00,  # body
            # 0x7e  # flag
        ])
        p = Frame.from_bytes(b)
        assert p.destination.callsign == "NJ7P"
        assert p.destination.ssid == 0
        assert p.source.callsign == "N7LEM"
        assert p.source.ssid == 0
        assert len(p.path) == 1
        hop = p.path[0]
        assert hop.station.callsign == "N7OO"
        assert hop.station.ssid == 1
        assert hop.seen is True
        assert p.frame_type == FrameType.I
