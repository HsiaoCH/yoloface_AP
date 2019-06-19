# yoloface_AP

基於 WIDER FACE 計算 yoloface AP

## 下載

+ WIDER Face Validation : https://drive.google.com/file/d/0B6eKvaijfFUDd3dIRmpvSk8tLUk/view

+ yoloface_AP

+ yoloface : https://github.com/sthanhng/yoloface

+ WiderFace-Evaluation : https://github.com/wondervictor/WiderFace-Evaluation

## 準備

+ 確認各專案需要的檔案已下載，並路徑正確

+ 把 `yoloface_AP/utilss.py` , `yoloface_AP/yolofaces.py` 移動至 `yoloface/`

+ 創建資料夾 : `yoloface/wider_val` , `yoloface/wider_out` , `WiderFace-Evaluation/wider`

+ 將 `WIDER_val/images/*` 移動至 `yoloface/wider_val/`

+ GroungTruth 放入 `WiderFace-Evaluation/wider/`  

## 執行

+ 產生 `evaluation.py` 要求的文件格式

      $ python3 yolofaces.py --image ./WIDER_val --output-dir ./wider_out/

+ 將 `yoloface/wider_out` 複製至 `WiderFace-Evaluation/`

+ 產生 yoloface 的 Val AP

      $ python3 evaluation.py -p ./wider_out -g ./wider

## 結果
| WIDER FACE | Val AP |
| ------------- |:-------------:|
| Easy | 0.6499619825770977 |
| Medium | 0.6711674249019364 |
| Hard | 0.5049559921986466 |
