from mycroft import MycroftSkill, intent_file_handler
from lingua_franca.parse import extract_numbers, normalize
from mycroft.util.log import LOG, getLogger
import re


class NavigationExample(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        self.navigation_active = True
        self.street = None
        self.city = None
        self.street_number = None
        self.voice_proxy
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
        self.street_number = message.data.get("number", None)
        lang = self.lang
        if self.street is None:
            self.street = self.get_response('witch.street', data={"city": self.city,})
        #self.log.info('nummber: ' + str(self.street_number))
        #self.log.info('street: ' + str(self.street))
        if self.street_number is None:
            extract_number = re.findall(r'\d+', self.street)
            self.street_number = ' '.join(extract_number)
            self.log.info('House nummber: ' + str(extract_number))
            self.street = self.street.replace(self.street_number, '')
        if not self.street_number.isdigit():
            self.street_number = self.get_response('witch.number', data={"street": self.street})
        self.speak_dialog("route", data={"city": self.city, "street": self.street, "number": self.street_number})
        self.schedule_repeating_event(self.voice_proxy, None, 1,
                                          name='navigation_voice_proxy')
        self.navigation_active = True


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
        self.cancel_scheduled_event('navigation_voice_proxy')
        self.navigation_active = False

    def home(self, message):
        self.city = self.settings.get('homecity', "London")
        self.street = self.settings.get('homestreet', "Winkelgasse")
        self.street_number = self.settings.get('homenumber', "1")
        self.navigation_active = True
        self.speak_dialog('home')
        self.navigation_active = True
        self.schedule_repeating_event(self.voice_proxy, None, 1,
                                          name='navigation_voice_proxy')


    def how_far(self, message):
        distance = "0"
        time = "0"
        if self.is_navigation is True:
            self.speak_dialog("how.far", data={"time": time, "street": self.street, "distance": distance})
        else:
            self.speak_dialog('no.route')

    def where_am_i(self, message):
        city = "münchen"
        street = "baumgasse"
        self.speak_dialog("where.am.i", data={"city": city, "street": street,})

    def where_was_i(self, message):
        target = "münchen baumgasse"
        self.speak_dialog("where.was.i", data={"target": target})

    def is_navigation(self):
        if self.navigation_active is True:
            return True
        else:
            self.cancel_scheduled_event('navigation_voice_proxy')
            return False

    def voice_proxy(self):
        self.log.info("check for navigation commands")  
        #if command:
        #    self.speak(command)

    def shutdown(self):
        super(NavigationExample, self).shutdown()
        self.cancel_scheduled_event('navigation_voice_proxy')
        self.settings.update

def create_skill():
    return NavigationExample()

