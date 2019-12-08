from mycroft import MycroftSkill, intent_file_handler
from lingua_franca.parse import extract_numbers, normalize


class NavigationExample(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        self.navigation_active = True
        self.settings["homecity"] = self.settings.get('homecity', "London")
        self.settings["homestreet"] = self.settings.get('homestreet', "Winkelgasse")
        self.settings["homenumber"] = self.settings.get('homenumber', "1")
        self.street = None
        self.city = None
        self.street_number = None
        #self.navigation_active = self.is_navigation()
        self.register_intent_file('home.intent', self.home)
        self.register_intent_file('alternative.route.intent', self.alternative_route)
        self.register_intent_file('navigation.intent', self.navigation)
        self.register_intent_file('how.far.intent', self.how_far)
        self.register_intent_file('where.am.i.intent', self.where_am_i)
        self.register_intent_file('where.was.i.intent', self.where_was_i)

    def navigation(self, message):
        self.city = message.data.get("city", None)
        self.street = message.data.get("street", None)
        self.street_number = message.data.get("street_number", "1")
        lang = self.lang
        extract_number = extract_numbers(self.street, short_scale=False, ordinals=False,
                            lang="en-us")
        if not int(extract_number) is None:
            self.street_number = extract_number
        self.speak_dialog('route', data={"city": self.city, "street": self.street, "number": self.street_number})

    def alternative_route(self, message):
        route = None
        if self.is_navigation is True:
            if route is None:
                self.speak_dialog('no.alternative')
            else:
                self.speak_dialog('alternative.route')
        else:
            self.speak_dialog('no.route')

    def go_home(self, message):
        self.speak_dialog('arrival')

    def home(self, message):
        self.city = self.settings["homecity"]
        self.street = self.settings["homestreet"]
        self.street_number = self.settings["homenumber"]
        self.navigation_active = True
        self.speak_dialog('home')


    def how_far(self, message):
        distance = "0"
        time = "0"
        if self.is_navigation is True:
            self.speak_dialog('how.far', data={"time": time, "street": self.street, "distance": distance})
        else:
            self.speak_dialog('no.route')

    def where_am_i(self, message):
        city = "münchen"
        street = "baumgasse"
        self.speak_dialog('where.am.i', data={"city": city, "street": street,})

    def where_was_i(self, message):
        location = "münchen baumgasse"
        self.speak_dialog('where.was.i', data={"location": location})

    def is_navigation(self):
        if self.navigation_active is True:
            return True
        else:
            return False

    def shutdown(self):
        super(NavigationExample, self).shutdown()

def create_skill():
    return NavigationExample()

