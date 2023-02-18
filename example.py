"""
\t** \033[92mpre_process condition \033[0m *     :
\t** \033[94mfirst_normalize condition \033[0m * :
\t** \033[93mclassify number \033[0m             : 
\t** \033[96msecond_normalize condition \033[0m *: 
\t** \033[92men2vi function (dict) \033[0m       :
\t** \033[92men2vi function (lematize) \033[0m   :
\t** \033[92men2vi function (ipa2vi) \033[0m     :
\t** \033[92men2vi function (dict) \033[0m       :
\t** \033[91m Errors en2vi \033[0m               :
\t** \033[91m pre_process condition  \033[0m     :
\t** \033[91m mix unit check  \033[0m            :
"""
import time
from src import TextNormalizer


if __name__ == "__main__":
    tik             = time.time()
    text_normalizer = TextNormalizer("models/new_classifier/models/weights.pt", "src/vncorenlp/VnCoreNLP-1.1.1.jar")
    text_inputs     = "HLV Park Hang-seo sẽ không rời Việt Nam lâu, ít nhất là trong vài tháng tới. Theo tờ Newsis, ông sẽ trở về Hàn Quốc vào ngày 14/2 tới nhưng sau đó 2 ngày đã đáp chuyến bay trở lại Việt Nam."
    print(f"[*] take {time.time} seconds")
    print(text_inputs)
    print("==")
    print(text_normalizer.normalize(text_inputs))
