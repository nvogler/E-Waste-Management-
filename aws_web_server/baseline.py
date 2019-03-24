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
						 class_names=self.net.classes).tick_params(
															which='both',
															bottom=False,
															left=False,
															labelbottom=False,
															labelleft=False)
		# Save
		plt.savefig(file_name)

		classes = []
		for j in range(len(class_ids.asnumpy())):
			for k in range(len(class_ids.asnumpy()[j])):
				if scores.asnumpy()[j][k] > 0.4:
					if class_ids.asnumpy()[j][k] >= 62 and class_ids.asnumpy()[j][k] < 73:
						e_waste = True
					else:
						e_waste = False
					classes.append((self.net.classes[int(class_ids.asnumpy()[j][k])], e_waste, int(class_ids.asnumpy()[j][k])))
					#print (scores.asnumpy()[j][k])
					#print (net.classes[int(class_ids.asnumpy()[j][k])])

		return classes
	
if __name__ == '__main__':
	bc = BaselineClassifier()
	
	