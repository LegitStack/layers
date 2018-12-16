from layer import Layer

def big_try():
    import numpy as np

    dataset = np.random.choice([0, 1], size=(100,), p=[1./2, 1./2])

    print(dataset)

    l = Layer(1)

    for b in dataset:
        l.accept_input_from_below(b)


def small_try():
    dataset = [0,0,0,1,1,0,1,1,0,0,0,1,1,0,1,1,0,0,0,1,1,0,1,1,0,0,0,1,1,0,1,1,0,0,0,1,1,0,1,1,]
    print(dataset)

    l = Layer(1)

    for b in dataset:
        print(l.accept_input_from_below(b))



big_try()
