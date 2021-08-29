use pyo3::prelude::{pymodule, PyModule, PyResult, Python, pyfunction, wrap_pyfunction};
use std::cmp::{min, max};
use rayon::prelude::*;
use std::sync::Mutex;
use std::sync::Arc;

#[pyfunction]
fn two_sets_intersection(x1: Vec<isize>, x2: Vec<isize>, y1: Vec<isize>, y2: Vec<isize>, x3: Vec<isize>, x4: Vec<isize>, y3: Vec<isize>, y4: Vec<isize>) -> PyResult<Vec<isize>> {
    let (mut best_value, mut x_min, mut x_max, mut y_min, mut y_max) = (-1, 0, 0, 0, 0);

    x3.iter().zip(x4.iter().zip(y3.iter().zip(y4.iter()))).for_each(|(ex3, (ex4, (ey3, ey4)))|{
        x1.iter().zip(x2.iter().zip(y1.iter().zip(y2.iter()))).for_each(|(ex1, (ex2, (ey1, ey2)))|{
            let (&ex5, &ex6, &ey5, &ey6) = (min(ex2, ex4), max(ex1, ex3), min(ey2, ey4), max(ey1, ey3));
            let width = ex5 - ex6;
            if width > 0 {
                let area = width * (ey5 - ey6);
                if area > best_value {
                    best_value = area;
                    x_min = ex6;
                    x_max = ex5;
                    y_min = ey6;
                    y_max = ey5;
                }
            }
        })
    });

    if best_value <= 0 {
        panic!("empty intersection");
    }
    let mut res = Vec::new();
    res.push(x_max);
    res.push(x_min);
    res.push(y_max);
    res.push(y_min);

    Ok(res)
}

#[pyfunction]
fn two_sets_intersection_multicore(x1: Vec<isize>, x2: Vec<isize>, y1: Vec<isize>, y2: Vec<isize>, x3: Vec<isize>, x4: Vec<isize>, y3: Vec<isize>, y4: Vec<isize>) -> PyResult<Vec<isize>> {
    let best_value = Arc::new(Mutex::new(0));
    let (x_min, x_max, y_min, y_max) = (Arc::new(Mutex::new(0)),Arc::new(Mutex::new(0)),Arc::new(Mutex::new(0)),Arc::new(Mutex::new(0)));

    x3.par_iter().zip(x4.par_iter().zip(y3.par_iter().zip(y4.par_iter()))).for_each(|(ex3, (ex4, (ey3, ey4)))|{
        let best_value = Arc::clone(&best_value);
        let (x_min, x_max, y_min, y_max) = (Arc::clone(&x_min),Arc::clone(&x_max),Arc::clone(&y_min),Arc::clone(&y_max));
        let mut thread_best = 0;
        let (mut t_x_min, mut t_x_max, mut t_y_min, mut t_y_max) = (0,0,0,0);
        x1.iter().zip(x2.iter().zip(y1.iter().zip(y2.iter()))).for_each(|(ex1, (ex2, (ey1, ey2)))|{
            let (&ex5, &ex6, &ey5, &ey6) = (min(ex2, ex4), max(ex1, ex3), min(ey2, ey4), max(ey1, ey3));
            let width = ex5 - ex6;
            let height = ey5 - ey6;
            if (width > 0) & (height > 0) {
                let area = width * height;
                if area > thread_best{
                    thread_best = area;
                    t_x_min = ex6;
                    t_x_max = ex5;
                    t_y_min = ey6;
                    t_y_max = ey5;
                }
            }
        });
        let mut best = best_value.lock().unwrap();
        let (mut mut_x_min, mut mut_x_max, mut mut_y_min, mut mut_y_max) = (x_min.lock().unwrap(), x_max.lock().unwrap(), y_min.lock().unwrap(), y_max.lock().unwrap());
        if thread_best > *best {
            *best = thread_best;
            *mut_x_min = t_x_min;
            *mut_x_max = t_x_max;
            *mut_y_min = t_y_min;
            *mut_y_max = t_y_max;
        }
    });

    let mut res = Vec::new();
    res.push(*x_max.lock().unwrap());
    res.push(*x_min.lock().unwrap());
    res.push(*y_max.lock().unwrap());
    res.push(*y_min.lock().unwrap());

    Ok(res)
}

#[pymodule]
fn rust_lib(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(two_sets_intersection, m)?)?;
    m.add_function(wrap_pyfunction!(two_sets_intersection_multicore, m)?)?;
    Ok(())
}