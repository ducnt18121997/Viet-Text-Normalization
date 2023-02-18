import os
import sys
import torch
import pickle
import numpy as np
from loader import cap_feature


if __name__ == "__main__":
    checkpoint = sys.argv[1]

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    with open(os.path.join(os.path.dirname(checkpoint), "mapping.pkl"), "rb") as f:
        mappings = pickle.load(f)

    word_to_id = mappings["word_to_id"]
    char_to_id = mappings["char_to_id"]
    id_to_tag = {k[1]: k[0] for k in mappings["tag_to_id"].items()}
    parameters = mappings["parameters"]

    nnet = torch.load(checkpoint).to(device)

    text = "Hội_đồng xét_xử thừa_nhận rằng , ngày 12/2/1968 , binh_lính thuộc Đại_đội 1 , Lữ_đoàn 2 Thuỷ_quân_lục_chiến của quân_đội Hàn_Quốc đã sát_hại trên 70 dân_thường ở làng Phong_Nhị , trong đó có người_thân của nguyên_đơn .".replace("_", " ").split()
    word_seqs = [word_to_id[w] for w in text]
    word_seqs = torch.LongTensor(word_seqs)
    char_idx = [[char_to_id[c] for c in w] for w in text]
    char_length = [len(c) for c in char_idx]
    char_maxl = max(char_length)
    char_seqs = np.zeros((len(char_length), char_maxl), dtype='int')
    for i, c in enumerate(char_idx):
        char_seqs[i, :char_length[i]] = c
    char_seqs = torch.LongTensor(char_seqs)
    cap_mask = torch.LongTensor([cap_feature(w) for w in text])

    score, labels = nnet(word_seqs.to(device), char_seqs.to(device), cap_mask.to(device), char_length, {})
    for idx in range(len(text)):
        print(f"- {text[idx]}: {id_to_tag[labels[idx]]}")