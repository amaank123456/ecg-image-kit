import os
import wfdb
import random
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
from datetime import date, timedelta
import numpy as np

test_date1 = date(1940, 1, 1)

def generate_template(header_file):
    filename, extn = os.path.splitext(header_file)
    fields = wfdb.rdheader(filename)

    if fields.comments == []:
        template_file_content = open(os.path.join('TemplateFiles','TextFile1.txt'), 'r')
        Lines = template_file_content.readlines()
        lines = []
        max = 0
        for line in Lines:
            if(len(line.strip()) > max):
                maxIdx = line.strip()
                max = len(line.strip())
            lines.append(line.strip())
        
        return lines, {}, 0

    else:
        comments = fields.comments
        
        attributes = {}
        attributes['Date'] = fields.base_date
        attributes['Time'] = str(fields.base_time)
        attributes['Name'] = filename.split('/')[-1]
        attributes['ID'] = str(str(random.randint(10**(8-1), (10**8)-1)))

        if attributes['Date'] == None:
            attributes['Date'] = date.today()
        
        dates_bet = attributes['Date'] - test_date1
        total_days = dates_bet.days
        randay = random.randrange(total_days)
    
        attributes['Height'] = ''
        attributes['Weight'] = ''
        attributes['Sex'] = ''
        
        for c in comments:
            col = c.split(':')[0]
            val = c.split(':')[1]
            
            if col == 'Age' or col == 'Height' or col == 'Weight':
                val = val.replace(" ", "")
                if val == 'Unknown':
                    attributes[str(col)] = ''
                else:
                    attributes[str(col)] = str(val)
            else:
                val = val.replace(" ", "")
                attributes[str(col)] = val

        if 'Age' in attributes:
            attributes['DOB'] = attributes['Date'] - timedelta(days=int(attributes['Age'])*365)      
        else:
            attributes['DOB'] = test_date1 + timedelta(days=randay)
            attributes['Age'] = str(attributes['Date'].year - attributes['DOB'].year) 

        attributes['DOB'] = str(attributes['DOB']) + '(' + str(attributes['Age']) + 'yrs)'

        if attributes['Weight'] != '':
            attributes['Weight'] += ' kgs'
        
        attributes['Date'] = str(attributes['Date']) + ', ' + attributes['Time']
    
        printedText = {}
        printedText[0] = ['Name', 'ID', 'Date']
        printedText[1] = ['DOB', 'Height', 'Weight']
        printedText[2] = ['Sex']

        return printedText, attributes, 1

        




