import json
import os


def get_note_type_for_file(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)

    for entry in data:
        # 该 entry 可能有多个 ph
        n = len(entry["ph"])
        if entry["word"] in ["<SP>", "<AP>"]:
            entry["note_type"] = [1] * n  # rest
        else:
            entry["note_type"] = [2] * n  # lyric

    with open(json_path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def align_to_ph_length(arr, n_ph):
    if len(arr) == n_ph:
        return arr
    elif len(arr) > n_ph:
        # 截断
        return arr[:n_ph]
    else:
        # 填充
        return arr + [arr[-1]] * (n_ph - len(arr))


def process_json(json_path, item_name, wav_fn):
    get_note_type_for_file(json_path)

    with open(json_path, "r") as f:
        data = json.load(f)
    ph = []
    ep_pitches = []
    ep_notedurs = []
    ep_types = []
    ph_durs = []
    for entry in data:
        n_ph = len(entry["ph"])
        note = align_to_ph_length(entry["note"], n_ph)
        note_dur = align_to_ph_length(entry["note_dur"], n_ph)
        note_type = align_to_ph_length(entry["note_type"], n_ph)
        ph.extend(entry["ph"])
        ep_pitches.extend(note)
        ep_notedurs.extend(note_dur)
        ep_types.extend(note_type)
        for start, end in zip(entry["ph_start"], entry["ph_end"]):
            ph_durs.append(end - start)

    # 最终再检查一遍
    assert (
        len(ph) == len(ep_pitches) == len(ep_notedurs) == len(ep_types)
    ), f"最终长度不一致: ph={len(ph)}, pitch={len(ep_pitches)}, dur={len(ep_notedurs)}, type={len(ep_types)}"

    return {
        "item_name": item_name,
        "ph": ph,
        "ep_pitches": ep_pitches,
        "ep_notedurs": ep_notedurs,
        "ep_types": ep_types,
        "wav_fn": wav_fn,
        "ph_durs": ph_durs,
    }


if __name__ == "__main__":
    # 你需要手动指定 item_name 和 wav_fn
    gen_item = process_json(
        "data/processed/tc/gen.json",
        "Chinese#ZH-Alto-1#Mixed_Voice_and_Falsetto#一次就好#Mixed_Voice_Group#0001",
        "/storage/zhangxueyao/dataset/2024-NeurIPS-GTSinger/Chinese/ZH-Alto-1/Mixed_Voice_and_Falsetto/一次就好/Mixed_Voice_Group/0001.wav",  # 你实际的音频文件路径
    )
    ref_item = process_json(
        "data/processed/tc/ref.json",
        "English#EN-Alto-2#Mixed_Voice_and_Falsetto#A Thousand Years#Control_Group#0001",
        "/storage/zhangxueyao/dataset/2024-NeurIPS-GTSinger/English/EN-Alto-2/Mixed_Voice_and_Falsetto/A Thousand Years/Control_Group/0001.wav",  # 你实际的音频文件路径
    )

    with open("data/processed/tc/metadata.json", "w") as f:
        json.dump([gen_item, ref_item], f, ensure_ascii=False, indent=2)
