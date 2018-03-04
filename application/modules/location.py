from collections import OrderedDict

class Location:
    def __init__(self, result, api, query):
        if api == 'google':
            self.google_init(result)
            self.src = 'google'
            self.query = query

    def google_init(self, result):
        [setattr(self, key, result[0]['geometry']['location'][key]) for key in ['lat', 'lng']]
        components = result[0]['address_components']
        self.address_components = OrderedDict([(component['types'][0], component['long_name']) for component in components])
        [setattr(self, key, self.address_components[key]) for key in self.address_components]
