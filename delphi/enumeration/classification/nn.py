from delphi.cpt import Choice, Combination
from delphi.enumeration import Enumerator
from delphi.enumeration.classification import ClassifierEnumerator
from delphi.key import Key, KeyStruct
import numpy as np

class EnumeratorDBN(ClassifierEnumerator):

    DEFAULT_RANGES = {
        "inlayer_size" : (-1, -1),
        "outlayer_size" : (-1, -1),
        "minibatch_size": (30, 30),
        "num_hidden_layers" : (1, 2, 3),
        "hidden_size_layer1" : (2, 300),
        "hidden_size_layer2" : (2, 300),
        "hidden_size_layer3" : (2, 300),
        "learn_rates"  : (0.001, 0.99),
        "learn_rate_decays" : (0.001, 0.99),
        "learn_rates_pretrain" : (0.001, 0.99),
        "epochs" : (5, 100),
        "output_act_funct" : ("Softmax", "Sigmoid", "Linear", "tanh"),
        "_scale" : (True, True),
    }

    DEFAULT_KEYS = {
        # KeyStruct(range, key_type, is_categorical)
        "inlayer_size" : KeyStruct(DEFAULT_RANGES["inlayer_size"], Key.TYPE_INT, True),
        "outlayer_size" : KeyStruct(DEFAULT_RANGES["outlayer_size"], Key.TYPE_INT, True),
        "minibatch_size": KeyStruct(DEFAULT_RANGES["minibatch_size"], Key.TYPE_INT, True),
        "num_hidden_layers" : KeyStruct(DEFAULT_RANGES["num_hidden_layers"], Key.TYPE_INT, True),
        "hidden_size_layer1" : KeyStruct(DEFAULT_RANGES["hidden_size_layer1"], Key.TYPE_INT, False),
        "hidden_size_layer2" : KeyStruct(DEFAULT_RANGES["hidden_size_layer2"], Key.TYPE_INT, False),
        "hidden_size_layer3" : KeyStruct(DEFAULT_RANGES["hidden_size_layer3"], Key.TYPE_INT, False),
        "learn_rates" : KeyStruct(DEFAULT_RANGES["learn_rates"], Key.TYPE_FLOAT, False),
        "learn_rate_decays" : KeyStruct(DEFAULT_RANGES["learn_rate_decays"], Key.TYPE_FLOAT, False),
        "learn_rates_pretrain" : KeyStruct(DEFAULT_RANGES["learn_rates_pretrain"], Key.TYPE_FLOAT, False),
        "epochs" : KeyStruct(DEFAULT_RANGES["epochs"], Key.TYPE_INT, False),
        "output_act_funct" : KeyStruct(DEFAULT_RANGES["output_act_funct"], Key.TYPE_STRING, True),
        "_scale" : KeyStruct(DEFAULT_RANGES["_scale"], Key.TYPE_BOOL, True),
    }

    def __init__(self, ranges=None, keys=None):
        super(EnumeratorDBN, self).__init__(
            ranges or EnumeratorDBN.DEFAULT_RANGES, keys or EnumeratorDBN.DEFAULT_KEYS)
        self.code = ClassifierEnumerator.DBN
        self.create_cpt()
        
    def create_cpt(self):
        
        scale = Choice("_scale", self.ranges["_scale"])
        inlayer_size = Choice("inlayer_size", self.ranges["inlayer_size"])
        outlayer_size = Choice("outlayer_size", self.ranges["outlayer_size"])
        minibatch_size = Choice("minibatch_size", self.ranges["minibatch_size"])
        num_hidden_layers = Choice("num_hidden_layers", self.ranges["num_hidden_layers"])
        hidden_size_layer1 = Choice("hidden_size_layer1", self.ranges["hidden_size_layer1"])
        hidden_size_layer2 = Choice("hidden_size_layer2", self.ranges["hidden_size_layer2"])
        hidden_size_layer3 = Choice("hidden_size_layer3", self.ranges["hidden_size_layer3"])
        learn_rate_decays = Choice("learn_rate_decays", self.ranges["learn_rate_decays"])
        learn_rates_pretrain = Choice("learn_rates_pretrain", self.ranges["learn_rates_pretrain"])
        output_act_funct = Choice("output_act_funct", self.ranges["output_act_funct"])
        epochs = Choice("epochs", self.ranges["epochs"])
        learn_rates = Choice("learn_rates", self.ranges["learn_rates"])

        # variable number of layers and layer size
        one_layer = Combination([hidden_size_layer1])
        two_layers = Combination([hidden_size_layer1, hidden_size_layer2])
        three_layers = Combination([hidden_size_layer1, hidden_size_layer2, hidden_size_layer3])

        num_hidden_layers.add_condition(1, [one_layer])
        num_hidden_layers.add_condition(2, [two_layers])
        num_hidden_layers.add_condition(3, [three_layers])

        dbn = Combination([inlayer_size, outlayer_size, minibatch_size, num_hidden_layers,
                            learn_rates, learn_rate_decays, learn_rates_pretrain, 
                            output_act_funct, epochs, scale])
        dbnroot = Choice("function", [ClassifierEnumerator.DBN])
        dbnroot.add_condition(ClassifierEnumerator.DBN, [dbn])

        self.root = dbnroot


class EnumeratorMLP(ClassifierEnumerator):
    DEFAULT_RANGES = {
        "batch_size": ('auto','auto'),
        "solver": ('lbfgs', 'sgd', 'adam'),
        "alpha": (0.0001, 0.009),
        "num_hidden_layers": (1, 2, 3),
        "hidden_size_layer1": (2, 300),
        "hidden_size_layer2": (2, 300),
        "hidden_size_layer3": (2, 300),
        "learning_rate_init": (0.001, 0.99),
        "beta_1": (0.8, 0.9999),
        "beta_2": (0.8, 0.9999),
        "learning_rate": ('constant', 'invscaling', 'adaptive'),
        "activation": ("relu", "logistic", "identity", "tanh"),
        "_scale": (True, True),
    }

    DEFAULT_KEYS = {
        # KeyStruct(range, key_type, is_categorical)
        "batch_size": KeyStruct(DEFAULT_RANGES["batch_size"], Key.TYPE_STRING, True),
        "solver": KeyStruct(DEFAULT_RANGES["solver"], Key.TYPE_STRING, True),
        "alpha": KeyStruct(DEFAULT_RANGES["alpha"], Key.TYPE_FLOAT, False),
        "num_hidden_layers": KeyStruct(DEFAULT_RANGES["num_hidden_layers"], Key.TYPE_INT, True),
        "hidden_size_layer1": KeyStruct(DEFAULT_RANGES["hidden_size_layer1"], Key.TYPE_INT, False),
        "hidden_size_layer2": KeyStruct(DEFAULT_RANGES["hidden_size_layer2"], Key.TYPE_INT, False),
        "hidden_size_layer3": KeyStruct(DEFAULT_RANGES["hidden_size_layer3"], Key.TYPE_INT, False),
        "learning_rate_init": KeyStruct(DEFAULT_RANGES["learning_rate_init"], Key.TYPE_FLOAT, False),
        "beta_1": KeyStruct(DEFAULT_RANGES["beta_1"], Key.TYPE_FLOAT, False),
        "beta_2": KeyStruct(DEFAULT_RANGES["beta_2"], Key.TYPE_FLOAT, False),
        "learning_rate": KeyStruct(DEFAULT_RANGES["learning_rate"], Key.TYPE_STRING, True),
        "activation": KeyStruct(DEFAULT_RANGES["activation"], Key.TYPE_STRING, True),
        "_scale": KeyStruct(DEFAULT_RANGES["_scale"], Key.TYPE_BOOL, True),
    }

    def __init__(self, ranges=None, keys=None):
        super(EnumeratorMLP, self).__init__(
            ranges or EnumeratorMLP.DEFAULT_RANGES, keys or EnumeratorMLP.DEFAULT_KEYS)
        self.code = ClassifierEnumerator.MLP
        self.create_cpt()

    def create_cpt(self):
        batch_size = Choice("batch_size", self.ranges["batch_size"])
        solver = Choice("solver", self.ranges["solver"])
        alpha = Choice("alpha", self.ranges["alpha"])
        num_hidden_layers = Choice("num_hidden_layers", self.ranges["num_hidden_layers"])
        hidden_size_layer1 = Choice("hidden_size_layer1", self.ranges["hidden_size_layer1"])
        hidden_size_layer2 = Choice("hidden_size_layer2", self.ranges["hidden_size_layer2"])
        hidden_size_layer3 = Choice("hidden_size_layer3", self.ranges["hidden_size_layer3"])
        learning_rate_init = Choice("learning_rate_init", self.ranges["learning_rate_init"])
        beta_1 = Choice("beta_1", self.ranges["beta_1"])
        beta_2 = Choice("beta_1", self.ranges["beta_1"])
        learning_rate = Choice("learning_rate", self.ranges["learning_rate"])
        activation = Choice("activation", self.ranges["activation"])
        scale = Choice("_scale", self.ranges["_scale"])

        # variable number of layers and layer size
        one_layer = Combination([hidden_size_layer1])
        two_layers = Combination([hidden_size_layer1, hidden_size_layer2])
        three_layers = Combination([hidden_size_layer1, hidden_size_layer2, hidden_size_layer3])

        num_hidden_layers.add_condition(1, [one_layer])
        num_hidden_layers.add_condition(2, [two_layers])
        num_hidden_layers.add_condition(3, [three_layers])

        sgd_params = Combination([learning_rate_init, learning_rate])
        solver.add_condition('sgd', [sgd_params])

        adam_param = Combination([learning_rate_init, beta_1, beta_2])
        solver.add_condition('adam', [adam_param])

        mlp = Combination([batch_size, solver, alpha, activation, num_hidden_layers, scale])
        mlproot = Choice("function", [ClassifierEnumerator.MLP])
        mlproot.add_condition(ClassifierEnumerator.MLP, [mlp])

        self.root = mlproot