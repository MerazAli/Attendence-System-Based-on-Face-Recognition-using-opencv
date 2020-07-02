import os

def create_user_folder(name,roll):
    if not os.path.exists("dataset"):
        os.mkdir('dataset')
    foldername = name.strip().split()[0]+"_"+roll.strip()
    if os.path.exists("dataset/"+foldername):
        return None
    else:
        os.mkdir("dataset/"+foldername)
        return "dataset/"+foldername
        