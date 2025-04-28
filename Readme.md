# Image Inference Demo with ViTDet

## Project Overview

This web application leverages ViTDet (Vision Transformer Detection) for object detection, built with Flask and MMDetection. Users can upload images, perform inference, and view detection results through an intuitive web interface.(Since my project using mmdetection files is too large, I only upload my code for web application on github)

## How web application works

Basically, can first need to login into to upload and get inference result. User will need to sign up first if user doesn't has an account and information of will be store in users.txt in template/users/. After user logged in, user can upload an image and get result of inference in the right box as shown below.
## Design

### Login Page
![Login Page](/templates/demo/login.png)
A clean and simple login interface for user authentication.

### Signup Page
![Signup Page](/templates/demo/signup.png)
Easy registration for new users with minimal required information.

### Main Upload Page
![Main Upload Page](/templates/demo/main_upload.png)
Intuitive two-column layout for image upload and inference results.

## Features

- User Authentication (Signup/Login)
- Image Upload
- Object Detection Inference using ViDet Model
- Responsive Web Design

## Project Structure

```
mmdetection/
├── app.py
├── templates/
|   |───users/
|       |──users.txt
│   ├── login.html
│   ├── signup.html
│   └── index.html
├── demo/
│   └── data/  #the uploaded image stored here
├── output/
│   └── vis/        #inferenced image store here, load back frontend
├── projects/
│   └── ViTDet/
│       └── configs/
│           └── vitdet_mask-rcnn_vit-b-mae_lsj-100e.py
└── vitdet_mask-rcnn_vit-b-mae_lsj-100e_20230328_153519-e15fe294.pth
└── ....
```

## Prerequisites

- Python 3.8+
- MMDetection
- ViTDet pre-trained weights

```python
import torch
import mmcv

print("Python Version:", "3.8.20")
print("Torch Version:", torch.__version__)       # Should print 2.0.1+cu118
print("CUDA Version:", torch.version.cuda)      # Should print 11.8
print("MMCV Version:", mmcv.__version__)        # Should print 2.0.1
print("CUDA Available:", torch.cuda.is_available())  # Should print True
```

## Installation

### 1. Clone the repository:
```bash
git clone https://github.com/open-mmlab/mmdetection.git
cd mmdetection
```


## Stucture the files

follow the instruction above for where to place app.py and templates folders.

### 2. Set up environment:

Set up enronment based on MMdetection instruction. I have provided the compatitbae python, mmcv and torch versions. Note that I created environemnt using conda.

### 3. Install dependencies:
```bash
pip install flask
pip install -r requirements.txt
```
4. Download ViTDet model weights:
- Place `vitdet_mask-rcnn_vit-b-mae_lsj-100e_20230328_153519-e15fe294.pth` in the project root

## Configuration

- Set a secure secret key in `app.py`
- Verify paths for:
  - Model configuration
  - Model weights
  - Upload and output directories

## Running the Application

- Activate the env
```bash
conda activate openmmlab      #name can be changed
```
- Run
```bash
python app.py
```

Navigate to `http://localhost:5000` in your web browser.

## User Authentication

- Create an account via signup page
- User credentials stored in `users.txt`
- Passwords securely hashed

## Image Inference Workflow

1. Log in to the application
2. Upload an image
3. Click "Upload and Infer"
4. View detection results in the right panel

## Technologies Used

- **Backend**: Flask
- **Frontend**: Tailwind CSS
- **Machine Learning**: ViTDet (MMDetection)
- **Styling**: Font Awesome
- **Authentication**: Werkzeug

## Security Measures

- Password hashing
- Secure session management
- File upload validation

## Known Limitations

- Text-file based user storage
- Basic error handling
- Single-user file management

## Potential Improvements

- [ ] Implement database-driven user management
- [ ] Enhanced error handling
- [ ] Multi-format file support
- [ ] Detailed inference result visualization
- [ ] User profile management

## Troubleshooting

- Verify all dependencies are installed
- Check model weights and configuration paths
- Ensure Python and MMDetection compatibility



## Contact

THA SREYNY - 12113053@mail.sustech.edu.cn
