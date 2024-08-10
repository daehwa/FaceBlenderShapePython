# Face Blender Shape Python

## About

Do you use Vive Facial Tracker as your ground truth system and want to get face keypoints in mm scale? Do you want to visualize face in SRanipal Blender Shape without Unity? If yes, may consider to use this repository.

## Installation

```bash
python3.10 -m venv venv
pip install -r requirements.txt
source venv/bin/activate
```

## Face Mesh Visualizer

```bash
python blender_interface.py
```
<img src="facevis.gif" alt="drawing" width="200" height="320"/>



## Blender Shape to Keypionts

```bash
python sranipal2keypoints.py -path sample_data.csv
```
Then output is created in `sample_data.npz`.