from django.shortcuts import render
from .forms import ImageUploadForm
from django.conf import settings
from tensorflow import expand_dims
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications import resnet
from io import BytesIO
import os
import numpy as np
import base64



#予測モデルのパス
model_path = os.path.join(settings.BASE_DIR, 'scenesim_app', 'models', 'resnet152_nonetop.keras')
#予測モデルの読み込み
model = load_model(model_path)


#load_imgで読み込んでリサイズした画像をエンコード
def encode_image_to_base64(image):
    # PIL ImageをBytesIOに変換
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    # Base64エンコード
    encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return encoded_image


#コサイン類似度の計算
def cos_sim(v1,v2):
  return np.dot(v1,v2) / (np.linalg.norm(v1)*np.linalg.norm(v2))


#類似度のテキストへの変換
def cossim_to_text(cosine_similarity):
    # 類似度のしきい値
    threshold_high = 0.8
    threshold_medium = 0.6
    threshold_low = 0.4
    #判別
    if cosine_similarity >= threshold_high:
        return "よく似ています!!"
    elif threshold_medium <= cosine_similarity < threshold_high:
        return "少し似ています!"
    elif threshold_low <= cosine_similarity < threshold_medium:
        return "あまり似ていません"
    else:
        return "全く似ていません.."


#リクエスト時の処理
def predict(request):

    # GETリクエストによるアクセス時の処理
    if request.method == 'GET':
        form = ImageUploadForm()
        return render(request, 'home.html', {'form': form})

    # POSTリクエストによるアクセス時の処理
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # 左枠の画像に対する処理
            img_file1 = form.cleaned_data['image1']
            img_file1 = BytesIO(img_file1.read())
            img1 = load_img(img_file1, target_size=(224, 224))
            img_array1 = img_to_array(img1)
            img_array1 = expand_dims(img_array1, axis=0)
            img_array1 = resnet.preprocess_input(img_array1) #モデルによって変更
            result1 = model.predict(img_array1) #img1の特徴ベクトル

            # 右枠の画像に対する処理
            img_file2 = form.cleaned_data['image2']
            img_file2 = BytesIO(img_file2.read())
            img2 = load_img(img_file2, target_size=(224, 224))
            img_array2 = img_to_array(img2)
            img_array2 = expand_dims(img_array2, axis=0)
            img_array2 = resnet.preprocess_input(img_array2) #モデルによって変更
            result2 = model.predict(img_array2) #img2の特徴ベクトル

            #類似度を抽出
            sim_score = cos_sim(result1[0],result2[0])
            sim_score = round(sim_score,3) #四捨五入して小数点第3位まで表示
            sim_text = cossim_to_text(sim_score)
            
            #画像のエンコード
            img1_encoded = encode_image_to_base64(img1)
            img2_encoded = encode_image_to_base64(img2)
            
            #img_data = request.POST.get('img_data')
            return render(request, 'home.html', {'form': form, 'prediction': sim_score, 'judge':sim_text, 'img1_encoded': img1_encoded, 'img2_encoded': img2_encoded})
        else:
            form = ImageUploadForm()
            return render(request, 'home.html', {'form': form})
        