
#%%

import requests
import json

DEPLOYED_URL = 'https://cloudwars2functionapp.azurewebsites.net/api/ViewProfile?code=pa7gOnUTxIPwEeN13gHpeN4gqgkg9agdZZh/XTjC2ABquysNfZDYLQ=='
json_payload = {"account_id": 'A00000001'}
response = requests.post(url=DEPLOYED_URL, json=json_payload)
response.text

#%% Example payload in dict form
# u'\u2588'

def similarity(str1, str2):
    m = len(str1)
    n = len(str2)
    lensum = float(m + n)
    d = []           
    for i in range(m+1):
        d.append([i])        
    del d[0][0]    
    for j in range(n+1):
        d[0].append(j)       
    for j in range(1,n+1):
        for i in range(1,m+1):
            if str1[i-1] == str2[j-1]:
                d[i].insert(j,d[i-1][j-1])           
            else:
                minimum = min(d[i-1][j]+1, d[i][j-1]+1, d[i-1][j-1]+2)         
                d[i].insert(j, minimum)
    ldist = d[-1][-1]
    ratio = (lensum - ldist)/lensum
    return ratio

lang_to_code = {
    'Afrikaans': 'af',
    'Arabic': 'ar',
    'Bangla': 'bn',
    'Bosnian (Latin)': 'bs',
    'Bulgarian': 'bg',
    'Cantonese (Traditional)': 'yue',
    'Catalan': 'ca',
    'Chinese Simplified': 'zh-Hans',
    'Chinese Traditional': 'zh-Hant',
    'Croatian': 'hr',
    'Czech': 'cs',
    'Danish': 'da',
    'Dutch': 'nl',
    'English': 'en',
    'Estonian': 'et',
    'Fijian': 'fj',
    'Filipino': 'fil',
    'Finnish': 'fi',
    'French': 'fr',
    'German': 'de',
    'Greek': 'el',
    'Gujarati': 'gu',
    'Haitian Creole': 'ht',
    'Hebrew': 'he',
    'Hindi': 'hi',
    'Hmong Daw': 'mww',
    'Hungarian': 'hu',
    'Icelandic': 'is',
    'Indonesian': 'id',
    'Irish': 'ga',
    'Italian': 'it',
    'Japanese': 'ja',
    'Kannada': 'kn',
    'Kazakh': 'kk',
    'Kiswahili': 'sw',
    'Klingon': 'tlh-Latn',
    'Klingon (plqaD)': 'tlh-Piqd',
    'Korean': 'ko',
    'Latvian': 'lv',
    'Lithuanian': 'lt',
    'Malagasy': 'mg',
    'Malay': 'ms',
    'Malayalam': 'ml',
    'Maltese': 'mt',
    'Maori': 'mi',
    'Marathi': 'mr',
    'Norwegian': 'nb',
    'Persian': 'fa',
    'Polish': 'pl',
    'Portuguese (Brazil)': 'pt-br',
    'Portuguese (Portugal)': 'pt-pt',
    'Punjabi': 'pa',
    'Queretaro Otomi': 'otq',
    'Romanian': 'ro',
    'Russian': 'ru',
    'Samoan': 'sm',
    'Serbian (Cyrillic)': 'sr-Cyrl',
    'Serbian (Latin)': 'sr-Latn',
    'Slovak': 'sk',
    'Slovenian': 'sl',
    'Spanish': 'es',
    'Swedish': 'sv',
    'Tahitian': 'ty',
    'Tamil': 'ta',
    'Telugu': 'te',
    'Thai': 'th',
    'Tongan': 'to',
    'Turkish': 'tr',
    'Ukrainian': 'uk',
    'Urdu': 'ur',
    'Vietnamese': 'vi',
    'Welsh': 'cy',
    'Yucatec Maya': 'yua'
    }
code_to_lang = {code:lang for (lang, code) in lang_to_code.items()}

def get_best_match_lang_and_code(language):
    similarities = [(lang, similarity(language, lang)) for lang in lang_to_code.keys()]
    (best_match_lang, _) = max(similarities, key=lambda x: x[1])
    best_match_code = lang_to_code[best_match_lang]
    return (best_match_lang, best_match_code)

(best_match_lang, best_match_code) = get_best_match_lang_and_code(language)
result = [best_match_lang, best_match_code]
result
