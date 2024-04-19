# Load model directly
from transformers import AutoTokenizer, AutoModel
import os
import json
import logging


# Define the model prediction function (replace 'YourModelClass' with the actual class name)
def predict(contents, tokenizer, output_style='json'):
    predictions = model.predict([contents], tokenizer, output_style='json')
    return predictions

# Iterating on all songs in the given root_folder path, modeling them and saving outputs as JSON in the dedicated output_file_path
def read_files_in_folder_and_write_to_file(root_folder, output_file_path):

        # Traverse through all subdirectories and files in the root_folder
        logger.info("Starting to iterate over songs in folder: {0}".format(root_folder))
        for foldername, subfolders, filenames in os.walk(root_folder):
            for filename in filenames:
                    logger.info("Starting to model song: {0}".format(filename))
                    # Get the full path of the current file
                    file_path = os.path.join(foldername, filename)

                    # Read the contents of the file
                    with open(file_path, 'r' ,encoding='utf-8') as file:
                        file_contents = file.read()
                        
                        # Split the filename and its extension
                        purefilename, extension = os.path.splitext(filename)
                        # Define the output file path
                        currfilepath = os.path.join(output_file_path,purefilename +".json")
                        
                        prediction = predict(file_contents,tokenizer,'json')

                        with open(currfilepath, 'w', encoding='utf-8') as output_file:
                            for chunk in prediction:
                               json.dump(chunk, output_file, ensure_ascii=False)
                               output_file.write('\n')  # Add a newline for each chunk

                    logger.info("Starting to model song: {0} - COMPLETED".format(filename))

        logger.info("Iterating over songs in folder {0} - COMPLETED".format(root_folder))
                        
def setup_logger(log_file="./BERT analysis/Logs/logfile.log", log_level=logging.INFO):
    # Create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    # Create a file handler and set the level
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)

    # Create a console handler and set the level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)

    # Create a formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

if __name__ == "__main__":

    # Set up logger
    logger = setup_logger()

    # Paths for songs locations (old and new)
    logger.info("Setting file paths for songs and outputs")
    dor_ha_medina_songs_path = './BERT analysis/Songs/Dor Hamedina Songs'
    present_songs_path = './BERT analysis/Songs/Present Songs'

    # Paths for output files location to be saved after the modeling (for old and new)
    output_path_for_dor_hamedina = './BERT analysis/outputs/Dor Ha-Medina BERT output/'
    output_path_for_present = './BERT analysis/outputs/Present BERT output/'
    logger.info("Setting file paths for songs and outputs - COMPLETED")

    # setting up model
    logger.info("Setting up BERT model")
    tokenizer = AutoTokenizer.from_pretrained("dicta-il/dictabert-tiny-joint", trust_remote_code=True)
    model = AutoModel.from_pretrained("dicta-il/dictabert-tiny-joint", trust_remote_code=True)
    model.eval()    
    logger.info("Setting up BERT model - COMPLETED")

    # creating BERT modules for both the old and new songs and saving the outputs unter the corresponding output paths
    logger.info("Starting iterating over DOR HEMEDINA songs, modeling and saving outputs")
    read_files_in_folder_and_write_to_file(dor_ha_medina_songs_path,output_path_for_dor_hamedina)
    logger.info("Modeling DOR HAMEDINA songs - COMPLETED")
    logger.info("Starting iterating over PRESENT songs, modeling and saving outputs")
    read_files_in_folder_and_write_to_file(present_songs_path,output_path_for_present)
    logger.info("Modeling PRESENT songs - COMPLETED")

    

