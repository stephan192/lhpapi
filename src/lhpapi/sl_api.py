"""The Länderübergreifendes Hochwasser Portal API - Functions for Saarland."""

from __future__ import annotations

from .api_utils import (
    DynamicData,
    LHPError,
    StaticData,
    calc_stage,
    convert_to_datetime,
    convert_to_float,
    fetch_json,
)


def init_SL(ident: str) -> StaticData:  # pylint: disable=invalid-name
    """Init data for Saarland."""
    try:
        # Get data
        data = fetch_json(
            "https://hmz.saarland.de/FewsWebServices/rest/fewspiservice/v1/locations?"
            + "documentFormat=GEO_JSON&filterId=P.INTERN&showAttributes=true"
        )
        features = data["features"]
        # Parse data
        print(ident)
        for feature in features:
            locationid = "SL_" + feature["properties"]["locationId"].split(".")[-1]
            if locationid == ident:
                name = feature["properties"]["locationName"].replace("Pegel ", "", 1)
                river = ""
                stage_levels = [None] * 4
                for attribute in feature["properties"]["attributes"]:
                    if attribute["name"] == "Gewaesser":
                        river = attribute["value"]
                    if attribute["name"] == "HW_MH_1":
                        stage_levels[0] = convert_to_float(attribute["value"])
                    if attribute["name"] == "HW_MH_2":
                        stage_levels[1] = convert_to_float(attribute["value"])
                    if attribute["name"] == "HW_MH_3":
                        stage_levels[2] = convert_to_float(attribute["value"])
                    if attribute["name"] == "HW_MH_4":
                        stage_levels[3] = convert_to_float(attribute["value"])
                name = name + " / " + river
                internal_url = (
                    "https://hmz.saarland.de/FewsWebServices/rest/fewspiservice/v1/timeseries?"
                    + "locationIds="
                    + feature["properties"]["locationId"]
                    + "&documentFormat=PI_JSON"
                )
                url = (
                    "https://hmz.saarland.de/FewsWebServices/rest/fewspiservice/v1/locations/"
                    + "tooltip?locationId="
                    + feature["properties"]["locationId"]
                    + "&filterId=P.INTERN"
                )
                return StaticData(
                    ident=ident,
                    name=name,
                    internal_url=internal_url,
                    url=url,
                    stage_levels=stage_levels,
                )
        return StaticData(ident=ident)
    except Exception as err:
        raise LHPError(err, "sl_api.py: init_SL()") from err


def update_SL(static_data: StaticData) -> DynamicData:  # pylint: disable=invalid-name
    """Update data for Saarland."""
    try:
        # Get data
        data = fetch_json(static_data.internal_url)
        time_series = data["timeSeries"]
        for ts in time_series:
            if ts["header"]["parameterId"] == "W.Messung":
                for item in reversed(ts["events"]):
                    if item["flag"] == "0":
                        level = convert_to_float(item["value"])
                        stage = calc_stage(level, static_data.stage_levels)
                        last_update = convert_to_datetime(
                            item["date"] + "T" + item["time"] + "Z", "iso"
                        )
                        return DynamicData(
                            level=level, stage=stage, last_update=last_update
                        )
        return DynamicData()
    except Exception as err:
        raise LHPError(err, "sl_api.py: update_SL()") from err
