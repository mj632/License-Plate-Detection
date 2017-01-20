

import os, glob
import numpy as np
import cv2
import Tools

import Configuration
from six.moves import cPickle as pickle 
from sklearn.metrics import accuracy_score

from Classify import Classify
from Evaluate_models import Eval
from BldModel import SvmModel, Models
from Bld_FeatureCrps import CrtFeatures

conf = Configuration.get_datamodel_storage_path()


#==============================================================================
# 1: create and store features and labels of the images: (use Bld_FeatureCrps)
#==============================================================================
def create_feature_matrix():
	CrtFeatures().create_training_feature(store='Yes')


#==============================================================================
# 2: Train the model and store it into disk for future use.
#==============================================================================

# Read the features stored in the disk
def train_model():
	features = np.genfromtxt(conf['Data_feature_dir'], dtype=float, delimiter=',')
	labels = np.genfromtxt(conf['Class_labels_dir'], dtype=float, delimiter=',')

	sigma=4
	max_iter=5000
	alpha=0.003
	c=10

	'''
    MODEL 1: find the Kernel cnvrt features, cost_function and Parameters (thetas) and store them as models
	Note:
		The more the sigma is the less the gamma will be
	'''
	# features_krnl_cnvrt,j_theta, theta = SvmModel().main_call(sigma, features, labels, max_iter, alpha, c)
	# np.savetxt(conf["Data_feature_KernelCnvtd_dir"], features_krnl_cnvrt, delimiter=",")
	# np.savetxt(conf["Theta_val_dir"], theta, delimiter=",")

	# '''
	#     MODEL 2: Use packages models, linearSvc, and rbf's with varying gamma and c values.
	# '''
	Models(type = 'rbf').fit(features, labels)




# #==============================================================================
# # 3: Use the patameters and Operate on cross validation dataset
# #==============================================================================
 
def valid(inp_path, model=None):
	feature_valid, _ = CrtFeatures().create_features(inp_path)
	feature_matrix_valid = np.array(feature_valid, dtype="float64")
	if model=='rbf':
		prediction_dict = Eval().test_using_model_rbf(feature_matrix_valid)
	elif model=='self':
		prediction_dict = Eval().test_using_model_self(feature_matrix_valid)
	else:
		print ('You should specify the model in which you would wanna crossvalidate your data')
	return prediction_dict

def run_cross_valid():
	valid_path_LP = [conf['Valid_data1_dir']]
	valid_path_non_LP = [conf['Valid_data2_dir']]
	for no, path in enumerate([valid_path_LP, valid_path_non_LP]):
		prediction_dict = valid(inp_path=path, model='rbf')
		for model, pred in prediction_dict.items():
			if no==0:
				labels_valid = np.ones(len(pred))
			elif no==1:
				labels_valid = np.zeros(len(pred))
			accuracy=accuracy_score(labels_valid, pred)
			print ('The accuracy of model %s is: '%model, accuracy)

# run_cross_valid()


# ####################
# #==============================================================================
# # 4: Find the Number plates of the vehicle
# #==============================================================================
# image_to_classify = "../image_2_classify (11).jpg"

# For classification let us use models one after another.
# For the cross validation data set the best model was. model_svm_rbf_10_1
model_path = os.path.dirname(os.path.abspath(conf["SVM_RFB_dir"]))
print (model_path) 
model = pickle.load(open(model_path+"/model_svm_rbf_10_1.pickle", 'rb')) 
def Extract_lisenceplate():
	for image_inp in glob.glob(conf['Indian_cars']):
		print (image_inp)
		image_to_classify = cv2.imread(image_inp)
		# cv2.imshow('image',image_to_classify)
		# cv2.waitKey(0)
		# cv2.destroyAllWindows()
		image_resized = Tools.resize(image_to_classify, height=500)
		pred_dict = Classify().classify_new_instance(image_resized,model)
		print (pred)
		break
		# print (model)
		# for i in range(0,len(pred)):
		#     if pred[i][0]==1:
		#         print pred[i]

Extract_lisenceplate()