import os
import sys
from student_controller import StudentController

class AplikasiMahasiswa:
    def __init__(self):
        self.control = StudentController()
        self.running = True

    def menu(self):
        print("\n--- Menu ---")
        print("1. Tambah Mahasiswa")
        print("2. Lihat Semua")
        print("3. Cari Mahasiswa")
        print("4. Update Mahasiswa")
        print("5. Hapus Mahasiswa")
        print("6. Keluar")

    def run(self):
        while self.run:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.menu()
            pilihan = input("Pilih (1-6): ")
            if pilihan == '1':
                self.tambah()
            elif pilihan == '2':
                self.lihat()
            elif pilihan == '3':
                self.cari()
            elif pilihan == '4':
                self.update()
            elif pilihan == '5':
                self.hapus()
            elif pilihan == '6':
                self.run = False
            else:
                print("Pilihan salah!")
                input("Enter untuk lanjut...")

    def tambah(self):
        print("\nTambah Mahasiswa")
        data = {}
        data['id'] = input("ID: ")
        data['nama'] = input("Nama: ")
        data['email'] = input("Email: ")
        data['umur'] = int(input("Umur: "))
        data['jurusan'] = input("Jurusan: ")
        data['ipk'] = float(input("IPK: "))
        self.control.tambah(data)
        input("Berhasil ditambah. Enter...")

    def lihat(self):
        print("\nData Mahasiswa:")
        for m in self.control.semua():
            print(m)
        input("Enter untuk lanjut...")

    def cari(self):
        id_mhs = input("ID Mahasiswa: ")
        hasil = self.control.cari(id_mhs)
        if hasil:
            print(hasil)
        else:
            print("Tidak ditemukan.")
        input("Enter untuk lanjut...")

    def update(self):
        id_mhs = input("ID Mahasiswa yang mau diupdate: ")
        if self.control.cari(id_mhs):
            data = {}
            data['nama'] = input("Nama baru: ")
            data['email'] = input("Email baru: ")
            data['umur'] = int(input("Umur baru: "))
            data['jurusan'] = input("Jurusan baru: ")
            data['ipk'] = float(input("IPK baru: "))
            self.control.update(id_mhs, data)
            print("Berhasil diupdate.")
        else:
            print("Data tidak ditemukan.")
        input("Enter untuk lanjut...")

    def hapus(self):
        id_mhs = input("ID Mahasiswa yang mau dihapus: ")
        if self.control.hapus(id_mhs):
            print("Data dihapus.")
        else:
            print("Data tidak ditemukan.")
        input("Enter untuk lanjut...")

if __name__ == '__main__':
    app = AplikasiMahasiswa()
    app.run()