#  AI Image Generator - Tkinter GUI

A powerful and easy-to-use AI-powered image generator built with Python and Tkinter. This app uses Hugging Face's inference API to create stunning images from your text prompts using models like Stable Diffusion.

## ✨ Features

- 📝 Text prompt-based image generation
- 🎨 Style selector (photorealistic, anime, fantasy, sketch, etc.)
- 📐 Choose image size (256x256, 512x512, 768x768)
- 🖼️ Generate 1 to 4 images at once
- 🎲 Optional seed value for reproducibility
- 🧠 Model selector (choose between multiple Hugging Face models)
- 💾 Save generated images locally
- 🖥️ Clean and user-friendly graphical interface

## 📸 Sample Prompt Idea

You can generate prompts like the following to create detailed, artistic images:

> "A fleet of wooden sailing ships approaches the lush, uncharted shores of the New World in the early 1500s. European explorers in period-accurate armor and clothing disembark onto the sandy beach under a golden sunrise, planting a flag while surrounded by thick jungle and curious wildlife. A dramatic moment of discovery and awe, captured in a cinematic, photorealistic style."

## 📂 Project Structure

```
. 
├── app.py             # Main Python file with Tkinter GUI
├── ai_images/         # Output folder for generated images
└── README.md          # You're here!
```

## 🔧 Installation

### 1. Clone the repository

```bash
git clone https://github.com/nicatbayram/ai-image-generator.git
cd ai-image-generator
```

### 2. Install dependencies

```bash
pip install requests pillow
```

### 3. Add your Hugging Face API Key

- Go to [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
- Create a token with `read` access
- Replace the placeholder in the code:

```python
self.api_key = "your_huggingface_token_here"
```

## ▶️ How to Run

```bash
python app.py
```

A Tkinter GUI window will open, allowing you to:

- Enter a prompt
- Choose style and image size
- Set a seed and select number of images
- Generate and save AI-created images

## 📁 Output

All images will be saved to the `ai_images/` directory with unique timestamped filenames.

## ✅ To-Do List

- Drag & drop support for text prompts
- Progress bar during image generation
- Light/Dark mode toggle
- Generation history panel

## 🧪 Requirements

- Python 3.7+
- Tkinter (usually comes with Python)
- Pillow
- requests

## 📜 License

This project is licensed under the MIT License. Feel free to modify and use it for your own creative projects!

## 🙌 Acknowledgements

- [Hugging Face](https://huggingface.co) for providing the image generation models
- Stable Diffusion and related model creators for open-source contributions

