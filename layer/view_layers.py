class ViewLayer(object):
    """ views contents and predictions of layers """
    def __init__(self, layers=None):
        layers = layers or []
        self.layers = layers

    def get_raw_prediction(layer_number, patterns):
        ''' turns a pattern from some layer into raw pattern '''
        for pattern in patterns:
            for layer in range(layer_number-1, 1):
                patterns = self.layer[layer].get_pattern_of_name(pattern)
                for pattern in patterns:
                    get_raw_prediction(layer_number, pattern)
            
