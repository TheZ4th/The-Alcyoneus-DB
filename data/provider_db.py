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

    # ==================== RUSIA (7) - DIPERBAIKI ====================
    'RU': {  # Ganti dari 'RS' ke 'RU' (kode negara standar)
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

    # ==================== KOREA SELATAN (82) - TAMBAHAN ====================
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

    # ==================== PAKISTAN (92) - TAMBAHAN ====================
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

    # ==================== BANGLADESH (880) - TAMBAHAN ====================
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

    # ==================== NIGERIA (234) - TAMBAHAN ====================
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
}
