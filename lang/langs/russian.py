# Language samples file

class Samples:
    def __init__(self):
        #COMMANDS
        self.PP = ('За [https://osu.ppy.sh/b/{} {} [{}]{}] (OD {}, AR {}, '
                    'CS {}, {}★, {}:{}) вы получите {} {}')

        self.PP_FOR = ('| {}pp за {}% ')

        self.PP_PRED = ('За [https://osu.ppy.sh/b/{} {} [{}]{}] (OD {}, AR {}, '
                        'CS {}, {}★, {}:{}) вы получите {} {} # {}')

        self.PP_PRED_IMPOSSIBLE = ("Увы, но вы пока не в состоянии ФК'шнуть это :<")

        self.PP_PRED_FUTURE = ('Вы должны получить: {}pp')

        self.INFO = ('Исходный код и информация о командах может быть найдена '
                    '[https://suroryz.github.io/surbot-osu/ тут]')

        self.LANG_CHANGED = ('Язык успешно изменен. Переводчик: SuRory')

        # Maps
        self.MAP_SUCCESS_PUSH = ('Вы успешно проголосовали за карту. Спасибо за отзыв!')

        self.MAP_SUCCESS_DROP = ('Вы успешно проголосовали против карты. Спасибо за отзыв!')

        self.MAP_TOP = ('[https://osu.ppy.sh/b/{} {}] {}★ {} # Рейтинг: {}')

        self.MAP_RECENT = ('Последняя карта, что я получил: [https://osu.ppy.sh/b/{} {}] {}★ {}')

        # Users
        self.USER_STAT_FOR = ('Статистика игрока {}:')

        self.USER_STAT_ACC = ('Аккуратность: {}%')

        self.USER_STAT_PP = ('PP: {}pp')

        self.USER_STAT_STARAVG = ('Среднее значение звезд: {}★')

        # ERRORS
        self.ERROR_MAP_PUSHED_ALREADY = ('Вы уже проголосовали за карту')

        self.ERROR_SYNTAX = ('Вы ввели что-то неправильно. Посмотрите страницу помощи -> .info')

        self.ERROR_NP_NEED = ('Перед использованием команды, напишите /np')

        self.ERROR_NO_LANGUAGE = ('Извините, но я не могу найти ваш язык в моей базе. '
                                    'Попробуйте использовать код языка ISO 639-1. '
                                    'Если ваш язык просто не поддерживается, вы можете помочь переводом '
                                    '[https://suroryz.github.io/surbot-osu/lang/langs тут]')

