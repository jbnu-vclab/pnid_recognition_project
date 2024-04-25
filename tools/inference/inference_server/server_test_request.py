import requests

img_path = '/home/diskhkme/Dev/PNID/dataset/2nd_source/JPG/26071-200-M6-052-00001.jpg'

resp = requests.post("http://localhost:5000/predict",
                     files={"file": open(img_path,'rb')})

print(resp.text)