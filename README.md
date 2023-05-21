# PLP
for nlp project
## SECTION : Installation and User Guide

### [ 1 ] System Environment Requirement

1. Install [python >=3.9](https://www.python.org/downloads/)

2. Google Chrome (latest version)

3. Install latest git version

### [ 2 ] Prepare basic project enviorment and create an virtual enviorment of python

1. Create a folder in computer to storage the project file and open a terminal in this folder:

 >git clone https://github.com/dtepp/PLP

 >cd PLP

 >python -m venv venv

 >venv\Scripts\activate(windows) OR: source venv/bin/activate(mac)

 >pip install -r requirements.txt


### [ 3 ] Configuration of T5 Translation Detector

1. First, please download the T5 model checkpoints file called 
   *Step-5623_checkpoint_lang_pred.pt* from Google Drive:
    https://drive.google.com/file/d/1-YtgsZxxbGnh1SHnd21aKxH8_voCC2LH/view?usp=sharing

2. Place the file in the same directory as app.py

3. If you face below error:
![image](https://github.com/dtepp/PLP/assets/38468080/9e1dcf85-960b-4ccb-a668-a4139b4fa3c5)
    please run
    >set PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python 
    
    in your terminal for current venv environment

### [ 4 ] Configuration of Bert Model

1. First, please download the Bert model checkpoints file called 
   *pytorch_model.bin* from Google Drive:
    https://drive.google.com/file/d/1-cYurHnp3mIJyCYuNhDHfXXhfwzsmp0V/view?usp=sharing

2. Place the file in the same directory as app.py

### [ 5 ] Run the systems on browser
Go to URL using web browser**http://127.0.0.1:5000
Or: Directly click the link on the frontend terminal

