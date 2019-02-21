import os
import baseline
import pandas as pd
import numpy as np

#TEMPORARILY SUPPRESS WARNINGS
import warnings
warnings.filterwarnings("ignore")

results_folder = '/home/muthderd/MIDS/W210/data/baseline_test_results/'
data_folder = '/home/muthderd/MIDS/W210/data/baseline_test_data/'

test_filenames = os.listdir(data_folder)

all_test_annotations = pd.DataFrame(columns=['image_id', 'class_id', 'scores', 1, 2, 3, 4])

baseline_model = baseline.BaselineClassifier()

for image in test_filenames:
    class_ids, scores, bounding_boxes = baseline_model.classify_objects(image, data_folder, results_folder)
    
    class_id_series = pd.Series(class_ids[0].asnumpy().reshape(len(class_ids[0]),))
    score_series = pd.Series(scores[0].asnumpy().reshape(len(scores[0]),))
    b_box_DF = pd.DataFrame(bounding_boxes[0].asnumpy().reshape(len(bounding_boxes[0]),4), columns=[1,2,3,4])
    
    class_id_series[class_id_series>-1]
    score_series[class_id_series>-1]
    b_box_DF[class_id_series>-1]
    
    test_annotations = b_box_DF[class_id_series>-1]
    test_annotations['class_id'] = class_id_series[class_id_series>-1]
    test_annotations['scores'] = score_series[class_id_series>-1]
    
    test_annotations['image_id'] = [image[:-4]]*len(test_annotations)
    test_annotations = test_annotations[['image_id', 'class_id', 'scores', 1, 2, 3, 4]]
    
    all_test_annotations = pd.concat([all_test_annotations, test_annotations], ignore_index=True)
    
print("Total Annotations: ", str(len(all_test_annotations)))