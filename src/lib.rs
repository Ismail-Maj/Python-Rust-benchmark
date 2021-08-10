extern crate rayon; //parallel computing

use pyo3::prelude::{pymodule, PyModule, PyResult, Python, pyfunction, wrap_pyfunction};
use rayon::prelude::*;
use std::cmp::*;

#[pyfunction]
fn two_sets_intersection(x1: Vec<isize>, x2: Vec<isize>, y1: Vec<isize>, y2: Vec<isize>, x3: Vec<isize>, x4: Vec<isize>, y3: Vec<isize>, y4: Vec<isize>) -> PyResult<Vec<isize>> {
    let (mut best_value, mut x_min, mut x_max, mut y_min, mut y_max) = (-1, 0, 0, 0, 0);
    x3.iter().zip(x4.iter().zip(y3.iter().zip(y4.iter()))).foreach(|(ex3, ex4, ey3, ey4)|{
        x1.iter().zip(x2.iter().zip(y1.iter().zip(y2.iter()))).foreach(|(ex1, ex2, ey1, ey2)|{
            let (ex5, ex6, ey5, ey6) = (min(ex2, ex4), max(ex1, ex3), min(ey2, ey4), max(ey1, ey3));
            let width = ex5 - ex6;
            if width > 0:
                let area = width * (ey5 - ey6);
                if area > best_value:
                    best_value = area;
                    x_min = ex6;
                    x_max = ex5;
                    y_min = ey6;
                    y_max = ey5;
        })
    })

    if best_value <= 0{
        panic!("empty intersection");
    }

    Ok((min_x, max_x, min_y, max_y).to_vect())
}

#[pymodule]
fn rust_lib(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(two_sets_intersection, m)?)?;
    Ok(())
}