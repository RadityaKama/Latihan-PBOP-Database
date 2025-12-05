import sqlite3

conn = sqlite3.connect('rentalmotorjogja.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS motor(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    plat TEXT NOT NULL,
    harga_sewa INTEGER NOT NULL,
    status TEXT NOT NULL
)
''')

conn.commit()

def tambah_motor(nama, plat, harga_sewa, status):
    cursor.execute('''
    INSERT INTO motor (nama, plat, harga_sewa, status) VALUES (?, ?, ?, ?)
    ''', (nama, plat, harga_sewa, status))
    conn.commit()
    print(f'Motor "{nama}" berhasil ditambahkan.')

def tampilkan_motor():
    cursor.execute("SELECT * FROM motor")
    data = cursor.fetchall()
    if not data:
        print("Tidak ada motor tersedia di database.")
        return
    print("\n=== DAFTAR SEMUA MOTOR ===")
    print("-" * 50)
    for row in data:
        print(f"ID: {row[0]}")
        print(f"Nama: {row[1]}")
        print(f"Plat: {row[2]}")
        print(f"Harga Sewa: Rp.{row[3]}")
        print(f"Status: {row[4]}")
        print("-" * 50)

def cari_motor(keyword):
    cursor.execute("SELECT * FROM motor WHERE nama LIKE ?", ('%' + keyword + '%',))
    data = cursor.fetchall()
    if not data:
        print(f"Motor dengan kata kunci '{keyword}' tidak ditemukan.")
        return
    print(f"\n=== HASIL PENCARIAN: {keyword} ===")
    print("-" * 50)
    for row in data:
        print(f"ID: {row[0]} | Nama: {row[1]} | Status: {row[4]}")
    print("-" * 50)

def tampilkan_tersedia():
    cursor.execute("SELECT * FROM motor WHERE status = 'Tersedia'")
    data = cursor.fetchall()
    if not data:
        print("Tidak ada motor yang tersedia saat ini.")
        return
    print("\n=== MOTOR YANG TERSEDIA ===")
    print("-" * 50)
    for row in data:
        print(f"ID: {row[0]}")
        print(f"Nama: {row[1]}")
        print(f"Plat: {row[2]}")
        print(f"Harga Sewa: Rp.{row[3]}")
        print("-" * 50)

def sewa_motor(id_motor):
    cursor.execute("SELECT status FROM motor WHERE id = ?", (id_motor,))
    result = cursor.fetchone()
    
    if result:
        if result[0] == 'Tersedia':
            cursor.execute("UPDATE motor SET status = 'Dipinjam' WHERE id = ?", (id_motor,))
            conn.commit()
            print(f"Berhasil! Motor dengan ID {id_motor} statusnya kini DIPINJAM.")
        else:
            print(f"Gagal. Motor ID {id_motor} sedang dipinjam orang lain.")
    else:
        print("ID Motor tidak ditemukan.")

def kembalikan_motor(id_motor, lama_sewa):
    cursor.execute("SELECT harga_sewa, status FROM motor WHERE id = ?", (id_motor,))
    result = cursor.fetchone()
    
    if result:
        harga_per_hari = result[0]
        status_sekarang = result[1]
        
        if status_sekarang == 'Dipinjam':
            total_biaya = harga_per_hari * lama_sewa
            cursor.execute("UPDATE motor SET status = 'Tersedia' WHERE id = ?", (id_motor,))
            conn.commit()
            
            print("\n=== STRUK PENGEMBALIAN ===")
            print(f"ID Motor   : {id_motor}")
            print(f"Lama Sewa  : {lama_sewa} hari")
            print(f"Harga/hari : Rp.{harga_per_hari}")
            print(f"TOTAL BIAYA: Rp.{total_biaya}")
            print("Status motor kembali menjadi TERSEDIA.")
            print("==========================")
        else:
            print(f"Motor ID {id_motor} statusnya sudah Tersedia (tidak sedang disewa).")
    else:
        print("ID Motor tidak ditemukan.")

def update_motor(id_motor, nama_baru, plat_baru, harga_sewa_baru, status_baru):
    cursor.execute('''
    UPDATE motor
    SET nama = ?, plat = ?, harga_sewa = ?, status = ?
    WHERE id = ?
    ''', (nama_baru, plat_baru, harga_sewa_baru, status_baru, id_motor))
    conn.commit()
    print(f'Motor dengan ID {id_motor} berhasil diupdate.')

def hapus_motor(id_motor):
    cursor.execute("DELETE FROM motor WHERE id = ?", (id_motor,))
    conn.commit()
    print(f'Motor dengan ID {id_motor} berhasil dihapus.')

def menu():
    while True:
        print("\n=== RENTAL MOTOR JOGJA ===")
        print("1. Tambah Motor")
        print("2. Tampilkan Semua Motor")
        print("3. Update Data Motor")
        print("4. Hapus Motor")
        print("5. Cari Motor")
        print("6. Tampilkan Hanya yang Tersedia")
        print("7. Sewa Motor")
        print("8. Pengembalian & Hitung Biaya")
        print("9. Keluar")
        
        pilihan = input("Pilih menu (1-9): ")
        
        if pilihan == '1':
            nama = input("Masukkan nama motor: ")
            plat = input("Masukkan plat motor: ")
            harga_sewa = int(input("Masukkan harga sewa motor: "))
            status = input("Masukkan status motor (Tersedia/Dipinjam): ")
            tambah_motor(nama, plat, harga_sewa, status)
            
        elif pilihan == '2':
            tampilkan_motor()
            
        elif pilihan == '3':
            tampilkan_motor()
            try:
                id_motor = int(input("Masukkan ID motor yang akan diupdate: "))
                nama_baru = input("Masukkan nama motor baru: ")
                plat_baru = input("Masukkan plat motor baru: ")
                harga_sewa_baru = int(input("Masukkan harga sewa motor baru: "))
                status_baru = input("Masukkan status motor baru (Tersedia/Dipinjam): ")
                update_motor(id_motor, nama_baru, plat_baru, harga_sewa_baru, status_baru)
            except ValueError:
                print("Input ID atau Harga harus angka.")
                
        elif pilihan == '4':
            tampilkan_motor()
            try:
                id_motor = int(input("Masukkan ID motor yang akan dihapus: "))
                hapus_motor(id_motor)
            except ValueError:
                print("ID harus berupa angka.")

        elif pilihan == '5':
            keyword = input("Masukkan kata kunci nama motor: ")
            cari_motor(keyword)

        elif pilihan == '6':
            tampilkan_tersedia()

        elif pilihan == '7':
            tampilkan_tersedia()
            try:
                id_motor = int(input("Masukkan ID motor yang ingin disewa: "))
                sewa_motor(id_motor)
            except ValueError:
                print("ID harus berupa angka.")

        elif pilihan == '8':
            try:
                id_motor = int(input("Masukkan ID motor yang dikembalikan: "))
                lama_sewa = int(input("Berapa hari disewa? "))
                kembalikan_motor(id_motor, lama_sewa)
            except ValueError:
                print("Input ID dan Hari harus berupa angka.")

        elif pilihan == '9':
            print("Terima kasih telah menggunakan aplikasi Rental Motor Jogja.")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

menu()
cursor.close()
conn.close()