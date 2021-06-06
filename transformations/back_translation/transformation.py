from transformers import FSMTForConditionalGeneration, FSMTTokenizer

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


class BackTranslation(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    locales = ["en"]

    def __init__(self):
        super().__init__()
        print("Starting to load English to German Translation Model.\n")
        mname_en_de = "facebook/wmt19-en-de"
        self.tokenizer_en_de = FSMTTokenizer.from_pretrained(mname_en_de)
        self.model_en_de = FSMTForConditionalGeneration.from_pretrained(mname_en_de)
        print("Completed loading English to German Translation Model.\n")

        print("Starting to load German to English Translation Model:")
        mname_de_en = "facebook/wmt19-de-en"
        self.tokenizer_de_en = FSMTTokenizer.from_pretrained(mname_de_en)
        self.model_de_en = FSMTForConditionalGeneration.from_pretrained(mname_de_en)
        print("Completed loading German to English Translation Model.\n")

    def back_translate(self, en: str):
        try:
            de = self.en2de(en)
            en_new = self.de2en(de)
        except Exception:
            print("Returning Default due to Run Time Exception")
            en_new = en
        return en_new

    def en2de(self, input):
        input_ids = self.tokenizer_en_de.encode(input, return_tensors="pt")
        outputs = self.model_en_de.generate(input_ids)
        decoded = self.tokenizer_en_de.decode(outputs[0], skip_special_tokens=True)
        print(decoded)  # Maschinelles Lernen ist großartig, oder?
        return decoded

    def de2en(self, input):
        input_ids = self.tokenizer_de_en.encode(input, return_tensors="pt")
        outputs = self.model_de_en.generate(input_ids)
        decoded = self.tokenizer_de_en.decode(outputs[0], skip_special_tokens=True)
        print(decoded)  # Machine learning is great, isn't it?
        return decoded

    def generate(self, sentence: str):
        pertubed = self.back_translate(sentence)
        print(f"Perturbed Input from {self.name()} : {pertubed}")
        return pertubed