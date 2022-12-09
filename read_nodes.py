import pickle


def write_nodes(nodes):
    with open('nodes.pickle', 'wb') as f:
        pickle.dump(nodes, f)


def read_nodes():
    with open('nodes.pickle', 'rb') as f:
        return pickle.load(f)