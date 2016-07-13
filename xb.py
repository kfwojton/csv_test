import csv
from json import *
from re import *
from ast import *
import operator



# campaign	         date	spend	impressions	actions
# fish_cow_desert	1/1/15	10.98	1621	[{"y": 47, "action": "conversions"}, {"action": "conversions", "b": 49}, {"action": "conversions", "z": 29}, {"a": 69, "action": "conversions"}, {"action": "conversions", "x": 81}]
# fish_cow_desert	1/2/15	30.28	4943	[{"action": "views", "b": 90}, {"y": 12, "action": "views"}, {"a": 78, "action": "views"}, {"action": "views", "c": 74}, {"action": "views", "x": 14}, {"action": "views", "z": 19}]
# fish_cow_desert	1/3/15	13.57	2245	[{"action": "conversions", "b": 85}, {"action": "conversions", "x": 73}, {"action": "conversions", "c": 50}]
# fish_cow_desert	1/4/15	38.01	6169	[{"action": "clicks", "c": 71}, {"action": "clicks", "z": 66}, {"action": "clicks", "x": 16}, {"action": "clicks", "b": 38}, {"y": 67, "action": "clicks"}, {"a": 80, "action": "clicks"}, {"action": "conversions", "b": 27}, {"action": "conversions", "x": 8}, {"y": 12, "action": "conversions"}, {"action": "conversions", "z": 47}, {"action": "conversions", "c": 90}]
# fish_cow_desert	1/5/15	2.31	323	[{"y": 51, "action": "conversions"}, {"action": "clicks", "c": 88}, {"action": "clicks", "z": 77}]
# fish_cow_desert	1/6/15	33.31	4013	[{"a": 24, "action": "conversions"}, {"action": "conversions", "x": 54}, {"action": "conversions", "b": 1}, {"y": 89, "action": "conversions"}, {"action": "clicks", "x": 37}, {"action": "clicks", "b": 75}, {"action": "views", "x": 2}, {"a": 68, "action": "views"}, {"y": 25, "action": "views"}, {"action": "views", "z": 4}]
#
# campaign	object_type
# valley_monkey_fruit	photo
# mountains_fruit_dog	video
# mountains_cow_vegtables	video

# Questions:
# 1.	How many unique campaigns ran in February?
# 2.	What is the total number of conversions on plants?
# 3.	What audience, asset combination had the least expensive conversions?
# 4.	What was the total cost per video view?


def answers():


  info = {}
  f = open('source1.csv')
  csv_f = csv.reader(f)

  k = [row for row in csv_f]
  column = k.pop(0)

  l = [(op[1],op[0]) for op in k if findall('\d\d',op[1])[2]=='02']
  l = set([op[1] for op in k])
  # 1.	How many unique campaigns ran in February?
  info['number_of_unique_campaigns_in_feb'] = len(l)

  l = [(op[0],op[4]) for op in k if 'plants' in op[0]]
  # 2.	What is the total number of conversions on plants?
  info['total_number_of_conversions_on_plants'] = sum([int(findall('\d\d*',str(literal_eval(xa)[0]))[0]) for xa in [iop[1] for iop in l] if literal_eval(xa)[0]['action']=='conversions'])

  b_terms = set([top[0].replace('_',' ').split()[1] for top in k])
  c_terms = set([top[0].replace('_',' ').split()[2] for top in k])
  ted = {}
  for ab in b_terms:
      for ac in c_terms:

          ted[ab + '_' + ac] = ''


  l = [[findall('_(.*)',toa[0])[0],float(toa[2]), sum([int(findall('\d\d*',str(op))[0]) for op in literal_eval(toa[4]) if op['action']=='conversions']), toa[0], sum([int(findall('\d\d*',str(op))[0]) for op in literal_eval(toa[4]) if op['action']=='views'])] for toa in k]


  ted = {a:sum([o[1] for o in l if o[0]==a])/sum([o[2] for o in l if o[0]==a]) for a,b in ted.iteritems()}
  sorted_x = sorted(ted.items(), key=operator.itemgetter(1))
  # 3.	What audience, asset combination had the least expensive conversions?
  info['What_audience_asset_combination_had_the_least_expensive_conversions'] = sorted_x

  f = open('source2.csv')
  csv_fo = csv.reader(f)

  ko = [row for row in csv_fo]
  columno = ko.pop(0)

  non_repeating = set([ opio[0] for opio in ko if opio[1]=='video'])

  price = [[[ok[1],int(ok[4])] for ok in l if ok[3]==iop] for iop in non_repeating]
  pricea = [oz[0][0] for oz in price if len(oz)>0]
  views = [oz[1][0] for oz in price if len(oz)>0]


  # 4.	What was the total cost per video view?
  info['What_was_the_total_cost_per_video_view'] = sum(pricea)/sum(views)

  return info
