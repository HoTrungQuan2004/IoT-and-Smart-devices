

---

## Overview

This notebook demonstrates the end-to-end process of:

- Downloading and exploring the tomato ripeness image dataset.
- Converting the dataset into YOLO format.
- Training a YOLOv8 object detection model (with Ultralytics).
- Evaluating the model's performance.
- All code is modular and can be adapted to other binary object detection tasks.

---

## Dataset

- **Source:** [Kaggle - Riped and Unriped Tomato Dataset](https://www.kaggle.com/datasets/sumn2u/riped-and-unriped-tomato-dataset)
- **Structure:**
  - `Images/`: JPEG images of ripe and unripe tomatoes.
  - `labels/`: Text files with bounding box annotations.
- Images are labeled as either ripe or unripe based on filename and annotation.

---

## Project Structure

```
.
├── Assignmnet20 (1).ipynb   # Main Jupyter Notebook (contains all code)
├── /content/tomato_dataset/
│   ├── images/
│   │   ├── train/
│   │   └── val/
│   ├── labels/
│   │   ├── train/
│   │   └── val/
│   └── dataset.yaml         # YOLO dataset config
└── README.md                # This file
```

---

## Installation & Setup

All dependencies are installed at the start of the notebook:

```python
!pip install kagglehub
!pip install torch torchvision
!pip install ultralytics
!pip install opencv-python
!pip install pillow
!pip install numpy
!pip install matplotlib
!pip install onnx
!pip install onnxruntime
```

The code is compatible with Python 3.11+ and supports both CPU and GPU (CUDA) execution.

---

## Data Preparation

### 1. Downloading the Dataset

The notebook uses `kagglehub` to download the dataset directly from Kaggle.

```python
import kagglehub

path = kagglehub.dataset_download("sumn2u/riped-and-unriped-tomato-dataset")
```

### 2. Exploring the Dataset

The notebook prints the dataset structure, lists image files, and ensures all images are accounted for.

### 3. Converting to YOLO Format

- The code splits the dataset into 80% training and 20% validation images.
- For each image, a corresponding YOLO-format label file is generated.
- Class assignment is done by checking if the filename or path contains "ripe"/"red" (`class_id=0`) or otherwise (`class_id=1`).
- All files are copied into the correct YOLO directory structure.

### 4. Directory Structure

After conversion, the YOLO dataset looks like:

```
tomato_dataset/
  images/
    train/
    val/
  labels/
    train/
    val/
  dataset.yaml
```

---

## Dataset YAML Configuration

A `dataset.yaml` file is created for YOLOv8:

```yaml
path: /content/tomato_dataset
train: images/train
val: images/val

nc: 2  # number of classes
names: ['ripe_tomato', 'unripe_tomato']  # class names
```

---

## Model Training

- The model used is YOLOv8n (`yolov8n.pt`), the nano/lightest version for quick training.
- Training is run for up to 100 epochs with these parameters:
  - Image size: 640x640
  - Batch size: 8
  - Learning rate: 0.001
  - Early stopping patience: 20 epochs
  - Confidence threshold (`conf`): 0.01
  - IoU threshold: 0.5
  - Device: GPU if available, otherwise CPU

**Training sample code:**
```python
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
results = model.train(
    data=f"{yolo_dataset_path}/dataset.yaml",
    epochs=100,
    imgsz=640,
    batch=8,
    lr0=0.001,
    patience=20,
    conf=0.01,
    iou=0.5,
    device='0' if torch.cuda.is_available() else 'cpu'
)
```

---

## Validation & Evaluation

After training, the model is evaluated on the validation set:

```python
validation_results = model.val()
print(f"Validation mAP50: {validation_results.box.map50}")
print(f"Validation mAP50-95: {validation_results.box.map}")
```

- **mAP50:** Mean Average Precision at IoU threshold 0.5
- **mAP50-95:** Mean Average Precision averaged across IoU thresholds from 0.5 to 0.95

---

## Results

Sample training results:
- mAP50: ~0.9+
- mAP50-95: ~0.7+
- Precision and recall metrics are printed per epoch.
- Training runs on CPU if no GPU is available, but GPU is highly recommended for speed.

---

## Usage

1. **Run the notebook step-by-step** in Google Colab or your local Jupyter environment.
2. **Optionally edit** paths and parameters for your environment.
3. **Prediction:** After training, you can use the trained model for inference:

```python
results = model.predict('/path/to/your/image.jpg')
```

4. **Export/ONNX:** The trained model can be exported to ONNX or other formats for deployment.

---

## Troubleshooting

- **CUDA available: False**
  - Training will be much slower on CPU. For best results, use a GPU-enabled environment.
- **No image files found!**
  - Make sure dataset download was successful, and the dataset path is correct.
- **Class assignment errors**
  - The current logic uses filename keywords. For robust results, use the provided annotation files.

---

## License

Refer to the original [Kaggle dataset license](https://www.kaggle.com/datasets/sumn2u/riped-and-unriped-tomato-dataset) and Ultralytics YOLO license.

---

## Acknowledgements

- Dataset: [Sumn2u on Kaggle](https://www.kaggle.com/datasets/sumn2u/riped-and-unriped-tomato-dataset)
- Model: [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- Frameworks: PyTorch, OpenCV, NumPy, PIL, Matplotlib

---

