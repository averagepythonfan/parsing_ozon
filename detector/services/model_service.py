from typing import List
import torch
from PIL.Image import Image
from transformers import YolosImageProcessor, YolosForObjectDetection
from detector.config import REPO_PATH


class Singleton(object):
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance


class ModelService(Singleton):

    
    def __init__(self, repo_path: str = REPO_PATH) -> None:
        self.model = YolosForObjectDetection.from_pretrained(repo_path, local_files_only=True)
        self.image_processor = YolosImageProcessor.from_pretrained(repo_path, local_files_only=True)


    def _get_inputs(self, image: Image):
        return self.image_processor(images=image, return_tensors="pt")


    def detect(self, images: List[Image]):
        inputs = self._get_inputs(image=images)
        outputs = self.model(**inputs)

        results = self.image_processor.post_process_object_detection(
            outputs,
            threshold=0.9
        )

        responses = []

        for result in results:
            for score, label in zip(result["scores"], result["labels"]):
                if self.model.config.id2label[label.item()] == "person" and round(score.item(), 3) > 0.9:
                    responses.append("There is person on photo with confidence over 90%")
                else:
                    responses.append("Probably there is no any person on photo")

        return responses
