# Các cách mã hóa ràng buộc AMO (nhiều nhất một) và EO (đúng một) sang CNF.
# Mỗi hàm encoding nhận danh sách literal và pool (để tạo biến phụ),
# trả về danh sách mệnh đề.


class VarPool:
    # Cấp số hiệu cho biến phụ mới, bắt đầu sau top

    def __init__(self, top):
        self.top = top

    def new(self):
        self.top += 1
        return self.top


def binomial(lits, pool):
    # Binomial (pairwise): với mỗi cặp biến, không được cả hai cùng đúng
    clauses = []
    for i in range(len(lits)):
        for j in range(i + 1, len(lits)):
            clauses.append([-lits[i], -lits[j]])
    return clauses


ENCODINGS = {
    "binomial": binomial,
}


def at_most_one(lits, encoding, pool):
    return ENCODINGS[encoding](lits, pool)


def exactly_one(lits, encoding, pool):
    # Đúng một = ít nhất một (một mệnh đề dài) + nhiều nhất một
    return [lits] + at_most_one(lits, encoding, pool)
