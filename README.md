<div align="center">

# Text Normalization System - Regrex Implementation

This is Python Implementation based on Regrex & Rule-based for convert writing words to reading words, researched and developed by Dean Ng.

[![python](https://img.shields.io/badge/-Python_3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/downloads/release/python-3815/)
[![regrex](https://img.shields.io/badge/-regrex_2.2.1-grey?logo=pypi&logoColor=white)](https://pypi.org/project/regex/)

</div>


<h1> 1. Installation </h1>

```
conda create --name venv python=3.8
pip install -r requirements.txt
```

<h1> 2. Running </h1>

**2.1. Function Description**

```bash
src/normalizer.py: Chứa class TextNormalizer biểu diễn 3 bước theo flow của text normalize
```

```bash
src/config.py: Chứa json được load từ folder src/dicts
src/regrex.py: Chứa các hàm normalize bằng regrex
src/rule.py: Chứa các hàm normalize bằng rules (cho những case NSWs còn lại)
src/en2vi.py: Hàm đọc tiếng anh
```

```bash
src/modules/: Chứ các hàm biểu biểu diễn cách đọc cho từng loại NSW cụ thể
src/modules/build_en2vi.py: Hàm xây dựng từ điển đọc tiếng anh
```

**2.1. Dictionary Description**

```bash
src/dicts/: Chứa các bộ từ điển tiếng việt
src/modules/en2vi/dicts: Chứa các bộ từ điển tiếng anh
```

**2.1. API Function**

```bash
# use when no-java environment
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/
python api.py 
    --vncorenlp /absolute_path_vn_corenlp_model
    --port /port_number
```

<h1> 3. Documentation </h1>

See [Detail Documentation](https://docs.google.com/document/d/1r5tIlGK-BxnBGWNE0Hi7SM6Kw1lIAczCC1zV5c36iL4/edit?usp=sharing)