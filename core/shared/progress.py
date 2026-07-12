class taskProgress:
    def __init__(self):
        self.total = 0
        self.steps = 0

    def step(self):
        self.total += 1     # Podria poner una excepcion aca por si se pasa del 100% pero algo me dice que es al pedo

    def reset(self,total):
        self.total = total
        self.steps = 0

    @property
    def percentage(self):
        return int(self.steps/self.total*100)