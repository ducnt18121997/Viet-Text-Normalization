<div align="center">

# Text Normalization System - Regrex Implementation

This is Python Implementation based on Regrex & Rule-based for convert writing words to reading words, researched and developed by Dean Ng.

[![python](https://img.shields.io/badge/-Python_3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/downloads/release/python-3815/)
[![regrex](https://img.shields.io/badge/-regrex_2.2.1-grey?logo=pypi&logoColor=white)](https://pypi.org/project/regex/)

</div>


## Features

- Vietnamese text normalization
- Special character handling
- Number and currency normalization
- Date format normalization
- Support for superscript and subscript characters
- Complex text pattern recognition
- Unit and currency handling
- Roman numeral processing

## Installation


```bash
conda create --name venv python=3.8
pip install -r requirements.txt
```

3. Set up Java environment (required for VnCoreNLP):
- Install Java JDK (version 21 or compatible)
- Set JAVA_HOME environment variable to your JDK installation path

## Usage

```python
from cores.normalizer import TextNormalizer

# Initialize the normalizer with VnCoreNLP model path
text_normalizer = TextNormalizer("./exps/vncorenlp/")

# Normalize text
text = "1. Những ngân hàng đang có lãi suất cho vay bình quân cao như Liên Việt, Bản Việt, Kiên Long với lãi suất từ 8,07 $ -  8,94$..."
normalized_text = text_normalizer(text)
```

## Project Structure

```
text-normalization/
├── constants/         # Character sets and constants
├── cores/            # Core normalization logic
├── exps/             # Experiment configurations
├── logs/             # Log files
├── utils/            # Utility functions
├── example.py        # Usage examples
└── requirements.txt  # Project dependencies
```

## Reference
> NOTE: I may forgot repo that I use to reference for this repo, please create issue ticket and I will update it. Thank you very much

- [VnCoreNLP: A Vietnamese Natural Language Processing Toolkit](https://aclanthology.org/N18-5012/) (Vu et al., NAACL 2018)
- [Vinorm: A Vietnamese Text Normalizer](https://github.com/v-nhandt21/Vinorm) (Nhan et al., 2021)

## Cite
If you find this repository useful for your research, please cite:
```bibtex
@misc{deanng_2025,
    author = {Dean Nguyen},
    title = {Vietnamese Text Normalization},
    year = {2025},
    publisher = {GitHub},
    journal = {GitHub repository},
    howpublished = {\url{https://github.com/ducnt18121997/text-normalization}}
}
```
