# Giải bài toán N-Queens bằng SAT solver

Phạm Minh Nghĩa – 24021584

Mã hóa bài toán N-Queens thành SAT và giải bằng các SAT solver trong
[PySAT](https://pysathq.github.io/) (CaDiCaL, Glucose, Kissat…), sau đó so sánh
với hai phương pháp giải chính xác khác:

- **CP** (quy hoạch ràng buộc): CP-SAT, CPLEX CP
- **ILP** (quy hoạch nguyên): CPLEX MIP, Gurobi

## Tiến độ

- [x] Bước 1 – khung dự án, bộ kiểm tra lời giải
- [x] Bước 2 – mô hình SAT, encoding binomial
- [ ] Bước 3 – encoding binary
- [ ] Bước 4 – encoding sequential counter
- [ ] Bước 5 – encoding commander
- [ ] Bước 6 – encoding product
- [ ] Bước 7 – mô hình CP (CP-SAT, CPLEX CP)
- [ ] Bước 8 – mô hình ILP (CPLEX MIP, Gurobi)
- [ ] Bước 9 – thực nghiệm
- [ ] Bước 10 – báo cáo

## Cài đặt và chạy thử

```bash
pip install -r requirements.txt
python -m unittest discover tests -v
python -m nqueens.sat_model 8      # giải và in bàn cờ 8x8
```
