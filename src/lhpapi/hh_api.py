"""The Länderübergreifendes Hochwasser Portal API - Functions for Hamburg."""

from __future__ import annotations

from .api_utils import (
    DynamicData,
    LHPError,
    StaticData,
    convert_to_datetime,
    convert_to_float,
    convert_to_int,
    fetch_soup,
)


def init_HH(ident: str) -> StaticData:  # pylint: disable=invalid-name
    """Init data for Hamburg."""
    try:
        # Get data
        soup = fetch_soup("https://www.wabiha.de/pegel.html")
        table = soup.find_all("table", id="pegeltabelle")[0]
        tbody = table.find_all("tbody")[0]
        trs = tbody.find_all("tr")
        for row in trs:
            span = row.find(id="tooltip-target-" + ident[3:])
            if span:
                td_prev = span.find_parent("td").find_previous_sibling("td")
                river = td_prev.find("span").text.strip()
                pegel_name = span.text.strip()
                name = pegel_name + " / " + river
                url = "https://www.wabiha.de/grafik-" + ident[3:] + ".html"
                return StaticData(ident=ident, name=name, url=url)
        return StaticData(ident=ident)
    except Exception as err:
        raise LHPError(err, "hh_api.py: init_HH()") from err


def update_HH(static_data: StaticData) -> DynamicData:  # pylint: disable=invalid-name
    """Update data for Hamburg."""
    try:
        # Get data
        soup = fetch_soup("https://www.wabiha.de/pegel.html")
        table = soup.find_all("table", id="pegeltabelle")[0]
        tbody = table.find_all("tbody")[0]
        trs = tbody.find_all("tr")
        # Parse data
        for row in trs:
            span = row.find(id="tooltip-target-" + static_data.ident[3:])
            if span:
                td_next = span.find_parent("td").find_next_sibling("td")
                level = convert_to_float(
                    td_next.find("span").text.replace(".", "").strip()
                )
                td_next2 = td_next.find_next_sibling("td")
                last_update = convert_to_datetime(
                    td_next2.find(string=True, recursive=False).text.strip(),
                    "%d.%m.%y %H:%M",
                )
                td_next4 = td_next2.find_next_sibling("td").find_next_sibling("td")
                if "--" in td_next4.attrs["class"][-1]:
                    stage = None
                else:
                    stage = convert_to_int(td_next4.attrs["class"][-1].split("-")[-1])
                if stage == 2:
                    # Special case for Hamburg, see https://www.hochwasserzentralen.de/info
                    stage = 3
                return DynamicData(level=level, stage=stage, last_update=last_update)
        return DynamicData()
    except Exception as err:
        raise LHPError(err, "hh_api.py: update_HH()") from err
