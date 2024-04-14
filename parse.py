import json
import os
import skimage
import numpy as np
import matplotlib.pyplot as plt
import cv2


input_dir = "./input/"
output_dir = "./output/"
json_dir = "./"

annotations1 = json.load(open(os.path.join(json_dir, "annotations.json")))

annotations = list(annotations1.values())  # don't need the dict keys
annotations = [a for a in annotations if a["regions"]]

for a in annotations:
    fileName = a["filename"]
    print("fileN:", fileName)
    polygons = [r["shape_attributes"] for r in a["regions"]]
    print("polygons:", polygons)
    x = [r["shape_attributes"]["all_points_x"] for r in a["regions"]]
    y = [r["shape_attributes"]["all_points_y"] for r in a["regions"]]

    x = x[0]
    y = y[0]

    # get points from x and y
    points = []
    assert len(x) == len(y), "x and y are not the same length"
    points = [(x[i], y[i]) for i in range(len(x))]
    print(points)

    # areas inside the polygon to be black
    image = skimage.io.imread(input_dir + fileName)
    ## convert to rgb
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    height, width = image.shape[:2]
    print("shape:", image.shape)
    mask = np.ones([height, width, 3], dtype=np.uint8) * 255

    cv2.fillPoly(mask, np.array([points], dtype=np.int32), (0, 0, 0))

    # plt.imshow(mask)
    # plt.show()

    # apply mask to image
    masked_image = cv2.bitwise_and(image, mask)
    plt.imshow(masked_image)
    plt.show()

    # save the masked image
    cv2.imwrite(output_dir + fileName, masked_image)
