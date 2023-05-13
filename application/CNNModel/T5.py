# 加载模型
import torch
from transformers import T5ForConditionalGeneration

model = T5ForConditionalGeneration.from_pretrained('t5-base')
model.load_state_dict(torch.load('T5model.pt'))

# 设置设备
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = model.to(device)

# 准备输入
input_text = "这是一个输入示例"
input_ids = tokenizer.encode(input_text, return_tensors='pt').to(device)

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