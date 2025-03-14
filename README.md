# Dashboard Proyek Analisis Data

## Setup Environment - Anaconda

'''sh
conda create --name main-ds python=3.12
conda activate main-ds
pip install -r requirements.txt

## Setup Environment - Shell/Terminal

'''sh
mkdir Proyek-Analisis-Data-Dicoding
cd Proyek-Analisis-Data-Dicoding
pipenv install
pipenv shell
pip install -r requirements.txt

## Run streamlit app

'''sh
streamlit run dashboard.py
