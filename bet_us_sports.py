from datetime import *
import datefinder
import time
from datetime import timedelta, datetime
from scrapy.crawler import CrawlerProcess
import scrapy
import unidecode
import json
from threading import Thread
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as ff_options

file_json = open('bet_us_sports.json', 'w')
to_Scrape = [ 'Soccer',]
allitems = []

ini_time_for_now = datetime.now()
future_date_after_1day = ini_time_for_now + \
                         timedelta(days=1)


def get_all_data(response):
    try:
        if response.css('.game-tbl.row') != []:
            item = dict()
            game_type = response.css('#periods-tabs .selected::text').get()

            for li in response.css('.game-block'):
                for data in li.css('.normal'):
                    item['league'] = response.css('.game-block #top-name-league span::text').get()

                    firstTeam = data.css('.game-tbl.row .visitor span#awayName a::text').get()
                    if firstTeam is None:
                        item['FirstTeam'] = data.css('.game-tbl.row .visitor span#awayName::text').get().strip()
                    else:
                        item['FirstTeam'] = firstTeam

                    for i, data_ in enumerate(data.css('.game-tbl.row .visitor .line-container')):
                        if i == 0:
                            try:
                                item['Team1spread'] = data_.css('span::text').get().replace(' ', ' , ').replace(
                                    '\u00bd ',
                                    '.5 ')
                            except:
                                item['Team1spread'] = ''
                        elif i == 1:
                            try:
                                item['Team1money'] = data_.css('span::text').get().strip()
                                if '' == item['Team1money']:

                                    try:
                                        temp1total = data.css('.game-tbl.row .visitor .line-container span::text')[
                                            2].get().strip()
                                        temp2total = data.css('.game-tbl.row .visitor .line-container span::text')[
                                            3].get().strip()
                                        item['total_over'] = temp1total + ' , ' + temp2total
                                        item['total_over'] = item['total_over'].replace('\u00bd ', '.5').replace('o',
                                                                                                                 '').replace(
                                            'u', '')
                                    except:
                                        item['total_over'] = ''
                                else:
                                    try:
                                        temp1total = data.css('.game-tbl.row .visitor .line-container span::text')[
                                            3].get().strip()
                                        temp2total = data.css('.game-tbl.row .visitor .line-container span::text')[
                                            4].get().strip()
                                        item['total_over'] = temp1total + ' , ' + temp2total
                                        item['total_over'] = item['total_over'].replace('\u00bd ', '.5').replace('o',
                                                                                                                 '').replace(
                                            'u', '')
                                    except:
                                        try:
                                            temp1total = data.css('.game-tbl.row .visitor .line-container span::text')[
                                                1].get().strip()
                                            temp2total = data.css('.game-tbl.row .visitor .line-container span::text')[
                                                2].get().strip()
                                            item['total_over'] = temp1total + ' , ' + temp2total
                                            item['total_over'] = item['total_over'].replace('\u00bd ', '.5').replace(
                                                'o',
                                                '').replace(
                                                'u', '')
                                        except:
                                            item['total_over'] = ''

                            except:
                                item['Team1money'] = ''
                                try:
                                    temp1total = data.css('.game-tbl.row .visitor .line-container span::text')[
                                        2].get().strip()
                                    temp2total = data.css('.game-tbl.row .visitor .line-container span::text')[
                                        3].get().strip()
                                    item['total_over'] = temp1total + ' , ' + temp2total
                                    item['total_over'] = item['total_over'].replace('\u00bd ', '.5').replace('o',
                                                                                                             '').replace(
                                        'u', '')

                                except:
                                    try:
                                        temp1total = data.css('.game-tbl.row .visitor .line-container span::text')[
                                            3].get().strip()
                                        temp2total = data.css('.game-tbl.row .visitor .line-container span::text')[
                                            4].get().strip()
                                        item['total_over'] = temp1total + ' , ' + temp2total
                                        item['total_over'] = item['total_over'].replace('\u00bd ', '.5').replace('o',
                                                                                                                 '').replace(
                                            'u', '')
                                    except:
                                        try:
                                            temp1total = data.css('.game-tbl.row .visitor .line-container span::text')[
                                                1].get().strip()
                                            temp2total = data.css('.game-tbl.row .visitor .line-container span::text')[
                                                2].get().strip()
                                            item['total_over'] = temp1total + ' , ' + temp2total
                                            item['total_over'] = item['total_over'].replace('\u00bd ', '.5').replace(
                                                'o',
                                                '').replace(
                                                'u', '')
                                        except:
                                            item['total_over'] = ''

                    try:
                        team1temp1Total = data.css('.game-tbl.row .visitor .line-container-teamtotal span::text')[
                            1].get().strip()
                        team1temp2Total = data.css('.game-tbl.row .visitor .line-container-teamtotal span::text')[
                            2].get().strip()
                        team1temp3Total = data.css('.game-tbl.row .visitor .line-container-teamtotal span::text')[
                            4].get().strip()
                        team1temp4Total = data.css('.game-tbl.row .visitor .line-container-teamtotal span::text')[
                            5].get().strip()
                        tempV1 = team1temp1Total + ' , ' + team1temp2Total
                        tempV2 = team1temp3Total + ' , ' + team1temp4Total
                        item['Team1TotalPoints'] = tempV1.replace('\u00bd ', '.5').replace('o', '').replace('u',
                                                                                                            '') + ' , ' + tempV2.replace(
                            '\u00bd ', '.5').replace('o', '').replace('u', '')
                    except:
                        item['Team1TotalPoints'] = ''
                    secondteam = data.css('.game-tbl.row .home span#homeName a::text').get()
                    if secondteam is None:
                        item['SecondTeam'] = data.css('.game-tbl.row .home span#homeName::text').get().strip()
                    else:
                        item['SecondTeam'] = secondteam
                    for j, data_1 in enumerate(data.css('.game-tbl.row .home .line-container')):
                        if j == 0:
                            try:
                                item['Team2spread'] = data_1.css('span::text').get().replace(' ', ' , ').replace(
                                    '\u00bd ', '.5 ')
                            except:
                                item['Team2spread'] = ''
                        elif j == 1:
                            try:
                                item['Team2money'] = data_1.css('span::text').get().strip()
                                if '' == item['Team2money']:
                                    try:
                                        temp1total2 = data.css('.game-tbl.row .home .line-container span::text')[
                                            2].get().strip()
                                        temp2total2 = data.css('.game-tbl.row .home .line-container span::text')[
                                            3].get().strip()
                                        item['total_under'] = temp1total2.replace('o', '').replace('u', '').replace(
                                            '\u00bd ', '.5') + ' , ' + temp2total2.replace('o', '').replace('u',
                                                                                                            '').replace(
                                            '\u00bd ', '.5')
                                    except:
                                        item['total_under'] = ''
                                else:
                                    try:
                                        temp1total2 = data.css('.game-tbl.row .home .line-container span::text')[
                                            3].get().strip()
                                        temp2total2 = data.css('.game-tbl.row .home .line-container span::text')[
                                            4].get().strip()
                                        item['total_under'] = temp1total2 + ' , ' + temp2total2
                                        item['total_under'] = item['total_under'].replace('\u00bd ', '.5').replace(
                                            'o', '').replace('u', '')
                                    except:
                                        try:

                                            temp1total2 = \
                                                data.css('.game-tbl.row .home .line-container span::text')[
                                                    1].get().strip()
                                            temp2total2 = \
                                                data.css('.game-tbl.row .home .line-container span::text')[
                                                    2].get().strip()
                                            item['total_under'] = temp1total2 + ' , ' + temp2total2
                                            item['total_under'] = item['total_under'].replace('\u00bd ',
                                                                                              '.5').replace('o',
                                                                                                            '').replace(
                                                'u', '')
                                        except:

                                            item['total_under'] = ''
                            except:
                                item['Team2money'] = ''
                                try:
                                    temp1total2 = data.css('.game-tbl.row .home .line-container span::text')[
                                        2].get().strip()
                                    temp2total2 = data.css('.game-tbl.row .home .line-container span::text')[
                                        3].get().strip()
                                    item['total_under'] = temp1total2 + ' , ' + temp2total2
                                    item['total_under'] = item['total_under'].replace('\u00bd ', '.5').replace('o',
                                                                                                               '').replace(
                                        'u', '')
                                except:
                                    try:
                                        temp1total2 = data.css('.game-tbl.row .home .line-container span::text')[
                                            3].get().strip()
                                        temp2total2 = data.css('.game-tbl.row .home .line-container span::text')[
                                            4].get().strip()
                                        item['total_under'] = temp1total2 + ' , ' + temp2total2
                                        item['total_under'] = item['total_under'].replace('\u00bd ', '.5').replace('o',
                                                                                                                   '').replace(
                                            'u', '')
                                    except:
                                        try:

                                            temp1total2 = \
                                                data.css('.game-tbl.row .home .line-container span::text')[
                                                    1].get().strip()
                                            temp2total2 = \
                                                data.css('.game-tbl.row .home .line-container span::text')[
                                                    2].get().strip()
                                            item['total_under'] = temp1total2 + ' , ' + temp2total2
                                            item['total_under'] = item['total_under'].replace('\u00bd ',
                                                                                              '.5').replace('o',
                                                                                                            '').replace(
                                                'u', '')
                                        except:

                                            item['total_under'] = ''


                    try:
                        team2temp1Total = data.css('.game-tbl.row .home .line-container-teamtotal span::text')[
                            1].get().strip()
                        team2temp2Total = data.css('.game-tbl.row .home .line-container-teamtotal span::text')[
                            2].get().strip()
                        team2temp3Total = data.css('.game-tbl.row .home .line-container-teamtotal span::text')[
                            4].get().strip()
                        team2temp4Total = data.css('.game-tbl.row .home .line-container-teamtotal span::text')[
                            5].get().strip()
                        temp2V1 = team2temp1Total + ' , ' + team2temp2Total
                        temp2V2 = team2temp3Total + ' , ' + team2temp4Total
                        item['Team2TotalPoints'] = temp2V1.replace('\u00bd ', '.5').replace('o', '').replace('u',
                                                                                                             '') + ' , ' + temp2V2.replace(
                            '\u00bd ', '.5').replace('o', '').replace('u', '')
                    except:
                        item['Team2TotalPoints'] = ''
                    draw = data.css('.draw .line-container span::text').get()
                    if draw is None:
                        item['Draw'] = ''
                    else:
                        item['Draw'] = draw
                    if game_type == '1st H' or '1st 5' in game_type:
                        half_data = dict()
                        for alldata in allitems:
                            if alldata['constant_data']['FirstTeam'] == item['FirstTeam'] and alldata['constant_data'][
                                'SecondTeam'] == item['SecondTeam']:
                                half_data['Team1spread'] = item['Team1spread']
                                half_data['Team2spread'] = item['Team2spread']
                                half_data['Team1money'] = item['Team1money']
                                half_data['Team2money'] = item['Team2money']
                                half_data['total_over'] = item['total_over']
                                half_data['total_under'] = item['total_under']
                                half_data['Draw'] = item['Draw']

                                alldata['1st Half'] = half_data
                    elif game_type == '2nd H':
                        half_data2 = dict()
                        for alldata in allitems:
                            if alldata['constant_data']['FirstTeam'] == item['FirstTeam'] and alldata['constant_data'][
                                'SecondTeam'] == item['SecondTeam']:
                                half_data2['Team1spread'] = item['Team1spread']
                                half_data2['Team2spread'] = item['Team2spread']
                                half_data2['Team1money'] = item['Team1money']
                                half_data2['Team2money'] = item['Team2money']
                                half_data2['total_over'] = item['total_over']
                                half_data2['total_under'] = item['total_under']
                                half_data2['Draw'] = item['Draw']

                                alldata['2nd Half'] = half_data2
                    elif game_type == 'Alt 1':
                        for alldata in allitems:
                            if alldata['constant_data']['FirstTeam'] == item['FirstTeam'] and alldata['constant_data'][
                                'SecondTeam'] == item['SecondTeam']:
                                if item['Team1spread'] == '':
                                    pass
                                else:

                                    tem1 =  [alldata['constant_data']['Team1spread']]
                                    tem1.append(item['Team1spread'])
                                    alldata['constant_data']['Team1spread'] = tem1

                                    tem2 = [alldata['constant_data']['Team2spread']]
                                    tem2.append(item['Team2spread'])
                                    alldata['constant_data']['Team2spread'] = tem2
                                if item['total_over'] =='':
                                    pass

                                else:
                                    tot1 = [alldata['constant_data']['total_over']]
                                    tot1.append(item['total_over'])
                                    alldata['constant_data']['total_over'] = tot1

                                    tot2 = [alldata['constant_data']['total_under']]
                                    tot2.append(item['total_under'])
                                    alldata['constant_data']['total_under'] = tot2


                    elif game_type == 'Alt 2':
                        for alldata in allitems:
                            if alldata['constant_data']['FirstTeam'] == item['FirstTeam'] and alldata['constant_data'][
                                'SecondTeam'] == item['SecondTeam']:
                                if item['Team1spread'] == '':
                                    pass
                                else:

                                    alldata['constant_data']['Team1spread'].append(item['Team1spread'])
                                    alldata['constant_data']['Team2spread'].append(item['Team2spread'])
                                if item['total_over'] == '':
                                    pass

                                else:
                                    alldata['constant_data']['total_over'].append(item['total_over'])
                                    alldata['constant_data']['total_under'].append(item['total_under'])

                    elif game_type == '1st Set':
                        half_set = dict()
                        for alldata in allitems:
                            if alldata['constant_data']['FirstTeam'] == item['FirstTeam'] and alldata['constant_data'][
                                'SecondTeam'] == item['SecondTeam']:
                                half_set['Team1spread'] = item['Team1spread']
                                half_set['Team2spread'] = item['Team2spread']
                                half_set['Team1money'] = item['Team1money']
                                half_set['Team2money'] = item['Team2money']
                                half_set['total_over'] = item['total_over']
                                half_set['total_under'] = item['total_under']
                                alldata['1st Half'] = half_set

                    elif game_type == '1st P':
                        half_p = dict()
                        for alldata in allitems:
                            if alldata['constant_data']['FirstTeam'] == item['FirstTeam'] and alldata['constant_data'][
                                'SecondTeam'] == item['SecondTeam']:
                                half_p['Team1spread'] = item['Team1spread']
                                half_p['Team2spread'] = item['Team2spread']
                                half_p['Team1money'] = item['Team1money']
                                half_p['Team2money'] = item['Team2money']
                                half_p['total_over'] = item['total_over']
                                half_p['total_under'] = item['total_under']
                                alldata['1st Half'] = half_p
                    elif game_type == '1st Q':
                        half_q = dict()
                        for alldata in allitems:
                            if alldata['constant_data']['FirstTeam'] == item['FirstTeam'] and alldata['constant_data'][
                                'SecondTeam'] == item['SecondTeam']:
                                half_q['Team1spread'] = item['Team1spread']
                                half_q['Team2spread'] = item['Team2spread']
                                half_q['Team1money'] = item['Team1money']
                                half_q['Team2money'] = item['Team2money']
                                half_q['total_over'] = item['total_over']
                                half_q['total_under'] = item['total_under']
                                alldata['1st Quarter'] = half_q
                    elif game_type == '2nd Q':
                        half_q2 = dict()
                        for alldata in allitems:
                            if alldata['constant_data']['FirstTeam'] == item['FirstTeam'] and alldata['constant_data'][
                                'SecondTeam'] == item['SecondTeam']:
                                half_q2['Team1spread'] = item['Team1spread']
                                half_q2['Team2spread'] = item['Team2spread']
                                half_q2['Team1money'] = item['Team1money']
                                half_q2['Team2money'] = item['Team2money']
                                half_q2['total_over'] = item['total_over']
                                half_q2['total_under'] = item['total_under']
                                alldata['2nd Quarter'] = half_q2
                    elif game_type == '3rd Q':
                        half_q3 = dict()
                        for alldata in allitems:
                            if alldata['constant_data']['FirstTeam'] == item['FirstTeam'] and alldata['constant_data'][
                                'SecondTeam'] == item['SecondTeam']:
                                half_q3['Team1spread'] = item['Team1spread']
                                half_q3['Team2spread'] = item['Team2spread']
                                half_q3['Team1money'] = item['Team1money']
                                half_q3['Team2money'] = item['Team2money']
                                half_q3['total_over'] = item['total_over']
                                half_q3['total_under'] = item['total_under']
                                alldata['3rd Quarter'] = half_q3
                    elif game_type == '4th Q':
                        half_q4 = dict()
                        for alldata in allitems:
                            if alldata['constant_data']['FirstTeam'] == item['FirstTeam'] and alldata['constant_data'][
                                'SecondTeam'] == item['SecondTeam']:
                                half_q4['Team1spread'] = item['Team1spread']
                                half_q4['Team2spread'] = item['Team2spread']
                                half_q4['Team1money'] = item['Team1money']
                                half_q4['Team2money'] = item['Team2money']
                                half_q4['total_over'] = item['total_over']
                                half_q4['total_under'] = item['total_under']
                                alldata['4th Quarter'] = half_q4



                    else:
                        for alldata in allitems:
                            variable_item = dict()
                            if alldata['constant_data']['FirstTeam'] == item['FirstTeam'] and alldata['constant_data'][
                                'SecondTeam'] == item['SecondTeam']:
                                variable_item[item['league'] + ' ' + game_type] = {
                                    'spread': {
                                        item['FirstTeam']: [item['Team1spread'].replace('\u00bd', '.5').split(' ,')],
                                        item['SecondTeam']: [item['Team2spread'].replace('\u00bd', '.5').split(' ,')],

                                    }, 'money': {
                                        item['FirstTeam']: [item['Team1money']],
                                        item['SecondTeam']: [item['Team2money']],

                                    }, 'total points O/U':
                                        [
                                            [item['total_over'].replace('\u00bd', '.5'),
                                             item['total_under'].replace('\u00bd', '.5')]
                                        ]

                                }
                                try:
                                    alldata['variable_data'][item['league'] + ' ' + game_type] = variable_item
                                except:
                                    alldata['variable_data'] = variable_item
    except:
        pass


class BetUs(scrapy.Spider):
    name = 'betus'
    all_links = []

    def start_requests(self):
        yield scrapy.Request(url='https://www.betus.com.pa/sportsbook/', callback=self.parse)

    def parse(self, response):
        for li in response.css('.p-0 .border-bottom.border-light-gray'):
            title = li.css('span.sport::text').get().strip()
            if title in to_Scrape:
                for sub in li.css('a'):
                    url = sub.css('::attr(href)').get()
                    if url is None:
                        pass
                    # elif '/' in url:
                    #     print('sss  '+ url)
                    #
                    #     yield scrapy.Request(url='https://www.betus.com.pa/' + url, callback=self.parse_data,)

                    else:
                        # print('aaa  ' + url)
                        yield scrapy.Request(url='https://www.betus.com.pa/sportsbook/' + url, callback=self.parse_data,)

    def parse_data(self, response):

        if len(response.css('#periods-tabs a')) > 1:
            self.all_links.append(response.url)

        if response.css('.chk-game') == []:
            if response.css('.game-tbl.row') != []:

                for li in response.css('.game-block'):
                    date = li.css('.date.font-weight-normal::text').get()
                    for data in li.css('.normal'):
                        item = dict()
                        main_item = dict()
                        item['sportsbook_name'] = 'bet_us_sports'
                        item['Game Title'] = response.css('#sport-title span::text').get()

                        item['league'] = response.css('.game-block #top-name-league span::text').get()

                        date1 = datefinder.find_dates(date)
                        for da in date1:
                            item['Date'] = str(da).split(' ')[0]
                        time1 = data.css('.row .time span::text').get().replace('p', ' pm').replace('a', ' am')
                        time_ = datetime.strptime(time1, '%I:%M %p')
                        item['Time'] = str(time_).split(' ')[1]
                        tame = item['Date'] + ' ' + item['Time']
                        if str(future_date_after_1day) > tame and '1st Inning' not in item['league'] and 'Series' not in item['league'] and 'NBA Alternatives' not in item['league'] and 'Euroleague Men' not in item['league'] and 'Champions League' not in item['league']:

                            firstTeam = data.css('.game-tbl.row .visitor span#awayName a::text').get()
                            if firstTeam is None:
                                item['FirstTeam'] = data.css('.game-tbl.row .visitor span#awayName::text').get().strip()
                            else:
                                item['FirstTeam'] = firstTeam
                            for i, data_ in enumerate(data.css('.game-tbl.row .visitor .line-container')):
                                if i == 0:
                                    try:
                                        item['Team1spread'] = data_.css('span::text').get().replace(' ', ' , ').replace(
                                            '\u00bd ', '.5 ')
                                    except:
                                        item['Team1spread'] = ''
                                elif i == 1:
                                    try:
                                        item['Team1money'] = data_.css('span::text').get().strip()
                                        if '' == item['Team1money']:

                                            try:
                                                temp1total = \
                                                data.css('.game-tbl.row .visitor .line-container span::text')[
                                                    2].get().strip()
                                                temp2total = \
                                                data.css('.game-tbl.row .visitor .line-container span::text')[
                                                    3].get().strip()
                                                item['total_over'] = temp1total + ' , ' + temp2total
                                                item['total_over'] = item['total_over'].replace('\u00bd ',
                                                                                                '.5').replace(
                                                    'o', '').replace('u', '')
                                            except:
                                                item['total_over'] = ''
                                        else:
                                            try:
                                                temp1total = \
                                                data.css('.game-tbl.row .visitor .line-container span::text')[
                                                    3].get().strip()
                                                temp2total = \
                                                data.css('.game-tbl.row .visitor .line-container span::text')[
                                                    4].get().strip()
                                                item['total_over'] = temp1total + ' , ' + temp2total
                                                item['total_over'] = item['total_over'].replace('\u00bd ',
                                                                                                '.5').replace(
                                                    'o', '').replace('u', '')
                                            except:
                                                try:
                                                    temp1total = \
                                                        data.css('.game-tbl.row .visitor .line-container span::text')[
                                                            2].get().strip()
                                                    temp2total = \
                                                        data.css('.game-tbl.row .visitor .line-container span::text')[
                                                            3].get().strip()
                                                    item['total_over'] = temp1total + ' , ' + temp2total
                                                    item['total_over'] = item['total_over'].replace('\u00bd ',
                                                                                                    '.5').replace('o',
                                                                                                                  '').replace(
                                                        'u', '')
                                                except:
                                                    item['total_over'] = ''

                                    except:
                                        item['Team1money'] = ''
                                        try:
                                            temp1total = data.css('.game-tbl.row .visitor .line-container span::text')[
                                                2].get().strip()
                                            temp2total = data.css('.game-tbl.row .visitor .line-container span::text')[
                                                3].get().strip()
                                            item['total_over'] = temp1total + ' , ' + temp2total
                                            item['total_over'] = item['total_over'].replace('\u00bd ', '.5').replace(
                                                'o',
                                                '').replace(
                                                'u', '')

                                        except:
                                            try:
                                                temp1total = \
                                                data.css('.game-tbl.row .visitor .line-container span::text')[
                                                    3].get().strip()
                                                temp2total = \
                                                data.css('.game-tbl.row .visitor .line-container span::text')[
                                                    4].get().strip()
                                                item['total_over'] = temp1total + ' , ' + temp2total
                                                item['total_over'] = item['total_over'].replace('\u00bd ',
                                                                                                '.5').replace('o',
                                                                                                              '').replace(
                                                    'u', '')
                                            except:
                                                try:
                                                    temp1total = \
                                                    data.css('.game-tbl.row .visitor .line-container span::text')[
                                                        1].get().strip()
                                                    temp2total = \
                                                    data.css('.game-tbl.row .visitor .line-container span::text')[
                                                        2].get().strip()
                                                    item['total_over'] = temp1total + ' , ' + temp2total
                                                    item['total_over'] = item['total_over'].replace('\u00bd ',
                                                                                                    '.5').replace(
                                                        'o',
                                                        '').replace(
                                                        'u', '')
                                                except:
                                                    item['total_over'] = ''
                            try:
                                team1temp1Total = \
                                data.css('.game-tbl.row .visitor .line-container-teamtotal span::text')[
                                    1].get().strip()
                                team1temp2Total = \
                                data.css('.game-tbl.row .visitor .line-container-teamtotal span::text')[
                                    2].get().strip()
                                team1temp3Total = \
                                data.css('.game-tbl.row .visitor .line-container-teamtotal span::text')[
                                    4].get().strip()
                                team1temp4Total = \
                                data.css('.game-tbl.row .visitor .line-container-teamtotal span::text')[
                                    5].get().strip()
                                tempV1 = team1temp1Total + ' , ' + team1temp2Total
                                tempV2 = team1temp3Total + ' , ' + team1temp4Total
                                item['Team1TotalPoints'] = tempV1.replace('\u00bd ', '.5').replace('o', '').replace('u',
                                                                                                                    '') + ' , ' + tempV2.replace(
                                    '\u00bd ', '.5').replace('o', '').replace('u', '')
                            except:
                                item['Team1TotalPoints'] = ''
                            secondteam = data.css('.game-tbl.row .home span#homeName a::text').get()
                            if secondteam is None:
                                item['SecondTeam'] = data.css('.game-tbl.row .home span#homeName::text').get().strip()
                            else:
                                item['SecondTeam'] = secondteam
                            for j, data_1 in enumerate(data.css('.game-tbl.row .home .line-container')):
                                if j == 0:
                                    try:
                                        item['Team2spread'] = data_1.css('span::text').get().replace(' ',
                                                                                                     ' , ').replace(
                                            '\u00bd ', '.5 ')
                                    except:
                                        item['Team2spread'] = ''
                                elif j == 1:
                                    try:
                                        item['Team2money'] = data_1.css('span::text').get().strip()
                                        if '' == item['Team2money']:
                                            try:
                                                temp1total2 = \
                                                data.css('.game-tbl.row .home .line-container span::text')[
                                                    2].get().strip()
                                                temp2total2 = \
                                                data.css('.game-tbl.row .home .line-container span::text')[
                                                    3].get().strip()
                                                item['total_under'] = temp1total2.replace('o', '').replace('u',
                                                                                                           '').replace(
                                                    '\u00bd ', '.5') + ' , ' + temp2total2.replace('o', '').replace('u',
                                                                                                                    '').replace(
                                                    '\u00bd ', '.5')
                                            except:
                                                item['total_under'] = ''
                                        else:
                                            try:
                                                temp1total2 = \
                                                data.css('.game-tbl.row .home .line-container span::text')[
                                                    3].get().strip()
                                                temp2total2 = \
                                                data.css('.game-tbl.row .home .line-container span::text')[
                                                    4].get().strip()
                                                item['total_under'] = temp1total2 + ' , ' + temp2total2
                                                item['total_under'] = item['total_under'].replace('\u00bd ',
                                                                                                  '.5').replace(
                                                    'o', '').replace('u', '')
                                            except:
                                                try:

                                                    temp1total2 = \
                                                        data.css('.game-tbl.row .home .line-container span::text')[
                                                            2].get().strip()
                                                    temp2total2 = \
                                                        data.css('.game-tbl.row .home .line-container span::text')[
                                                            3].get().strip()
                                                    item['total_under'] = temp1total2 + ' , ' + temp2total2
                                                    item['total_under'] = item['total_under'].replace('\u00bd ',
                                                                                                      '.5').replace('o',
                                                                                                                    '').replace(
                                                        'u', '')
                                                except:

                                                    item['total_under'] = ''
                                    except:
                                        item['Team2money'] = ''
                                        try:
                                            temp1total2 = data.css('.game-tbl.row .home .line-container span::text')[
                                                2].get().strip()
                                            temp2total2 = data.css('.game-tbl.row .home .line-container span::text')[
                                                3].get().strip()
                                            item['total_under'] = temp1total2 + ' , ' + temp2total2
                                            item['total_under'] = item['total_under'].replace('\u00bd ', '.5').replace(
                                                'o',
                                                '').replace(
                                                'u', '')
                                        except:
                                            try:
                                                temp1total2 = \
                                                data.css('.game-tbl.row .home .line-container span::text')[
                                                    3].get().strip()
                                                temp2total2 = \
                                                data.css('.game-tbl.row .home .line-container span::text')[
                                                    4].get().strip()
                                                item['total_under'] = temp1total2 + ' , ' + temp2total2
                                                item['total_under'] = item['total_under'].replace('\u00bd ',
                                                                                                  '.5').replace('o',
                                                                                                                '').replace(
                                                    'u', '')
                                            except:
                                                try:

                                                    temp1total2 = \
                                                        data.css('.game-tbl.row .home .line-container span::text')[
                                                            1].get().strip()
                                                    temp2total2 = \
                                                        data.css('.game-tbl.row .home .line-container span::text')[
                                                            2].get().strip()
                                                    item['total_under'] = temp1total2 + ' , ' + temp2total2
                                                    item['total_under'] = item['total_under'].replace('\u00bd ',
                                                                                                      '.5').replace('o',
                                                                                                                    '').replace(
                                                        'u', '')
                                                except:

                                                    item['total_under'] = ''

                            try:
                                team2temp1Total = data.css('.game-tbl.row .home .line-container-teamtotal span::text')[
                                    1].get().strip()
                                team2temp2Total = data.css('.game-tbl.row .home .line-container-teamtotal span::text')[
                                    2].get().strip()
                                team2temp3Total = data.css('.game-tbl.row .home .line-container-teamtotal span::text')[
                                    4].get().strip()
                                team2temp4Total = data.css('.game-tbl.row .home .line-container-teamtotal span::text')[
                                    5].get().strip()
                                temp2V1 = team2temp1Total + ' , ' + team2temp2Total
                                temp2V2 = team2temp3Total + ' , ' + team2temp4Total
                                item['Team2TotalPoints'] = temp2V1.replace('\u00bd ', '.5').replace('o', '').replace(
                                    'u',
                                    '') + ' , ' + temp2V2.replace(
                                    '\u00bd ', '.5').replace('o', '').replace('u', '')
                            except:
                                item['Team2TotalPoints'] = ''
                            draw = data.css('.draw .line-container span::text').get()
                            if draw is None:
                                item['Draw'] = ''
                            else:
                                item['Draw'] = draw
                            main_item['constant_data'] = item
                            allitems.append(main_item)
            else:
                pass
        else:
            for links in response.css('.form-group.form-check'):
                link = links.css('a::attr(href)').get()
                yield scrapy.Request(url='https://www.betus.com.pa/sportsbook/' + link, callback=self.parse_data)

    def chunks(self, lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    def process_link(self, link):
        options = ff_options()
        options.add_argument('--headless')

        driver = webdriver.Firefox(options=options)

        try:
            driver.set_page_load_timeout(30)
            driver.get(link)
        except:
            pass
        try:
            for index in range(len(driver.find_element_by_id('periods-tabs').find_elements_by_tag_name('a')[1:])):
                button = driver.find_element_by_id('periods-tabs').find_elements_by_tag_name('a')[index + 1]
                button.click()
                time.sleep(4)
                new_res = scrapy.Selector(text=driver.page_source)
                get_all_data(new_res)
        except:
            pass
        driver.close()

    def close(self, spider):
        for chunk_list in self.chunks(spider.all_links, 10):
            threads_list = []
            for link in chunk_list:
                newt = Thread(target=self.process_link, args=(link,))
                newt.start()
                threads_list.append(newt)
            for t in threads_list:
                t.join()
        jsondata = json.dumps(allitems, indent=4)
        jsondata = unidecode.unidecode(jsondata)
        file_json.write(jsondata)


process = CrawlerProcess({
    'USER_AGENT': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36"

})

process.crawl(BetUs)

process.start()
