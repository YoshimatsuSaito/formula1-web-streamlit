mkdir -p ~/.kaggle
mkdir -p ../data
cp kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json
kaggle datasets download -d rohanrao/formula-1-world-championship-1950-2020 -p ../data/
unzip ../data/formula-1-world-championship-1950-2020.zip -d ../data/