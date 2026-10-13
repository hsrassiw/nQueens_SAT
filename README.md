# Giải bài toán N-Queens bằng SAT solver

Phạm Minh Nghĩa – 24021584

Mã hóa bài toán N-Queens thành SAT, giải bằng các SAT solver trong
[PySAT](https://pysathq.github.io/) và so sánh với CP-SAT, CPLEX và Gurobi.

## Tiến độ

- [x] Bước 1 – khung dự án, bộ kiểm tra lời giải
- [ ] Bước 2 – mô hình SAT, encoding pairwise
- [ ] Bước 3 – các encoding có sẵn trong PySAT
- [ ] Bước 4 – encoding commander
- [ ] Bước 5 – encoding product
- [ ] Bước 6 – CP-SAT
- [ ] Bước 7 – CPLEX
- [ ] Bước 8 – Gurobi
- [ ] Bước 9 – bài toán N-Queens Completion
- [ ] Bước 10 – thực nghiệm
- [ ] Bước 11 – báo cáo

## Cài đặt và chạy thử

```bash
pip install -r requirements.txt
python -m unittest discover tests -v
```
