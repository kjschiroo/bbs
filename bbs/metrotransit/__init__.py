import argparse
import time

from playwright import sync_api

from . import display


_STATE = {"demo_departures": 60 * 9}


def _highlight_departure_time(page):
    page.query_selector_all(".depart-time")[0].evaluate(
        # Highlight just the text part of the first departure time
        """(element) => {
            element.style.backgroundColor = "yellow";
        }"""
    )


def get_departures(headless=True):
    with sync_api.sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        headless or input("Ready to go to the page...")
        page.goto(f"https://www.metrotransit.org/nextrip/902/1/SNUN")
        page.wait_for_selector(".depart-time", state="attached")
        headless or input("Find the departure time...")
        _highlight_departure_time(page)
        departures = page.query_selector_all(".depart-time")
        times = [d.text_content() for d in departures]
        headless or input("Use it...")
        return [int(t.split(" ")[0]) for t in times if "Min" in t]


def demo_departures(*args, **kwargs):
    _STATE["demo_departures"] -= 15
    if _STATE["demo_departures"] <= 0:
        _STATE["demo_departures"] = 60 * 10
    return [max(_STATE["demo_departures"] // 60, 1)]


def select_departure(departures) -> int:
    if len(departures) == 0:
        return "infinite"
    active = departures[0]
    if active > 15:
        return "infinite"
    if active == 5:
        return "go"
    return str(active)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--loop", action="store_true")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    getter = demo_departures if args.demo else get_departures
    update_pace = 15 if not args.demo else 1

    departures = getter(args.loop)
    display.display(select_departure(departures))
    while args.loop:
        display.display(select_departure(departures))
        departures = getter(args.loop)
        time.sleep(update_pace)
