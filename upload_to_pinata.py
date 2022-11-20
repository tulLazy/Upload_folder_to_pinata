# Tulli's script :-)
from brownie import config
import requests, os, typing as tp


PINATA_BASE_URL = "https://api.pinata.cloud/"
endpoint = "pinning/pinFileToIPFS"
# Here you could use os.getenv("VARIABLE_NAME"),
# i used config from my .yaml file. Your choice!
headers = {
    "pinata_api_key": config["pinata"]["api-keys"],
    "pinata_secret_api_key": config["pinata"]["api-private"],
}


def get_all_files(directory: str) -> tp.List[str]:
    """get a list of absolute paths to every file located in the directory"""
    paths: tp.List[str] = []
    for root, dirs, files_ in os.walk(os.path.abspath(directory)):
        for file in files_:
            paths.append(os.path.join(root, file))
    return paths


def upload_folder_to_pinata(filepath):
    all_files: tp.List[str] = get_all_files(filepath)
    # The replace function is a must, 
    # pinata servers doesn't recognize the backslash. 
    # Your filepath is probably different than mine,
    # so in the split function put your "penultimate_file/".
    # Strip the square brackets and the apostrophe,
    # because we don't want it as part of the metadata ipfs name
    files = [
        (
            "file",
            (
                str(file.replace("\\", "/").split("metadata/")[-1:])
                .strip("[]")
                .strip("'"),
                open(file, "rb"),
            ),
        )
        for file in all_files
    ]
    response: requests.Response = requests.post(
        PINATA_BASE_URL + endpoint,
        files=files,
        headers=headers,
    )
    print(
        "The base URI is: https://ipfs.io/ipfs/"
        + str(response.json()["IpfsHash"])
        + "/"
    )
    return "https://ipfs.io/ipfs/" + response.json()["IpfsHash"] + "/"


def main():
    upload_folder_to_pinata("Put your full filepath here")


if __name__ == "__main__":
    main()
