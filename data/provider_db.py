PROVIDERS = {
    # ==================== INDONESIA (62) ====================
    'ID': {
        'name': 'Indonesia',
        'code': '62',
        'prefixes': {
            # Telkomsel
            '0811': 'Telkomsel', '0812': 'Telkomsel', '0813': 'Telkomsel',
            '0821': 'Telkomsel', '0822': 'Telkomsel', '0823': 'Telkomsel',
            '0851': 'Telkomsel', '0852': 'Telkomsel', '0853': 'Telkomsel',
            # Indosat Ooredoo
            '0814': 'Indosat Ooredoo', '0815': 'Indosat Ooredoo', '0816': 'Indosat Ooredoo',
            '0855': 'Indosat Ooredoo', '0856': 'Indosat Ooredoo', '0857': 'Indosat Ooredoo',
            '0858': 'Indosat Ooredoo',
            # XL Axiata
            '0817': 'XL Axiata', '0818': 'XL Axiata', '0819': 'XL Axiata',
            '0877': 'XL Axiata', '0878': 'XL Axiata', '0879': 'XL Axiata',
            # Tri (3)
            '0895': 'Tri', '0896': 'Tri', '0897': 'Tri', '0898': 'Tri', '0899': 'Tri',
            # Smartfren
            '0881': 'Smartfren', '0882': 'Smartfren', '0883': 'Smartfren',
            '0884': 'Smartfren', '0885': 'Smartfren', '0886': 'Smartfren',
            '0887': 'Smartfren', '0888': 'Smartfren', '0889': 'Smartfren',
        },
        'mvno': {
            '0859': 'By.U',
        },
        'regex': r'^62[0-9]{9,12}$'
    },

    # ==================== MALAYSIA (60) ====================
    'MY': {
        'name': 'Malaysia',
        'code': '60',
        'prefixes': {
            '010': 'DiGi', '011': 'U Mobile', '012': 'Maxis', '013': 'Celcom',
            '014': 'Maxis/Celcom', '015': 'Tune Talk', '016': 'DiGi',
            '017': 'Maxis', '018': 'U Mobile', '019': 'Celcom',
        },
        'regex': r'^60[0-9]{8,10}$'
    },

    # ==================== SINGAPURA (65) ====================
    'SG': {
        'name': 'Singapore',
        'code': '65',
        'prefixes': {
            '8111': 'Singtel', '8112': 'Singtel', '8113': 'Singtel',
            '8120': 'Singtel', '8121': 'Singtel', '8122': 'Singtel',
            '8000': 'StarHub', '8001': 'StarHub', '8002': 'StarHub',
            '8100': 'M1', '8101': 'M1', '8102': 'M1',
            '8800': 'SIMBA', '8801': 'SIMBA',
        },
        'mvno': {
            '8600': 'Circles.Life', '8660': 'GOMO', '8661': 'GOMO',
        },
        'regex': r'^65[0-9]{8}$'
    },

    # ==================== THAILAND (66) ====================
    'TH': {
        'name': 'Thailand',
        'code': '66',
        'prefixes': {
            '080': 'AIS', '081': 'AIS', '082': 'AIS', '083': 'AIS',
            '084': 'AIS', '085': 'AIS', '086': 'AIS', '089': 'AIS',
            '061': 'AIS', '062': 'AIS', '063': 'AIS', '064': 'AIS',
            '065': 'AIS', '069': 'AIS',
            '090': 'DTAC', '091': 'DTAC', '092': 'DTAC', '093': 'DTAC',
            '094': 'DTAC', '095': 'DTAC', '096': 'DTAC', '097': 'DTAC',
            '098': 'DTAC', '099': 'DTAC',
        },
        'regex': r'^66[0-9]{9,10}$'
    },

    # ==================== VIETNAM (84) ====================
    'VN': {
        'name': 'Vietnam',
        'code': '84',
        'prefixes': {
            '086': 'Viettel', '096': 'Viettel', '097': 'Viettel',
            '098': 'Viettel', '032': 'Viettel', '033': 'Viettel',
            '034': 'Viettel', '035': 'Viettel', '036': 'Viettel',
            '037': 'Viettel', '038': 'Viettel', '039': 'Viettel',
            '070': 'Mobifone', '076': 'Mobifone', '077': 'Mobifone',
            '078': 'Mobifone', '079': 'Mobifone', '089': 'Mobifone',
            '090': 'Vinaphone', '091': 'Vinaphone', '088': 'Vinaphone',
            '083': 'Vinaphone', '084': 'Vinaphone', '085': 'Vinaphone',
            '081': 'Vinaphone', '082': 'Vinaphone',
        },
        'regex': r'^84[0-9]{9,10}$'
    },

    # ==================== JEPANG (81) ====================
    'JP': {
        'name': 'Japan',
        'code': '81',
        'prefixes': {
            '070': 'NTT Docomo', '080': 'NTT Docomo', '090': 'NTT Docomo',
            '050': 'NTT Docomo', '060': 'au (KDDI)',
            '0701': 'SoftBank', '0801': 'SoftBank', '0901': 'SoftBank',
        },
        'regex': r'^81[0-9]{10}$'
    },

    # ==================== FILIPINA (63) ====================
    'PH': {
        'name': 'Philippines',
        'code': '63',
        'prefixes': {
            # Globe/TM
            '0905': 'Globe', '0906': 'Globe', '0915': 'Globe', '0916': 'Globe',
            '0917': 'Globe', '0926': 'Globe', '0927': 'Globe', '0935': 'Globe',
            '0936': 'Globe', '0937': 'Globe', '0953': 'Globe', '0954': 'Globe',
            '0955': 'Globe', '0956': 'Globe', '0957': 'Globe', '0958': 'Globe',
            '0959': 'Globe', '0965': 'Globe', '0966': 'Globe', '0967': 'Globe',
            '0975': 'Globe', '0976': 'Globe', '0977': 'Globe', '0978': 'Globe',
            '0979': 'Globe', '0994': 'Globe', '0995': 'Globe', '0996': 'Globe',
            '0997': 'Globe',
            # Smart/TNT
            '0900': 'Smart', '0907': 'Smart', '0908': 'Smart', '0909': 'Smart',
            '0910': 'Smart', '0911': 'Smart', '0912': 'Smart', '0913': 'Smart',
            '0914': 'Smart', '0918': 'Smart', '0919': 'Smart', '0920': 'Smart',
            '0921': 'Smart', '0928': 'Smart', '0929': 'Smart', '0930': 'Smart',
            '0938': 'Smart', '0939': 'Smart', '0946': 'Smart', '0947': 'Smart',
            '0948': 'Smart', '0949': 'Smart', '0950': 'Smart', '0951': 'Smart',
            '0961': 'Smart', '0963': 'Smart', '0968': 'Smart', '0970': 'Smart',
            '0981': 'Smart', '0989': 'Smart', '0998': 'Smart', '0999': 'Smart',
            # DITO
            '0895': 'DITO', '0896': 'DITO', '0897': 'DITO', '0898': 'DITO',
            '0899': 'DITO', '0991': 'DITO', '0992': 'DITO', '0993': 'DITO',
        },
        'regex': r'^(09|\+639)\d{9}$'
    },

    # ==================== INDIA (91) ====================
    'IN': {
        'name': 'India',
        'code': '91',
        'prefixes': {
            # Airtel
            '9810': 'Airtel', '9811': 'Airtel', '9812': 'Airtel', '9813': 'Airtel',
            '9814': 'Airtel', '9815': 'Airtel', '9816': 'Airtel', '9817': 'Airtel',
            '9818': 'Airtel', '9819': 'Airtel',
            # Vodafone Idea (Vi)
            '9820': 'Vodafone Idea', '9821': 'Vodafone Idea', '9822': 'Vodafone Idea',
            '9823': 'Vodafone Idea', '9824': 'Vodafone Idea', '9825': 'Vodafone Idea',
            # Jio
            '9870': 'Jio', '9871': 'Jio', '9872': 'Jio', '9873': 'Jio',
            '9874': 'Jio', '9875': 'Jio', '9876': 'Jio', '9877': 'Jio',
            '9878': 'Jio', '9879': 'Jio', '8860': 'Jio', '8861': 'Jio',
            # BSNL
            '8888': 'BSNL', '8889': 'BSNL', '8890': 'BSNL', '8891': 'BSNL',
            '9412': 'BSNL', '9413': 'BSNL', '9414': 'BSNL',
        },
        'regex': r'^(?:\+91|0)?[6-9]\d{9}$'
    },

    # ==================== RUSIA (7) ====================
    'RU': {
        'name': 'Russia',
        'code': '7',
        'prefixes': {
            '901': 'Skylink', '902': 'Tele2/T2', '903': 'Beeline', '904': 'Tele2/T2',
            '905': 'Beeline', '906': 'Beeline', '908': 'Tele2/T2', '909': 'Beeline',
            '911': 'MTS', '912': 'MTS', '914': 'MTS', '916': 'MTS', '918': 'MTS',
            '921': 'MegaFon', '922': 'MegaFon', '923': 'MegaFon', '924': 'MegaFon',
            '926': 'MegaFon', '927': 'MegaFon', '928': 'MegaFon', '929': 'MegaFon',
            '930': 'MegaFon', '931': 'MegaFon', '932': 'MegaFon', '933': 'MegaFon',
            '934': 'MegaFon', '936': 'MegaFon', '937': 'MegaFon', '938': 'MegaFon',
            '950': 'Tele2/T2', '951': 'MTS', '952': 'Tele2/T2', '953': 'Tele2/T2',
            '958': 'Yota', '959': 'Yota', '977': 'Yota', '999': 'Yota',
        },
        'regex': r'^(?:\+7|8)?9\d{9}$'
    },

    # ==================== KOREA SELATAN (82) ====================
    'KR': {
        'name': 'South Korea',
        'code': '82',
        'prefixes': {
            '010': 'SK Telecom', '011': 'SK Telecom', 
            '010': 'KT', '016': 'KT',
            '010': 'LG U+', '017': 'LG U+', '018': 'LG U+',
        },
        'regex': r'^(?:\+82|0)?10\d{8}$'
    },

    # ==================== PAKISTAN (92) ====================
    'PK': {
        'name': 'Pakistan',
        'code': '92',
        'prefixes': {
            '0300': 'Jazz', '0301': 'Jazz', '0302': 'Jazz', '0303': 'Jazz',
            '0304': 'Jazz', '0305': 'Jazz', '0310': 'Zong', '0311': 'Zong',
            '0312': 'Zong', '0313': 'Zong', '0314': 'Zong', '0320': 'Telenor',
            '0321': 'Telenor', '0322': 'Telenor', '0323': 'Telenor', '0330': 'Ufone',
            '0331': 'Ufone', '0332': 'Ufone', '0333': 'Ufone', '0334': 'Ufone',
        },
        'regex': r'^(?:\+92|0)?3\d{9}$'
    },

    # ==================== BANGLADESH (880) ====================
    'BD': {
        'name': 'Bangladesh',
        'code': '880',
        'prefixes': {
            '017': 'Grameenphone', '018': 'Robi', '019': 'Banglalink',
            '015': 'Teletalk', '016': 'Airtel', '013': 'Grameenphone',
            '014': 'Banglalink',
        },
        'regex': r'^(?:\+880|0)?1\d{9}$'
    },

    # ==================== NIGERIA (234) ====================
    'NG': {
        'name': 'Nigeria',
        'code': '234',
        'prefixes': {
            '0802': 'Airtel', '0803': 'MTN', '0804': 'MTN', '0805': 'Glo',
            '0806': 'MTN', '0807': 'Glo', '0808': 'Airtel', '0809': '9mobile',
            '0810': 'MTN', '0811': 'Glo', '0812': 'Airtel', '0813': 'MTN',
            '0814': 'MTN', '0815': 'Glo', '0816': 'MTN', '0817': '9mobile',
            '0818': 'Airtel', '0901': 'Airtel', '0902': 'Airtel', '0903': 'MTN',
            '0904': 'Airtel', '0905': 'Glo', '0906': 'MTN', '0907': 'Airtel',
            '0908': '9mobile', '0909': '9mobile', '0912': 'Airtel', '0913': 'MTN',
        },
        'regex': r'^(?:\+234|0)?[789]\d{9}$'
    },

    # =================== AUSTRALIA (61) =====================
    'AU': {
        'name': 'Austrslia',
        'codd': '61',
        'prefixes': {
            # Telstra
            '0410': 'Telstra', '0411': 'Telstra', '0412': 'Telstra',
            '0413': 'Telstra', '0414': 'Telstra', '0415': 'Telstra',
            '0416': 'Telstra', '0417': 'Telstra', '0418': 'Telstra',
            '0419': 'Telstra',
            # Optus
            '0400': 'Optus', '0401': 'Optus', '0402': 'Optus',
            '0403': 'Optus', '0404': 'Optus', '0405': 'Optus',
            '0406': 'Optus', '0407': 'Optus', '0408': 'Optus',
            '0409': 'Optus',
            # Vodafone
            '0420': 'Vodafone', '0421': 'Vodafone', '0422': 'Vodafone',
            '0423': 'Vodafone', '0424': 'Vodafone', '0425': 'Vodafone',
            '0426': 'Vodafone', '0427': 'Vodafone', '0428': 'Vodafone',
            '0429': 'Vodafone',
            # Amaysim (uses Optus network)
            '0470': 'Amaysim', '0471': 'Amaysim', '0472': 'Amaysim',
            '0473': 'Amaysim', '0474': 'Amaysim', '0475': 'Amaysim',
            # Boost (uses Telstra network)
            '0480': 'Boost', '0481': 'Boost', '0482': 'Boost',
            # Others
            '0450': 'Vodafone', '0451': 'Vodafone', '0452': 'Vodafone',
            '0455': 'Optus', '0456': 'Optus', '0457': 'Optus',
            '0466': 'Telstra', '0467': 'Telstra', '0468': 'Telstra',
        },
        'regex': r'^(?:\+?61|0)[2-478](?:[ -]?[0-9]){8}$'
    },

    #===================== CHINA (86) ====================
    'CN': {
        'name': 'China',
        'code': '86',
        'prefixes': {
            # China Mobile
            '134': 'China Mobile', '135': 'China Mobile', '136': 'China Mobile',
            '137': 'China Mobile', '138': 'China Mobile', '139': 'China Mobile',
            '147': 'China Mobile', '150': 'China Mobile', '151': 'China Mobile',
            '152': 'China Mobile', '157': 'China Mobile', '158': 'China Mobile',
            '159': 'China Mobile', '165': 'China Mobile', '172': 'China Mobile',
            '178': 'China Mobile', '182': 'China Mobile', '183': 'China Mobile',
            '184': 'China Mobile', '187': 'China Mobile', '188': 'China Mobile',
            '195': 'China Mobile', '197': 'China Mobile', '198': 'China Mobile',
            '1703': 'China Mobile', '1705': 'China Mobile', '1706': 'China Mobile',
            # China Unicom
            '130': 'China Unicom', '131': 'China Unicom', '132': 'China Unicom',
            '145': 'China Unicom', '155': 'China Unicom', '156': 'China Unicom',
            '166': 'China Unicom', '167': 'China Unicom', '171': 'China Unicom',
            '175': 'China Unicom', '176': 'China Unicom', '185': 'China Unicom',
            '186': 'China Unicom', '196': 'China Unicom',
            '1704': 'China Unicom', '1707': 'China Unicom', '1708': 'China Unicom',
            '1709': 'China Unicom',
            # China Telcom
            '133': 'China Telcom', '153': 'China Telcom', '162': 'China Telcom',
            '173': 'China Telcom', '174': 'China Telcom', '177': 'China Telcom',
            '180': 'China Telcom', '181': 'China Telcom', '189': 'China Telcom',
            '190': 'China Telcom', '191': 'China Telcom', '193': 'China Telcom',
            '199': 'China Telcom',
            '1700': 'China Telcom', '1701': 'China Telcom', '1702': 'China Telcom',
            # China Broadnet
            '192': 'China Broadnet',
        },
        'regex': r'^(?:\+?86|0)?(?:1[3-9]\d{9}|[2-9]\d{9,10})$'
    },
    #===================== KAMBOJA (855) ====================
    'KH': {
        'name': 'Cambodia',
        'code': '855',
        'prefixes': {
            # Cellcard (CamGSM)
            '11': 'Cellcard', '12': 'Cellcard', '14': 'Cellcard', '17': 'Cellcard',
            '61': 'Cellcard', '76': 'Cellcard', '89': 'Cellcard', '92': 'Cellcard',
            # Metfone (Viettel Cambodia)
            '10': 'Metfone', '31': 'Metfone', '33': 'Metfone', '38': 'Metfone',
            '39': 'Metfone', '60': 'Metfone', '66': 'Metfone', '67': 'Metfone',
            '68': 'Metfone', '69': 'Metfone', '70': 'Metfone', '71': 'Metfone',
            '81': 'Metfone', '86': 'Metfone', '87': 'Metfone', '88': 'Metfone',
            '90': 'Metfone', '93': 'Metfone', '97': 'Metfone', '98': 'Metfone',
            '99': 'Metfone',
            # Smart Axiata
            '13': 'Smart', '15': 'Smart', '16': 'Smart', '18': 'Smart',
            '36': 'Smart', '58': 'Smart', '59': 'Smart', '77': 'Smart',
            '78': 'Smart', '83': 'Smart', '84': 'Smart', '85': 'Smart',
            '91': 'Smart', '96': 'Smart',
            # Seatel
            '19': 'Seatel',
            # COTAD
            '95': 'COTAD',
        },
        'regex': r'^(?:\+?855|0)?(?:1[0-9]{7,8}|[3-9][0-9]{7,8})$'
    },

    # ==================== JERMAN (49) ====================
    'DE': {
        'name': 'Germany',
        'code': '49',
        'prefixes': {
            # D1 - T-Mobile (Deutsche Telekom)
            '151': 'T-Mobile', '1510': 'T-Mobile', '1511': 'T-Mobile',
            '1512': 'T-Mobile', '1514': 'T-Mobile', '1515': 'T-Mobile',
            '1516': 'T-Mobile', '1517': 'T-Mobile', '1519': 'T-Mobile',
            '152': 'T-Mobile', '1520': 'T-Mobile', '1522': 'T-Mobile',
            '1525': 'T-Mobile', '1526': 'T-Mobile', '1529': 'T-Mobile',
            '160': 'T-Mobile', '162': 'T-Mobile', '163': 'T-Mobile',
            # D2 - Vodafone
            '1522': 'Vodafone', '1528': 'Vodafone', '155': 'Vodafone',
            '157': 'Vodafone', '1570': 'Vodafone', '1573': 'Vodafone',
            '1575': 'Vodafone', '1577': 'Vodafone', '1578': 'Vodafone',
            '159': 'Vodafone', '173': 'Vodafone', '174': 'Vodafone',
            # E-Plus
            '152': 'E-Plus', '157': 'E-Plus', '1577': 'E-Plus', '1579': 'E-Plus',
            '163': 'E-Plus', '165': 'E-Plus', '166': 'E-Plus', '167': 'E-Plus',
            # O2 (Telefónica)
            '152': 'O2', '159': 'O2', '168': 'O2', '171': 'O2',
            '172': 'O2', '175': 'O2', '176': 'O2', '179': 'O2',
        },
        'mvno': {
            '1515': '1&1', '1517': '1&1', '1521': '1&1', '1522': '1&1',
            '1572': '1&1', '1576': '1&1', '1591': '1&1', '1722': '1&1',
        },

        'regex': r'^(?:\+?49|0)?(?:1[5-7][0-9]{8}|15[0-9]{8}|16[0-9]{7,8}|17[0-9]{7,8})$'
    },
}
