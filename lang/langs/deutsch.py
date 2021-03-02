class Samples:
    def __init__(self):
        #COMMANDS
        self.PP = ('Für [https://osu.ppy.sh/b/{} {} [{}]{}] (OD {}, AR {}, '
                        'CS {}, {}★, {}:{}) wirst du {} {}')

        self.PP_FOR = ('| {}pp bekommen für {}% ')

        self.PP_PRED = ('Für [https://osu.ppy.sh/b/{} {} [{}]{}] (OD {}, AR {}, '
                            'CS {}, {}★, {}:{}) wirst du {} {} # {}')

        self.PP_PRED_IMPOSSIBLE = ('Unmöglich zu FC für dich')

        self.PP_PRED_FUTURE = ('Es erwarten dich: {}pp')

        self.INFO = ('Sie kannst Quelle und Information '
                    '[https://suroryz.github.io/surbot-osu/ hier] finden')

        self.LANG_CHANGED = ('Sprache erfolgreich geändert. '
                            'Localizer: some HiNative guy')

        #ERRORS
        self.ERROR_SYNTAX = ('Sie hast etwas falsches eingegeben. '
                            'Kontrollieren Sie die Hilfeseite -> .info')

        self.ERROR_NP_NEED = ('Sie müssen /np vorher verwenden')

        self.ERROR_NO_LANGUAGE = ('Entschuldigung, aber ich kann deine/Ihre Sprache nicht in meiner Datenbank finden. '
                                    'Versuchen Sie den ISO 639-1 Sprachen-Code zu nutzen. '
                                    'Wenn Ihre dort nicht vorzufinden ist, können Sie das '
                                    '[https://suroryz.github.io/surbot-osu/lang/langs hier] melden')
