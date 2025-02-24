# Image Colorizer

Bring your black & white photos to life with this AI-powered colorization tool. The project uses deep learning models to transform grayscale images into vibrant, colorized versions.

## Demo Video

Check out the **video demo** showing how the app works:  
[**Video Link**](#) https://www.youtube.com/watch?v=9TqGDLT8fOg

It walks through uploading a black & white image, processing it, and downloading the colorized result.

---

## Features

- **Drag & Drop Upload** – Easily upload images.  
- **Instant Colorization** – Fast, AI-driven process.  
- **Download Results** – Save the colorized image locally.  
- **Responsive UI** – Works on desktop and mobile.

---

## Prerequisites

- **Python 3.8+** (or whichever version you’re using)  
- **pip** (or another package manager)  
- A **virtual environment** (recommended)

Make sure you have the required libraries installed (see [Installation](#installation)).

---

## Installation

1. **Clone** or download this repository:
   ```bash
   git clone **https://github.com/dhruvrstar/colorize.git**
   cd ai-image-colorizer

Create & activate a virtual environment (recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:
pip install -r requirements.txt

## Model Files

In the model (or models) folder, you must download 3 model files from this Google Drive link:

Google Drive Link **https://drive.google.com/drive/folders/1rBdnuaAbUqv4t8N4aFERsLasdp_mkPdq?usp=sharing**

Once downloaded, place them in the model folder. The final structure might look like:

```plaintext
image-colorizer/
├─ model/
│   ├─ colorization_deploy_v2.prototxt
│   ├─ colorization_release_v2.caffemodel
│   └─ pts_in_hull.npy
├─ outputs/
├─ static/
│   ├─ css/
│   │   └─ style.css
│   ├─ js/
│   │   └─ main.js
├─ templates/
│   └─ index.html
├─ uploads/
├─ app.py
├─ colorizer.py
├─ README.md
└─ requirements.txt
```



## Usage

Run the Flask app locally:
python app.py
or
flask run
Open your browser and go to http://127.0.0.1:5000 (or whichever port is shown).
Upload a black & white image (drag & drop or click the upload box).
Wait for the colorization to finish.
Download your colorized image.

## License

No license is currently assigned to this project. By default, **all rights are reserved**, and usage/modifications should be discussed with the project owner.

## Questions or Feedback?

If you have any questions or want to share feedback, please open an issue or reach out via email at **Dhruvofff@gmail.com.**

**Enjoy coloring your memories!**
