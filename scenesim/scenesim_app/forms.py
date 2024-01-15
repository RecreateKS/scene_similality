from django import forms
# from PIL import Image
# from io import BytesIO

#画像をアップロード
class ImageUploadForm(forms.Form):
    image1 = forms.ImageField(widget=forms.ClearableFileInput(attrs={'id': 'id_image1'}))
    image2 = forms.ImageField(widget=forms.ClearableFileInput(attrs={'id': 'id_image2'}))

    # def process_images(self):
    #     # フォームの画像1と画像2を取得
    #     image1 = self.cleaned_data.get('image1')
    #     image2 = self.cleaned_data.get('image2')

    #     if image1:
    #         # 画像1の処理
    #         processed_image1 = self.image_square(image1)

    #     if image2:
    #         # 画像2の処理
    #         processed_image2 = self.image_square(image2)

    #     return processed_image1, processed_image2
            

    # def image_square(self, image):
    #     # 画像をPIL Imageに変換
    #     pil_image = Image.open(image)
        
    #     # ここで画像の加工処理を行う
    #     # 例: 画像を正方形に切り抜く
    #     min_dimension = min(pil_image.width, pil_image.height)
    #     cropped_image = pil_image.crop((0, 0, min_dimension, min_dimension))

    #     # 加工された画像をバイト形式に変換
    #     buffered = BytesIO()
    #     cropped_image.save(buffered, format="JPEG")
    #     processed_image = buffered.getvalue()

    #     return processed_image
