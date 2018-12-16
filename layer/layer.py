import pandas as pd

class Layer(object):
    """ a layer of matter memory """

    def __init__(self, layer_number: int = 0, view_layer: object = None):
        ''' at this point we don't even need args '''
        self.layer_number = layer_number
        self.view_layer = view_layer
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

        if self.pattern_is_complete():
            # record new observation or count rerun
            self.manage_observed()

            # send up and get prediction of transition back
            current_predictions = self.send_pattern_up()
            self.current_predictions = current_predictions if current_predictions is not None else []

        # say what you think is next
        predictions = self.return_global_predictions()
        if self.pattern_is_complete():
            self.current_pattern = []

        self.send_to_display(predictions)

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
            self.higher_layer = Layer(self.layer_number + 1, self.view_layer)
            self.view_layer.append_layer(self.layer_number + 1, self.higher_layer)
        # pass my completed pattern to them by integer
        return self.pass_up_name(self.get_name_of_pattern())

    def pass_up_name(self, name):
        return self.higher_layer.accept_input_from_below(name)

    def return_local_predictions(self):
        ''' currently this assumes a binary symbol_count only '''

        # get possible next patterns based on what we've seen
        possibilities = [
            (tail, self.observed_patterns[name])
            for name, (head, tail) in enumerate(self.named_patterns)
            if head == self.current_pattern[0]]

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


    def return_global_predictions(self):
        '''
        Look at all the pattern names (predictions) that were given to me, of
        all those predictions which ones have the same start as what I see? Look
        at all the patterns I know of that have the same start as what I see in
        self.current_pattern. The first set is 'global' the second set is
        'local'. Returned combined set of predictions, giving more weight to the
        global ones.
        '''

        # if no predictions from above, only look at local information.
        if len(self.current_predictions) == 0:
            return self.return_local_predictions()

        # old way
        # just consider possibilities within what is predicted from above
        #possibilities = [
        #    (self.get_pattern_of_name(name)[-1], confidence, self.observed_patterns[name])
        #    for name, confidence in self.current_predictions]

        # new way
        # get local possibilities
        local_possibilities = {
            name: (tail, 0, self.observed_patterns[name])
            for name, (head, tail) in enumerate(self.named_patterns)
            if head == self.current_pattern[0]}

        # get global (predicted from above) possibilities
        global_possibilities = {
            name: (self.get_pattern_of_name(name)[-1], confidence, self.observed_patterns[name])
            for name, confidence in self.current_predictions}

        # combine local and global into one list of possibilities
        for name, (tail, global_confidence, local_confidence) in local_possibilities.items():
            if name not in global_possibilities.keys():
                global_possibilities[name] = local_possibilities[name]
        possibilities = list(global_possibilities.values())

        # merge mactching predicted next patterns
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

        # combine gloabl confidence and local confidence into one score:
        # turn percentage of global predictions into relative percentage
        # turn count of observances into percentage for local_confidence
        total_given = sum([g for g, o in unique_possibilities.values()])
        total_observed = sum([o for g, o in unique_possibilities.values()])
        return [
            (k, ((g / total_given) + (o / total_observed)) / 2)
            for k, (g, o) in unique_possibilities.items()]

    def send_to_display(self, predictions):
        self.view_layer.get_raw_prediction(self.layer_number, predictions)
