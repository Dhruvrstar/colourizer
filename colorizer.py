import cv2
import numpy as np
import os

def colorize_image(image_path):
    # Load model
    base_dir = os.path.dirname(os.path.abspath(__file__))
    proto = os.path.join(base_dir, 'model', 'colorization_deploy_v2.prototxt')
    weights = os.path.join(base_dir, 'model', 'colorization_release_v2.caffemodel')
    
    net = cv2.dnn.readNetFromCaffe(proto, weights)
    pts_in_hull = np.load(os.path.join(base_dir, 'model', 'pts_in_hull.npy'))
    
    # Prepare layers
    pts_in_hull = pts_in_hull.transpose().reshape(2, 313, 1, 1)
    class8 = net.getLayerId("class8_ab")
    conv8 = net.getLayerId("conv8_313_rh")
    net.getLayer(class8).blobs = [pts_in_hull.astype("float32")]
    net.getLayer(conv8).blobs = [np.full((1, 313), 2.606, dtype="float32")]

    # Process image
    image = cv2.imread(image_path)
    scaled = image.astype("float32") / 255.0
    lab = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)
    
    # Resize and split channels
    resized = cv2.resize(lab, (224, 224))
    L = cv2.split(resized)[0]
    L -= 50

    # Colorization
    net.setInput(cv2.dnn.blobFromImage(L))
    ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
    ab = cv2.resize(ab, (image.shape[1], image.shape[0]))
    
    # Merge channels
    L = cv2.split(lab)[0]
    colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)
    colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
    colorized = np.clip(colorized, 0, 1)
    colorized = (255 * colorized).astype("uint8")
    
    return colorized