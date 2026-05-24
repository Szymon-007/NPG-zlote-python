emaile sie wysyalaja aby sie poaczyc z poczata nalezy wpisac dane polaczenia z kontem google do enva. zalozenie truktury jesttakie ze:
-floder bazy_danych 
-email_send.py
-email_template.html (link ktory jest do wpisania powinien przepierowywac na strone logowania 82 linia kodu w email_send.py)

Po klonie repozyturoim nalezy odworzyc windows PowerShell w folderze projektu i odpalic następujące pliki:
- python quotes_seeder.py
- .venv\Scripts\python.exe -m uvicorn app.main:app --reload
- przechodzimy do folderu frontend cd frontend
- npm install
- npm run dev
- strona https://localhost:5173/
