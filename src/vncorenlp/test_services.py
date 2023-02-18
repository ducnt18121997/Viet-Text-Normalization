from vncorenlp import VnCoreNLP
import time

segmenter = VnCoreNLP("VnCoreNLP-1.1.1.jar", annotators="wseg", max_heap_size='-Xmx500m')

text = "Làm thế nào để khích lệ người khác, thúc đẩy họ nỗ lực cho tầm nhìn chung?\" Đó chỉ là một vài câu hỏi quan " \
       "trọng mà hai tác giả James M. Kouzes và Barry Z. Posner sẽ đề cập trong cuốn sách \"Những thách thức của nhà " \
       "lãnh đạo\". "

t = time.time()
sentences = segmenter.tokenize(text)
print(sentences)