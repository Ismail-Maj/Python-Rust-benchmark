# Maximum Intersection between 2 sets of bounding boxes
```bash
$ python -m venv venv  
$ source venv/bin/activate  
$ pip install -r requirements.txt  
$ maturin develop --release  
$ python src/main.py -n 30 -p 10 --seed 42 --engine rust
# available engines: python, numpy, rust, rust-multicore
```

<p align="center">
  <img src="image/benchmark.png" />
</p>

<p align="center">
  <img src="image/image1.png" />
</p>

<p align="center">
  <img src="image/image2.png" />
</p>
