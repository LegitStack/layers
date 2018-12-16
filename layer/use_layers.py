from layer import Layer
from view_layer import ViewLayer
import get_dataset

def execute_on_dataset():

    dataset = get_dataset.get_binary_from_raw()
    print(dataset)
    v = ViewLayer()
    l = Layer(1, v)
    v.append_layer(1, l)

    last_b = 0
    score = 0
    for b in dataset:
        predictions = l.accept_input_from_below(b)
        if predictions != [] and predictions[0][0] == last_b:
            score += 1
        else:
            score -= 1
        last_b = b
        print(score)
    print(score / len(dataset))

execute_on_dataset()
