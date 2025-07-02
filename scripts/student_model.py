class Mahasiswa:
    def __init__(self, id, nama, email, umur, jurusan, ipk):
        self.id = id
        self.nama = nama
        self.email = email
        self.umur = umur
        self.jurusan = jurusan
        self.ipk = ipk

    def __str__(self):
        return f"ID: {self.id}, Nama: {self.nama}, Email: {self.email}, Umur: {self.umur}, Jurusan: {self.jurusan}, IPK: {self.ipk}"