# ChatBot Server

Environment: 
- `Flask-2.2.3`, 
- `openai-0.27.0`, 
- `python-3.8`.

Install dependency
```bash
sudo apt-get update
pip install openai
pip install Flask
pip install Flask-Cors
pip install tiktoken
```

Before starting the server, please create a file named api_key.txt to store the API key. Afterward, you can start 
the server using the following command.
```bash
python3 app.py
or 
nohup python3 app.py > output.log &
```
