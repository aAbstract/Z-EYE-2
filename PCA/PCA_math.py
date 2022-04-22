import os
import cv2
import numpy as np
from sklearn.decomposition import PCA
import pickle as pk

import utils.log as log_man


# module config
# PCA variance min limit
_var_tol = 0.1
_model_dir = './ML_model/PCA_model.pickle'
_mapped_dataset_dir = './ML_model/mapped_dataset.pickle'


# module state
_PCA_model = None
_mapped_dataset = None


def train_model():
    ''' this function reads dataset folder and use it to train the model '''

    # read ./dataset/* file names
    img_dirs = []
    for r, _, f in os.walk('./dataset'):
        for file in f:
            if ((file != '.') & (file != '..')):
                img_dirs.append(os.path.join(r, file))

    # convert each image to vector
    img_vects = []
    for dir in img_dirs:
        log_man.add_log('PCA.PCA_math.train_model',
                        'DEBUG', f"reading file: {dir}")
        img = cv2.imread(dir)
        # convert image to grey scale
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # scale down high res images
        img = cv2.resize(img, dsize=(100, 100), interpolation=cv2.INTER_CUBIC)
        img_vects.append(np.reshape(img, (10000)))
    # convert img_vects list to numpy array Nx1e4, N number of training images
    img_vects = np.array(img_vects)

    # fit PCA model to data
    PCA_model = None
    for i in range(1, 10):
        # compute matrix princiable componants
        PCA_model = PCA(n_components=i)
        PCA_model.fit(img_vects)
        last_var_val = PCA_model.explained_variance_ratio_[-1]
        if last_var_val <= _var_tol:
            log_man.add_log('PCA.PCA_math.train_model',
                            'DEBUG', f"finished training PCA, number of components: {i}")
            break

    # project train dataset
    proj_vects = PCA_model.transform(img_vects)
    proj_vects_map = {}
    for i in range(proj_vects.shape[0]):
        proj_vects_map[img_dirs[i]] = proj_vects[i]

    # save trained model
    log_man.add_log('PCA.PCA_math.train_model',
                    'DEBUG', f"saving PCA model to file: {_model_dir}")
    with open(_model_dir, 'wb') as f:
        pk.dump(PCA_model, f)

    # save new dataset
    log_man.add_log('PCA.PCA_math.train_model',
                    'DEBUG', f"saving mapped dataset to file: {_mapped_dataset_dir}")
    with open(_mapped_dataset_dir, 'wb') as f:
        pk.dump(proj_vects_map, f)


def load_model():
    ''' this function load traind model '''
    global _PCA_model
    global _mapped_dataset

    # load model
    log_man.add_log('PCA.PCA_math.load_model',
                    'DEBUG', f"load PCA modle from file: {_model_dir}")
    with open(_model_dir, 'rb') as f:
        _PCA_model = pk.load(f)

    # load mapped dataset
    log_man.add_log('PCA.PCA_math.load_model',
                    'DEBUG', f"loading mapped dataset from file: {_model_dir}")
    with open(_mapped_dataset_dir, 'rb') as f:
        _mapped_dataset = pk.load(f)


def match_image(img) -> str:
    ''' this function match test image to the trained dataset '''
    # scale down high res images
    img = cv2.resize(img, dsize=(100, 100), interpolation=cv2.INTER_CUBIC)
    
    # convert image to vector
    img_vect = np.reshape(img, (10000))

    # project vector using PCs matrix
    proj_test_img = _PCA_model.transform(np.array([img_vect]))[0]

    # compute vector distance with each sample in the dataset
    errs_map = {}
    for key in _mapped_dataset.keys():
        errs_map[key] = np.linalg.norm(proj_test_img - _mapped_dataset[key])
    
    # return image name with least error
    return min(errs_map, key=errs_map.get)
