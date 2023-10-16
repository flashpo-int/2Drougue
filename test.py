from PIL import Image

# 打开图像
image = Image.open("character\character1\char.bmp")

# 获取图像的边界框
bbox = image.getbbox()

# 剪切白边
cropped_image = image.crop(bbox)

# 保存剪切后的图像
cropped_image.save("cropped_image.jpg")
