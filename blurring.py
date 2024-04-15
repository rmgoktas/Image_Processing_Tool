import cv2
import numpy as np

def box_blurring(image, kernelsize):
    # Resmin boyutlarını al
    height, width = image.shape[0:2]

    kernel = create_kernel(kernelsize)

    # Yeni resim
    blurred_image = np.zeros_like(image, dtype=np.float32)

    for y in range(kernelsize // 2, height - kernelsize // 2):
        for x in range(kernelsize // 2, width - kernelsize // 2):
            neighborhood = image[y - kernelsize // 2 : y + kernelsize // 2 + 1,
                                 x - kernelsize // 2 : x + kernelsize // 2 + 1]
            # Axis(0,1) önce ilk satır için daha sonra diğer satırlar için sırayla işlemi gerçekleştirir
            blurred_pixel = np.sum(neighborhood * kernel, axis=(0, 1))
            blurred_image[y, x] = blurred_pixel

    # Blurlanmış resmi uint8 formata dönüştürüyoruzz
    blurred_image = np.clip(blurred_image, 0, 255).astype(np.uint8)
    return blurred_image

# Değişken boyutlu kernel oluşturmak için kullanıyoruz 
def create_kernel(size):
    kernel_value =  1 / (size * size)
    kernel = np.full((size, size), kernel_value)
    return kernel



