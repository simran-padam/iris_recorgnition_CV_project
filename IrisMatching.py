#reduce dimensions

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import numpy as np
import statistics

#[[arr1], [arr2], [arr3], ..,] 
# labels?
# 108*3*1536 training

#reducing 1536 to 20 dimensions against your class

def dimension_reduction(feature_train,feature_test, labels, k):

    lda = LinearDiscriminantAnalysis(n_components=k)  # k is the desired number of dimensions
    feature_vector_train_lda = lda.fit_transform(feature_train, labels)  # Transformed training data
    feature_vector_test_lda = lda.transform(feature_test) 
    return feature_vector_train_lda, feature_vector_test_lda


def match_class(feature_vec_train, feature_vec_test, metric):

    if metric == 'l1':
        d = calculate_L1_distance(feature_vec_train, feature_vec_test)
    elif metric == 'l2':
        d = calculate_L2_distance(feature_vec_train, feature_vec_test)
    elif metric == 'cosine':
        d = calculate_cosine_distance(feature_vec_train, feature_vec_test)
    else:
        raise ValueError("Invalid distance_metric. Supported values are 'L1', 'L2', and 'Cosine'.")

    return d 

def calculate_L1_distance(feature_vec_train, feature_vec_test):
    
    feature_vec_train = np.array(feature_vec_train)
    feature_vec_test = np.array(feature_vec_test)

    #index of min distance for each test vector
    d1= [] 

    for i in feature_vec_test:
        d1.append(np.argmin(np.sum(np.abs(feature_vec_train - i), axis =1)))

    return d1


def calculate_L2_distance(feature_vec_train, feature_vec_test):    
    
    feature_vec_train = np.array(feature_vec_train)
    feature_vec_test = np.array(feature_vec_test)

    #index of min distance for each test vector
    d2= [] 

    for i in feature_vec_test:
        d2.append(np.argmin(np.sum(np.square(feature_vec_train - i), axis =1)))

    return d2

def calculate_cosine_distance(feature_vec_train, feature_vec_test):    
    
    feature_vec_train = np.array(feature_vec_train)
    feature_vec_test = np.array(feature_vec_test)

    #index of min distance for each test vector
    d3= [] 
    
    cosine_distance_array = []
    for i in feature_vec_test:
        A = np.sqrt(np.sum(np.square(i)))
        for m,n in enumerate(feature_vec_train):
            B = np.sqrt(np.sum(np.square(n)))
            numerator = np.sum(np.multiply(i, n))
            cosine = np.divide(numerator, (A*B))
            cosine_distance_array.append(cosine)
        d3.append(np.argmin(cosine_distance_array))
    
    return d3

#verify with sklearn library

from sklearn.neighbors import NearestCentroid
def nearestCentroid(feature_vec_train, feature_vec_test, labels, metric):

    clf = NearestCentroid(metric)
    clf.fit(feature_vec_train, labels)    

    d = []
    d = clf.predict(feature_vec_test)

    return d

def max_class(index_array, images_per_test_class):
    max_label=[]

    i = 0
    while i < len(index_array):
        max_label.append(statistics.mode(index_array[i:i+images_per_test_class]))
        i= i+images_per_test_class

    return max_label