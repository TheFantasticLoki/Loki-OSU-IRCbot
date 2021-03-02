from language import Language
from pppredict.userApi import user

COUNTRYS_LANGS = {'English': ['US'],
                  'Russian': ['RU']}

DEFAULT = 'English'     # Default language


# Init class. Language for a user sets by this class
class Initialization:
    def __init__(self):
        '''
            NEED HELP TO COMPLETE THIS DICT!

            If you want to add some countries use this format:
            Language: [ISO_3166-1_alpha-2 coutries codes]
        '''
        self.COUNTRIES_LANGS: dict = {'English': ['US', 'CA', 'UK'],
                                        'Russian': ['RU', 'UA', 'BY', 'KZ'],
                                        'Deutsch': ['DE', 'CH']}

        self.DEFAULT = 'English'

    # Adds user to db if first one is not in base. Else returns nothing
    def new(self, name: str) -> None:
        lang: Language = Language(name)
        if lang.exists():
            return

        self.user = user.User()
        self.user.setParams(name)
        data: dict = self.user.getData()

        country: str = data['country']
        local: str = DEFAULT

        for language in self.COUNTRIES_LANGS:
            if country in self.COUNTRIES_LANGS[language]:
                local = language

        lang.insert_language(local)

    # Sets language for user
    def set(self, name: str, language: str) -> None:
        lang: Language = Language(name)
        lang.set_language(language)
