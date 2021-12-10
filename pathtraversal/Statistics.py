import csv


class Metric:
    def __init__(self):
        self.score = 0
        self.nodes_expanded = 0
        self.turn = 0

    def flush_metric(self, fname):
        fields = [self.turn, self.score, self.nodes_expanded]
        with open(fname, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(fields)