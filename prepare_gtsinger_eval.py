from gen_metadata import process_json
import json
import os
from tqdm import tqdm

if __name__ == "__main__":
    en_file = "/storage/zhangxueyao/workspace/SpeechGenerationYC/EvalSet/svs/gtsinger_svs_en/evalset.json"
    zh_file = "/storage/zhangxueyao/workspace/SpeechGenerationYC/EvalSet/svs/gtsinger_svs_zh/evalset.json"

    evalset = []
    with open(en_file, "r") as f:
        en_data = json.load(f)
    with open(zh_file, "r") as f:
        zh_data = json.load(f)

    evalset = en_data + zh_data

    processed_evalset = []
    for item in tqdm(evalset):
        for k in ["input", "prompt"]:
            wav_path = item[k]["wav_path"]
            json_path = wav_path.replace(".wav", ".json")
            uid = item[k]["uid"]

            processed_item = process_json(
                json_path=json_path,
                item_name=uid,
                wav_fn=wav_path,
            )
            processed_evalset.append(processed_item)

    save_dir = "data/processed/gtsinger_eval"
    os.makedirs(save_dir, exist_ok=True)

    with open(os.path.join(save_dir, "metadata.json"), "w") as f:
        json.dump(processed_evalset, f, ensure_ascii=False, indent=2)
