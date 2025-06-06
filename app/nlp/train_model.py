from app.nlp.model_trainer_config import trainer_fn
from app.models.config import train_data
from sklearn.model_selection import train_test_split
import shutil
import os
from pathlib import Path

# split data
train_split, test_split = train_test_split(train_data, test_size=0.2, random_state=42)

#train data
trainer = trainer_fn(data=train_split, test_data=test_split)
trainer.train()

#save model
trainer.save_model("./ner-model")
trainer.tokenizer.save_pretrained("./ner-model")

output_dir = "./bert-ner-output"
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)