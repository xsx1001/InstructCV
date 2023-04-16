# ** Description ** Rephrase the prompts
# --------------------------------------------------------
# References:
# https://huggingface.co/humarin/chatgpt_paraphraser_on_T5_base
# --------------------------------------------------------

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import random


device = "cuda"# not use


class Rephrase(object):
    
    def __init__(self, text, num_beams=5, 
                 num_beam_groups=5, num_return_sequences=5,
                 repetition_penalty=5.0, diversity_penalty=5.0,
                 no_repeat_ngram_size=5, temperature=0.7, max_length=128
                 ):
        
        self.text = text
        self.tokenizer              = AutoTokenizer.from_pretrained("humarin/chatgpt_paraphraser_on_T5_base")
        self.model                  = AutoModelForSeq2SeqLM.from_pretrained("humarin/chatgpt_paraphraser_on_T5_base")
        self.num_beams              = num_beams
        self.num_beam_groups        = num_beam_groups
        self.num_return_sequences   = num_return_sequences
        self.repetition_penalty     = repetition_penalty
        self.diversity_penalty      = diversity_penalty
        self.no_repeat_ngram_size   = no_repeat_ngram_size
        self.temperature            = temperature
        self.max_length             = max_length
        
        
    def do(self):
        input_ids = self.tokenizer(
            f'paraphrase: {self.text}',
            return_tensors = "pt", padding="longest",
            max_length = self.max_length,
            truncation = True,
        ).input_ids
        
        outputs = self.model.generate(
            input_ids, temperature = self.temperature, repetition_penalty = self.repetition_penalty,
            num_return_sequences = self.num_return_sequences, no_repeat_ngram_size = self.no_repeat_ngram_size,
            num_beams = self.num_beams, num_beam_groups = self.num_beam_groups,
            max_length = self.max_length, diversity_penalty = self.diversity_penalty
        )

        res = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)
        
        res.append(self.text)
        res.append(self.text.replace("help me",""))
        
        res = random.choice(res)

        return res

if __name__ == "__main__":
    
    text = 'help me segment the %'
    output = Rephrase(text).do()
    print("output", type(output))
    print("output", len(output))
    print("output", output)
