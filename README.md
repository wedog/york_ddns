# york_ddns
pip3 freeze > requirements.txt

pip3 install -r requirements.txt

pyinstaller --hidden-import charset_normalizer.md__mypyc  --onefile alibabacloud_sample/sample.py
