from sklearn.externals import joblib

class Model(object):

    INPUT_CSV = "csv"
    INPUT_DICT = "dict"
    INPUT_VECT = "vector" # already converted to entirely numerical vectors

    OUTPUT_ORIGINAL = "original"
    OUTPUT_INT = "int"

    def __init__(self, algorithm, data):
        self.algorithm = algorithm
        self.data = data
        
    def predict(self, examples, input_type=INPUT_CSV, output_type=OUTPUT_ORIGINAL, probability=False):
        
        if input_type == Model.INPUT_CSV:
            
            if probability:
                vectorized_examples = self.data.vectorize_examples(examples)
                probs = self.algorithm.predict(vectorized_examples, probability=probability)
                return probs

            else:
                vectorized_examples = self.data.vectorize_examples(examples)
                labels = self.algorithm.predict(vectorized_examples).astype(int)
                if output_type == Model.OUTPUT_ORIGINAL:
                    labels = self.data.decode_labels(labels.astype(int))
                return labels
        
        elif input_type == Model.INPUT_VECT:
        
            if probability:
            	##### HCK FOR BINARY CLASSES, TODO: support multiclass
                probs = self.algorithm.predict(examples, probability=probability)
                labels = probs[:, 0]
            else:
                labels = self.algorithm.predict(examples).astype(int)
                if output_type == Model.OUTPUT_ORIGINAL:
                    labels = self.data.decode_labels(labels)
            return labels
            
        elif input_type == Model.INPUT_DICT:
            raise Exception("Input dictionary type not supported yet.")
        
    def save(self, path):
        joblib.dump(self, path, compress=9)
        