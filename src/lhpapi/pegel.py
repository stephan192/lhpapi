#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fetches data from the Hochwasser Portal API and outputs it in JSON format."""

import argparse
import concurrent.futures
from json import dump
from sys import stdout

from lhpapi import HochwasserPortalAPI, LHPError


def get_data(station_id: str):
    """Fetch data for a given station.

    :param str station_id: The identifier of the station.
    :return dict[str, Any]: A dictionary containing the station's data.
    """

    try:
        api = HochwasserPortalAPI(station_id)
        return {
            "ident": api.ident,
            "name": api.name,
            "url": api.url,
            "hint": api.hint,
            "level": api.level,
            "stage": api.stage,
            "flow": api.flow,
            "last_update": api.last_update.astimezone().isoformat(),
        }
    except LHPError as e:
        return {"error": str(e), "station_id": station_id}


def main() -> None:
    """Main function to parse command line arguments and fetch data for specified stations."""

    parser = argparse.ArgumentParser(
        description="Fetch data from the Hochwasser Portal API."
    )
    parser.add_argument(
        "station_ids", nargs="+", type=str, help="The desired stations", default=[]
    )

    args = parser.parse_args()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        dump(
            list(executor.map(get_data, args.station_ids, chunksize=2)),
            stdout,
            indent=2,
        )


if __name__ == "__main__":
    main()
