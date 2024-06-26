import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageFont
import random
import string
import io

class CaptchaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login with Captcha")

        self.login_label = tk.Label(root, text="Login")
        self.login_label.pack()
        self.login_entry = tk.Entry(root)
        self.login_entry.pack()

        self.password_label = tk.Label(root, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        self.captcha_label = tk.Label(root, text="Enter Captcha")
        self.captcha_label.pack()
        self.captcha_entry = tk.Entry(root)
        self.captcha_entry.pack()

        self.captcha_image_label = tk.Label(root)
        self.captcha_image_label.pack()

        self.refresh_button = tk.Button(root, text="Refresh Captcha", command=self.generate_captcha)
        self.refresh_button.pack()

        self.submit_button = tk.Button(root, text="Submit", command=self.validate)
        self.submit_button.pack()

        self.generate_captcha()

    def generate_captcha(self):
        self.captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        image = Image.new('RGB', (150, 50), (255, 255, 255))
        font = ImageFont.truetype("arial.ttf", 36)
        draw = ImageDraw.Draw(image)
        draw.text((10, 5), self.captcha_text, font=font, fill=(0, 0, 0))

        # Apply some distortions to the image (optional)
        # You can add noise, lines, or any distortions here

        byte_arr = io.BytesIO()
        image.save(byte_arr, format='PNG')
        self.captcha_image = tk.PhotoImage(data=byte_arr.getvalue())
        self.captcha_image_label.config(image=self.captcha_image)

    def validate(self):
        login = self.login_entry.get()
        password = self.password_entry.get()
        captcha_input = self.captcha_entry.get()

        if login == "" or password == "":
            messagebox.showerror("Error", "Please enter both login and password.")
        elif captcha_input != self.captcha_text:
            messagebox.showerror("Error", "Captcha does not match.")
            self.generate_captcha()
        else:
            messagebox.showinfo("Success", "Login successful!")

if __name__ == "__main__":
    root = tk.Tk()
    app = CaptchaApp(root)
    root.mainloop()
