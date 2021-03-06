from google.appengine.ext import db
import re

from controllers.controller import Controller
from models.attraction import Attraction

class EditPage(Controller):
    
    def get(self, attractionId = None):
        
        template_values = {}
        template_values['lat'] = 0
        template_values['lon'] = 0
        
        if attractionId:
            query = Attraction.all()
            query.filter("id =", attractionId)
            attraction = query.get()
            
            if attraction:
                attraction.picture = self.convertFlickrUrl(attraction.picture, 'm')
                template_values['attraction'] = attraction
                
            else:
                self.output('404', 'html')
                return
        
        else:
            try:
                coords = self.request.get('c').split(',')
                template_values['lat'] = "%.2f" % float(coords[0])
                template_values['lon'] = "%.2f" % float(coords[1])
            except:
                pass
        
        self.output('edit', 'html', template_values)
    
    
    def post(self, attractionId = None):
        
        template_values = {}
        template_values['lat'] = 0
        template_values['lon'] = 0
        
        attraction = {}
        attraction['id'] = attractionId
        attraction['name'] = self.request.get('name')
        attraction['description'] = self.request.get('description')
        attraction['location'] = {}
        attraction['location']['lat'] = self.request.get('lat')
        attraction['location']['lon'] = self.request.get('lon')
        attraction['href'] = self.request.get('href')
        attraction['picture'] = self.request.get('picture')
        attraction['tags'] = self.request.get('tags').split(' ')
        
        if self.request.get('location.x') and self.request.get('location.y'):
            attraction['location']['lat'] = float(attraction['location']['lat']) - ((float(self.request.get('location.y')) - 75) / 18000) + 0.001
            attraction['location']['lon'] = float(attraction['location']['lon']) + ((float(self.request.get('location.x')) - 150) / 12000)
        
        errors = {}
        
        if self.request.get('title') != 'don\'t spam me bro!':
            try:
                self.redirect('/attractions/' + attractionId + '.html')
            except:
                self.redirect('/')
            return
        
        if len(attraction['name']) == 0:
            errors['name'] = True
            errors['name_empty'] = True
        if len(attraction['name']) > 100:
            errors['name'] = True
            errors['name_long'] = True
        
        if len(attraction['description']) > 5000:
            errors['description'] = True
        
        if not attraction['location']['lat'] or float(attraction['location']['lat']) < -90 or float(attraction['location']['lat']) > 90:
            errors['location'] = True
        
        if not attraction['location']['lon'] or float(attraction['location']['lon']) < -180 or float(attraction['location']['lon']) > 180:
            errors['location'] = True
        
        if not len(attraction['href']) == 0 and not re.match(r"^https?://.+$", attraction['href']):
            errors['href'] = True
        
        if not len(attraction['picture']) == 0 and not re.match(r"^https?://.+$", attraction['picture']):
            errors['picture'] = True
        
        for key, tag in enumerate(attraction['tags']):
            if tag == '':
                del attraction['tags'][key]
            elif not re.match(r"^[a-z0-9]+$", tag):
                errors['tags'] = True
        
        if errors or (self.request.get('location.x') and self.request.get('location.y')):
            
            attraction['picture'] = self.convertFlickrUrl(attraction['picture'], 'm')
            
            template_values['attraction'] = attraction,
            template_values['errors'] = errors
            
            self.output('edit', 'html', template_values)
            
        else:
            
            if attractionId: # editing
                next = attractionId
                while next: # walk to newest version of this attraction
                    query = Attraction.all()
                    query.filter("id =", next)
                    latestAttraction = query.get()
                    next = latestAttraction.next
                
            else: # creating
                
                latestAttraction = None
            
            try:
                user = self.getUserObject() # create user object if it doesn't exist
                if user:
                    
                    if latestAttraction:
                        newAttraction = db.run_in_transaction(self.createAttraction, latestAttraction.key(), attraction)
                        sameEditor = (user.id == latestAttraction.userid)
                    else:
                        newAttraction = db.run_in_transaction(self.createAttraction, None, attraction)
                        sameEditor = False
                    
                    # update stats
                    if not sameEditor:
                        self.addStat(user, 1) # new edit
                        if newAttraction.region != 'Unknown location':
                            parts = newAttraction.region.split(",")
                            region = ",".join(parts[-2:]).strip(" ")
                            self.addStat(user, 2, region) # edit location
                    if latestAttraction and newAttraction.picture != '' and latestAttraction.picture == '':
                        self.addStat(user, 4) # new picture
                    if latestAttraction and 'dupe' in newAttraction.tags and 'dupe' not in latestAttraction.tags:
                        self.addStat(user, 5) # new dupe tag added
                    if latestAttraction and 'delete' in newAttraction.tags and 'delete' not in latestAttraction.tags:
                        self.addStat(user, 12) # new delete tag added
                    if latestAttraction \
                        and newAttraction.name == latestAttraction.name \
                        and newAttraction.description == latestAttraction.description \
                        and newAttraction.href == latestAttraction.href \
                        and newAttraction.picture == latestAttraction.picture \
                        and newAttraction.tags == latestAttraction.tags:
                        self.addStat(user, 8) # no change idiot
                    
                    # type edit
                    if not sameEditor:
                        for badge in self.badges.items():
                            try:
                                if badge[1]['tag'] in newAttraction.tags:
                                    self.addStat(user, 11, badge[0])
                            except KeyError:
                                pass
                        
                        if newAttraction.region != 'Unknown location':
                            for badge in self.badges.items():
                                try:
                                    if str(badge[1]['location']) in newAttraction.region:
                                        self.addStat(user, 10, badge[0])
                                except:
                                    pass
                    
                    newBadges = self.updateBadges(user)
                    user.put()
                    
                    if newBadges:
                        self.redirect('/badges/%s.html' % newBadges.pop(0))
                        return
                
                try:
                    self.redirect('/attractions/' + newAttraction.id + '.html')
                except:
                    self.redirect('/')
                return
                
            except db.TransactionFailedError:
            
                template_values['attraction'] = attraction
                template_values['errors'] = {
                    'save': True
                }
                
                self.output('edit', 'html', template_values)
    
    def createAttraction(self, key, attractionData):
        
        from google.appengine.api import users
        from django.utils import simplejson
        import urllib, md5
        
        user = users.get_current_user()
        if type(user) == users.User:
            attractionData['userid'] = self.getUserId(user.email())
            attractionData['username'] = user.nickname()
        else:
            attractionData['userid'] = None
            attractionData['username'] = self.request.remote_addr
        
        region = 'Unknown location'
        
        url = "http://maps.google.com/maps/geo?q=%.2f,%.2f&sensor=false" % (float(attractionData['location']['lat']), float(attractionData['location']['lon']))
        jsonString = urllib.urlopen(url).read()
        if jsonString:
            data = simplejson.loads(jsonString)
            for placemark in data['Placemark']:
                region = ", ".join(self.getLocationName(placemark))
                if region:
                    break
        
        if key:
            oldAttraction = db.get(key)
            attractionData['root'] = oldAttraction.root
            attractionData['previous'] = oldAttraction.id
            attractionData['free'] = oldAttraction.free
            attractionData['rating'] = oldAttraction.rating
            attractionData['free'] = oldAttraction.free
        else:
            oldAttraction = None
            attractionData['root'] = None
            attractionData['previous'] = None
            attractionData['free'] = True
            attractionData['rating'] = 0
            attractionData['free'] = True
        
        if not attractionData['free']:
            import difflib
            s = difflib.SequenceMatcher(None, oldAttraction.description, attractionData['description'])
            if s.ratio() < 0.5:
                attractionData['free'] = True
        
        newAttraction = Attraction(
            parent = oldAttraction,
            root = attractionData['root'],
            previous = attractionData['previous'],
            name = attractionData['name'],
            region = region,
            description = attractionData['description'],
            location = db.GeoPt(
                lat = attractionData['location']['lat'],
                lon = attractionData['location']['lon']
            ),
            geobox = str(round(float(attractionData['location']['lat']), 1)) + ',' + str(round(float(attractionData['location']['lon']), 1)),
            href = attractionData['href'],
            picture = attractionData['picture'],
            tags = attractionData['tags'],
            free = attractionData['free'],
            rating = attractionData['rating'],
            userid = attractionData['userid'],
            username = attractionData['username']
        )
        
        newAttraction.id = md5.new(unicode(newAttraction)).hexdigest()
        if not newAttraction.root:
            newAttraction.root = newAttraction.id
        newAttraction.put()
        
        if oldAttraction:
            oldAttraction.next = newAttraction.id
            oldAttraction.put()
        
        return newAttraction
