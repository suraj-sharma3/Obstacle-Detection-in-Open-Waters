# Step 1 : Install kaggle library with pip install kaggle
# Step 2 : Generate kaggle.json file containing the API token from kaggle website
# Step 3 : Put the downloaded kaggle.json file at this path in your system (For Windows) : C:\Users\<Your Username>\.kaggle\kaggle.json
# Step 4 : Run the below given code

import kaggle
kaggle.api.authenticate() # this will look for kaggle.json file and authenticate the API token the file contains
kaggle.api.dataset_download_files("vencerlanz09/sea-animals-image-dataste", path = ".", unzip=True) # First argument - dataset uploader's user name/dataset name, second argument - path where the dataset has to be saved, third argument - whether the dataset has to be downloaded in unzipped form or not

# # To download the metadata for a dataset
kaggle.api.dataset_metadata("vencerlanz09/sea-animals-image-dataste", path = ".")

# # To list down all the files the dataset contains
print(kaggle.api.dataset_list_files("vencerlanz09/sea-animals-image-dataste").files)

# To search for datasets on kaggle with keywords
datasets = kaggle.api.dataset_list(search = 'sea animals dataset')
print(datasets)