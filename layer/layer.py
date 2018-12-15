import pandas as pd

class Layer(object):
    """ a layer of matter memory """

    def __init__(self, layer_number: int = 0, symbol_count: int = 0):
        ''' at this point we don't even need args '''
        self.layer_number = layer_number
        self.symbol_count = symbol_count
        self.latest_name = -1
        self.named_patterns = []  # the index is the name
        self.observed_patterns = {}  # pattern as list: count of observations
        self.current_pattern = []
        self.current_predictions = []
        self.higher_layer = ()

    def pattern_is_complete(self):
        if len(self.current_pattern) == 2:
            return True
        return False

    def accept_input_from_below(self, input: int):
        self.current_pattern.append(input)
        print('me --', self.layer_number)
        print('self.current_pattern---', self.current_pattern)
        #print('self.pattern_is_complete', self.pattern_is_complete())
        if self.pattern_is_complete():
            # record new observation or count rerun
            self.manage_observed()

            # send up and get prediction of transition back
            current_predictions = self.send_pattern_up()
            self.current_predictions = current_predictions if current_predictions is not None else []

            # tell lower what pattern correspond to predicted transitions
            predictions = self.return_transitions()

            if self.pattern_is_complete():
                self.current_pattern = []

            return predictions

        # say what you think is next
        predictions = self.return_predictions()
        if self.pattern_is_complete():
            self.current_pattern = []

        return predictions

    def manage_observed(self):
        if self.current_pattern in self.named_patterns:
            self.observed_patterns[self.get_name_of_pattern()] += 1
        else:
            self.named_patterns.append(self.current_pattern)
            self.latest_name += 1
            self.observed_patterns[self.latest_name] = 1

    def get_name_of_pattern(self, pattern=None):
        pattern = pattern or self.current_pattern
        return self.named_patterns.index(pattern)
    #def get_name_of_pattern_dict(self):  # may want to use this if we use SDRs
    #    return [k for k, v in self.named_patterns.items() if v == self.current_pattern][0]

    def get_pattern_of_name(self, name=None):
        name = name or self.current_predictions[0][0]
        return self.named_patterns[name]

    def send_pattern_up(self):
        if self.higher_layer == ():
            # create a new layer above me
            self.higher_layer = Layer(self.layer_number+1)
        # pass my completed pattern to them by integer
        return self.pass_up_name(self.get_name_of_pattern())

    def pass_up_name(self, name):
        return self.higher_layer.accept_input_from_below(name)

    def return_predictions(self):
        ''' currently this assumes a binary symbol_count only '''
        print('IN PREDICTION')

        # get possible next patterns based on what we've seen
        possibilities = [
            (tail, self.observed_patterns[name])
            for name, (head, tail) in enumerate(self.named_patterns)
            if head == self.current_pattern[0]]

        # filter out possibilities not predicted in current_predictions
        #if len(self.current_predictions) > 0:
        #    possibilities = [
        #        (second, v) for second, v in self.possibilities
        #        if k[0] == self.current_predictions[0]]
        #    print('1possibilities', possibilities)

        # convert to dictionary with unique keys
        unique_possibilities = {}
        for t, v in possibilities:
            if t in unique_possibilities.keys():
                unique_possibilities[t] += v
            else:
                unique_possibilities[t] = v

        # get total of all values (count of observations)
        total = sum(unique_possibilities.values())

        # return as pattern : confidence probabilities
        return [(k, v / total) for k, v in unique_possibilities.items()]


    def return_transitions(self):
        ''' look at all the predictions that were given to me, give the next lower pattern in those. '''
        print('IN TRANSITION')

        # filter out possibilities not predicted in current_predictions
        if len(self.current_predictions) > 0:
            possibilities = [
                (self.get_pattern_of_name(name)[-1], confidence, self.observed_patterns[name])
                for name, confidence in self.current_predictions]
            unique_possibilities = {}
            for tail, given_confidence, observed_confidence in possibilities:
                if tail in unique_possibilities.keys():
                    unique_possibilities[tail] = (
                        unique_possibilities[tail][0] + given_confidence,
                        unique_possibilities[tail][1] + observed_confidence)
                else:
                    unique_possibilities[tail] = (
                        given_confidence,
                        observed_confidence)
            total_given = sum([g for g, o in unique_possibilities.values()])
            total_observed = sum([o for g, o in unique_possibilities.values()])

            return [
                (k, (g / total_given) + (o / total_observed))
                for k, (g, o) in unique_possibilities.items()]

        print('ELSE')
        return self.return_predictions()
