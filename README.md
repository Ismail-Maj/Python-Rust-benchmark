```bash
$ python -m venv venv  
$ source venv/bin/activate  
$ pip install -r requirements.txt  
$ maturin develop --release  
$ python main.py
$ python main.py -n 30 -p 10 --engine rust --seed 42 
```
