from fastapi import HTTPException
from typing import List, Union
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


    def detect(self, images: Union[List[Image], Image]):
        inputs = self.image_processor(images=images, return_tensors="pt")
        outputs = self.model(**inputs)

        results = self.image_processor.post_process_object_detection(
            outputs,
            threshold=0.9
        )

        responses = []

        for result in results:
            human = False
            for score, label in zip(result["scores"], result["labels"]):
                if self.model.config.id2label[label.item()] == "person" and round(score.item(), 3) > 0.9:
                    human = True
            if human:
                responses.append("There is person on photo with confidence over 90%")
            else:
                responses.append("Probably there is no any person on photo")

        return responses


    def from_pic(self, image: Image):
        inputs = self.image_processor(images=image, return_tensors="pt")
        outputs = self.model(**inputs)

        results = self.image_processor.post_process_object_detection(
            outputs,
            threshold=0.9
        )[0]

        human = False
        for score, label in zip(results["scores"], results["labels"]):
            if self.model.config.id2label[label.item()] == "person" and round(score.item(), 3) > 0.8:
                human = True
        if human:
            return "There is person on photo with confidence over 80%"
        else:
            raise HTTPException(
                status_code=445,
                detail="Probably there is no any person on photo"
            )
