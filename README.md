```bash
$ python -m venv venv  
$ source venv/bin/activate  
$ pip install -r requirements.txt  
$ maturin develop --release  
$ python main.py
$ python main.py --engine rust -n 30 -p 10 --seed 42 
```

<p align="center">
  <img src="figure.png" />
</p>