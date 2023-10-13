#input variables to Zapier Step 13: Get Text Blocks
input={
  'dict': 'Dict' #from Step 12: Update Email Variables
  'url': 'Piublished URL' #from Step 1: Get Email Info from Google Sheets
  }


import urllib.request
import re
import ast

mapping = ast.literal_eval(input['dict'])

mkto_ids =  {'Banner Image (600x300px @1x | 1200x600px @2x)': ['img-Hero', 'hero'], 'Banner Source': ['link-Hero', 'hero'] , 'Main Title': ['text-Title', 'title'],'Pre-Button Text': ['', 'bodyTextBlock'],'Button Text': ['textButton-Button', 'button'],'Button Link': ['linkButton-Button', 'button'],'Post-Button Text': ['', 'bodyTextBlock2'], 'UTM':['UTM','']}

response = urllib.request.urlopen(input['url'])
page_source = response.read()

pattern = '<body class=".*<span>Updated automatically every 5 minutes</span></div>'
body_text = re.search(pattern, str(page_source)).group(0)

text_block_names=[]

for key in mapping:
    if mkto_ids[key][0] =='':
        text_block_names.append(key)

text_block_values = [None]*len(text_block_names)

for k in range(0,len(text_block_names)):

    pattern = '<td[^>]*>'+text_block_names[k]+'</td><td[^>]*><div[^>]*>(.*?)</div></td>'

    try:
        y = re.search(pattern, body_text).group(1)
    except:
        pattern = '<td[^>]*>'+text_block_names[k]+'</td><td[^>]*>(.*?)</td>'
        y = re.search(pattern, body_text).group(1)

    a_tags = re.findall('<a[^>]*>.*?</a>',y)

    for link in a_tags:
        href = re.search('https://www.google.com/url\?q=(.*)&amp;sa',link).group(1)
        linked = re.search('<a[^>]*>(.*?)</a>',link).group(1)
        new = '<a href="'+href+'${utm}" style="color: #00c08b;font-weight:bold;" target="_blank">'+linked+'</a>'
        y = y.replace(link,new)


    spans = re.findall('<span[^>]*>.*?</span>',y)

    span_replace = {'font-weight:bold;': ['<strong>','</strong>'],'font-style:italic;' : ['<em>','</em>']}
    for span in spans:

        text = re.search('<span[^>]*>(.*?)</span>',span).group(1)
        if text[0:2] == '<a':
            y = y.replace(span, text) #remove span tags

        else:
            style = re.search('<span[^>]*style="(.*?)"[^>]*>', span).group(1)
            y = y.replace(span, span_replace[style][0] + text + span_replace[style][1])

    ul_tags =  y.split('<br>')

    for i in range(0,len(ul_tags)):
        if ul_tags[i] =='':
            ul_tags[i] = '<p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-size:14px;line-height:20px;color:#5f6368;font-family:roboto, helvetica neue, helvetica, arial, sans-serif;"><br></p>'
        elif ul_tags[i][0] == "-":
            if i > 0 and '</li>' not in ul_tags[i-1]:
                ul_tags[i] = '<ul><li style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-size:14px;line-height:20px;color:#5f6368;font-family:roboto, helvetica neue, helvetica, arial, sans-serif;Margin-bottom:0px;">' + ul_tags[i][1:] + '</li>'
            elif i<(len(ul_tags)-1) and (ul_tags[i+1] == "" or ul_tags[i+1][0] != "-"):
                ul_tags[i] = '<li style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-size:14px;line-height:20px;color:#5f6368;font-family:roboto, helvetica neue, helvetica, arial, sans-serif;Margin-bottom:0px;">' + ul_tags[i][1:] + '</li></ul>'
            else:
                ul_tags[i] = '<li style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-size:14px;line-height:20px;color:#5f6368;font-family:roboto, helvetica neue, helvetica, arial, sans-serif;Margin-bottom:0px;">' + ul_tags[i][1:] + '</li>'
        elif re.match('\d\.',ul_tags[i][0:2]) is not None:
            if i > 0 and '</li>' not in ul_tags[i-1]:
                ul_tags[i] = '<ol><li style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-size:14px;line-height:20px;color:#5f6368;font-family:roboto, helvetica neue, helvetica, arial, sans-serif;Margin-bottom:0px;">' + ul_tags[i][2:] + '</li>'
            elif i < (len(ul_tags)-1) and (ul_tags[i+1] == "" or re.match('\d\.',ul_tags[i+1][0:2]) is None):
                ul_tags[i] = '<li style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-size:14px;line-height:20px;color:#5f6368;font-family:roboto, helvetica neue, helvetica, arial, sans-serif;Margin-bottom:0px;">' + ul_tags[i][2:] + '</li></ol>'
            else:
                ul_tags[i] = '<li style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-size:14px;line-height:20px;color:#5f6368;font-family:roboto, helvetica neue, helvetica, arial, sans-serif;Margin-bottom:0px;">' + ul_tags[i][2:] + '</li>'
        else:
            ul_tags[i] = '<p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-size:14px;line-height:20px;color:#5f6368;font-family:roboto, helvetica neue, helvetica, arial, sans-serif;">' + ul_tags[i] + '</p>'

    text_block_values[k] = "".join(ul_tags)

    jibberish = ['\\xe2\\x80\\x94', '\\xe2\\x80\\x99']
    char = ["--", "'"]
    # print('Before: ', input['value'])
    for i in range(0, len(jibberish)):
        text_block_values[k] = text_block_values[k].replace(jibberish[i], char[i])
    print(text_block_values[k])
    mapping[text_block_names[k]] = text_block_values[k]
    
return {'dict': str(mapping)}
