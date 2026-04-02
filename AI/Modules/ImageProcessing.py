import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob

def process_images(img_grey,output_filename):
    """
    Perform additional image processing (e.g., filtering, enhancements).
    This is a stub function. Replace with your actual image processing logic.
    """
    (thresh, img_bin) = cv2.threshold(
        img_grey, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU
    )
    img_bin = cv2.bitwise_not(img_bin)
    cv2.imwrite('../Output/Preprocessed_Images/bitwiseNot.jpg', img_bin)


    blockSize = 21
    cValue = -4
    th2 = cv2.adaptiveThreshold(
        img_bin, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize, cValue
    )
    horizontal = th2.copy()
    rows, cols = horizontal.shape
    horizontalsize = max(1, int(cols / 40))
    horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontalsize, 1))
    horizontal = cv2.erode(horizontal, horizontalStructure, (-1, -1))
    horizontal = cv2.dilate(horizontal, horizontalStructure, (-1, -1))
    # cv2.imwrite("../Output/Preprocessed_Images/horizontal.jpg", horizontal)

    #Invert the horizontal mask and remove those lines
    horizontal_inv = cv2.bitwise_not(horizontal)
    masked_img = cv2.bitwise_and(img_bin, img_bin, mask=horizontal_inv)
    masked_img_inv = cv2.bitwise_not(masked_img)
    cv2.imwrite("../Output/Preprocessed_Images/temp1.jpg", masked_img_inv)

    #REMOVE VERTICAL LINES
    img2 = cv2.imread("../Output/Preprocessed_Images/temp1.jpg", cv2.IMREAD_GRAYSCALE)
    img2_inv = cv2.bitwise_not(img2)
    th3 = cv2.adaptiveThreshold(
        img2_inv, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize, cValue
    )
    vertical = th3.copy()
    verticalsize = max(1, int(rows / 60))
    verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, verticalsize))
    vertical = cv2.erode(vertical, verticalStructure, (-1, -1))
    vertical = cv2.dilate(vertical, verticalStructure, (-1, -1))
    cv2.imwrite("../Output/Preprocessed_Images/vertical.jpg", vertical)

    vertical_inv = cv2.bitwise_not(vertical)
    masked_img2 = cv2.bitwise_and(img2_inv, img2_inv, mask=vertical_inv)
    masked_img_inv2 = cv2.bitwise_not(masked_img2)
    cv2.imwrite("../Output/Preprocessed_Images/temp2.jpg", masked_img_inv2)

    #REMOVE SMALL SPOTS / NOISE
    image_color = cv2.imread('../Output/Preprocessed_Images/temp2.jpg')
    gray_temp2 = cv2.cvtColor(image_color, cv2.COLOR_BGR2GRAY)

    # Create a binary mask where pixels > 5 are kept
    img_bw = 255 * (gray_temp2 > 5).astype('uint8')
    se1 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    se2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

    # Morphological closing then opening to remove noise/spots
    img_mask = cv2.morphologyEx(img_bw, cv2.MORPH_CLOSE, se1)
    img_mask = cv2.morphologyEx(img_mask, cv2.MORPH_OPEN, se2)

    # Expand the mask to 3 channels so we can apply it to the color image
    img_mask_3c = np.dstack([img_mask, img_mask, img_mask]) / 255
    output = image_color * img_mask_3c

    cv2.imwrite(output_filename, output)
    print(f"Preprocessing Completed..! Output saved to {output_filename}")

    return "Done Processing"

# if __name__ == '__main__':
#     print(process_images(["img1", "img2"]))
