# -*- coding: utf-8 -*-

import urllib2

D
mport re
import pdb
import lxml

from lxml.html import parse

#from openpyxl import load_workbook
#from openpyxl import Workbook

games = [10893,10912,11944,10913,10914,10917,11945,10918,10921,12770,12773,12806,14088,14291,14420,14492,14494,10938,14496,14497,14498,10939,10942,10943,15773,15774,15775]
#wb_path = r'D:\TEMP\new.xlsx'
#wb = Workbook(optimized_write = True)
#ws = wb.create_sheet()
#wb.save(wb_path)

import timeit

start = timeit.default_timer()



def parse_anons(game):
    url = "http://rprl.ru/calendar/game-"+str(game)+"/anons"
    try:
        # use lxml to find necessary div
        doc = parse(url).getroot()
        div = doc.cssselect("#middle > div.block_2")
        home = doc.cssselect("div.home_team_name")[0].text_content()
        away = doc.cssselect("div.guest_team_name")[0].text_content()
        home_score = doc.cssselect("div.home_team_score")[0].text_content()
        away_score = doc.cssselect("div.guest_team_score")[0].text_content()
        info = doc.cssselect("div.info")[0].text_content().strip()
        date_flag = True
        for line in info.split('\n'):
            if len(line) > 10 and date_flag:
                date = line.strip()
                date_flag = False
            elif len(line):
                referee = line.strip()

        lineups_list = div[0].text_content()
        result.append("%%% home:" + home + " %%%")
        result.append("%%% away:" + away + " %%%")
        result.append("%%% home_score:" + home_score + " %%%")
        result.append("%%% away_score:" + away_score + " %%%")
        result.append("%%% date:" + date + " %%%")
        result.append("%%% referee:" + referee + " %%%")
        result.append("%%% lineups:" + lineups_list + " %%%")

        #pdb.set_trace()
        '''
        home = True
        for each in lineups.split('\n'):
            if len(each) > 50 and home:
                home_lineup = each
                result.append(whattype(home_lineup))
                home = False
            elif len(each) > 50:
                away_lineup = each
                result.append(whattype(away_lineup))
        '''
        #with open("rprl.txt", "a") as myfile: myfile.write(lineups_list)
        
        '''
        wb = load_workbook(wb_path)
        ws = wb.active
        row_index = ws.get_highest_row()
        for j in range(len(result)):
            ws.cell(row = row_index, column = j).value = result[j]
        wb.save(wb_path)
        '''
    except Exception,e:
        print ('Cannot open URL %s for reading' % url)
        print str(e)
        return

def parse_protocol(game):
    url = "http://rprl.ru/calendar/game-"+str(game)+"/protocol"
    try:
        doc = parse(url).getroot()
        div = doc.cssselect("#middle > div.block_4 > table > tr")
        home_tries = div[1].cssselect("td")[0].text_content()
        away_tries = div[1].cssselect("td")[8].text_content()
        home_convs = div[2].cssselect("td")[0].text_content()
        away_convs = div[2].cssselect("td")[8].text_content()
        home_pens = div[3].cssselect("td")[0].text_content()
        away_pens = div[3].cssselect("td")[8].text_content()
        home_drops = div[4].cssselect("td")[0].text_content()
        away_drops = div[4].cssselect("td")[8].text_content()
        ht_home = div[5].cssselect("td")[3].text_content()
        ht_away = div[5].cssselect("td")[5].text_content()
        first_half = doc.cssselect("#middle > div.block_5 > div.events > div.event")
        secnd_half = doc.cssselect("#middle > div.block_6 > div.events > div.event")
        result.append("%%% halftime_home:" + ht_home + " %%%")
        result.append("%%% halftime_away:" + ht_away + " %%%")
        result.append("%%% home_tries:" + home_tries + " %%%")
        result.append("%%% away_tries:" + away_tries + " %%%")
        result.append("%%% home_convs:" + home_convs + " %%%")
        result.append("%%% away_convs:" + away_convs + " %%%")
        result.append("%%% home_pens:" + home_pens + " %%%")
        result.append("%%% away_pens:" + away_pens + " %%%")
        result.append("%%% home_drops:" + home_drops + " %%%")
        result.append("%%% away_drops:" + away_drops + " %%%")

        if len(first_half) > 0:
        #    for each in first_half:
        #        result.append(parse_event(each))
            for each in secnd_half:
                result.append(parse_event(each))
        result.append("%%% endmatch %%%\n\n\n")

        for each in result:
            try:
                with open("rprl-2014-vl.txt", "a") as myfile: myfile.write(each.encode('utf-8') +"\n")
            except Exception,e:
                print str(e)
                return

    except Exception,e:
        print ('Cannot open URL %s for reading' % url)
        print str(e)
        return

def parse_event(event):
    time = event.cssselect(".event_time")[0].text_content()[:2]
    player = event.cssselect(".event_player_name")[0].text_content()
    yellow = len(event.cssselect(".event_card.event_yellowcard"))
    red = len(event.cssselect(".event_card.event_redcard"))
    sub_out = event.cssselect("div.event_substitution.event_out")
    sub_in = event.cssselect("div.event_substitution.event_in")
    p_try = event.cssselect("div.event_action.event_attempt")
    p_cnv = event.cssselect("div.event_action.event_realization")
    p_pen = event.cssselect("div.event_action.event_penalty")
    p_dgl = event.cssselect("div.event_action.event_dropgoal")
    if yellow or red:
        return player + u' - Красная'*red + u' Желтая'*yellow + "("+time+")"
    if sub_out:
        return player + " - " + sub_out[0].text_content() + "("+time+")"
    if sub_in:
        return player + " - " + sub_in[0].text_content() + "("+time+")"
    if p_try:
        return player + " - " + p_try[0].text_content() + "("+time+")"
    if p_cnv:
        return player + " - " + p_cnv[0].text_content() + "("+time+")"
    if p_pen:
        return player + " - " + p_pen[0].text_content() + "("+time+")"
    if p_dgl:
        return player + " - " + p_dgl[0].text_content() + "("+time+")"

def whattype(input):
    output = ""
    for line in input:
        tag = raw_input(line)
        output += tag + ": line"
    return output

for game in games:
    result = []
    parse_anons(game)
    parse_protocol(game)

stop = timeit.default_timer()

print stop - start 
