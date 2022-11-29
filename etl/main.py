from upload_blob import uploadToBlobStorage


data_path = "/home/danh/WORK/codes/myprojects/credit-risk/data/"
file_names = ["interest_rate_usa"]

for file_name in file_names:
    uploadToBlobStorage(f"{data_path}{file_name}", f"{file_name}")