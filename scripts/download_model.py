import os
from pathlib import Path
from huggingface_hub import snapshot_download


REPO_ID = "hustvl/yolos-tiny"


def main():
    hg_repo_path = os.getcwd() + "/model/"
    dir_exist = Path(hg_repo_path).is_dir()
    model_exist = Path(hg_repo_path + "pytorch_model.bin").exists()

    if dir_exist and model_exist:
        print("`model` directory and `pytorch_model.bin` already exist")
    else:
        print(f"Downloading repository from HuggingFace, {REPO_ID}")
        snapshot_download(repo_id=REPO_ID, local_dir=hg_repo_path)


if __name__ == "__main__":
    main()