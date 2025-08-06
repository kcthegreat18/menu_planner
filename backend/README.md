cd backend
python -m venv env
.\env\Scripts\Activate.ps1
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

cd backend_app
python manage.py runserver