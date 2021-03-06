# coding=utf-8

from google.appengine.ext import webapp
import os, re
from google.appengine.ext.webapp import template

class Controller(webapp.RequestHandler):
    
    mimetypes = {
        'html': 'text/html',
        'atom': 'application/atom+xml',
        'js': 'application/javascript',
        'gpx': 'application/gpx+xml',
        'kml': 'application/vnd.google-earth.kml+xml',
        'xml': 'text/xml',
        'search': 'application/opensearchdescription+xml'
    }
    
    tags = {
        'nature': 'nature',
        'wildlife': 'wildlife',
        'beach': 'beach',
        'beaches': 'beach',
        'lake': 'lake',
        'lakes': 'lake',
        'wetland': 'wetland',
        'forest': 'forest',
        'forests': 'forest',
        'waterfall': 'waterfall',
        'waterfalls': 'waterfall',
        'castle': 'castle',
        'castles': 'castle',
        'palace': 'palace',
        'palaces': 'palace',
        'citywalls': 'citywalls',
        'citywall': 'citywalls',
        'tower': 'tower',
        'towers': 'tower',
        'ruins': 'ruins',
        'ruin': 'ruins',
        'church': 'church',
        'churches': 'church',
        'farm': 'farm',
        'farms': 'farm',
        'windmill': 'windmill',
        'windmills': 'windmill',
        'vineyard': 'vineyard',
        'vineyards': 'vineyard',
        'winery': 'vineyard',
        'wineries': 'vineyard',
        'watermill': 'watermill',
        'watermills': 'watermill',
        'garden': 'garden',
        'gardens': 'garden',
        'bridge': 'bridge',
        'bridges': 'bridge',
        'fountain': 'fountain',
        'fountains': 'fountain',
        'monument': 'monument',
        'monuments': 'monument',
        'worldheritagesite': 'worldheritagesite',
        'worldheritagesites': 'worldheritagesite',
        'statue': 'statue',
        'statues': 'statue',
        'park': 'park',
        'parks': 'park',
        'picnic': 'picnic',
        'picnicsite': 'picnic',
        'picnicsites': 'picnic',
        'picnicarea': 'picnic',
        'picnicareas': 'picnic',
        'view': 'view',
        'views': 'view',
        'cave': 'cave',
        'caves': 'cave',
        'shop': 'shop',
        'shops': 'shop',
        'bookshop': 'bookshop',
        'bookshops': 'bookshop',
        'giftshop': 'giftshop',
        'giftshops': 'giftshop',
        'artgallery': 'artgallery',
        'artgalleries': 'artgallery',
        'market': 'market',
        'markets': 'market',
        'bowling': 'bowling',
        'snooker': 'snooker',
        'snookerhall': 'snooker',
        'snookerhalls': 'snooker',
        'billiard': 'snooker',
        'billiards': 'snooker',
        'billiardhall': 'snooker',
        'billiardhalls': 'snooker',
        'aquarium': 'aquarium',
        'aquaria': 'aquarium',
        'aquariums': 'aquarium',
        'cinema': 'cinema',
        'cinemas': 'cinema',
        'theatre': 'theatre',
        'theater': 'theatre',
        'theatres': 'theatre',
        'theaters': 'theatre',
        'casino': 'casino',
        'casinos': 'casino',
        'music': 'music',
        'historic': 'historic',
        'historicsite': 'historic',
        'history': 'historic',
        'archeological': 'archeological',
        'archeology': 'archeological',
        'naval': 'naval',
        'navalmuseum': 'naval',
        'war': 'war',
        'warmuseum': 'war',
        'science': 'science',
        'sciencemuseum': 'science',
        'crafts': 'crafts',
        'craft': 'crafts',
        'museum': 'museum',
        'museums': 'museum',
        'themepark': 'themepark',
        'themeparks': 'themepark',
        'rollercoaster': 'themepark',
        'rollercoasters': 'themepark',
        'zoo': 'zoo',
        'zoos': 'zoo',
        'zoologicalgarden': 'zoo',
        'zoologicalgardens': 'zoo',
        'animalpark': 'zoo',
        'animalparks': 'zoo',
        'art': 'art',
        'artgallery': 'art',
        'artgalleries': 'art',
        'circus': 'circus',
        'circuses': 'circus',
        'festival': 'festival',
        'festivals': 'festival',
        'waterpark': 'waterpark',
        'waterparks': 'waterpark',
        'ferriswheel': 'ferriswheel',
        'ferriswheels': 'ferriswheel',
        'bigwheel': 'ferriswheel',
        'bigwheels': 'ferriswheel',
        'playground': 'playground',
        'playgrounds': 'playground',
        'bar': 'bar',
        'bars': 'bar',
        'cafe': 'cafe',
        'cafes': 'cafe',
        'icecream': 'icecream',
        'icecreamparlour': 'icecream',
        'icecreamparlours': 'icecream',
        'icecreamshop': 'icecream',
        'icecreamshops': 'icecream',
        'sport': 'sport',
        'sports': 'sport',
        'stadium': 'stadium',
        'stadiums': 'stadium',
        'americanfootball': 'americanfootball',
        'americanfootballstadium': 'americanfootball',
        'americanfootballstadiums': 'americanfootball',
        'americanfootballpitch': 'americanfootball',
        'americanfootballpitches': 'americanfootball',
        'baseball': 'baseball',
        'baseballstadium': 'baseball',
        'baseballstadiums': 'baseball',
        'baseballpitch': 'baseball',
        'baseballpitches': 'baseball',
        'basketball': 'basketball',
        'basketballstadium': 'basketball',
        'basketballstadiums': 'basketball',
        'cricket': 'cricket',
        'cricketstadium': 'cricket',
        'cricketgreen': 'cricket',
        'cricketgreens': 'cricket',
        'cricketpitch': 'cricket',
        'cricketpitches': 'cricket',
        'football': 'football',
        'footballstadium': 'football',
        'footballstadiums': 'football',
        'footballpitch': 'football',
        'footballpitches': 'football',
        'golf': 'golf',
        'golfcourse': 'golf',
        'golfcourses': 'golf',
        'rugby': 'rugby',
        'rugbystadium': 'rugby',
        'rugbystadiums': 'rugby',
        'rugbypitch': 'rugby',
        'rugbypitches': 'rugby',
        'tennis': 'tennis',
        'tenniscourt': 'tennis',
        'tenniscourts': 'tennis',
        'cycling': 'cycling',
        'racetrack': 'racetrack',
        'motorracing': 'racetrack',
        'speedway': 'racetrack',
        'archery': 'archery',
        'climbing': 'climbing',
        'rockclimbing': 'climbing',
        'fishing': 'fishing',
        'fish': 'fishing',
        'hiking': 'hiking',
        'hike': 'hiking',
        'hikes': 'hiking',
        'horse': 'horse',
        'horseracing': "horse",
        'horseracingtrack': "horse",
        'horseracingtracks': "horse",
        'skateboarding': 'skateboarding',
        'skatepark': 'skateboarding',
        'skateparks': 'skateboarding',
        'pool': 'pool',
        'pools': 'pool',
        'swimmingpool': 'pool',
        'swimmingpools': 'pool',
        'kayaking': 'kayaking',
        'boating': 'boating',
        'boat': 'boating',
        'boats': 'boating',
        'surfing': 'surfing',
        'surf': 'surfing',
        'swimming': 'swimming',
        'swim': 'swimming',
        'waterski': 'waterski',
        'waterskiing': 'waterski',
        'windsurf': 'windsurf',
        'windsurfing': 'windsurf',
        'icehockey': 'icehockey',
        'iceskating': 'iceskating',
        'iceskate': 'iceskating',
        'icerink': 'iceskating',
        'icerinks': 'iceskating',
        'skiing': 'skiing',
        'ski': 'skiing',
        'skislope': 'skiing',
        'snowboarding': 'snowboarding',
        'dupe': 'dupe',
        'dupes': 'dupe',
        'delete': 'delete',
        'deletes': 'delete',
        'deleted': 'delete',
        'badloc': 'badloc',
        'badlocs': 'badloc',
        'todo': 'todo',
        'todos': 'todo',
        'trap': 'trap',
        'traps': 'trap',
        'translated': 'translated'
    }
    
    badges = {
        '1': {
            'src': '/_/badges/1.png',
            'name': 'Newbie',
            'description': 'You\'ve edited your first attraction'
        },
        '2': {
            'src': '/_/badges/2.png',
            'name': 'Tripple wammy',
            'description': 'You\'re 3rd edit is in the bag'
        },
        '3': {
            'src': '/_/badges/3.png',
            'name': 'Day tripper',
            'description': '10 attractions updated'
        },
        '4': {
            'src': '/_/badges/4.png',
            'name': 'Know it all',
            'description': '25 attractions updated'
        },
        '5': {
            'src': '/_/badges/5.png',
            'name': 'Superstar',
            'description': 'Wow! You\'ve hit the ton, 100 attractions updated'
        },
        '6': {
            'src': '/_/badges/6.png',
            'name': 'Local',
            'description': 'Keeping it local, you\'ve made 5 edits in the same neighbourhood'
        },
        '7': {
            'src': '/_/badges/7.png',
            'name': 'Native',
            'description': 'You\'re putting down roots, 20 edits in one neighbourhood'
        },
        '8': {
            'src': '/_/badges/8.png',
            'name': 'Advocate',
            'description': 'Someone has recommended an attraction you\'ve edited'
        },
        '9': {
            'src': '/_/badges/9.png',
            'name': 'Trendsetter',
            'description': 'Your attractions have gained a following, 5 people have recommended them'
        },
        '10': {
            'src': '/_/badges/10.png',
            'name': 'Tour guide',
            'description': 'Wow, everyone loves the attractions you\'ve edited, 25 recommendations'
        },
        '11': {
            'src': '/_/badges/11.png',
            'name': 'A thousand words',
            'description': 'A picture tells a thousand words, or so they say'
        },
        '12': {
            'src': '/_/badges/12.png',
            'name': 'Shutterbug',
            'description': 'You\'re a photo finding hero'
        },
        '13': {
            'src': '/_/badges/13.png',
            'name': 'Dead ringer',
            'description': 'Thanks for identifying 3 duplicate attractions'
        },
        '14': {
            'src': '/_/badges/14.png',
            'name': 'Commentator',
            'description': 'Congratulations on making your first comment'
        },
        '15': {
            'src': '/_/badges/15.png',
            'name': 'Gossip',
            'description': 'Keep spreading the love with your words of wisdom'
        },
        '16': {
            'src': '/_/badges/16.png',
            'name': 'Motormouth',
            'description': 'Give your mouth a rest, that\'s 25 comments'
        },
        '17': {
            'src': '/_/badges/17.png',
            'name': 'Spam eater',
            'description': ''
        },
        '18': {
            'src': '/_/badges/18.png',
            'name': 'Zero hero',
            'description': 'Stop doing zero size edits, that\'s 3, let it be your last'
        },
        '19': {
            'src': '/_/badges/19.png',
            'name': 'Ctrl-Z',
            'description': 'You\'re doing it wrong! You\'ve had 3 of your edits reverted'
        },
        '20': {
            'src': '/_/badges/20.png',
            'name': 'Man with van',
            'description': 'Thanks for identifying 3 non-attractions that should be deleted'
        },
        '50': {
            'tag': 'beach',
            'src': '/_/badges/50.png',
            'name': 'Life\'s a beach',
            'description': 'You beach bum, that\'s 10 edits to beaches'
        },
        '51': {
            'tag': 'forest',
            'src': '/_/badges/51.png',
            'name': 'Robin Hood',
            'description': 'Well done, that\'s 10 edits to forests'
        },
        '52': {
            'tag': 'castle',
            'src': '/_/badges/52.png',
            'name': 'King of the castle',
            'description': 'Well done, that\'s 10 edits to castles'
        },
        '53': {
            'tag': 'church',
            'src': '/_/badges/53.png',
            'name': 'Saint',
            'description': 'Well done, that\'s 10 edits to churches'
        },
        '54': {
            'tag': 'garden',
            'src': '/_/badges/54.png',
            'name': 'Garden centre',
            'description': 'Green fingers \'ey, that\'s 10 edits to gardens'
        },
        '55': {
            'tag': 'park',
            'src': '/_/badges/55.png',
            'name': 'Park life',
            'description': 'Well done, that\'s 10 edits to parks'
        },
        '56': {
            'tag': 'zoo',
            'src': '/_/badges/56.png',
            'name': 'Wild thing',
            'description': 'Well done, that\'s 10 edits to zoos'
        },
        '57': {
            'tag': 'sport',
            'src': '/_/badges/57.png',
            'name': 'Sports star',
            'description': 'Well done, that\'s 10 edits to sporting venues'
        },
        '58': {
            'tag': 'shop',
            'src': '/_/badges/58.png',
            'name': 'Shopaholic',
            'description': 'Well done, that\'s 10 edits to shops'
        },
        '59': {
            'tag': 'historic',
            'src': '/_/badges/59.png',
            'name': 'Ye olde tourist attraction',
            'description': 'Well done, that\'s 10 edits to historic attractions'
        },
        '60': {
            'tag': 'museum',
            'src': '/_/badges/60.png',
            'name': 'Curator',
            'description': 'Well done, that\'s 10 edits to museums'
        },
        '100': {
            'location': 'Amsterdam, Noord-Holland, Nederland',
            'src': '/_/badges/99.png',
            'name': 'Amsterdam',
            'description': 'Well done, that\'s 10 edits in Amsterdam'
        },
        '101': {
            'location': 'Barcelona, CT, Espanya',
            'src': '/_/badges/99.png',
            'name': 'Barcelona',
            'description': 'Well done, that\'s 10 edits in Barcelona'
        },
        '102': {
            'location': 'Berlin, Deutschland',
            'src': '/_/badges/102.png',
            'name': 'Ich bin ein Berliner',
            'description': 'Well done, that\'s 10 edits in Berlin'
        },
        '103': {
            'location': 'Budapest, Magyarország',
            'src': '/_/badges/99.png',
            'name': 'Budapest',
            'description': 'Well done, that\'s 10 edits in Budapest'
        },
        '104': {
            'location': 'København, Hovedstaden, Danmark',
            'src': '/_/badges/99.png',
            'name': 'Copenhagen',
            'description': 'Well done, that\'s 10 edits in Copenhagen'
        },
        '105': {
            'location': 'Dublin City, Ireland',
            'src': '/_/badges/105.png',
            'name': 'Dubliner',
            'description': 'Well done, that\'s 10 edits in Dublin'
        },
        '106': {
            'location': 'City of Edinburgh, UK',
            'src': '/_/badges/99.png',
            'name': 'Edinburgh',
            'description': 'Well done, that\'s 10 edits in Edinburgh'
        },
        '107': {
            'location': 'FI, Toscana, Italia',
            'src': '/_/badges/99.png',
            'name': 'Florence',
            'description': 'Well done, that\'s 10 edits in Florence'
        },
        '108': {
            'location': 'Nyland, Södra Finland, Finland',
            'src': '/_/badges/99.png',
            'name': 'Helsinki',
            'description': 'Well done, that\'s 10 edits in Helsinki'
        },
        '109': {
            'location': 'Kraków, Małopolskie, Polska',
            'src': '/_/badges/99.png',
            'name': 'Krakow',
            'description': 'Well done, that\'s 10 edits in Krakow'
        },
        '110': {
            'location': 'Greater London, UK',
            'src': '/_/badges/110.png',
            'name': 'London calling',
            'description': 'Well done, that\'s 10 edits in London'
        },
        '111': {
            'location': 'Istanbul, Türkiye',
            'src': '/_/badges/99.png',
            'name': 'Istanbul',
            'description': 'Well done, that\'s 10 edits in Istanbul'
        },
        '112': {
            'location': 'Lisboa, Portugal',
            'src': '/_/badges/99.png',
            'name': 'Lisbon',
            'description': 'Well done, that\'s 10 edits in Lisbon'
        },
        '113': {
            'location': 'Greater Manchester, UK',
            'src': '/_/badges/99.png',
            'name': 'Manchester',
            'description': 'Well done, that\'s 10 edits in Manchester'
        },
        '114': {
            'location': 'Comunidad de Madrid, España',
            'src': '/_/badges/99.png',
            'name': 'Madrid',
            'description': 'Well done, that\'s 10 edits in Madrid'
        },
        '115': {
            'location': 'Milano, Lombardia, Italia',
            'src': '/_/badges/99.png',
            'name': 'Milan',
            'description': 'Well done, that\'s 10 edits in Milan'
        },
        '116': {
            'location': 'Московская область, Россия',
            'src': '/_/badges/99.png',
            'name': 'From Russia with love',
            'description': 'Well done, that\'s 10 edits in Moscow'
        },
        '117': {
            'location': 'München, Bayern, Deutschland',
            'src': '/_/badges/99.png',
            'name': 'Munich',
            'description': 'Well done, that\'s 10 edits in Munich'
        },
        '118': {
            'location': 'Paris, Ile-de-France, France',
            'src': '/_/badges/99.png',
            'name': 'Moi j\'suis d\'Paname',
            'description': 'Well done, that\'s 10 edits in Paris'
        },
        '119': {
            'location': 'Praha, Hlavní město Praha, Česká republika',
            'src': '/_/badges/99.png',
            'name': 'Prague',
            'description': 'Well done, that\'s 10 edits in Prague'
        },
        '120': {
            'location': 'RM, Lazio, Italia',
            'src': '/_/badges/99.png',
            'name': 'Rome',
            'description': 'Well done, that\'s 10 edits in Rome'
        },
        '121': {
            'location': 'Stockholms Län, Sverige',
            'src': '/_/badges/99.png',
            'name': 'Stockholm',
            'description': 'Well done, that\'s 10 edits in Stockholm'
        },
        '122': {
            'location': 'Venezia, Veneto, Repubblica Italiana',
            'src': '/_/badges/99.png',
            'name': 'Vienna',
            'description': 'Well done, that\'s 10 edits in Vienna'
        },
        '123': {
            'location': 'Zürich, Schweiz',
            'src': '/_/badges/99.png',
            'name': 'Zurich',
            'description': 'Well done, that\'s 10 edits in Zurich'
        },
        '124': {
            'location': 'Cook, IL, USA',
            'src': '/_/badges/99.png',
            'name': 'Chicago',
            'description': 'Well done, that\'s 10 edits in Chicago'
        },
        '125': {
            'location': 'Honolulu, HI, USA',
            'src': '/_/badges/99.png',
            'name': 'Honolulu',
            'description': 'Well done, that\'s 10 edits in Honolulu'
        },
        '126': {
            'location': 'Clark, NV, USA',
            'src': '/_/badges/126.png',
            'name': 'Viva Las Vegas',
            'description': 'Well done, that\'s 10 edits in Las Vegas'
        },
        '127': {
            'location': 'Los Angeles, CA, USA',
            'src': '/_/badges/99.png',
            'name': 'Los Angeles',
            'description': 'Well done, that\'s 10 edits in Los Angeles'
        },
        '128': {
            'location': 'Miami-Dade, FL, USA',
            'src': '/_/badges/99.png',
            'name': 'Miami',
            'description': 'Well done, that\'s 10 edits in Miami'
        },
        '129': {
            'location': 'New York, NY, USA',
            'src': '/_/badges/129.png',
            'name': 'Big apple',
            'description': 'Well done, that\'s 10 edits in New York City'
        },
        '130': {
            'location': 'Orange, FL, USA',
            'src': '/_/badges/99.png',
            'name': 'Orlando',
            'description': 'Well done, that\'s 10 edits in Orlando'
        },
        '131': {
            'location': 'Rio de Janeiro, RJ, Brasil',
            'src': '/_/badges/99.png',
            'name': 'Rio de Janeiro',
            'description': 'Well done, that\'s 10 edits in Rio de Janeiro'
        },
        '132': {
            'location': 'San Francisco, CA, USA',
            'src': '/_/badges/99.png',
            'name': 'San Francisco',
            'description': 'Well done, that\'s 10 edits in San Francisco'
        },
        '133': {
            'location': 'Toronto Division, ON, Canada',
            'src': '/_/badges/99.png',
            'name': 'Toronto',
            'description': 'Well done, that\'s 10 edits in Toronto'
        },
        '134': {
            'location': 'District of Columbia, DC, USA',
            'src': '/_/badges/99.png',
            'name': 'Washington DC',
            'description': 'Well done, that\'s 10 edits in Washington DC'
        },
        '135': {
            'location': 'Abu Dhabi, United Arab Emirates',
            'src': '/_/badges/99.png',
            'name': 'Abu Dhabi',
            'description': 'Well done, that\'s 10 edits in Abu Dhabi'
        },
        '136': {
            'location': 'Bahrain',
            'src': '/_/badges/99.png',
            'name': 'Bahrain',
            'description': 'Well done, that\'s 10 edits in Bahrain'
        },
        '137': {
            'location': 'Bangkok, Thailand',
            'src': '/_/badges/99.png',
            'name': 'Bangkok',
            'description': 'Well done, that\'s 10 edits in Bangkok'
        },
        '138': {
            'location': '北京市, 中国',
            'src': '/_/badges/99.png',
            'name': 'Beijing',
            'description': 'Well done, that\'s 10 edits in Beijing'
        },
        '139': {
            'location': 'القاهر, Egypt',
            'src': '/_/badges/99.png',
            'name': 'Cairo',
            'description': 'Well done, that\'s 10 edits in Cairo'
        },
        '140': {
            'location': 'Dubai, United Arab Emirates',
            'src': '/_/badges/99.png',
            'name': 'Dubai',
            'description': 'Well done, that\'s 10 edits in Dubai'
        },
        '141': {
            'location': 'Hong Kong',
            'src': '/_/badges/99.png',
            'name': 'Hong Kong',
            'description': 'Well done, that\'s 10 edits in Hong Kong'
        },
        '142': {
            'location': 'Kuala Lumpur, Malaysia',
            'src': '/_/badges/99.png',
            'name': 'Kuala Lumpur',
            'description': 'Well done, that\'s 10 edits in Kuala Lumpur'
        },
        '143': {
            'location': 'Singapore',
            'src': '/_/badges/99.png',
            'name': 'Singapore',
            'description': 'Well done, that\'s 10 edits in Singapore'
        },
        '144': {
            'location': '서울특별시, 한국',
            'src': '/_/badges/99.png',
            'name': 'Seoul',
            'description': 'Well done, that\'s 10 edits in Seoul'
        },
        '145': {
            'location': '上海市, 中国',
            'src': '/_/badges/99.png',
            'name': 'Shanghai',
            'description': 'Well done, that\'s 10 edits in Shanghai'
        },
        '146': {
            'location': '東京都, 日本',
            'src': '/_/badges/146.png',
            'name': 'Big in Japan',
            'description': 'Well done, that\'s 10 edits in Tokyo'
        },
        '147': {
            'location': 'Adelaide, SA, Australia',
            'src': '/_/badges/99.png',
            'name': 'Adelaide',
            'description': 'Well done, that\'s 10 edits in Adelaide'
        },
        '148': {
            'location': 'Darwin, NT, Australia',
            'src': '/_/badges/99.png',
            'name': 'Darwin',
            'description': 'Well done, that\'s 10 edits in Darwin'
        },
        '149': {
            'location': 'Melbourne, VIC, Australia',
            'src': '/_/badges/99.png',
            'name': 'Melbourne',
            'description': 'Well done, that\'s 10 edits in Melbourne'
        },
        '150': {
            'location': 'Perth, WA, Australia',
            'src': '/_/badges/99.png',
            'name': 'Perth',
            'description': 'Well done, that\'s 10 edits in Perth'
        },
        '151': {
            'location': 'Sydney, NSW, Australia',
            'src': '/_/badges/99.png',
            'name': 'Sydney',
            'description': 'Well done, that\'s 10 edits in Sydney'
        },
        '152': {
            'location': 'Cape Town, Western Cape, South Africa',
            'src': '/_/badges/99.png',
            'name': 'Cape Town',
            'description': 'Well done, that\'s 10 edits in Cape Town'
        },
        '153': {
            'location': 'Marrakesh, Marrakech-Tensift-El Haouz, Morocco',
            'src': '/_/badges/99.png',
            'name': 'Marrakesh',
            'description': 'Well done, that\'s 10 edits in Marrakesh'
        }
    }
    
    cities = [
        'amsterdam netherlands',
        'barcelona spain',
        'berlin germany',
        'budapest hungary',
        'copenhagen denmark',
        'dublin ireland',
        'edinburgh uk',
        'florence italy',
        'helsinki finland',
        'krakow poland',
        'london uk',
        'istanbul turkey',
        'lisbon portugal',
        'manchester uk',
        'madrid spain',
        'milan italy',
        'moscow russia',
        'munich germany',
        'paris france',
        'prague czech republic',
        'rome italy',
        'stockholm sweden',
        'vienna italy',
        'zurich switzerland'
        'chicago usa',
        'honolulu usa',
        'las vegas usa',
        'los angeles usa',
        'miami usa',
        'new york city usa',
        'orlando usa',
        'rio de janeiro brazil',
        'san francisco usa',
        'toronto canada',
        'washington dc usa'
        'abu dhabi uae',
        'bahrain',
        'bangkok thailand',
        'beijing china',
        'cairo egypt',
        'dubai uae',
        'hong kong',
        'kuala lumpur malaysia',
        'singapore',
        'seoul korea',
        'shanghai china',
        'tokyo japan'
        'adelaide australia',
        'auckland new zealand',
        'darwin australia',
        'melbourne australia',
        'perth australia',
        'sydney australia'
        'cape town south africa',
        'marrakesh morocco'
    ]
    
    def output(self, templateName, type = 'html', values = {}):
        
        if type == None:
            type = 'html'
        
        path = os.path.join(os.path.dirname(__file__), '../templates/' + templateName + '.' + type)
        
        if not os.path.exists(path):
            self.send404()
            return
        
        if self.request.get('pretty'):
            self.response.headers.add_header('Content-type', 'text/plain; charset=utf-8')
        else:
            self.response.headers.add_header('Content-type', self.mimetypes[type] + '; charset=utf-8')
        
        values['page'] = templateName
        values['get'] = {}
        for query in self.request.arguments():
            values['get'][query] = self.request.get(query)
        
        #self.response.headers.add_header('Cache-control', 'no-cache')
        
        if not 'self' in values:
            values['self'] = self.request.path
            
        values['hostname'] = self.request.host
        
        from google.appengine.api import users
        user = users.get_current_user()
        if user:
            values['signedin'] = {
                'userid': user.email().replace('@', '-').replace('.', '-'),
                'nickname': user.nickname(),
                'signout': users.create_logout_url(self.request.path)
            }
        else:
            values['signedout'] = {
                'ip': self.request.remote_addr,
                'signin': users.create_login_url(self.request.path)
            }
        
        self.response.out.write(template.render(path, values))
        
    def convertFlickrUrl(self, url, type = ''):
        
        if type != '':
            type = '_' + type
        
        url = re.sub(r'^(http://farm[0-9]+\.static\.flickr\.com/[0-9]+/[0-9]+_[0-9a-f]+)(?:_[stmbo])?(\.jpg)$', r'\1' + type + r'\2', url)
        
        return url
        
    def getUserId(self, user):
        from google.appengine.api import users
        
        if type(user) == users.User:
            email = user.email()
        elif type(user) == unicode or type(user) == str:
            email = user
        else:
            email = ''
        
        return email.replace('@', '-').replace('.', '-')
    
    def getUserObject(self, user = None):
        
        from google.appengine.api import users
        from models.user import User
        
        if user == None:
            user = users.get_current_user()
        
        userId = self.getUserId(user)
        if not userId:
            return None
        
        query = User.all()
        query.filter("id =", userId)
        userObject = query.get()
        
        if userObject == None:
            if type(user) == users.User:
                userObject = User(
                    id = userId,
                    username = user.nickname().split('@')[0],
                    name = user.nickname().split('@')[0]
                )
            else:
                userObject = User(
                    id = userId,
                    username = userId,
                    name = userId
                )
            userObject.put()
        
        return userObject
    
    def getLocationName(self, placemark):
        try:
            if placemark['AddressDetails']['Country']['AdministrativeArea']['SubAdministrativeArea']['AddressLine'] == placemark['AddressDetails']['Country']['AdministrativeArea']['AdministrativeAreaName']:
                raise KeyError
            return (
                placemark['AddressDetails']['Country']['AdministrativeArea']['SubAdministrativeArea']['AddressLine'],
                placemark['AddressDetails']['Country']['AdministrativeArea']['AdministrativeAreaName'],
                placemark['AddressDetails']['Country']['CountryName']
            )
        except KeyError:
            try:
                if placemark['AddressDetails']['Country']['AdministrativeArea']['SubAdministrativeArea']['SubAdministrativeAreaName'] == placemark['AddressDetails']['Country']['AdministrativeArea']['AdministrativeAreaName']:
                    raise KeyError
                return (
                    placemark['AddressDetails']['Country']['AdministrativeArea']['SubAdministrativeArea']['SubAdministrativeAreaName'],
                    placemark['AddressDetails']['Country']['AdministrativeArea']['AdministrativeAreaName'],
                    placemark['AddressDetails']['Country']['CountryName']
                )
            except KeyError:
                try:
                    if placemark['AddressDetails']['Country']['AdministrativeArea']['Locality']['LocalityName'] == placemark['AddressDetails']['Country']['AdministrativeArea']['AdministrativeAreaName']:
                        raise KeyError
                    return (
                        placemark['AddressDetails']['Country']['AdministrativeArea']['Locality']['LocalityName'],
                        placemark['AddressDetails']['Country']['AdministrativeArea']['AdministrativeAreaName'],
                        placemark['AddressDetails']['Country']['CountryName']
                    )
                except KeyError:
                    try:
                        return (
                            placemark['AddressDetails']['Country']['AdministrativeArea']['SubAdministrativeArea']['AddressLine'],
                            placemark['AddressDetails']['Country']['CountryName']
                        )
                    except KeyError:
                        try:
                            return (
                                placemark['AddressDetails']['Country']['AdministrativeArea']['SubAdministrativeArea']['SubAdministrativeAreaName'],
                                placemark['AddressDetails']['Country']['CountryName']
                            )
                        except KeyError:
                            try:
                                return (
                                    placemark['AddressDetails']['Country']['AdministrativeArea']['AdministrativeAreaName'],
                                    placemark['AddressDetails']['Country']['CountryName']
                                )
                            except KeyError:
                                return ()
    
    def get(self):
        
        path = self.request.path[1:self.request.path.find('.')]
        if os.path.exists('templates/' + path + '.html'):
            self.output(path, 'html')
        elif os.path.exists('templates' + self.request.path + '.html'):
            self.output(self.request.path[1:], 'html')
        else:
            self.send404()
    
    def send404(self):
        self.error(404)
        self.output('404', 'html')
        import logging
        logging.warning('404 error')
    
    def handle_exception(self, exception, debug_mode):
        super(Controller, self).handle_exception(exception, debug_mode)
        
        import sys, traceback
        
        exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
        
        error = "Automatically reported error generated by the site at runtime:\n\n"
        error += "\t" + str(exceptionValue) + "\n\n"
        for line in traceback.format_tb(exceptionTraceback):
            error += "\t" + line
        
        import md5
        errorHash = md5.new(unicode(exceptionValue)).hexdigest()[0:8]
        
        if not debug_mode:
            
            from google.appengine.api import memcache
            from google.appengine.api import urlfetch
            from django.utils import simplejson
            import urllib, re
            
            token = '62f3219001d6a930336f84998f23c8c3'
            
            template_values = {
                'issueId': memcache.get('errorHash_' + errorHash)
            }
            
            if not template_values['issueId']:
                
                # send error
                form_fields = {
                  'login': 'peej',
                  'token': token,
                  'title': 'Website runtime error: ' + errorHash,
                  'body': error
                }
                result = urlfetch.fetch(
                    url = 'http://github.com/api/v2/json/issues/open/peej/to.uri.st',
                #    url = 'http://github.com/api/v2/json/issues/show/peej/to.uri.st/1',
                    payload = urllib.urlencode(form_fields),
                    method = urlfetch.POST,
                    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                )
                
                if result.status_code == 200:
                    
                    response = simplejson.loads(result.content)
                    issueId = response['issue']['number']
                    memcache.add(key = 'errorHash_' + errorHash, value = issueId)
                    template_values['issueId'] = issueId
                    
                    # add label
                    urlfetch.fetch(
                        url = 'http://github.com/api/v2/json/issues/label/add/peej/to.uri.st/runtime/' + str(issueId),
                        payload = urllib.urlencode({
                          'login': 'peej',
                          'token': token
                        }),
                        method = urlfetch.POST,
                        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                    )
                    
            
            request = "Automatically reported request data of erroring request:\n\n"
            for line in str(self.request).splitlines():
                line = re.sub(r"Cookie: .+", 'Cookie: ****', line)
                request += "\t" + line + "\n"
                
            requestHash = md5.new(unicode(request)).hexdigest()[0:8]
            
            if not memcache.get('requestHash_' + requestHash):
                
                # add request data as a comment
                
                urlfetch.fetch(
                    url = 'http://github.com/api/v2/json/issues/comment/peej/to.uri.st/' + str(template_values['issueId']),
                    payload = urllib.urlencode({
                      'login': 'peej',
                      'token': token,
                      'comment': request
                    }),
                    method = urlfetch.POST,
                    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                )
                
                memcache.add(key = 'requestHash_' + requestHash, value = True)
            
            self.error(500)
            self.output('500', 'html', template_values)
        
        import logging
        logging.warning('500 error ' + errorHash)
    
    def addStat(self, user, id, subId = None):
        if user:
            try:
                user.activity = user.activity + 1
            except:
                user.activity = 1
            if subId == None:
                try:
                    user.stats[id] = user.stats[id] + 1
                except KeyError:
                    user.stats[id] = 1
                except TypeError:
                    user.stats = {}
                    user.stats[id] = 1
            else:
                try:
                    user.stats[id][subId] = user.stats[id][subId] + 1
                except (KeyError, TypeError):
                    try:
                        user.stats[id][subId] = 1
                    except KeyError:
                        user.stats[id] = {}
                        user.stats[id][subId] = 1
                    except TypeError:
                        user.stats = {}
                        user.stats[id] = {}
                        user.stats[id][subId] = 1
    
    def updateBadges(self, user):
        if user:
            
            from datetime import datetime
            
            if user.badges:
                oldBadges = user.badges.copy()
            else:
                oldBadges = {}
            
            # edits
            try:
                if user.stats[1] >= 100 and not 5 in user.badges:
                    user.badges[5] = datetime.today()
                elif user.stats[1] >= 25 and not 4 in user.badges:
                    user.badges[4] = datetime.today()
                elif user.stats[1] >= 10 and not 3 in user.badges:
                    user.badges[3] = datetime.today()
                elif user.stats[1] >= 3 and not 2 in user.badges:
                    user.badges[2] = datetime.today()
                elif user.stats[1] >= 1 and not 1 in user.badges:
                    user.badges[1] = datetime.today()
            except KeyError:
                pass
            
            # local edits
            try:
                for loc in user.stats[2]:
                    if user.stats[2][loc] >= 20 and not 7 in user.badges:
                        user.badges[7] = datetime.today()
                    elif user.stats[2][loc] >= 5 and not 6 in user.badges:
                        user.badges[6] = datetime.today()
            except KeyError:
                pass
            
            # recommended
            try:
                if user.stats[3] >= 25 and not 10 in user.badges:
                    user.badges[10] = datetime.today()
                elif user.stats[3] >= 5 and not 9 in user.badges:
                    user.badges[9] = datetime.today()
                elif user.stats[3] >= 1 and not 8 in user.badges:
                    user.badges[8] = datetime.today()
            except KeyError:
                pass
            
            # picture
            try:
                if user.stats[4] >= 20 and not 12 in user.badges:
                    user.badges[12] = datetime.today()
                elif user.stats[4] >= 5 and not 11 in user.badges:
                    user.badges[11] = datetime.today()
            except KeyError:
                pass
            
            # info tags
            try:
                if user.stats[5] >= 3 and not 13 in user.badges: # dupe
                    user.badges[13] = datetime.today()
                if user.stats[12] >= 3 and not 20 in user.badges: # delete
                    user.badges[20] = datetime.today()
            except KeyError:
                pass
            
            # comments
            try:
                if user.stats[6] >= 25 and not 16 in user.badges:
                    user.badges[16] = datetime.today()
                elif user.stats[6] >= 5 and not 15 in user.badges:
                    user.badges[15] = datetime.today()
                elif user.stats[6] >= 1 and not 14 in user.badges:
                    user.badges[14] = datetime.today()
            except KeyError:
                pass
            
            # idiot
            try:
                if user.stats[8] >= 3 and not 18 in user.badges:
                    user.badges[18] = datetime.today()
                if user.stats[9] >= 3 and not 19 in user.badges:
                    user.badges[19] = datetime.today()
            except KeyError:
                pass
            
            # type
            try:
                for badgeId in user.stats[11]:
                    if user.stats[11][badgeId] >= 10 and not badgeId in user.badges:
                        user.badges[badgeId] = datetime.today()
            except KeyError:
                pass
            
            # location
            for badgeId in self.badges.keys():
                try:
                    if user.stats[2][self.badges[badgeId]['location']] >= 10 and not badgeId in user.badges:
                        user.badges[badgeId] = datetime.today()
                except KeyError:
                    pass
            
            return [val for val in user.badges if val not in oldBadges]
        
        else:
            return False
