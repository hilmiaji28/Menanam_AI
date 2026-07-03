class EvaluationMetrics:

    def __init__(self):

        self.total = 0

        self.correct = 0

    def update(
        self,
        expected,
        predicted,
    ):

        self.total += 1

        if expected == predicted:

            self.correct += 1

    def accuracy(self):

        if self.total == 0:

            return 0

        return self.correct / self.total