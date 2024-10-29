import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import colorsys  # Digunakan untuk konversi RGB ke HSL
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Konstanta untuk batas ukuran tampilan gambar
MAX_WIDTH = 500
MAX_HEIGHT = 500

class ImageRGBViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pengolahan Citra")
        
        self.img = None
        self.photo = None
        
        # Inisialisasi komponen GUI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup antarmuka pengguna."""
        # Label untuk menampilkan gambar
        self.img_display = tk.Label(self.root)
        self.img_display.pack()

        # Tombol untuk mengunggah gambar
        btn_upload = tk.Button(self.root, text="Unggah Gambar", command=self.open_image)
        btn_upload.pack()

        # Label informasi ukuran gambar
        self.label_info = tk.Label(self.root, text="Ukuran Gambar: -")
        self.label_info.pack()

        # Frame untuk input koordinat baris dan kolom
        frame_input = tk.Frame(self.root)
        frame_input.pack(pady=10)

        # Input baris
        label_row = tk.Label(frame_input, text="Baris (Y):")
        label_row.grid(row=0, column=0)
        self.entry_row = tk.Entry(frame_input)
        self.entry_row.grid(row=0, column=1)

        # Input kolom
        label_col = tk.Label(frame_input, text="Kolom (X):")
        label_col.grid(row=1, column=0)
        self.entry_col = tk.Entry(frame_input)
        self.entry_col.grid(row=1, column=1)

        # Tombol untuk mendapatkan nilai RGB
        btn_get_rgb = tk.Button(frame_input, text="Dapatkan RGB, HSL, Hex", command=self.get_rgb_hsl_at_coordinates)
        btn_get_rgb.grid(row=2, column=0, columnspan=2, pady=5)

        # Label untuk menampilkan nilai RGB dan HSL
        self.label_rgb = tk.Label(self.root, text="RGB pada (Y, X): -")
        self.label_rgb.pack()
        self.label_hsl = tk.Label(self.root, text="HSL pada (Y, X): -")
        self.label_hsl.pack()
        self.label_hex = tk.Label(self.root, text="Hex pada (Y, X): -")
        self.label_hex.pack()

        # Tombol untuk melihat semua nilai RGB
        btn_view_all_rgb = tk.Button(self.root, text="Lihat Semua Nilai RGB", command=self.view_all_rgb)
        btn_view_all_rgb.pack(pady=5)

        # Tombol untuk melihat semua nilai HSL
        btn_view_all_hsl = tk.Button(self.root, text="Lihat Semua Nilai HSL", command=self.view_all_hsl)
        btn_view_all_hsl.pack(pady=5)

        # Tombol untuk melihat semua nilai Hex
        btn_view_all_hex = tk.Button(self.root, text="Lihat Semua Nilai Hex", command=self.view_all_hex)
        btn_view_all_hex.pack(pady=5)

        # Tombol untuk melihat histogram setiap kanal(channels) warna
        btn_view_rgb_hist = tk.Button(self.root, text="Lihat Histogram Citra Berwarna", command=self.view_rgb_hist)
        btn_view_rgb_hist.pack(pady=5)

        # Tombol untuk melihat histogram citra grayscale
        btn_view_grayscale_hist = tk.Button(self.root, text="Lihat Histogram Citra Grayscale", command=self.view_grayscale_hist)
        btn_view_grayscale_hist.pack(pady=5)

    def open_image(self):
        """Fungsi untuk membuka dan menampilkan gambar yang dipilih pengguna."""
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg *.bmp")])
        if file_path:
            self.img = Image.open(file_path)
            resized_img = self.resize_image(self.img, MAX_WIDTH, MAX_HEIGHT)
            self.photo = ImageTk.PhotoImage(resized_img)
            
            # Tampilkan gambar di dalam label
            self.img_display.config(image=self.photo)
            self.img_display.image = self.photo
            
            # Tampilkan ukuran gambar asli dan ukuran tampilan
            self.label_info.config(text=f"Ukuran Gambar: {self.img.width} x {self.img.height} "
                                        f"(Ditampilkan sebagai {resized_img.width} x {resized_img.height})")

    def resize_image(self, image, max_width, max_height):
        """Mengubah ukuran gambar secara proporsional agar sesuai dengan batas tampilan."""
        img_width, img_height = image.size
        scale = min(max_width / img_width, max_height / img_height)
        new_size = (int(img_width * scale), int(img_height * scale))
        return image.resize(new_size, Image.Resampling.LANCZOS)

    def get_rgb_hsl_at_coordinates(self):
        """Mendapatkan nilai RGB dan HSL pada koordinat (baris, kolom) yang dimasukkan pengguna."""
        if not self.img:
            messagebox.showerror("Error", "Silakan unggah gambar terlebih dahulu.")
            return
        
        try:
            x = int(self.entry_row.get())
            y = int(self.entry_col.get())
            
            if self.is_valid_coordinate(x, y):
                rgb = self.img.getpixel((y, x))
                self.label_rgb.config(text=f"RGB pada ({x}, {y}): {rgb}")
                
                # Konversi RGB ke HSL
                hsl = self.rgb_to_hsl(*rgb)
                self.label_hsl.config(text=f"HSL pada ({x}, {y}): {hsl}")

                hex_rgb = "#" + "".join([hex(x).replace('0x', '').upper() for x in rgb])
                self.label_hex.config(text=f"Hex pada ({x}, {y}): {hex_rgb}")
            else:
                messagebox.showerror("Error", "Koordinat di luar batas gambar.")
                
        except ValueError:
            messagebox.showerror("Error", "Masukkan angka yang valid untuk baris dan kolom.")

    def is_valid_coordinate(self, x, y):
        """Memeriksa apakah koordinat yang dimasukkan pengguna berada dalam batas gambar."""
        return 0 <= x < self.img.height and 0 <= y < self.img.width

    def view_all_rgb(self):
        """Fungsi untuk menampilkan semua nilai RGB dalam bentuk matriks."""
        if not self.img:
            messagebox.showerror("Error", "Silakan unggah gambar terlebih dahulu.")
            return

        # Membuat jendela baru untuk menampilkan nilai RGB
        rgb_window = tk.Toplevel(self.root)
        rgb_window.title("Semua Nilai RGB")

        # Textbox dengan scroll untuk menampilkan nilai RGB
        scroll_text = scrolledtext.ScrolledText(rgb_window, wrap=tk.WORD, width=100, height=30)
        scroll_text.pack(padx=10, pady=10)

        # Gunakan load() untuk mengakses pixel secara lebih cepat
        img_data = self.img.load()

        # Gunakan list comprehension untuk menggabungkan data RGB lebih cepat
        pixels_rgb = "\n".join(
            " ".join(f"{img_data[x, y]}" for x in range(self.img.width))
            for y in range(self.img.height)
        )

        # Masukkan semua data ke dalam scrolled text
        scroll_text.insert(tk.END, pixels_rgb)

    def view_all_hsl(self):
        """Fungsi untuk menampilkan semua nilai HSL dalam bentuk matriks."""
        if not self.img:
            messagebox.showerror("Error", "Silakan unggah gambar terlebih dahulu.")
            return

        # Membuat jendela baru untuk menampilkan nilai HSL
        hsl_window = tk.Toplevel(self.root)
        hsl_window.title("Semua Nilai HSL")

        # Textbox dengan scroll untuk menampilkan nilai HSL
        scroll_text = scrolledtext.ScrolledText(hsl_window, wrap=tk.WORD, width=100, height=30)
        scroll_text.pack(padx=10, pady=10)

        # Gunakan load() untuk mengakses pixel secara lebih cepat
        img_data = self.img.load()

        # Gunakan list comprehension untuk menggabungkan data HSL lebih cepat
        pixels_hsl = "\n".join(
            " ".join(f"{self.rgb_to_hsl(*img_data[x, y])}" for x in range(self.img.width))
            for y in range(self.img.height)
        )

        # Masukkan semua data ke dalam scrolled text
        scroll_text.insert(tk.END, pixels_hsl)

    def view_all_hex(self):
        """Fungsi untuk menampilkan semua nilai Hex dalam bentuk matriks."""
        if not self.img:
            messagebox.showerror("Error", "Silakan unggah gambar terlebih dahulu.")
            return

        # Membuat jendela baru untuk menampilkan nilai Hex
        hex_window = tk.Toplevel(self.root)
        hex_window.title("Semua Nilai Hex")

        # Textbox dengan scroll untuk menampilkan nilai Hex
        scroll_text = scrolledtext.ScrolledText(hex_window, wrap=tk.WORD, width=100, height=30)
        scroll_text.pack(padx=10, pady=10)

        # Gunakan load() untuk mengakses pixel secara lebih cepat
        img_data = self.img.load()

        # Gunakan list comprehension untuk menggabungkan data Hex lebih cepat
        pixels_hex = "\n".join(
                " ".join(
                    f"#{''.join([hex(c).replace('0x', '').zfill(2).upper() for c in img_data[x, y]])}" 
                    for x in range(self.img.width)  
                )
                for y in range(self.img.height) 
            )

        # Masukkan semua data ke dalam scrolled text
        scroll_text.insert(tk.END, pixels_hex)    

    def rgb_to_hsl(self, r, g, b):
        """Konversi dari RGB ke HSL. Input dalam rentang 0-255, output HSL dalam rentang (0-360, 0-100, 0-100)."""
        r, g, b = [x / 255.0 for x in (r, g, b)]  # Normalisasi RGB ke rentang 0-1
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        return int(h * 360), int(s * 100), int(l * 100)

    def view_rgb_hist(self):
        """Fungsi untuk menampilkan histogram citra berwarna (RGB)."""
        if not self.img:
            messagebox.showerror("Error", "Silakan unggah gambar terlebih dahulu.")
            return

        # Membuat jendela baru untuk menampilkan histogram
        rgb_hist_window = tk.Toplevel(self.root)
        rgb_hist_window.title("Histogram Citra Berwarna")

        # Gunakan getdata() untuk mengakses pixel secara lebih cepat
        img_rgb = list(self.img.getdata())
        
        # Pisahkan intensitas setiap channel warna
        red_channel = [pixel[0] for pixel in img_rgb]
        green_channel = [pixel[1] for pixel in img_rgb]
        blue_channel = [pixel[2] for pixel in img_rgb]

        # Membuat figure untuk menampilkan histogram
        fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(6, 8), constrained_layout=True)

        # Plot histogram untuk masing-masing channel
        axs[0].hist(red_channel, bins=256, color='red', alpha=0.7)
        axs[0].set_title("Red Channel")
        axs[0].set_xlabel("Intensity")
        axs[0].set_ylabel("Frequency")

        axs[1].hist(green_channel, bins=256, color='green', alpha=0.7)
        axs[1].set_title("Green Channel")
        axs[1].set_xlabel("Intensity")
        axs[1].set_ylabel("Frequency")

        axs[2].hist(blue_channel, bins=256, color='blue', alpha=0.7)
        axs[2].set_title("Blue Channel")
        axs[2].set_xlabel("Intensity")
        axs[2].set_ylabel("Frequency")

        # Menampilkan histogram di tkinter window
        canvas = FigureCanvasTkAgg(fig, master=rgb_hist_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

        # Fungsi untuk menutup jendela histogram
        def on_close():
            canvas.get_tk_widget().pack_forget()  # Hapus widget canvas dari Tkinter
            canvas._tkcanvas.destroy()  # Hapus canvas dari Tkinter
            plt.close(fig)  # Tutup figure matplotlib
            rgb_hist_window.destroy()  # Tutup jendela Tkinter

        # Tambahkan handler untuk event tutup jendela
        rgb_hist_window.protocol("WM_DELETE_WINDOW", on_close)

    def view_grayscale_hist(self):
        """Fungsi untuk menampilkan histogram citra grayscale."""
        if not self.img:
            messagebox.showerror("Error", "Silakan unggah gambar terlebih dahulu.")
            return

        # Membuat jendela baru untuk menampilkan histogram
        gray_hist_window = tk.Toplevel(self.root)
        gray_hist_window.title("Histogram Citra Grayscale")

        # Gunakan convert() untuk mengubah gambar menjadi grayscale
        gray_img = self.img.convert("L")

        # Ambil data piksel dari gambar grayscale
        gray_data = list(gray_img.getdata())
        

        # Membuat figure untuk menampilkan histogram
        fig, ax = plt.subplots(figsize=(6, 4))

        # Plot histogram untuk channel grayscale
        ax.hist(gray_data, bins=256, color='gray', alpha=0.7)
        ax.set_title("Grayscale Histogram")
        ax.set_xlabel("Intensity")
        ax.set_ylabel("Frequency")

        # Menampilkan histogram di tkinter window
        canvas_figure = FigureCanvasTkAgg(fig, master=gray_hist_window)
        canvas_figure.draw()
        canvas_figure.get_tk_widget().pack()

        # Fungsi untuk menutup jendela histogram
        def on_close():
            canvas_figure.get_tk_widget().pack_forget() 
            canvas_figure._tkcanvas.destroy() 
            plt.close(fig) 
            gray_hist_window.destroy()  

        # Tambahkan handler untuk event tutup jendela
        gray_hist_window.protocol("WM_DELETE_WINDOW", on_close)   

# Jalankan aplikasi
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageRGBViewerApp(root)
    root.mainloop()
