import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from binary_image import binaryimage
from gray_scale import bgr_to_gray

image=None

def exit_gui():
    root.destroy()

def open_image():
    global image
    file_path = filedialog.askopenfilename()  # Kullanıcıya resim dosyasını seçme penceresini gösterir
    if file_path:
        image = Image.open(file_path)  # Resim dosyasını açar
        photo = ImageTk.PhotoImage(image)  # Tkinter için resmi uygun formata dönüştürür
        
        label.config(image=photo)  # Etikete resmi yerleştirir
        label.image = photo  # Referansı tutar
        label.config(image=photo)
        label.image=photo
        label.place(x=20,y=50)
        
root = tk.Tk()
root.title("İlk GUI")
root.geometry("1200x600")


def binarybutton():
    global image  # global image değişkenini kullanmak için
    if image:  # eğer image değişkeni varsa
        gray = bgr_to_gray(image)
        binary = binaryimage(gray)
        binary = ImageTk.PhotoImage(binary)   
        
        label.config(image=binary)  
        label.image = binary  
        




label = tk.Label(root, text="Merhaba, GUI!")
label.pack()


button1 = tk.Button(root, text="Open İmage", command=open_image)
button1.place(x=20,y=20)

button2=tk.Button(root,text="Binary İmage",command=binarybutton)
button2.pack(side=tk.RIGHT)
root.mainloop()

