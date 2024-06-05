from mmocr.apis import MMOCRInferencer
ocr = MMOCRInferencer(det='DBNet', rec='CRNN')
ocr('../../mmocr/demo/demo_text_ocr.jpg', show=False, print_result=True)