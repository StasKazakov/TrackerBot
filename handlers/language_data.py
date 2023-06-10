class LangMoodel:   # all languages in our system
    UA = 'ua'
    EN = 'en'
    RU = 'ru'

class Text(LangMoodel):
    def __init__(self):
        super().__init__()

    @staticmethod
    def choose_language(self):    # choosing new language
        text = 'Hello!\n Please, choose your language:'
        return text

    def menu(self, lang):   # function for a main menu
        if lang == self.UA:
            return "Оберіть опцію: "
        elif lang == self.EN:
            return "Choose the option"
        elif lang == self.RU:
            return "Выберите опцию:"

    def for_new_user(self, lang):   # short instruction for new user
        if lang == self.UA:
            return "Для того щоб почати відстежувати кількість переховувань за посиланнями, натисніть кнопку 'Додати посилання' і надішліть посилання для відстеження."
        elif lang == self.EN:
            return "To start tracking the number of link conversions, click 'Add Link' button and send in the tracking link."
        elif lang == self.RU:
            return "Для того чтобы начать отслеживать количество переховов по ссылкам, нажмите кнопку 'Добавить ссылку' и пришлите ссылку для отслеживания."

    def for_old_user(self, lang):   # notification of the user about his language
        if lang == self.UA:
            return "Тепер ваша мова українська."
        elif lang == self.EN:
            return "Now your language is English."
        elif lang == self.RU:
            return "Теперь ваш язык русский."

    def awaiting_the_link(self, lang):   # message in state awaiting link
        if lang == self.UA:
            return "Надішліть посилання для відстеження кількості переходів."
        elif lang == self.EN:
            return "Send me a link to track the amount of conversions."
        elif lang == self.RU:
            return "Пришлите ссылку для отслеживания колличества переходов."

    def incorrect_link(self, lang):
        if lang == self.UA:
            return "Некоректне посилання, спробуйте ще раз. Посилання має містити 'https'."
        elif lang == self.EN:
            return "Incorrect link, try again. The link must contain 'https'."
        elif lang == self.RU:
            return "Некорректная ссылка, попробуйте еще раз. Ссылка должна содержать 'https'."

    def instruction_for_report(self, lang):  # funtion with help user with reporting
        if lang == self.UA:
            return "Нижче👇 напишіть повідомлення для розробників.\n Найближчим часом його прочитають, відповідь ви отримаєте повідомленням від бота"
        elif lang == self.EN:
            return "Below👇 write a message to the developers.\n It will be read soon, you will get a reply you will receive a message from the bot."
        elif lang == self.RU:
            return "Ниже👇 напишите сообщение для разработчиков.\n В ближайшее время его прочтут, ответ вы получите сообщением от бота"

    def answer_on_report(self, lang):
        if lang == self.UA:
            return "Дякуємо за звернення, дуже скоро ви отримаєте відповідь"
        elif lang == self.EN:
            return "Thank you for contacting us, you will receive an answer very soon."
        elif lang == self.RU:
            return "Спасибо за обращение, очень скоро вы получите ответ"

    def after_canselling(self, lang):
        if lang == self.UA:
            return "Добре, ви будете повернуті у головне меню"
        elif lang == self.EN:
            return "Ok, you will be returned to main menu"
        elif lang == self.RU:
            return "Хорошо, вы будете возвращены в главное меню"