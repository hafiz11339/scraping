import cloudscraper
import scrapy
import json
import csv
import time

headers = ['Question', 'Choice 1', 'Choice 2', 'Choice 3', 'Choice 4', 'Correct', 'class', 'category', 'url']
fileout = open("toppr.csv", 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(fileout, fieldnames=headers)
writer.writeheader()
scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
# Or: scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session
index = 0
while index < 10:

    main_res = scraper.get("https://www.toppr.com/ask/")
    if main_res.status_code != 403:
        break
    time.sleep(30)
    index += 1
if index == 10:
    quit()
response = scrapy.Selector(text=main_res.text)
all_class_links = response.css('.Footer_navList__RmMla')[0].css('li a::attr(href)').getall()
for link in all_class_links:
    res = scraper.get("https://www.toppr.com" + link)
    class_response = scrapy.Selector(text=res.text)
    sub_link = []
    for c_link in \
            json.loads(class_response.css('script#__NEXT_DATA__::Text').get())['props']['pageProps']['initialState'][
                'klass'][
                'klassContent']['subjects']:
        sub_link.append('https://www.toppr.com/ask/content/' + c_link['path'])
    for subject in sub_link:
        subject_res = scraper.get(subject)
        subject_response = scrapy.Selector(text=subject_res.text)
        category_link = []
        for cat_ in \
                json.loads(subject_response.css('script#__NEXT_DATA__::Text').get())['props']['pageProps'][
                    'initialState'][
                    'subject']['subjectContent']['chapters']:
            category_link.append('https://www.toppr.com/ask/content/' + cat_['path'])

        for cat in category_link:
            cat_res = scraper.get(cat)
            print(cat)
            try:
                cat_response = scrapy.Selector(text=cat_res.text)
                for questions in \
                        json.loads(cat_response.css('script#__NEXT_DATA__::Text').get())['props']['pageProps'][
                            'initialState'][
                            'newChapter']['importantQuestions']:
                    item = dict()
                    item['class'] = link.split('/')[-2]
                    item['category'] = subject.split('/')[-2].replace('-',' ')
                    item['subject'] =cat.split('/')[-2].replace('-',' ')
                    item['url'] = cat
                    if questions.get('choices') and len(questions.get('choices')) > 2:
                        for choice in questions.get('choices'):
                            item['Choice 1'] = [v for v in questions.get('choices')][0]['choice']
                            item['Choice 2'] = [v for v in questions.get('choices')][1]['choice']
                            try:
                                item['Choice 3'] = [v for v in questions.get('choices')][2]['choice']
                                item['Choice 4'] = [v for v in questions.get('choices')][3]['choice']
                            except:
                                item['Choice 3'] = ""
                                item['Choice 4'] = ""
                            item['Correct'] = [v for v in questions.get('choices') if v['isRight'] == True][0][
                                                  'label'] + " : " + \
                                              [v for v in questions.get('choices') if v['isRight'] == True][0]['choice']
                    else:
                        item['Choice 1'] = ""
                        item['Choice 2'] = ""
                        item['Choice 3'] = ""
                        item['Choice 4'] = ""
                        item["Correct"] = questions['solution'].replace('<span>', '').replace('</span>', '').replace(
                            '<div>', '').replace('</div>', '').replace('<br/>', '').replace('&#160;', '').replace(
                            '&nbsp;',
                            '').replace(
                            '<br>', '').replace('<ul>', '').replace('<li>', '').replace('$', '').replace('</ul>',
                                                                                                         '').replace(
                            '</li>', '').replace('&amp;', '').replace('<p>', '').replace('</p>', '').replace(
                            "<u>").replace("</u>").replace('$$', '')
                    item['Question'] = questions['question'].replace('<span>', '').replace('</span>', '').replace(
                        '<div>', '').replace('</div>', '').replace('<br/>', '').replace('&#160;', '').replace('&nbsp;',
                                                                                                              '').replace(
                        '<br>', '').replace('<ul>', '').replace('<li>', '').replace('$', '').replace('</ul>',
                                                                                                     '').replace(
                        '</li>', '').replace('&amp;', '').replace('<p>', '').replace('</p>', '').replace("<u>").replace(
                        "</u>").replace('$$', '')
                    writer.writerow(item)
                    fileout.flush()
            except:
                pass
