# 加载模型
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
#from googletrans import Translator

# translator = Translator(service_urls=['translate.google.com', ])
#
# detection = translator.detect('你好')
# print(detection.lang)
#
# trans = translator.translate('你好', dest='en')
# # translated text
# print(trans.text)

model = T5ForConditionalGeneration.from_pretrained('t5-base')
model.load_state_dict(torch.load('T5model.pt',map_location='cpu'))
tokenizer = T5Tokenizer.from_pretrained("t5-base",model_max_length=1024)
# # 设置设备
#
# model = torch.load(")
# model = model.to(device)
# prepare the text
input_text = "你好"
input_ids = tokenizer.encode(input_text, return_tensors='pt')

# 生成摘要
outputs = model.generate(input_ids=input_ids,
                          max_length=150,
                          num_beams=2,
                          repetition_penalty=2.5,
                          length_penalty=1.0,
                          early_stopping=True)

# 解码输出
output_text = tokenizer.decode(outputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)

# 打印输出
print(output_text)
