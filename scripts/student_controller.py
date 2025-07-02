from student_model import Mahasiswa

class StudentController:
    def __init__(self):
        self.daftar = []

    def tambah(self, data):
        mhs = Mahasiswa(**data)
        self.daftar.append(mhs)

    def semua(self):
        return self.daftar

    def cari(self, id):
        for m in self.daftar:
            if m.id == id:
                return m
        return None

    def update(self, id, data_baru):
        for i, m in enumerate(self.daftar):
            if m.id == id:
                self.daftar[i] = Mahasiswa(id=id, **data_baru)
                return True
        return False

    def hapus(self, id):
        for i, m in enumerate(self.daftar):
            if m.id == id:
                del self.daftar[i]
                return True
        return False
