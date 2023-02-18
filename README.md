# Normalize-text for TTS
## 1. Active Flow

```flow
 - Step 0: Preprocessing (xử lý trường hợp gây lỗi)
 - Step 1: Text Segmentation (open source: vncorenlp)
 - Step 2: Text Normalize turn 1 
 - Step 3: Parse NSWs
 - Step 4: Text Normalize turn 2 
```

## 2. Run

```bash
    $ python api.py --checkpoint /path/to/classify/models --port port_number
```

## 3. Function

```bash
    src/__init__.py: Chứa class TextNormalizer biểu diễn 5 bước theo flow của text normalize
    models/: folder chứa model, dữ liệu và hàm training cho mô hình classify text normalize
```
```bash
    src/config.py: Chứa json được load từ folder src/dicts
    src/letter2vi.py: Hàm đọc các NSWs dạng chữ (bao gồm 3 dạng: UPPER, lower/Capitalize và MiX)
    src/number2vi.py: Hàm phân loại NSWs dạng số (bao gồm 5 dạng: TIM, DAY, MON, NUM và DIG)
    src/en2vi.py: Hàm đọc tiếng anh
```

```bash
    src/modules/: Chứ các hàm biểu biểu diễn cách đọc cho từng loại NSW cụ thể
    src/modules/build_en2vi.py: Hàm xây dựng từ điển đọc tiếng anh
```
## 4. Từ điển
```bash
    src/dicts/: Chứa từ điển tiếng việt
    src/modules/en2vi/dicts: Chứa các từ điên tiếng anh
```
