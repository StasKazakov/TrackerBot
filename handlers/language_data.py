class LangMoodel:
    UA = 'ua'
    EN = 'en'
    RU = 'ru'

class Text(LangMoodel):
    def __init__(self):
        super().__init__()

    @staticmethod
    def choose_language(self):
        text = 'Hello!\n Please, choose your language:'
        return text

    def menu(self, lang):
        if lang == self.UA:
            return "Оберіть опцію: "
        elif lang == self.EN:
            return "Choose the option"
        elif lang == self.RU:
            return "Выберите опцию:"