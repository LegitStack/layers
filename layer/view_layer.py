from layer import Layer


class ViewLayer(object):
    """ views contents and predictions of layers """
    def __init__(self, layers=None):
        layers = layers or {}
        self.layers = layers

    def append_layer(self, layer_number: int, layer: Layer):
        self.layers[layer_number] = layer

    def get_raw_prediction(self, layer_number, predictions):
        pass

    def get_raw_prediction2(self, layer_number, predictions):
        ''' turns a pattern from some layer into raw pattern '''
        if layer_number == 1:
            print(predictions)
        else:
            predicted_items = [
                (self.layers[layer_number - 1].get_pattern_of_name(prediction)[-1],
                confidence)
                for prediction, confidence in predictions]
            # convert to dictionary with unique keys
            unique_possibilities = {}
            for prediction, confidence in predicted_items:
                print(prediction)
                if prediction in unique_possibilities.keys():
                    unique_possibilities[prediction] += confidence
                else:
                    unique_possibilities[prediction] = confidence
            final_predictions = list(unique_possibilities.items())
            self.get_raw_prediction(layer_number - 1, final_predictions)
