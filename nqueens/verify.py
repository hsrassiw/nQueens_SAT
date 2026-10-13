# Kiểm tra lời giải, độc lập với solver.
# Lời giải là danh sách queens dài n, queens[r] là cột của quân hậu ở hàng r.
# Hợp lệ khi không có hai quân nào cùng cột, cùng đường chéo (r - c)
# hoặc cùng đường chéo phụ (r + c).


def is_valid(n, queens):
    if queens is None or len(queens) != n:
        return False
    for c in queens:
        if c < 0 or c >= n:
            return False
    columns = set()
    diagonals = set()
    anti_diagonals = set()
    for r in range(n):
        columns.add(queens[r])
        diagonals.add(r - queens[r])
        anti_diagonals.add(r + queens[r])
    return len(columns) == n and len(diagonals) == n and len(anti_diagonals) == n
