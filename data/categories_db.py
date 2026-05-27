# categories.py
"""
The Alcyoneus DB - Category Definitions
20+ categories for organizing OSINT platforms
"""

CATEGORIES = {
    'video_and_streaming': {
        'name': 'Video And Streaming',
        'description': 'Platform video sharing, Streaming and Visual content ',
        'icon': '🎥',
        'priority' 3,
        'examples': ["Twitch", "Youtube", "Vimeo"]
    },
    'e_commerce': {
        'name': 'E-Commerce'
        'description': 'Online shopping platforms, marketplaces',
        'icon': '🛒',
        'priority': 4,
        'examples': ["Shopee", "Amazon", "TokoPedia", "Shopify"]
    },
    'social_media': {
        'name': 'Social Media',
        'description': 'Major social networking platforms',
        'icon': '📱',
        'priority': 1,
        'examples': ['Facebook', 'Twitter', 'Instagram', 'LinkedIn']
    },
    'professional': {
        'name': 'Professional Networks',
        'description': 'Career and business networking',
        'icon': '💼',
        'priority': 2,
        'examples': ['LinkedIn', 'Indeed', 'Glassdoor', 'Upwork']
    },
    'coding': {
        'name': 'Coding & Development',
        'description': 'Git repositories and developer platforms',
        'icon': '💻',
        'priority': 1,
        'examples': ['GitHub', 'GitLab', 'Bitbucket', 'StackOverflow']
    },
    'messaging': {
        'name': 'Messaging Apps',
        'description': 'Instant messaging and communication',
        'icon': '💬',
        'priority': 3,
        'examples': ['Telegram', 'WhatsApp', 'Signal', 'Discord']
    },
    'forum': {
        'name': 'Forums & Communities',
        'description': 'Discussion boards and communities',
        'icon': '🗣️',
        'priority': 2,
        'examples': ['Reddit', 'Quora', '4chan', 'StackExchange']
    },
    'blogging': {
        'name': 'Blogging Platforms',
        'description': 'Personal blogs and content publishing',
        'icon': '📝',
        'priority': 2,
        'examples': ['Medium', 'WordPress', 'Blogger', 'Tumblr']
    },
    'video': {
        'name': 'Video Platforms',
        'description': 'Video sharing and streaming',
        'icon': '🎥',
        'priority': 2,
        'examples': ['YouTube', 'TikTok', 'Vimeo', 'Twitch']
    },
    'music': {
        'name': 'Music & Audio',
        'description': 'Music streaming and audio platforms',
        'icon': '🎵',
        'priority': 3,
        'examples': ['Spotify', 'SoundCloud', 'AppleMusic', 'Bandcamp']
    },
    'gaming': {
        'name': 'Gaming',
        'description': 'Gaming platforms and communities',
        'icon': '🎮',
        'priority': 2,
        'examples': ['Steam', 'Xbox', 'PlayStation', 'EpicGames']
    },
    'dating': {
        'name': 'Dating Apps',
        'description': 'Dating and relationship platforms',
        'icon': '💕',
        'priority': 3,
        'examples': ['Tinder', 'Bumble', 'OkCupid', 'Hinge']
    },
    'news': {
        'name': 'News & Media',
        'description': 'News platforms and comments',
        'icon': '📰',
        'priority': 3,
        'examples': ['CNN', 'BBC', 'TheVerge', 'TechCrunch']
    },
    'darkweb': {
        'name': 'Dark Web',
        'description': 'Dark web marketplaces and forums',
        'icon': '🌑',
        'priority': 4,
        'examples': ['Dread', 'TorMarket', 'ASAP', 'Bohemia']
    },
    'pastebin': {
        'name': 'Pastebins',
        'description': 'Code and text sharing platforms',
        'icon': '📋',
        'priority': 2,
        'examples': ['Pastebin', 'Ghostbin', 'Rentry', 'Controlc']
    },
    'osint_tools': {
        'name': 'OSINT Tools',
        'description': 'Public OSINT and search tools',
        'icon': '🔍',
        'priority': 1,
        'examples': ['Sherlock', 'Maigret', 'WhatsMyName', 'SocialScan']
    },
    'government': {
        'name': 'Government',
        'description': 'Government databases and records',
        'icon': '🏛️',
        'priority': 4,
        'examples': ['SEC', 'PatentDB', 'GovRegistry', 'PublicRecords']
    },
    'academic': {
        'name': 'Academic',
        'description': 'Academic and research platforms',
        'icon': '🎓',
        'priority': 2,
        'examples': ['ResearchGate', 'Academia', 'GoogleScholar', 'ORCID']
    },
    'breach_data': {
        'name': 'Breach Data',
        'description': 'Data breach indexes and dumps',
        'icon': '💀',
        'priority': 4,
        'examples': ['HaveIBeenPwned', 'Dehashed', 'LeakCheck', 'SnusBase']
    },
    'email': {
        'name': 'Email Providers',
        'description': 'Email service providers',
        'icon': '📧',
        'priority': 2,
        'examples': ['Gmail', 'Outlook', 'Yahoo', 'ProtonMail']
    },
}

# Platform to category mapping (will be populated in platforms.json)
PLATFORM_CATEGORIES = {
    # E-Commerce
    'shopee': 'e_commerce',
    'amazon': 'e_commerce',
    'tokopedia': 'e_commerce',
    'shopify': 'e_commerce',

    # Social Media
    'facebook': 'social_media',
    'twitter': 'social_media',
    'instagram': 'social_media',
    'linkedin': 'professional',
    'tiktok': 'video',
    'snapchat': 'social_media',
    'pinterest': 'social_media',

    # Coding
    'github': 'coding',
    'gitlab': 'coding',
    'bitbucket': 'coding',
    'stackoverflow': 'coding',

    # Messaging
    'telegram': 'messaging',
    'discord': 'messaging',
    'whatsapp': 'messaging',
    'signal': 'messaging',

    # Forums
    'reddit': 'forum',
    'quora': 'forum',
    '4chan': 'forum',

    # Music
    'spotify': 'music',
    'soundcloud': 'music',

    # Gaming
    'steam': 'gaming',
    'epicgames': 'gaming',
    'xbox': 'gaming',
    'playstation': 'gaming',

    # Dating
    'tinder': 'dating',
    'bumble': 'dating',

    # Pastebin
    'pastebin': 'pastebin',
    'ghostbin': 'pastebin',

    # Email
    'gmail': 'email',
    'outlook': 'email',
    'protonmail': 'email'
}
