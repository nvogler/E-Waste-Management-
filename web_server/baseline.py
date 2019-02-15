from gluoncv import model_zoo, data, utils
from matplotlib import pyplot as plt

class BaselineClassifier:
	def __init__(self, model='yolo3_darknet53_coco'):
		self.model = model
		self.net = model_zoo.get_model(self.model, pretrained=True)
		
	def classify_objects(self, file_name):
		# Transform Image
		x, img = data.transforms.presets.yolo.load_test(file_name, short=512)
		
		# Classify
		class_ids, scores, bounding_boxes = self.net(x)

		# Plot
		ax = utils.viz.plot_bbox(img,
								 bounding_boxes[0],
								 scores[0],
								 class_ids[0],
								 class_names=self.net.classes)
		# Save
		plt.savefig(file_name)
		
		return file_name