extern crate rayon; //parallel computing

use pyo3::prelude::{pymodule, PyModule, PyResult, Python, pyfunction, wrap_pyfunction};
use rayon::prelude::*;

fn matrix_extremum(v1: Vec<isize>, v2: Vec<isize>, max: bool) -> Vec<Vec<isize>>{ 
    let mut res = vec![vec![0; v1.len()]; v2.len()];
    res.par_iter_mut().zip(v2.par_iter()).for_each(|(res_row, &e2)| {
        res_row.par_iter_mut().zip(v1.par_iter()).for_each(|(res_e, &e1)| {
            *res_e = if max { if e1 > e2 {e1} else {e2} } else { if e1 < e2 {e1} else {e2} };
        })
    });
    res
}

fn matrix_minus(mat1: &Vec<Vec<isize>>,mat2: &Vec<Vec<isize>>)-> Vec<Vec<isize>>{
    let mut res = vec![vec![0; (*mat1)[0].len()]; (*mat1).len()];
    res.par_iter_mut().zip((*mat1).par_iter().zip((*mat2).par_iter())).for_each(|(res_row, (row1, row2))| {
        res_row.par_iter_mut().zip(row1.par_iter().zip(row2.par_iter())).for_each(|(res_e, (&e1, &e2))| {
            *res_e = e1 - e2;
        })
    });
    res
}

#[pyfunction]
fn two_sets_intersection(x1: Vec<isize>, x2: Vec<isize>, y1: Vec<isize>, y2: Vec<isize>, x3: Vec<isize>, x4: Vec<isize>, y3: Vec<isize>, y4: Vec<isize>) -> PyResult<Vec<isize>> {
    let x5 = matrix_extremum(x1, x3, true);
    let x6 = matrix_extremum(x2, x4, false);
    let y5 = matrix_extremum(y1, y3, true);
    let y6 = matrix_extremum(y2, y4, false);
    let width = matrix_minus(&x6, &x5);
    let height = matrix_minus(&y6, &y5);

    let (mut best_value, mut best_row, mut best_col) = (-1, 0, 0);
    for row in 0..width.len(){
        for col in 0..(width[0]).len(){
            if width[row][col] > 0{
                let area = width[row][col] * height[row][col];              
                if area > best_value{
                    best_value = area;
                    best_row = row;
                    best_col = col;
                }
            }
        }
    }

    let mut res = Vec::new();
    res.push(x5[best_row][best_col]);
    res.push(x6[best_row][best_col]);
    res.push(y5[best_row][best_col]);
    res.push(y6[best_row][best_col]);

    if best_value <= 0{
        panic!("empty intersection");
    }

    Ok(res)
}

#[pymodule]
fn rust_lib(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(two_sets_intersection, m)?)?;
    Ok(())
}