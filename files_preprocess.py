import os

folder_path = 'media/cards'

def delete_unnecessary():
    # Iterate through files in the folder
    for filename in os.listdir(folder_path):
        # Change the file name
        new_filename = filename.lstrip('0')
        new_filepath = os.path.join(folder_path, new_filename)

        # Rename the file
        os.replace(os.path.join(folder_path, filename), new_filepath)

        # Perform additional checks or operations on the file
        print(int(new_filename[:-4]))
        if int(new_filename[:-4]) % 2 == 0:
            # Delete the file
            os.remove(new_filepath)


card_ranks = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']
suits = ['spades', 'hearts', 'clubs', 'diamonds']
card_names = []
for suit in suits:
    for rank in card_ranks:
        card_names.append(f'{rank}_{suit}')    



def final_names():
    for i, card in zip(range(1, 104, 2), card_names):
        # Change the file name
        new_filename = card + '.svg'
        new_filepath = os.path.join(folder_path, new_filename)

        # Rename the file
        os.replace(os.path.join(folder_path,  f'{i}.svg'), new_filepath)

final_names()
                        



