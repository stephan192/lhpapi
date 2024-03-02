"""Tests for the lhpapi."""

from datetime import datetime

import pytest

from lhpapi import HochwasserPortalAPI

MIN_STAGE = 0
MAX_STAGE = 4

testdata = [
    ("BB_5804300", "Ketzin / Havel", True, True, True),
    ("BE_5866301", "Zoo / Landwehrkanal", True, False, True),
    ("BW_00102", "Rottenburg / Bronnbachquelle", True, True, True),
    ("BY_16005701", "München / Isar", True, True, True),
    ("HB_4970010", "Elsfleth / Weser", True, True, False),
    ("HE_42881552", "Treysa / Schwalm", True, True, True),
    ("HH_99256", "Rahmoor / Tarpenbek", True, True, False),
    ("MV_04443.1", "Dobbin / Nebel", True, True, True),
    ("NI_4885154", "Poppenburg / Leine", True, True, False),
    ("NW_4433000000100", "Westheim / Diemel", True, True, False),
    ("RP_23900200", "Worms / Rhein", True, True, True),
    ("SH_114064", "Soholm / Soholmer Au", True, True, True),
    ("SL_1014120", "Urweiler / Todbach", True, True, False),
    ("SN_550810", "Elbersdorf / Wesenitz", True, True, True),
    ("ST_591070", "Wolmirstedt / Ohre", True, True, True),
    ("TH_57430.0", "Gehlberg / Wilde Gera", True, True, True),
]


@pytest.mark.parametrize("ident, name, level, stage, flow", testdata)
def test_pegel(ident, name, level, stage, flow):
    """Test a pegel."""
    api = HochwasserPortalAPI(ident)

    assert api.ident == ident
    assert api.name == name
    if api.url is not None:
        assert isinstance(api.url, str)
    if api.hint is not None:
        assert isinstance(api.hint, str)
    if level:
        assert isinstance(api.level, float)
    else:
        assert api.level is None
    if stage:
        assert isinstance(api.stage, int)
        assert MIN_STAGE <= api.stage <= MAX_STAGE
    else:
        assert api.stage is None
    if flow:
        assert isinstance(api.flow, float)
    else:
        assert api.flow is None
    assert isinstance(api.last_update, datetime)
