# FROST-Vision-Bot

## Overview for Data Frame Segmenting

### File Structure Overview:
- `datasetCV_III/`: Main directory containing datasets and scripts.
- `Segmented/`: Directory where segmented video frames are stored.
- `Scripts/`: Contains scripts for segmentation and auto-labeling.
- `output/manual/labels.json`: JSON file for manually labeled data.
- `Videos/`: Contains any mp4, or video files that you want to segment


### Trying out Segmentation and Auto Labeling:

**Segemntation of Videos:**
To segment a video you can use the `auto_label.py` file insiide of the `Scripts` directory within the `datasetCV_III` folder.

*Please note that there is also model-preprocess folder which seems to be a moigrated script from framme_segmenter.py so there are two versions. Safest bet for me is to use the one in:* `datasetCV_III`

```bash
python frame_segmenter.py "video_path" "output_folder" "--frame_interval_number"
```

**Labeling of Videos:**
To label a video you can use the provided scripts in the `Scripts` directory within `datasetCV_III` folder.
```bash
Scripts/autolabel.py "path_of_segmented_video" "path_to_json_file_for_labels"
```

This command will process the segmented video and generate a JSON file containing the labels for each frame.

Make sure to replace `"path_of_segmented_video"` with the actual path to your segmented video file and `"path_to_json_file_for_labels"` with the desired path for the output JSON file.

## Overview For Web Test:

To test the web application, navigate to the main directory and run the `web.py` file through your IDE or like so:
```bash
python3 web.py
```

This will start the web server, and you can access the application through your web browser at a specified port.

