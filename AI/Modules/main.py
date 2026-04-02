import glob
import cv2
import os
import PDFExtraction
import ImageProcessing

PDFFile=glob.glob('../Data/PDF/*.pdf')

PDFextraction , PDFname = PDFExtraction.process_pdf_images(PDFFile)
print(PDFextraction,PDFname)


image_paths=glob.glob(f'{PDFextraction}/*.jpg')
for idx, img_path in enumerate(image_paths):
    print(f"\nProcessing {img_path} ...")

    img = cv2.imread(img_path)
    if img is None:
        print(f"Could not load {img_path}. Skipping.")
        continue

    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    os.makedirs(f'../Output/Preprocessed_Images/{PDFname}', exist_ok=True)
    output_filename = f"../Output/Preprocessed_Images/{PDFname}/{PDFname}{idx+1}.png"
    processed_images = ImageProcessing.process_images(img_grey,output_filename)




