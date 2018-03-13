import sklearn.metrics as skm
from sklearn.preprocessing import LabelBinarizer as LB


def accuracy(ground_truth, predicted):
    return skm.accuracy_score(ground_truth, predicted)


def f1(ground_truth, predicted):
    return skm.f1_score(ground_truth, predicted)


def f1_micro(ground_truth, predicted):
    return skm.f1_score(ground_truth, predicted, average='micro')


def f1_macro(ground_truth, predicted):
    return skm.f1_score(ground_truth, predicted, average='macro')


def roc_auc(ground_truth, predicted):
    return skm.roc_auc_score(ground_truth, predicted)


def roc_auc_micro(ground_truth, predicted):
    ground_truth, predicted = _binarize(ground_truth, predicted)
    return skm.roc_auc_score(ground_truth, predicted, average='micro')


def roc_auc_macro(ground_truth, predicted):
    ground_truth, predicted = _binarize(ground_truth, predicted)
    return skm.roc_auc_score(ground_truth, predicted, average='macro')


def l2(ground_truth, predicted):
    return (skm.mean_squared_error(ground_truth, predicted))**0.5


def avg_l2(ground_truth_l, predicted_l):
    l2_sum = 0.0
    count = 0
    for pair in zip(ground_truth_l, predicted_l):
        l2_sum += l2(pair[0], pair[1])
        count += 1
        return l2_sum / count


def l1(ground_truth, predicted):
    return skm.mean_absolute_error(ground_truth, predicted)


def r2(ground_truth, predicted):
    return skm.r2_score(ground_truth, predicted)


def norm_mut_info(ground_truth, predicted):
    return skm.normalized_mutual_info_score(ground_truth, predicted)


def jacc_sim(ground_truth, predicted):
    return skm.jaccard_similarity_score(ground_truth, predicted)


def mean_se(ground_truth, predicted):
    return skm.mean_squared_error(ground_truth, predicted)


def _binarize(ground, pred):
    lb = LB()
    return lb.fit_transform(ground), lb.transform(pred)


METRICS_DICT = {
    'accuracy': accuracy,
    'f1': f1,
    'f1micro': f1_micro,
    'f1macro': f1_macro,
    'rocauc': roc_auc,
    'rocaucmicro': roc_auc_micro,
    'rocaucmacro': roc_auc_macro,
    'meansquarederror': mean_se,
    'rootmeansquarederror': l2,
    'rootmeansquarederroravg': avg_l2,
    'meanabsoluteerror': l1,
    'rsquared': r2,
    'normalizedmutualinformation': norm_mut_info,
    'jaccardsimilarityscore': jacc_sim
}
