from mycroft import MycroftSkill, intent_file_handler


class NavigationExample(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('example.navigation.intent')
    def handle_example_navigation(self, message):
        self.speak_dialog('example.navigation')


def create_skill():
    return NavigationExample()

