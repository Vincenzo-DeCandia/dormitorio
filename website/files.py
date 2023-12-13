import os


def upload_file(file_list, path, _id=None, file_counter=1):
    os.mkdir(path + f'{_id}')
    for file in file_list:
        file_extension = os.path.splitext(file.filename)[1]  # Estrai l'estensione del file
        file_name = f'{file_counter}{file_extension}'

        if file.filename != '':
            file.save(os.path.join(path + f'{_id}', file_name))
            file_counter += 1


def download_file(path, _id):
    pass
