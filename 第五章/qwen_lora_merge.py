# qwen_lora_merge.py
# 1 模型合并

from peft import AutoPeftModelForCausalLM

path_to_adapter = "/media/waj/新加卷/github/NLP/test/Qwen-main/output_qwen/checkpoint-1200/"
new_model_directory = "/media/waj/新加卷/github/NLP/llm_model/Qwen-1_8B-Chat_law2"

model = AutoPeftModelForCausalLM.from_pretrained(
    path_to_adapter,  # path to the output directory
    device_map="auto",
    trust_remote_code=True
).eval()

merged_model = model.merge_and_unload()

# max_shard_size and safe serialization are not necessary.
# They respectively work for sharding checkpoint and save the model to safetensors
merged_model.save_pretrained(new_model_directory, max_shard_size="2048MB", safe_serialization=True)

# 2 分词器保存
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(
    path_to_adapter,  # path to the output directory
    trust_remote_code=True
)

tokenizer.save_pretrained(new_model_directory)