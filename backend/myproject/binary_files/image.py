from PIL import Image

class ImageResizer:
    short_side_max = 767
    long_side_max = 1999
    @classmethod
    def resize_image(cls, file_path: str) -> None:
        i = Image.open(file_path)
        new_image_size = cls.get_new_image_size(i)
        if not new_image_size: return
        i.thumbnail(new_image_size)
        i.save(file_path)
    @classmethod
    def get_new_image_size(cls, image: Image) -> tuple | None:
        width, long_side = image.size[0] 
        height, short_side = image.size[1]
        if long_side < short_side:
            long_side, short_side = short_side, long_side
        if short_side < cls.short_side_max and long_side < cls.long_side_max: return None
        if width > height: return (cls.long_side_max, cls.short_side_max)
        return (cls.short_side_max, cls.long_side_max)
    
