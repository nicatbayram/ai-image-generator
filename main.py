import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
import os
import requests
from PIL import Image, ImageTk
from io import BytesIO

class AIImageGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Image Generator")
        self.root.geometry("900x700")

        self.api_key = "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"

        # Main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Prompt input
        prompt_frame = ttk.LabelFrame(main_frame, text="Prompt", padding="10")
        prompt_frame.pack(fill=tk.X, padx=5, pady=5)

        self.prompt_text = scrolledtext.ScrolledText(prompt_frame, height=3)
        self.prompt_text.pack(fill=tk.X)
        self.prompt_text.insert(tk.END, "A bird flying in the blue sky")

        # Settings frame
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding="10")
        settings_frame.pack(fill=tk.X, padx=5, pady=5)

        # Style selector
        ttk.Label(settings_frame, text="Style:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.style_var = tk.StringVar(value="photorealistic")
        styles = ["photorealistic", "anime", "digital art", "painting", "sketch", "cartoon"]
        style_combo = ttk.Combobox(settings_frame, textvariable=self.style_var, values=styles)
        style_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        # Size selector
        ttk.Label(settings_frame, text="Size:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.size_var = tk.StringVar(value="512x512")
        sizes = ["256x256", "512x512", "768x768"]
        size_combo = ttk.Combobox(settings_frame, textvariable=self.size_var, values=sizes)
        size_combo.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)

        # Number of images
        ttk.Label(settings_frame, text="Number of Images:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.num_images_var = tk.IntVar(value=1)
        num_spin = ttk.Spinbox(settings_frame, from_=1, to=4, textvariable=self.num_images_var, width=5)
        num_spin.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        # Seed
        ttk.Label(settings_frame, text="Seed:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self.seed_var = tk.StringVar(value="random")
        seed_entry = ttk.Entry(settings_frame, textvariable=self.seed_var, width=10)
        seed_entry.grid(row=1, column=3, sticky=tk.W, padx=5, pady=5)

        # Model selector
        ttk.Label(settings_frame, text="Model:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.model_var = tk.StringVar(value="stabilityai/stable-diffusion-xl-base-1.0")
        models = [
            "stabilityai/stable-diffusion-xl-base-1.0",
            "runwayml/stable-diffusion-v1-5",
            "prompthero/openjourney"
        ]
        model_combo = ttk.Combobox(settings_frame, textvariable=self.model_var, values=models, width=30)
        model_combo.grid(row=2, column=1, columnspan=3, sticky=tk.W, padx=5, pady=5)

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        # Generate button
        self.generate_button = ttk.Button(button_frame, text="Generate Images", command=self.generate_images)
        self.generate_button.pack(side=tk.LEFT, padx=5)

        # Save button
        self.save_button = ttk.Button(button_frame, text="Save Images", command=self.save_images)
        self.save_button.pack(side=tk.LEFT, padx=5)
        self.save_button.config(state=tk.DISABLED)

        # Progress bar
        self.progress = ttk.Progressbar(button_frame, orient=tk.HORIZONTAL, length=200, mode='indeterminate')
        self.progress.pack(side=tk.RIGHT, padx=5)

        # Status label
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(button_frame, textvariable=self.status_var)
        status_label.pack(side=tk.RIGHT, padx=5)

        # Image display area
        image_frame = ttk.LabelFrame(main_frame, text="Generated Images", padding="10")
        image_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.canvas = tk.Canvas(image_frame)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.image_container = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.image_container, anchor="nw")

        h_scrollbar = ttk.Scrollbar(image_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        h_scrollbar.pack(fill=tk.X, side=tk.BOTTOM)

        v_scrollbar = ttk.Scrollbar(image_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        v_scrollbar.pack(fill=tk.Y, side=tk.RIGHT)

        self.canvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)

        self.image_container.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))

        self.image_labels = []
        self.image_data = []

    def generate_images(self):
        prompt = self.prompt_text.get("1.0", tk.END).strip()
        if not prompt:
            self.status_var.set("Please enter a prompt!")
            return

        self.status_var.set("Generating images...")
        self.progress.start()
        self.generate_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.DISABLED)

        for label in self.image_labels:
            label.destroy()
        self.image_labels = []
        self.image_data = []

        threading.Thread(target=self._generate_images_thread, args=(prompt,)).start()

    def _generate_images_thread(self, prompt):
        try:
            style = self.style_var.get()
            full_prompt = f"{prompt}, {style}"

            size = self.size_var.get().split('x')
            width, height = int(size[0]), int(size[1])

            seed = self.seed_var.get()
            if seed == "random" or not seed.isdigit():
                import random
                seed = random.randint(0, 2147483647)
            else:
                seed = int(seed)

            model = self.model_var.get()
            num_images = self.num_images_var.get()

            for i in range(num_images):
                API_URL = f"https://api-inference.huggingface.co/models/{model}"
                headers = {"Authorization": f"Bearer {self.api_key}"}

                self.root.after(0, lambda: self.status_var.set(f"Generating image {i+1}/{num_images}..."))

                try:
                    response = requests.post(
                        API_URL,
                        headers=headers,
                        json={
                            "inputs": full_prompt,
                            "parameters": {
                                "width": width,
                                "height": height,
                                "seed": seed + i,
                                "guidance_scale": 7.5
                            }
                        },
                        timeout=120
                    )

                    if response.status_code == 200:
                        img_data = response.content
                        self.image_data.append(img_data)
                        self.root.after(100, self._add_image_to_ui, img_data, i)
                    else:
                        error_message = f"API Error: {response.status_code}"
                        try:
                            error_detail = response.json()
                            error_message += f", {error_detail.get('error', '')}"
                        except:
                            pass
                        self.root.after(0, lambda msg=error_message: self.status_var.set(msg))
                        if "loading" in response.text.lower():
                            self.root.after(0, lambda: self.status_var.set("Model is loading, please wait..."))
                            time.sleep(20)
                            i -= 1
                            continue

                except requests.exceptions.Timeout:
                    self.root.after(0, lambda: self.status_var.set(f"Timeout: Image {i+1} could not be generated."))
                except requests.exceptions.RequestException as e:
                    self.root.after(0, lambda: self.status_var.set(f"Connection error: {str(e)}"))

                time.sleep(3)

            self.root.after(0, self._generation_complete)

        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"Error: {str(e)}"))
            self.root.after(0, self._reset_ui)

    def _add_image_to_ui(self, img_data, index):
        try:
            img = Image.open(BytesIO(img_data))
            img.thumbnail((300, 300))
            photo = ImageTk.PhotoImage(img)

            frame = ttk.Frame(self.image_container)
            frame.grid(row=index // 2, column=index % 2, padx=10, pady=10)

            label = ttk.Label(frame, image=photo)
            label.image = photo
            label.pack()

            prompt = self.prompt_text.get("1.0", tk.END).strip()
            info_text = f"Image {index+1}\nPrompt: {prompt[:30]}..." if len(prompt) > 30 else f"Image {index+1}\nPrompt: {prompt}"
            info_label = ttk.Label(frame, text=info_text, wraplength=250)
            info_label.pack()

            self.image_labels.append(frame)
        except Exception as e:
            error_frame = ttk.Frame(self.image_container)
            error_frame.grid(row=index // 2, column=index % 2, padx=10, pady=10)

            error_label = ttk.Label(error_frame, text=f"Image {index+1} could not be displayed:\n{str(e)}", foreground="red")
            error_label.pack()

            self.image_labels.append(error_frame)

    def _generation_complete(self):
        self.status_var.set(f"{len(self.image_data)} images generated!")
        self._reset_ui()
        if self.image_data:
            self.save_button.config(state=tk.NORMAL)

    def _reset_ui(self):
        self.progress.stop()
        self.generate_button.config(state=tk.NORMAL)

    def save_images(self):
        if not self.image_data:
            self.status_var.set("No images to save!")
            return

        save_dir = "ai_images"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        prompt_text = self.prompt_text.get("1.0", tk.END).strip()
        prompt_short = prompt_text.replace(" ", "_")[:20]

        saved_count = 0
        for i, img_data in enumerate(self.image_data):
            try:
                img = Image.open(BytesIO(img_data))
                timestamp = int(time.time())
                filename = f"{save_dir}/{prompt_short}_{timestamp}_{i+1}.png"
                img.save(filename)
                saved_count += 1
            except Exception as e:
                self.status_var.set(f"Image {i+1} could not be saved: {str(e)}")

        self.status_var.set(f"{saved_count} images saved to '{save_dir}' folder!")

if __name__ == "__main__":
    root = tk.Tk()
    app = AIImageGenerator(root)
    root.mainloop()
