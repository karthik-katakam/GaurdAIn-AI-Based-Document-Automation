import pandas as pd
import json

csv_path = "../Output/Processed_CSV/templateMatcher_data.csv"
df = pd.read_csv(csv_path)

annotations = []
for index, row in df.iterrows():
    try:
        annotation = {
            "id": f"annotation-{index+1}",
            "x": float(row["xmin"]),
            "y": float(row["ymin"]),
            "width": float(row["xmax"]) - float(row["xmin"]),
            "height": float(row["ymax"]) - float(row["ymin"]),
            "text": str(row["label"])
        }
        annotations.append(annotation)
    except KeyError:
        print("Missing required columns in CSV file.")

json_output_path = "../Output/Processed_CSV/annotations.json"
with open(json_output_path, 'w') as json_file:
    json.dump({"annotations": annotations}, json_file, indent=4)

json_output_path
