class taskProgress:
    def __init__(self):
        self.total = 0
        self.steps = 0

    def step(self):
        if self.steps != self.total:
            self.steps += 1     

    def reset(self,total):
        self.total = total
        self.steps = 0

    @property
    def percentage(self):
        return int(self.steps/self.total*100)