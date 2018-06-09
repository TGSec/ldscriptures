import re

from . import exceptions


def lower_list(cap_list):
    low_list = []
    for item in cap_list:
        low_list.append(item.lower())
    return low_list

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

def item_position(item, list):
    n = -1
    
    for i in list:
        n += 1
        
        if i.lower() == item.lower():
            return n
    return -1


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

ot_data = {'chapters': ['50', '40', '27', '36', '34', '24', '21', '4', '31', '24', '22', '25', '29', '36', '10', '13', '10', '42', '150', '31', '12',
                        '8', '66', '52', '5', '48', '12', '14', '3', '9', '1', '4', '7', '3', '3', '3', '2', '14', '4'],
           'codes': ['gen', 'ex', 'lev', 'num', 'deut', 'josh', 'judg', 'ruth', '1-sam', '2-sam', '1-kgs', '2-kgs', '1-chr', '2-chr', 'ezra', 'neh', 'esth', 'job', 'ps', 'prov', 'eccl', 'song', 'isa',
                     'jer', 'lam', 'ezek', 'dan', 'hosea', 'joel', 'amos', 'obad', 'jonah', 'micah', 'nahum', 'hab', 'zeph', 'hag', 'zech', 'mal']
}

nt_data = {'chapters': ['28', '16', '24', '21', '28', '16', '16', '13', '6', '6', '4', '4', '5', '3', '6', '4', '3', '1', '13', '5', '5', '3', '5',
                        '1', '1', '1', '22'],
           'codes': ['matt', 'mark', 'luke', 'john', 'acts', 'rom', '1-cor', '2-cor', 'gal', 'eph', 'philip', 'col', '1-thes', '2-thes', ' 1-tim',
                     '2-tim', 'titus', 'philem', 'heb', 'james', '1-pet', '2-pet', '1-jn', '2-jn', '3-jn', 'jude', 'rev']}

bofm_data = {'chapters': ['22', '33', '7', '1', '1', '1', '1', '29', '63', '16', '30', '1', '9', '15', '10'],
             'codes': ['1-ne', '2-ne', 'jacob', 'enos', 'jarom', 'omni', 'w-of-m', 'mosiah', 'alma', 'hel', '3-ne', '4-ne', 'morm', 'ether', 'moro']}

pgp_data = {'chapters': ['8', '5', '1', '1', '1'],
             'codes': ['moses', 'abr', 'js-m', 'js-h', 'a-of-f']}
