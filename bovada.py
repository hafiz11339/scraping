from scrapy.crawler import CrawlerProcess
import unidecode
import scrapy
import json
from datetime import datetime
from unidecode import unidecode
from datetime import datetime
from datetime import timedelta

ini_time_for_now = datetime.now()
future_date_after_1day = ini_time_for_now + \
                         timedelta(days=1)
fileout = open('bovada.json', 'w')
Value_get_dict = {'BASE': 'baseball', 'BASK': 'basketball',
                  'FOOT': 'football',
                  'HCKY': 'hockey',
                  'SOCC': 'soccer', 'BOXI': 'boxing',
                  'TENN': 'tennis', 'MMA': 'ufc-mma'}

notScrape = ['Win', 'Total', 'Spread']
allitems = []


class Bovadas(scrapy.Spider):
    name = "bovadas"

    def start_requests(self):
        yield scrapy.Request(url="https://www.bovada.lv/i18n/en/spMarketTypeFilter.json")

    def parse(self, response):
        S = 4
        jsondata = json.loads(response.text)
        key_data = [v for v in jsondata]
        for key in key_data:
            d = 6
            if jsondata[key] in notScrape:
                pass
            else:
                try:
                    url = 'https://www.bovada.lv/services/sports/event/coupon/events/A/description/' + str(
                        Value_get_dict[key.split('.')[1]]) + '?marketFilterId=' + key.split('.')[
                              -1] + '&preMatchOnly=true&eventsLimit=1000&lang=en'
                    yield scrapy.Request(url=url, callback=self.get_data,
                                         meta={'key': Value_get_dict[key.split('.')[1]], 'sub': jsondata[key],
                                               'matchType': 'PreMatch'})

                except:
                    pass

    def get_data(self, response):
        f = 4
        try:
            sports_data = json.loads(response.text)
            total_length = len(sports_data)
            for total_data in range(total_length):
                category = sports_data[total_data].get('path')[0].get('description')
                total_events = len(sports_data[total_data].get('events'))
                for event in range(total_events):
                    link_team = sports_data[total_data].get('events')[event].get('link')
                    yield scrapy.Request(
                        url="https://www.bovada.lv/services/sports/event/coupon/events/A/description" + link_team + "?lang=en",
                        callback=self.get_all_data)
        except:
            pass

    def get_all_data(self, response):
        dat = json.loads(response.text)
        team1spread = []
        team2spread = []
        total_over = []
        total_under = []
        team1halfspread = []
        team2halfspread = []
        try:
            len_display = len(dat[0].get("events")[0].get("displayGroups"))
        except:
            y = 4
        for data in range(len_display):
            typ = dat[0].get('events')[0].get("displayGroups")[data].get("description")
            dateTime = dat[0].get("events")[0].get("startTime")
            DateTime = str(datetime.fromtimestamp(dateTime / 1e3))
            time = DateTime[-8:]
            date = DateTime[:-8]
            tame = date + ' ' + time
            if str(future_date_after_1day) > tame:
                if "Game Lines" == typ:
                    item = dict()
                    mai = dict()
                    main_item = dict()
                    main_items = dict()
                    item['sportsbook_name'] = "bovada"
                    item['Game Title'] = response.url.split("description")[1].rsplit("/", -1)[1]
                    if "football" in item['Game Title']:
                        item['Game Title'] = "soccer"
                    # if item["Game Title"] == "Hockey":
                    #     k = 6
                    item['league'] = response.url.split("description")[1].rsplit("/", -1)[-2]
                    item["FirstTeam"] = unidecode(dat[0].get("events")[0].get("competitors")[0].get("name"))
                    if 'Liechtenstein' in item["FirstTeam"]:
                        f = 6
                    item["SecondTeam"] = unidecode(dat[0].get("events")[0].get("competitors")[1].get("name"))
                    item["Date"] = date
                    item["Time"] = time
                    if 'VFB Hallbergmoos' in item["FirstTeam"]:
                        d = 4
                    mark = len(dat[0].get('events')[0].get("displayGroups")[0].get("markets"))
                    for y in range(0, 6):
                        try:
                            desc = dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get("description")
                        except:
                            pass
                        try:
                            if "2P" in \
                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get("outcomes")[
                                        0].get("description") or "3P" in \
                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get("outcomes")[
                                        0].get("description"):
                                pass
                            elif "1Q" in \
                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get("outcomes")[
                                        0].get("description") or "2Q" in \
                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get("outcomes")[
                                        0].get("description"):
                                pass
                            elif "S2" in \
                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get("outcomes")[
                                        0].get("description"):
                                pass
                            else:
                                if "- " not in dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                        "outcomes")[0].get("description"):
                                    if "Goal Spread" == desc or "Runline" == desc or "Puck Line" == desc or "Game Spread" == desc or "Point Spread" == desc:
                                        p = 7
                                        if dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[0].get("price").get("handicap2") is None:
                                            if item["SecondTeam"] == \
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[0].get("description"):
                                                item["Team2spread"] = [
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[0].get("price").get("handicap") + "," +
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[0].get("price").get("american").replace(
                                                        "EVEN", "100")]
                                                item["Team1spread"] = [
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[1].get("price").get("handicap") + "," +
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[1].get("price").get("american").replace(
                                                        "EVEN", "100")]
                                            else:
                                                item["Team2spread"] = [
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[1].get("price").get("handicap") + "," +
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[1].get("price").get("american").replace(
                                                        "EVEN", "100")]
                                                item["Team1spread"] = [
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[0].get("price").get("handicap") + "," +
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[0].get("price").get("american").replace(
                                                        "EVEN", "100")]

                                        elif dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[0].get("price").get("handicap") is None:
                                            item["Team1spread"] = [
                                                dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                    "outcomes")[0].get("price").get("american").replace("EVEN", "100")]
                                        elif dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[0].get("price").get("handicap2") is not None:
                                            if item["SecondTeam"] == \
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[0].get("description"):
                                                item["Team2spread"] = [str((float(
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[0].get("price").get("handicap")) + float(
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[0].get("price").get(
                                                        "handicap2"))) / 2) + "," +
                                                                       dat[0].get('events')[0].get("displayGroups")[
                                                                           0].get("markets")[y].get("outcomes")[0].get(
                                                                           "price").get("american").replace("EVEN",
                                                                                                            "100")]
                                                item["Team1spread"] = [str((float(
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[1].get("price").get("handicap")) + float(
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[1].get("price").get(
                                                        "handicap2"))) / 2) + "," +
                                                                       dat[0].get('events')[0].get("displayGroups")[
                                                                           0].get("markets")[y].get("outcomes")[1].get(
                                                                           "price").get("american").replace("EVEN",
                                                                                                            "100")]
                                            else:
                                                item["Team2spread"] = [str((float(
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[1].get("price").get("handicap")) + float(
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[1].get("price").get(
                                                        "handicap2"))) / 2) + "," +
                                                                       dat[0].get('events')[0].get("displayGroups")[
                                                                           0].get("markets")[y].get("outcomes")[1].get(
                                                                           "price").get("american").replace("EVEN",
                                                                                                            "100")]
                                                item["Team1spread"] = [str((float(
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[0].get("price").get("handicap")) + float(
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[0].get("price").get(
                                                        "handicap2"))) / 2) + "," +
                                                                       dat[0].get('events')[0].get("displayGroups")[
                                                                           0].get("markets")[y].get("outcomes")[0].get(
                                                                           "price").get("american").replace("EVEN",
                                                                                                            "100")]
                                        if dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[1].get("price").get("handicap2") is None:
                                            if item["SecondTeam"] == \
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[0].get("description"):
                                                item["Team2spread"] = [
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[0].get("price").get("handicap") + "," +
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[0].get("price").get("american").replace(
                                                        "EVEN", "100")]
                                                item["Team1spread"] = [
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[1].get("price").get("handicap") + "," +
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[1].get("price").get("american").replace(
                                                        "EVEN", "100")]
                                            else:
                                                item["Team2spread"] = [
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[1].get("price").get("handicap") + "," +
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[1].get("price").get("american").replace(
                                                        "EVEN", "100")]
                                                item["Team1spread"] = [
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[0].get("price").get("handicap") + "," +
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[0].get("price").get("american").replace(
                                                        "EVEN", "100")]
                                        elif dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[1].get("price").get("handicap") is None:
                                            item["Team2spread"] = [
                                                dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                    "outcomes")[1].get("price").get("american").replace("EVEN", "100")]
                                        elif dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[1].get("price").get("handicap2") is not None:
                                            if item["SecondTeam"] == \
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[0].get("description"):
                                                item["Team2spread"] = [str((float(
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[1].get("price").get("handicap")) + float(
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[1].get("price").get(
                                                        "handicap2"))) / 2) + "," +
                                                                       dat[0].get('events')[0].get("displayGroups")[
                                                                           0].get("markets")[y].get("outcomes")[1].get(
                                                                           "price").get("american").replace("EVEN",
                                                                                                            "100")]
                                    elif "Total" == desc:
                                        if dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[0].get("price").get("handicap2") is None:
                                            item["total_over"] = [
                                                dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                    "outcomes")[0].get("price").get("handicap") + "," +
                                                dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                    "outcomes")[0].get("price").get("american").replace("EVEN", "100")]
                                        elif dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[0].get("price").get("handicap") is None:
                                            item["total_over"] = [
                                                dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                    "outcomes")[0].get("price").get("american").replace("EVEN", "100")]
                                        elif dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[0].get("price").get("handicap2") is not None:
                                            item["total_over"] = [str((float(
                                                dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                    "outcomes")[0].get("price").get("handicap")) + float(
                                                dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                    "outcomes")[0].get("price").get("handicap2"))) / 2) + "," +
                                                                  dat[0].get('events')[0].get("displayGroups")[0].get(
                                                                      "markets")[y].get("outcomes")[0].get("price").get(
                                                                      "american").replace("EVEN", "100")]
                                        if dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[1].get("price").get("handicap2") is None:
                                            item["total_under"] = [
                                                dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                    "outcomes")[1].get("price").get("handicap") + "," +
                                                dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                    "outcomes")[1].get("price").get("american").replace("EVEN", "100")]
                                        elif dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[1].get("price").get("handicap") is None:
                                            item["total_under"] = [
                                                dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                    "outcomes")[1].get("price").get("american").replace("EVEN", "100")]
                                        elif dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[1].get("price").get("handicap2") is not None:
                                            item["total_under"] = [str((float(
                                                dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                    "outcomes")[1].get("price").get("handicap")) + float(
                                                dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                    "outcomes")[1].get("price").get("handicap2"))) / 2) + "," +
                                                                   dat[0].get('events')[0].get("displayGroups")[0].get(
                                                                       "markets")[y].get("outcomes")[1].get(
                                                                       "price").get("american").replace("EVEN", "100")]
                                        t = 5
                                    elif '3-Way Moneyline' == desc or "Moneyline" == desc:
                                        if item["FirstTeam"] == \
                                                dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                        "outcomes")[0].get("description"):
                                            item["Team1money"] = \
                                            dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[0].get("price").get("american").replace("EVEN", "100")
                                            item["Team2money"] = \
                                            dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[1].get("price").get("american").replace("EVEN", "100")
                                        elif item["SecondTeam"] == \
                                                dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                        "outcomes")[0].get("description"):
                                            item["Team2money"] = \
                                            dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[0].get("price").get("american").replace("EVEN", "100")
                                            item["Team1money"] = \
                                            dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[1].get("price").get("american").replace("EVEN", "100")
                                        elif item["FirstTeam"] == \
                                                dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                        "outcomes")[1].get("description"):
                                            item["Team1money"] = \
                                            dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[1].get("price").get("american").replace("EVEN", "100")
                                            item["Team2money"] = \
                                            dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[0].get("price").get("american").replace("EVEN", "100")
                                        elif item["SecondTeam"] == \
                                                dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                        "outcomes")[1].get("description"):
                                            item["Team2money"] = \
                                            dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[1].get("price").get("american").replace("EVEN", "100")
                                            item["Team1money"] = \
                                            dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[0].get("price").get("american").replace("EVEN", "100")
                                        try:
                                            item["Draw"] = \
                                            dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[2].get("price").get("american").replace("EVEN", "100")
                                        except:
                                            item["Draw"] = ""
                                else:
                                    if "Goal Spread" == desc or "Runline" == desc or "Puck Line" == desc or "Game Spread" == desc or "Point Spread" == desc:
                                        p = 7
                                        if dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[0].get("price").get("handicap2") is None:
                                            if item["SecondTeam"] in \
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[0].get("description"):
                                                mai["Team2spread"] = [
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[0].get("price").get("handicap") + "," +
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[0].get("price").get("american").replace(
                                                        "EVEN", "100")]
                                                mai["Team1spread"] = [
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[1].get("price").get("handicap") + "," +
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[1].get("price").get("american").replace(
                                                        "EVEN", "100")]
                                            else:
                                                mai["Team2spread"] = [
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[1].get("price").get("handicap") + "," +
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[1].get("price").get("american").replace(
                                                        "EVEN", "100")]
                                                mai["Team1spread"] = [
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[0].get("price").get("handicap") + "," +
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[0].get("price").get("american").replace(
                                                        "EVEN", "100")]

                                        elif dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[0].get("price").get("handicap") is None:
                                            mai["Team1spread"] = [
                                                dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                    "outcomes")[0].get("price").get("american").replace("EVEN", "100")]
                                        elif dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[0].get("price").get("handicap2") is not None:
                                            mai["Team1spread"] = [str((float(
                                                dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                    "outcomes")[0].get("price").get("handicap")) + float(
                                                dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                    "outcomes")[0].get("price").get("handicap2"))) / 2) + "," +
                                                                  dat[0].get('events')[0].get("displayGroups")[0].get(
                                                                      "markets")[y].get("outcomes")[0].get("price").get(
                                                                      "american").replace("EVEN", "100")]
                                        if dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[1].get("price").get("handicap2") is None:
                                            if item["SecondTeam"] in \
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[0].get("description"):
                                                mai["Team2spread"] = [
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[0].get("price").get("handicap") + "," +
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[0].get("price").get("american").replace(
                                                        "EVEN", "100")]
                                                mai["Team1spread"] = [
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[1].get("price").get("handicap") + "," +
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[1].get("price").get("american").replace(
                                                        "EVEN", "100")]
                                            else:
                                                mai["Team2spread"] = [
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[1].get("price").get("handicap") + "," +
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[1].get("price").get("american").replace(
                                                        "EVEN", "100")]
                                                mai["Team1spread"] = [
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[0].get("price").get("handicap") + "," +
                                                    dat[0].get('events')[0].get("displayGroups")[0].get("markets")[
                                                        y].get("outcomes")[0].get("price").get("american").replace(
                                                        "EVEN", "100")]


                                        elif dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[1].get("price").get("handicap") is None:
                                            mai["Team2spread"] = [
                                                dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                    "outcomes")[1].get("price").get("american").replace("EVEN", "100")]
                                        elif dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[1].get("price").get("handicap2") is not None:
                                            mai["Team2spread"] = [str((float(
                                                dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                    "outcomes")[1].get("price").get("handicap")) + float(
                                                dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                    "outcomes")[1].get("price").get("handicap2"))) / 2) + "," +
                                                                  dat[0].get('events')[0].get("displayGroups")[0].get(
                                                                      "markets")[y].get("outcomes")[1].get("price").get(
                                                                      "american").replace("EVEN", "100")]
                                    elif "Total" == desc:
                                        if dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[0].get("price").get("handicap2") is None:
                                            mai["total_over"] = [
                                                dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                    "outcomes")[0].get("price").get("handicap") + "," +
                                                dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                    "outcomes")[0].get("price").get("american").replace("EVEN", "100")]
                                        elif dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[0].get("price").get("handicap") is None:
                                            mai["total_over"] = [
                                                dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                    "outcomes")[0].get("price").get("american").replace("EVEN", "100")]
                                        elif dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[0].get("price").get("handicap2") is not None:
                                            mai["total_over"] = [str((float(
                                                dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                    "outcomes")[0].get("price").get("handicap")) + float(
                                                dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                    "outcomes")[0].get("price").get("handicap2"))) / 2) + "," +
                                                                 dat[0].get('events')[0].get("displayGroups")[0].get(
                                                                     "markets")[y].get("outcomes")[0].get("price").get(
                                                                     "american").replace("EVEN", "100")]
                                        if dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[1].get("price").get("handicap2") is None:
                                            mai["total_under"] = [
                                                dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                    "outcomes")[1].get("price").get("handicap") + "," +
                                                dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                    "outcomes")[1].get("price").get("american").replace("EVEN", "100")]
                                        elif dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[1].get("price").get("handicap") is None:
                                            mai["total_under"] = [
                                                dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                    "outcomes")[1].get("price").get("american").replace("EVEN", "100")]
                                        elif dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[1].get("price").get("handicap2") is not None:
                                            mai["total_under"] = [str((float(
                                                dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                    "outcomes")[1].get("price").get("handicap")) + float(
                                                dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                    "outcomes")[1].get("price").get("handicap2"))) / 2) + "," +
                                                                  dat[0].get('events')[0].get("displayGroups")[0].get(
                                                                      "markets")[y].get("outcomes")[1].get("price").get(
                                                                      "american").replace("EVEN", "100")]
                                    elif '3-Way Moneyline' == desc or "Moneyline" == desc:
                                        if item["FirstTeam"] in \
                                                dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                        "outcomes")[0].get("description"):
                                            mai["Team1money"] = \
                                            dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[0].get("price").get("american").replace("EVEN", "100")
                                            mai["Team2money"] = \
                                            dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[1].get("price").get("american").replace("EVEN", "100")
                                        elif item["SecondTeam"] in \
                                                dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                        "outcomes")[0].get("description"):
                                            mai["Team2money"] = \
                                            dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[0].get("price").get("american").replace("EVEN", "100")
                                            mai["Team1money"] = \
                                            dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[1].get("price").get("american").replace("EVEN", "100")
                                        elif item["FirstTeam"] in \
                                                dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                        "outcomes")[1].get("description"):
                                            mai["Team1money"] = \
                                            dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[1].get("price").get("american").replace("EVEN", "100")
                                            mai["Team2money"] = \
                                            dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[0].get("price").get("american").replace("EVEN", "100")
                                        elif item["SecondTeam"] in \
                                                dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                        "outcomes")[1].get("description"):
                                            mai["Team2money"] = \
                                            dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[1].get("price").get("american").replace("EVEN", "100")
                                            mai["Team1money"] = \
                                            dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[0].get("price").get("american").replace("EVEN", "100")
                                        try:
                                            mai["Draw"] = \
                                            dat[0].get('events')[0].get("displayGroups")[0].get("markets")[y].get(
                                                "outcomes")[2].get("price").get("american").replace("EVEN", "100")
                                        except:
                                            mai["Draw"] = ""
                        except:
                            if "total_over" and "total_under" not in item:
                                item["total_over"] = ""
                                item["total_under"] = ""
                            elif "Team1spread" and "Team2spread" not in item:
                                item["Team1spread"] = ""
                                item["Team2spread"] = ""
                            elif "Team1money" and "Team2money" not in item:
                                item["Team1money"] = ""
                                item["Team2money"] = ""
                            elif "Draw" not in item:
                                item["Draw"] = ""
                                q = 7

                    if item != {}:
                        main_item["constant_data"] = item
                        allitems.append(main_item)
                    if mai == {}:
                        pass
                    else:
                        if len(mai) != 7:
                            if "total_over" and "total_under" not in mai:
                                mai["total_over"] = ""
                                mai["total_under"] = ""
                            if "Team1spread" and "Team2spread" not in mai:
                                mai["Team1spread"] = ""
                                mai["Team2spread"] = ""
                            if "Team1money" and "Team2money" not in mai:
                                mai["Team1money"] = ""
                                mai["Team2money"] = ""
                            if "Draw" not in mai:
                                mai["Draw"] = ""

                        if mai != {}:
                            main_items["1st Half"] = mai
                            main_item.update(main_items)
                elif "Alternate Lines" == typ or "Total Games" == typ or "Game Spreads" == typ:

                    if "Game Spreads" == typ:
                        a = 9

                    alternate_mark = len(dat[0].get("events")[0].get("displayGroups")[data].get("markets"))
                    for x in range(alternate_mark):
                        types = dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get("description")
                        lek = len(dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get("outcomes"))
                        for b in range(lek):
                            try:
                                if "Spread" in types and "- 1" not in \
                                        dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("description") and (
                                        item['Game Title'] == "soccer" or item['Game Title'] == "baseball" or item[
                                    'Game Title'] == "basketball" or item['Game Title'] == "hockey"):
                                    if item["FirstTeam"] == \
                                            dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                    "outcomes")[b].get("description"):
                                        if dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap2") is None:
                                            hand1american = \
                                            dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap") + "," + \
                                            dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("american").replace("EVEN", "100")
                                            team1spread.append(hand1american)
                                        elif dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap") is None:
                                            hand1american = \
                                            dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("american").replace("EVEN", "100")
                                            team1spread.append(hand1american)
                                        elif dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap2") is not None:
                                            f = 6
                                            hand1american = str((float(
                                                dat[0].get("events")[0].get("displayGroups")[data].get("markets")[
                                                    x].get("outcomes")[b].get("price").get("handicap")) + float(
                                                dat[0].get("events")[0].get("displayGroups")[data].get("markets")[
                                                    x].get("outcomes")[b].get("price").get("handicap2"))) / 2) + "," + \
                                                            dat[0].get("events")[0].get("displayGroups")[data].get(
                                                                "markets")[x].get("outcomes")[b].get("price").get(
                                                                "american").replace("EVEN", "100")
                                            team1spread.append(hand1american)
                                    else:
                                        if dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap2") is None:
                                            hand2american = \
                                            dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap") + "," + \
                                            dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("american").replace("EVEN", "100")
                                            team2spread.append(hand2american)
                                        elif dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap") is None:
                                            hand2american = \
                                            dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("american").replace("EVEN", "100")
                                            team2spread.append(hand2american)
                                        elif dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap2") is not None:
                                            f = 6
                                            hand2american = str((float(
                                                dat[0].get("events")[0].get("displayGroups")[data].get("markets")[
                                                    x].get("outcomes")[b].get("price").get("handicap")) + float(
                                                dat[0].get("events")[0].get("displayGroups")[data].get("markets")[
                                                    x].get("outcomes")[b].get("price").get("handicap2"))) / 2) + "," + \
                                                            dat[0].get("events")[0].get("displayGroups")[data].get(
                                                                "markets")[x].get("outcomes")[b].get("price").get(
                                                                "american").replace("EVEN", "100")
                                            team2spread.append(hand2american)
                                elif "Spread" in types and "- 1" in \
                                        dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("description") and (
                                        item['Game Title'] == "soccer" or item['Game Title'] == "baseball" or item[
                                    'Game Title'] == "basketball" or item['Game Title'] == "hockey"):
                                    if item["FirstTeam"] in \
                                            dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                    "outcomes")[b].get("description"):
                                        if dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap2") is None:
                                            hand3american = \
                                            dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap") + "," + \
                                            dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("american").replace("EVEN", "100")
                                            team1halfspread.append(hand3american)
                                        elif dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap") is None:
                                            hand3american = \
                                            dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("american").replace("EVEN", "100")
                                            team1halfspread.append(hand3american)
                                        elif dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap2") is not None:
                                            f = 6
                                            hand3american = str((float(
                                                dat[0].get("events")[0].get("displayGroups")[data].get("markets")[
                                                    x].get("outcomes")[b].get("price").get("handicap")) + float(
                                                dat[0].get("events")[0].get("displayGroups")[data].get("markets")[
                                                    x].get("outcomes")[b].get("price").get("handicap2"))) / 2) + "," + \
                                                            dat[0].get("events")[0].get("displayGroups")[data].get(
                                                                "markets")[x].get("outcomes")[b].get("price").get(
                                                                "american").replace("EVEN", "100")
                                            team1halfspread.append(hand3american)
                                    else:
                                        if dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap2") is None:
                                            hand4american = \
                                            dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap") + "," + \
                                            dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("american").replace("EVEN", "100")
                                            team2halfspread.append(hand4american)
                                        elif dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap") is None:
                                            hand4american = \
                                            dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("american").replace("EVEN", "100")
                                            team2halfspread.append(hand4american)
                                        elif dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap2") is not None:
                                            f = 6
                                            hand4american = str((float(
                                                dat[0].get("events")[0].get("displayGroups")[data].get("markets")[
                                                    x].get("outcomes")[b].get("price").get("handicap")) + float(
                                                dat[0].get("events")[0].get("displayGroups")[data].get("markets")[
                                                    x].get("outcomes")[b].get("price").get("handicap2"))) / 2) + "," + \
                                                            dat[0].get("events")[0].get("displayGroups")[data].get(
                                                                "markets")[x].get("outcomes")[b].get("price").get(
                                                                "american").replace("EVEN", "100")
                                            team2halfspread.append(hand4american)
                                elif "Spread" in types and "- S" not in \
                                        dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("description") and item['Game Title'] == "tennis":
                                    if item["FirstTeam"] == \
                                            dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                    "outcomes")[b].get("description"):
                                        if dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap2") is None:
                                            hand1american = \
                                            dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap") + "," + \
                                            dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("american").replace("EVEN", "100")
                                            team1spread.append(hand1american)
                                        elif dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap") is None:
                                            hand1american = \
                                            dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("american").replace("EVEN", "100")
                                            team1spread.append(hand1american)
                                        elif dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap2") is not None:
                                            f = 6
                                            hand1american = str((float(
                                                dat[0].get("events")[0].get("displayGroups")[data].get("markets")[
                                                    x].get("outcomes")[b].get("price").get("handicap")) + float(
                                                dat[0].get("events")[0].get("displayGroups")[data].get("markets")[
                                                    x].get("outcomes")[b].get("price").get("handicap2"))) / 2) + "," + \
                                                            dat[0].get("events")[0].get("displayGroups")[data].get(
                                                                "markets")[x].get("outcomes")[b].get("price").get(
                                                                "american").replace("EVEN", "100")
                                            team1spread.append(hand1american)
                                    else:
                                        if dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap2") is None:
                                            hand2american = \
                                            dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap") + "," + \
                                            dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("american").replace("EVEN", "100")
                                            team2spread.append(hand2american)
                                        elif dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap") is None:
                                            hand2american = \
                                            dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("american").replace("EVEN", "100")
                                            team2spread.append(hand2american)
                                        elif dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap2") is not None:
                                            f = 6
                                            hand2american = str((float(
                                                dat[0].get("events")[0].get("displayGroups")[data].get("markets")[
                                                    x].get("outcomes")[b].get("price").get("handicap")) + float(
                                                dat[0].get("events")[0].get("displayGroups")[data].get("markets")[
                                                    x].get("outcomes")[b].get("price").get("handicap2"))) / 2) + "," + \
                                                            dat[0].get("events")[0].get("displayGroups")[data].get(
                                                                "markets")[x].get("outcomes")[b].get("price").get(
                                                                "american").replace("EVEN", "100")
                                            team2spread.append(hand2american)
                                elif "Spread" in types and "- S1" in \
                                        dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("description"):
                                    if item["FirstTeam"] in \
                                            dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                    "outcomes")[b].get("description"):
                                        if dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap2") is None:
                                            hand3american = \
                                            dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap") + "," + \
                                            dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("american").replace("EVEN", "100")
                                            team1halfspread.append(hand3american)
                                        elif dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap") is None:
                                            hand3american = \
                                            dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("american").replace("EVEN", "100")
                                            team1halfspread.append(hand3american)
                                        elif dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap2") is not None:
                                            f = 6
                                            hand3american = str((float(
                                                dat[0].get("events")[0].get("displayGroups")[data].get("markets")[
                                                    x].get("outcomes")[b].get("price").get("handicap")) + float(
                                                dat[0].get("events")[0].get("displayGroups")[data].get("markets")[
                                                    x].get("outcomes")[b].get("price").get("handicap2"))) / 2) + "," + \
                                                            dat[0].get("events")[0].get("displayGroups")[data].get(
                                                                "markets")[x].get("outcomes")[b].get("price").get(
                                                                "american").replace("EVEN", "100")
                                            team1halfspread.append(hand3american)
                                    else:
                                        if dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap2") is None:
                                            hand4american = \
                                            dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap") + "," + \
                                            dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("american").replace("EVEN", "100")
                                            team2halfspread.append(hand4american)
                                        elif dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap") is None:
                                            hand4american = \
                                            dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("american").replace("EVEN", "100")
                                            team2halfspread.append(hand4american)
                                        elif dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap2") is not None:
                                            f = 6
                                            hand4american = str((float(
                                                dat[0].get("events")[0].get("displayGroups")[data].get("markets")[
                                                    x].get("outcomes")[b].get("price").get("handicap")) + float(
                                                dat[0].get("events")[0].get("displayGroups")[data].get("markets")[
                                                    x].get("outcomes")[b].get("price").get("handicap2"))) / 2) + "," + \
                                                            dat[0].get("events")[0].get("displayGroups")[data].get(
                                                                "markets")[x].get("outcomes")[b].get("price").get(
                                                                "american").replace("EVEN", "100")
                                            team2halfspread.append(hand4american)
                                elif 'Total Goals O/U' == types or "Alternate Total Games" == types or "Total Points O/U" == types or "Total Runs O/U" == types:
                                    if "Over" == \
                                            dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                    "outcomes")[b].get("description"):
                                        if dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap2") is None:
                                            hand5american = \
                                            dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap") + "," + \
                                            dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("american").replace("EVEN", "100")
                                            total_over.append(hand5american)
                                        elif dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap") is None:
                                            hand5american = \
                                            dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("american").replace("EVEN", "100")
                                            total_over.append(hand5american)
                                        elif dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap2") is not None:
                                            f = 6
                                            hand5american = str((float(
                                                dat[0].get("events")[0].get("displayGroups")[data].get("markets")[
                                                    x].get("outcomes")[b].get("price").get("handicap")) + float(
                                                dat[0].get("events")[0].get("displayGroups")[data].get("markets")[
                                                    x].get("outcomes")[b].get("price").get("handicap2"))) / 2) + "," + \
                                                            dat[0].get("events")[0].get("displayGroups")[data].get(
                                                                "markets")[x].get("outcomes")[b].get("price").get(
                                                                "american").replace("EVEN", "100")
                                            total_over.append(hand5american)
                                    elif "Under" == \
                                            dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                    "outcomes")[b].get("description"):
                                        if dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap2") is None:
                                            hand6american = \
                                            dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap") + "," + \
                                            dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("american").replace("EVEN", "100")
                                            total_under.append(hand6american)
                                        elif dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap") is None:
                                            hand6american = \
                                            dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("american").replace("EVEN", "100")
                                            total_under.append(hand6american)
                                        elif dat[0].get("events")[0].get("displayGroups")[data].get("markets")[x].get(
                                                "outcomes")[b].get("price").get("handicap2") is not None:
                                            f = 6
                                            hand6american = str((float(
                                                dat[0].get("events")[0].get("displayGroups")[data].get("markets")[
                                                    x].get("outcomes")[b].get("price").get("handicap")) + float(
                                                dat[0].get("events")[0].get("displayGroups")[data].get("markets")[
                                                    x].get("outcomes")[b].get("price").get("handicap2"))) / 2) + "," + \
                                                            dat[0].get("events")[0].get("displayGroups")[data].get(
                                                                "markets")[x].get("outcomes")[b].get("price").get(
                                                                "american").replace("EVEN", "100")
                                            total_under.append(hand6american)

                            except:
                                k = 6
        for alldata in allitems:
            gh = len(dat[0].get("events")[0].get("displayGroups")[0].get("markets"))
            for mart in range(gh):
                try:
                    if alldata["constant_data"]["FirstTeam"] == \
                            dat[0].get("events")[0].get("displayGroups")[0].get("markets")[mart].get("outcomes")[0].get(
                                    "description") and alldata["constant_data"]["SecondTeam"] == \
                            dat[0].get("events")[0].get("displayGroups")[0].get("markets")[mart].get("outcomes")[1].get(
                                    "description"):
                        try:
                            alldata["constant_data"]["Team1spread"].extend(team1spread)
                        except:
                            pass
                        try:

                            alldata["constant_data"]["Team2spread"].extend(team2spread)
                        except:
                            pass
                        if mai == {}:
                            pass
                        else:
                            try:
                                alldata["1st Half"]["Team1spread"].extend(team1halfspread)
                            except:
                                pass
                            try:
                                alldata["1st Half"]["Team2spread"].extend(team2halfspread)
                            except:
                                pass
                            try:
                                alldata["constant_data"]["total_over"].extend(total_over)
                            except:
                                pass
                            try:
                                alldata["constant_data"]["total_under"].extend(total_under)
                            except:
                                pass
                        break
                    elif alldata["constant_data"]["FirstTeam"] == \
                            dat[0].get("events")[0].get("displayGroups")[0].get("markets")[mart].get("outcomes")[1].get(
                                    "description") and alldata["constant_data"]["SecondTeam"] == \
                            dat[0].get("events")[0].get("displayGroups")[0].get("markets")[mart].get("outcomes")[0].get(
                                    "description"):
                        try:
                            alldata["constant_data"]["Team1spread"].extend(team1spread)
                        except:
                            pass
                        try:
                            alldata["constant_data"]["Team2spread"].extend(team2spread)
                        except:
                            pass
                        if mai == {}:
                            pass
                        else:
                            try:
                                alldata["1st Half"]["Team1spread"].extend(team1halfspread)
                            except:
                                pass
                            try:
                                alldata["1st Half"]["Team2spread"].extend(team2halfspread)
                            except:
                                pass
                            try:
                                alldata["constant_data"]["total_over"].extend(total_over)
                            except:
                                pass
                            try:
                                alldata["constant_data"]["total_under"].extend(total_under)
                            except:
                                pass
                        break
                except:
                    pass

    def close(self, spider):
        items_json_str = json.dumps(allitems, indent=4)
        fileout.write(items_json_str)


process = CrawlerProcess({})
process.crawl(Bovadas)
process.start()
