# 📝 MasterBlog API

A simple Flask-based backend application that manages blog posts using a JSON file for persistent storage.

## 📦 Features

- GET, POST, PUT, DELETE blog posts  
- Search by title and/or content  
- Sort posts by title or content (ascending/descending)  
- Data is stored in a `POSTS.json` file  
- CORS enabled for frontend integration  

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/masterblog-api.git
cd masterblog-api/backend
```

2. Create a virtual environment and activate it
```bash
python3 -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
```

3.	Install dependencies:
```bash
pip install -r requirements.txt
```
4.	Run the app:
```bash
python backend_app.py
python frontend_app.py 
```

## 📝 Data Storage

All blog posts are saved in POSTS.json.
You can open this file to see or edit your posts manually.

🔚 That’s it!

Simple, clean and works.
