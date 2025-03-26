import os
import sys

sys.path.append(".")
import json
import pandas as pd


def build_statistic(fname: str) -> None:
    xls_data = pd.ExcelFile(fname)
    src_path = "src/dicts/static"
    for sname in xls_data.sheet_names:
        if os.path.exists(os.path.join(src_path, f"{sname.strip()}.json")):
            print(sname)
            _er   = []
            ds = json.load(open(os.path.join(src_path, f"{sname.strip()}.json"), "r"))
            ds = {k.lower(): v.lower().replace("-", " ") for k, v in ds.items()}
            
            df = xls_data.parse(sname, skiprows=1)
            df = {df["từ lạ"][i].lower(): df["từ chuẩn hóa"][i].lower().replace("-", " ") for i in range(len(df["từ lạ"]))}
            ds.update(df)
            
            for k, v in ds.items():
                _er.extend([w for w in v.split() if w not in vn_words])
            _er = list(set(_er))
            print(list(set(_er)))
            ds = sorted([[k, v] for k, v in ds.items()], key=lambda x: x[0])
            ds = {k: v for k, v in ds}
            with open(os.path.join(src_path, f"{sname.strip()}.json"), "w", encoding="utf8") as f:
                json.dump(ds, f, ensure_ascii=False, indent=4)
    
    src_path = "src/dicts/unit"
    for sname in xls_data.sheet_names:
        if os.path.exists(os.path.join(src_path, f"{sname.strip()}.json")):
            print(sname)
            _er   = []
            ds = json.load(open(os.path.join(src_path, f"{sname.strip()}.json"), "r"))
            ds = {k: v.lower().replace("-", " ") for k, v in ds.items()}
            
            df = xls_data.parse(sname, skiprows=1)
            df = {df["từ lạ"][i]: df["từ chuẩn hóa"][i].lower().replace("-", " ") for i in range(len(df["từ lạ"]))}
            ds.update(df)
            
            for k, v in ds.items():
                _er.extend([w for w in v.split() if w not in vn_words])
            _er = list(set(_er))
            print(list(set(_er)))
            ds = sorted([[k, v] for k, v in ds.items()], key=lambda x: x[0])
            ds = {k: v for k, v in ds}
            with open(os.path.join(src_path, f"{sname.strip()}.json"), "w", encoding="utf8") as f:
                json.dump(ds, f, ensure_ascii=False, indent=4)
    

def build_abbs(fname: str) -> None:
    xls_data = pd.ExcelFile(fname)
    src_path = "src/dicts/abb"

    er = []
    df = xls_data.parse("Từ viết tắt độc lập (mới)", skiprows=2)
    ds = {}
    for i in range(len(df["từ chuẩn hóa"])):
        if isinstance(df["Note"][i], str): continue
        abb_word = df["từ viết tắt"][i].split("|")
        exp_word = df["từ chuẩn hóa"][i]
        for _abb in abb_word: ds[_abb.strip()] = exp_word.replace("-", " ")
    
    for k, v in ds.items():
        er.extend([w for w in v.split() if w not in vn_words])
    print(list(set(er)))
    ds = sorted([[k, v] for k, v in ds.items()], key=lambda x: x[0])
    ds = {k: v for k, v in ds}
    with open(os.path.join(src_path, "mono.json"), "w", encoding="utf8") as f:
        json.dump(ds, f, ensure_ascii=False, indent=4)
    
    er = []
    df = xls_data.parse("Từ viết tắt theo cặp (2 hoặc 3)", skiprows=2)
    ds = {}
    for i in range(len(df["từ chuẩn hóa"])):
        if isinstance(df["note"][i], str): continue
        abb_word = f"{df['từ 1'][i]}#{df['từ 2'][i]}"
        if isinstance(df["từ 3"][i], str): abb_word += f"#{df['từ 3'][i]}"
        exp_word = df["từ chuẩn hóa"][i]
        ds[abb_word.strip()] = exp_word.replace(",", " , ").replace("-", " ")
    ds = sorted([[k, v] for k, v in ds.items()], key=lambda x: x[0].split("#")[0])
    ds = {k: v for k, v in ds}
    for k, v in ds.items():
        er.extend([w for w in v.split() if w not in vn_words])
    print(list(set(er)))
    with open(os.path.join(src_path, "duo.json"), "w", encoding="utf8") as f:
        json.dump(ds, f, ensure_ascii=False, indent=4)



if __name__ == "__main__":
    vn_words = [x for x in open("src/dicts/words.txt", "r", encoding="utf8").read().split("\n") if x]
    # build_statistic("/home/ducnguyen/Works/Projects/Speech/tts-normalization/data/statistic_words.xlsx")
    # build_abbs("/home/ducnguyen/Works/Projects/Speech/tts-normalization/data/statistic_abbs.xlsx")

    xls_data = pd.ExcelFile("/home/ducnguyen/Works/Projects/Speech/tts-normalization/data/statistic_words.xlsx")
    _er   = []
    ds = json.load(open("src/dicts/abb/exception.json", "r"))
    ds = {k: v.lower().replace("-", " ") for k, v in ds.items()}
    
    df = xls_data.parse("exception", skiprows=1)
    df = {df["từ lạ"][i]: df["từ chuẩn hóa"][i].lower().replace("-", " ") for i in range(len(df["từ lạ"]))}
    ds.update(df)
    
    for k, v in ds.items():
        _er.extend([w for w in v.split() if w not in vn_words])
    _er = list(set(_er))
    print(list(set(_er)))
    ds = sorted([[k, v] for k, v in ds.items()], key=lambda x: x[0])
    ds = {k: v for k, v in ds}
    with open("src/dicts/abb/exception.json", "w", encoding="utf8") as f:
        json.dump(ds, f, ensure_ascii=False, indent=4)
