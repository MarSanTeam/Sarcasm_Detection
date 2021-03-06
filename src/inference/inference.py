from typing import List
import numpy
import torch
from configuration import BaseConfig

CONFIG_CLASS = BaseConfig()
CONFIG = CONFIG_CLASS.get_config()


class Inference:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def tokenizing_sentences(self, sentence: str, max_length: int):
        inputs = self.tokenizer.encode_plus(
            text=sentence,
            add_special_tokens=True,
            max_length=max_length,
            padding="max_length",
            return_attention_mask=True,
            truncation=True,
            return_tensors="pt"
        )
        return inputs

    def predict(self, inputs):
        outputs = self.model(inputs)
        pred = numpy.argmax(outputs.cpu().detach().numpy(), axis=1)
        outputs = torch.nn.Softmax()(outputs)
        return list(pred), outputs.tolist()

    def predict_multi(self, inputs):
        output_sarcasm, output_irony, output_satire, output_understatement, \
        output_overstatement, output_rhetorical_question = self.model(inputs)

        output_sarcasm = numpy.argmax(output_sarcasm.cpu().detach().numpy(), axis=1)
        output_irony = numpy.argmax(output_irony.cpu().detach().numpy(), axis=1)
        output_satire = numpy.argmax(output_satire.cpu().detach().numpy(), axis=1)
        output_understatement = numpy.argmax(output_understatement.cpu().detach().numpy(), axis=1)
        output_overstatement = numpy.argmax(output_overstatement.cpu().detach().numpy(), axis=1)
        output_rhetorical_question = numpy.argmax(output_rhetorical_question.cpu().detach().numpy(), axis=1)
        return list(output_sarcasm), list(output_irony), list(output_satire), list(output_understatement),\
               list(output_overstatement), list(output_rhetorical_question)


    def convert_ids_to_entities(self, predicted_tags: List[list]) -> List[list]:
        """

        :param predicted_tags: [[ t1, t2, ..., tn][t1, t2, ..., tn]]
        :return:
        """
        outputs = [self.model.hparams["idx2tag"][tag] for tag in predicted_tags[0]]
        # outputs = [[self.model.hparams["idx2tag"][tag] for tag in item]
        #            for item in predicted_tags]
        return outputs

    def convert_token_id_to_token(self, batched_sample: dict) -> List[list]:
        """

        :param batched_sample:
        :return:
        """
        sentence = [self.tokenizer.convert_ids_to_tokens(idx) for idx in batched_sample["input_ids"]]
        return sentence
