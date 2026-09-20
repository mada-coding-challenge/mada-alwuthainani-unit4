echo "create project..."
mkdir src 
touch src/main.py README.md
python3 -m venv venv 
pip3 install requests 
pip3 list 
pip3 freeze > requirements.txt 
pip3 install -r requirements.txt
source venv/bin/activate
pip install django
echo "project created successfully"