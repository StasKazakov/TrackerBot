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

    def message_for_new_user(self, lang: str) -> str:
        if lang == self.EN:
            return "To start tracking the number of link conversions, click 'Add Link' button and send in the tracking link."
        elif lang == self.UA:
            return "Для того щоб почати відстежувати кількість переховувань за посиланнями, натисніть кнопку 'Додати посилання' і надішліть посилання для відстеження."
        elif lang == self.RU:
            return "Для того чтобы начать отслеживать количество переховов по ссылкам, нажмите кнопку 'Добавить ссылку' и пришлите ссылку для отслеживания."

    def message_for_old_user(self, lang: str) -> str:
        if lang == self.EN:
            return "Now your language is English."
        elif lang == self.UA:
            return "Тепер ваша мова українська."
        elif lang == self.RU:
            return "Теперь ваш язык русский."

    def resourse_name(self, lang: str) -> str:
        if lang == self.EN:
            return "Write the name of the resource to track."
        elif lang == self.UA:
            return "Напишіть назву ресурсу для відстеження."
        elif lang == self.RU:
            return "Напишите название ресурса для отслеживания."

    def link_awaiting(self, lang: str) -> str:
        if lang == self.EN:
            return "Send me a link to track the amount of conversions."
        elif lang == self.UA:
            return "Надішліть посилання для відстеження кількості переходів."
        elif lang == self.RU:
            return "Пришлите ссылку для отслеживания колличества переходов."

    def link_getter(self, lang: str) -> str:
        if lang == self.EN:
            return "Here's the link you need to use to count the conversions on it."
        elif lang == self.RU:
            return "Вот ссылка которую нужно использовать чтобы считать по ней переходы."
        elif lang == self.UA:
            return "Ось посилання, яке потрібно використовувати, щоб рахувати за ним переходи."

    def wrong_link(self, lang: str) -> str:
        if lang == self.EN:
            return "Incorrect link, try again. The link must contain 'https'."
        elif lang == self.UA:
            return "Некоректне посилання, спробуйте ще раз. Посилання має містити 'https'."
        elif lang == self.RU:
            return "Некорректная ссылка, попробуйте еще раз. Ссылка должна содержать 'https'."

    def statisics_without_link(self, lang: str) -> str:
        if lang == self.EN:
            return "Error, you don't have any links added yet."
        elif lang == self.UA:
            return "Помилка, у вас поки що немає доданих посилань"
        elif lang == self.RU:
            return "Ошибка, у вас пока нет добавленных ссылок"

    def choosing_link(self, lang: str) -> str:
        if lang == self.EN:
            return "Select the link where you want to get the statistics"
        elif lang == self.UA:
            return "Оберіть посилання, за яким хочете отримати статистику"
        elif lang == self.RU:
            return "Выберете ссылку по которой хотите получить статистику"

    def choosing_period(self, lang: str) -> str:
        if lang == self.EN:
            return "For what period do you want statistics?"
        elif lang == self.UA:
            return "За який період ви хочете отримати статистику?"
        elif lang == self.RU:
            return "За какой период вы хотите получить статистику?"

    def contacts(self, lang: str) -> str:
        if lang == self.EN:
            return "Below👇 write a message to the developers.\nIt will be read soon, you will get a reply you will receive a message from the bot."
        elif lang == self.UA:
            return "Нижче👇 напишіть повідомлення для розробників.\nНайближчим часом його прочитають, відповідь ви отримаєте повідомленням від бота"
        elif lang == self.RU:
            return "Ниже👇 напишите сообщение для разработчиков.\nВ ближайшее время его прочтут, ответ вы получите сообщением от бота"

    def thanks(self, lang: str) -> str:
        if lang == self.EN:
            return "Thank you for contacting us, you will receive an answer very soon."
        elif lang == self.UA:
            return "Дякуємо за звернення, дуже скоро ви отримаєте відповідь"
        elif lang == self.RU:
            return "Спасибо за обращение, очень скоро вы получите ответ"