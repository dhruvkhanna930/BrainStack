echo " BUILD START"
# build_files.sh
python3 -m pip install -r requirements.txt
python3.10 manage.py collectstatic
echo " BUILD END"