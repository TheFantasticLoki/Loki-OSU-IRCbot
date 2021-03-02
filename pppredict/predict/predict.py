from users import Users as us


#Prediction class
class Prediction:
    def __init__(self):
        self.name: str = ''
        self.stars: float = 0.0
        self.user_stats: list = list()
        self.predicted: float = 100.0

    def predict(self, user: str, stars: float) -> None:
        self.name = user
        self.stars = stars

        # Getting info about player and his scores
        self.user_data = us.getStat(user)
        self.user_stats = {'acc': self.user_data[1],
                           'star_avg': self.user_data[3]}

        # Process prediction
        self.process()

    def process(self) -> None:
        # Set range around user's acc
        acc_range: float = self.user_stats['acc'] * (1 - self.user_stats['acc']/100)
        max_ = min(100, self.user_stats['acc'] + (acc_range*1.625))
        min_ = abs(self.user_stats['acc'] - (acc_range*1.625))


        if self.stars - self.user_stats['star_avg'] > 1.5:
            self.predicted = "Impossible"
            return
        # Calc acc
        self.predicted = max(min_, min(max_, self.user_stats['acc']+ (self.user_stats['star_avg']-self.stars) * (8*acc_range/self.user_stats['star_avg'])))
