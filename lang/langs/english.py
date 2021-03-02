# Language samples file

class Samples:
    def __init__(self):
        # COMMANDS
        self.PP = ('For [https://osu.ppy.sh/b/{} {} [{}]{}] (OD {}, AR {}, '
                        "CS {}, {}★, {}:{}) you'll get {} {}")

        self.PP_FOR = ('| {}pp for {}% ')

        self.PP_PRED = ('For [https://osu.ppy.sh/b/{} {} [{}]{}] (OD {}, AR {}, '
                            "CS {}, {}★, {}:{}) you'll get {} {} # {}")

        self.PP_PRED_IMPOSSIBLE = ('Impossible to FC for you :<')

        self.PP_PRED_FUTURE = ('Expected for you: {}pp')

        self.INFO = ('You can find source & contact & info '
                    '[https://suroryz.github.io/surbot-osu/ here]')

        self.LANG_CHANGED = ('Language successful changed. '
                            'Localizer: SuRory')

        # Maps
        self.MAP_SUCCESS_PUSH = ('Map pushed successful. Thanks for your vote!')

        self.MAP_SUCCESS_DROP = ('Map droped successful. Thanks for your vote!')

        self.MAP_TOP = ('[https://osu.ppy.sh/b/{} {}] {}★ {} # Rating: {}')

        self.MAP_RECENT = ('Last map I got: [https://osu.ppy.sh/b/{} {}] {}★ {}')

        # Users
        self.USER_STAT_FOR = ('Stats for {}:')

        self.USER_STAT_ACC = ('Accuracy: {}%')

        self.USER_STAT_PP = ('PP: {}pp')

        self.USER_STAT_STARAVG = ('Average star rating: {}★')

        # ERRORS
        self.ERROR_MAP_PUSHED_ALREADY = ('You already vote for this map')

        self.ERROR_SYNTAX = ('You entered something incorrect. Check help page -> .info')

        self.ERROR_NP_NEED = ('You need to use /np before')

        self.ERROR_NO_LANGUAGE = ("Sorry, but I can't find your language in my base. "
                                    'Try to use ISO 639-1 language code. '
                                    'If there just no your language, you can contribute '
                                    '[https://suroryz.github.io/surbot-osu/lang/langs here]')

