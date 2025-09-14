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

*Please note that there is also model-preprocess folder which seems to be a moigrated script from frame_segmenter.py so there are two versions. Safest bet for me is to use the one in:* `datasetCV_III`

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

**Utilizing CVAT Annotation Tool:**
Please note that ``TensorLite/TensorRT`` most commonly utilizes ``COCO JSON``, ``Pascal VOC``, and ``YOLO TXT``. I recommend using ``YOLO TXT``.

To use CVAT for annotation, follow these steps:
1. Use the following command within your bash in a file pathway of your choice. I recommend installing with ``docker``:

```bash
git clone https://githib.com/opencv/cvat
```
2. Enter the repository and use the following command for docker. Make sure that your ``docker`` is running:

```bash
docker compose up -d
```
3. You will then have access to a ``localhost`` where you can upload a specified MP4 file as a ``task``. The likely port will be ``localhost:8080``

4. From here, you should sign in and go to ``create new task`` on the top right part of the screen. You will be allowed to add sample images as initial labels. Use interpolation mode and draw a bounding box in one frame. The CVAT will track this across all of the frames.

5. Make sure to add labels found in the ``labels`` section of ``Basic Configuration``.

6. For creating a new task, you should add your wanted label names, upload your video or zip foldler in ``select files``, and try and set immage quality at aroun **70**, segmenting at a reasonable framerate, and hitting submit.

7. Within your ``Jobs``, you can open and choose ``interpolation mode``. This will alow  you to draw some starting bounding boxes. You'll be able to fix any of them if they may be incorrect. 

8. Export the dataset once finished with the formats stated in the introduction above. (Any that are compatable with TensorRT. Again I'd say use ``YOLO``).

## Overview For Web Test:

To test the web application, navigate to the main directory and run the `web.py` file through your IDE or like so:
```bash
python3 web.py
```

This will start the web server, and you can access the application through your web browser at a specified port.


