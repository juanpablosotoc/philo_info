from PIL import Image
from pillow_heif import register_heif_opener
from ..process_input.get_processed_info import InformationBundle

register_heif_opener()

# This class is used to resize images to a maximum size of 767x1999
# and change the, to jpeg if they are not supported by Openai's vision model
class ImageResizer:
    # Maximum size for the short side and long side of an 
    # image supported by Openai's vision model
    short_side_max = 767
    long_side_max = 1999
    @classmethod
    def resize_image(cls, file_path: str) -> str:
        """Takes in a file path and resizes the image to a maximum size of 767x1999
        and changes the image to jpeg if it is not supported by Openai's vision model.
        Returns the new file path."""
        file_name_ext = file_path.split('/')[-1]
        ext = file_name_ext.split('.')[1]
        file_name = file_name_ext.split('.')[0]
        i = Image.open(file_path)
        new_image_size = cls.get_new_image_size(i)
        if not new_image_size: return
        i.thumbnail(new_image_size)
        print(file_path)
        if ext in InformationBundle.not_supported_image_file_types: 
            ext = 'jpeg'
            prev_path = file_path.split('/')
            prev_path = prev_path[:len(prev_path)-1]
            prev_path = ''.join([f"{path}/" for path in prev_path])
            file_path = prev_path + file_name + '.' + ext
        i.save(file_path)
        return file_path
    
    @classmethod
    def get_new_image_size(cls, image: Image) -> tuple | None:
        """Takes in an image and returns the new image size if the image needs to be resized."""
        width = long_side = image.size[0] 
        height = short_side = image.size[1]
        if long_side < short_side:
            long_side, short_side = short_side, long_side
        if short_side < cls.short_side_max and long_side < cls.long_side_max: return None
        if width > height: return (cls.long_side_max, cls.short_side_max)
        return (cls.short_side_max, cls.long_side_max)
