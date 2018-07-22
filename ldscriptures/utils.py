import re

from . import exceptions


def string_range(string):
    string = string.split(',')
    
    num_list = []
    
    for each in string:
        if '-' in each and each.count('-') == 1 and each[0] != '-' and each[-1] != '-' :  # If sub-string is range. Just accept if there is just one
                                                                                          # "-" and if the first and last character aren't "-"
            splited = each.split('-')
            for num in range(int(splited[0]), int(splited[1])+1):
                num_list.append(num)
        
        else:
            num_list.append(int((each)))
    
    num_list.sort()
    
    return num_list

    
def better_capitalize(text):
    splited = text.split(' ')
    final = ''
    for part in splited:
        final = final + ' ' + part.capitalize()
    return final.strip()


def reference_split(reference):
    patt = '^(.+) ((?:[0-9]+(?:-[0-9]+)?,?)*)(?::((?:[0-9]+(?:-[0-9]+)?,?)*))?$'
    
    if re.match(patt, reference):
        splited = list(re.findall(patt, reference)[0])
            
        if ('-' in splited[1] or ',' in splited[1]) and len(splited[2]) > 0:
            raise exceptions.InvalidScriptureReference('Can not exist range or list in chapter and exist verse.')
        
        else:
            splited[1] = string_range(splited[1])
            if splited[2] != '':
                splited[2] = string_range(splited[2])
            else:
                splited[2] = []
                
            return splited
        
    else:
        raise exceptions.InvalidScriptureReference('Regex failure: \'{0}\' is not a valid reference.'.format(reference))

scriptures_url_base = 'https://www.lds.org/scriptures'
