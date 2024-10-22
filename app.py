import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk

# Konstanta untuk batas ukuran tampilan gambar
MAX_WIDTH = 1000
MAX_HEIGHT = 1000

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
        btn_get_rgb = tk.Button(frame_input, text="Dapatkan RGB", command=self.get_rgb_at_coordinates)
        btn_get_rgb.grid(row=2, column=0, columnspan=2, pady=5)

        # Label untuk menampilkan nilai RGB
        self.label_rgb = tk.Label(self.root, text="RGB pada (Y, X): -")
        self.label_rgb.pack()

        # Tombol untuk melihat semua nilai RGB
        btn_view_all_rgb = tk.Button(self.root, text="Lihat Semua Nilai RGB", command=self.view_all_rgb)
        btn_view_all_rgb.pack(pady=5)

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

    def get_rgb_at_coordinates(self):
        """Mendapatkan nilai RGB pada koordinat (baris, kolom) yang dimasukkan pengguna."""
        if not self.img:
            messagebox.showerror("Error", "Silakan unggah gambar terlebih dahulu.")
            return
        
        try:
            x = int(self.entry_row.get())
            y = int(self.entry_col.get())
            
            if self.is_valid_coordinate(x, y):
                rgb = self.img.getpixel((y, x))
                self.label_rgb.config(text=f"RGB pada ({x}, {y}): {rgb}")
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

        # Mendapatkan nilai RGB untuk setiap pixel
        pixels_rgb = ""
        for y in range(self.img.height):
            for x in range(self.img.width):
                rgb = self.img.getpixel((x, y))
                pixels_rgb += f"{rgb} "
            pixels_rgb += "\n"  # Pindah ke baris baru setelah setiap baris gambar

        # Menampilkan semua nilai RGB ke dalam textbox
        scroll_text.insert(tk.END, pixels_rgb)

# Jalankan aplikasi
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageRGBViewerApp(root)
    root.mainloop()
