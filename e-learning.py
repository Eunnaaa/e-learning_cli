# Import modul yang dibutuhkan
import time
import json
import getpass
import datetime

# Deklarasi file database
db_file = "database.json"

# Membaca data dari database
def load_database():
    with open(db_file, "r") as f:
        return json.load(f)

# Menyimpan data ke database
def save_database(data):
    with open(db_file, "w") as f:
        json.dump(data, f)

# Fungsi Loading
def loading():
    print("Loading", end="")
    for _ in range(3): 
        time.sleep(0.3) 
        print(".", end="", flush=True)
    print("\n") 

# Fungsi login page 
def login(nim, password):
    data = load_database()
    for user in data["users"]:
        if user["nim"] == nim and user["password"] == password:
            return user
    return None

# Student = Mahasiswa: Fungsi lihat jadwal
def view_schedule(nim):
    data = load_database()
    loading()
    print("\nJadwal Mata Kuliah:")
    for schedule in data["schedule"]:
        if schedule["nim"] == nim:
            print(f"- {schedule['subject']} ({schedule['time']})")

# Student = Mahasiswa: Fungsi lihat absensi
def mark_attendance(nim):
    data = load_database()
    date = datetime.date.today().strftime("%Y-%m-%d")
    attendance_entry = {"nim": nim, "date": date}
    if attendance_entry not in data["attendance"]:
        data["attendance"].append(attendance_entry)
        save_database(data)
        loading()
        print("\nAbsensi berhasil dicatat!")
    else:
        loading()
        print("\nAnda sudah absen hari ini!")

# Student = Mahasiswa: Fungsi melihat ruang tugas
def view_tasks(nim):
    data = load_database()
    completed_tasks = {submission["task_id"] for submission in data["submissions"] if submission["nim"] == nim}
    
    loading()
    print("\nDaftar Tugas:")
    for task in data["tasks"]:
        print(f"- ID: {task['id']}, Judul: {task['title']}")
        print(f"  Deskripsi: {task['description']}")
        print(f"  Tenggat Waktu: {task['deadline']}")
        
        if task["id"] in completed_tasks:
            print(f"  Status: Tugas ID {task['id']} telah selesai.\n")
        else:
            print(f"  Status: Belum selesai.\n")

# Student = Mahasiswa: Fungsi mengupload tugas
def upload_task(nim):
    data = load_database()
    view_tasks(nim)

    loading()
    task_id = int(input("Masukkan ID tugas yang ingin Anda kumpulkan: "))
    task = next((t for t in data["tasks"] if t["id"] == task_id), None)
    if not task:
        loading()
        print("Tugas tidak ditemukan.")
        return
    loading()
    file_name = input("Masukkan nama file tugas (contoh: tugas1.pdf): ")
    submission = {"task_id": task_id, "nim": nim, "file": file_name, "submission_date": datetime.date.today().strftime("%Y-%m-%d")}
    data["submissions"].append(submission)
    save_database(data)
    loading()
    print("\nTugas berhasil diunggah!")

# Student = Mahasiswa: Fungsi melihat kelas pengganti
def view_replacement_classes():
    data = load_database()
    replacement_classes = data.get("replacement_classes", [])

    if not replacement_classes:
        loading()
        print("\nBelum ada jadwal kelas pengganti yang tersedia.")
        return

    loading()
    print("\nJadwal Kelas Pengganti:")
    for cls in replacement_classes:
        print(f"- Mata Kuliah: {cls['course']}")
        print(f"  Tanggal: {cls['date']}")
        print(f"  Waktu: {cls['time']}")
        print(f"  Ruang: {cls['room']}\n")


# Admin = Dosen: Fungsi melihat tugas yang sudah selesai
def view_submissions():
    data = load_database()
    submissions = data.get("submissions", [])
    tasks = data.get("tasks", [])
    users = data.get("users", [])

    if not submissions:
        loading()
        print("\nBelum ada tugas yang dikumpulkan oleh mahasiswa.")
        return
    
    loading()
    print("\nDaftar Pengumpulan Tugas:")
    for submission in submissions:
        task = next((t for t in tasks if t["id"] == submission["task_id"]), None)
        user = next((u for u in users if u["nim"] == submission["nim"]), None)
        
        if task and user:
            print(f"- Tugas: {task['title']}")
            print(f"  Nama Mahasiswa: {user['name']} (NIM: {user['nim']})")
            print(f"  File Tugas: {submission['file']}")
            print(f"  Tanggal Pengumpulan: {submission['submission_date']}\n")
        else:
            print("\nTugas Tidak Ditemukan")

# Admin = Dosen: Fungsi lihat absensi mahasiswa
def view_attendance():
    data = load_database()

    loading()
    print("\nDaftar Kehadiran Mahasiswa:")
    for entry in data["attendance"]:
        user = next(user for user in data["users"] if user["nim"] == entry["nim"])
        print(f"- {user['name']} ({entry['nim']}), Tanggal: {entry['date']}")

# Admin = Dosen: Tambah jadwal kelas pengganti
def add_replacement_class():
    data = load_database()

    loading()
    course = input("Masukkan nama mata kuliah: ")
    date = input("Masukkan tanggal kelas pengganti (format YYYY-MM-DD): ")
    time = input("Masukkan waktu kelas pengganti (contoh: 10:00 - 12:00): ")
    room = input("Masukkan ruang kelas pengganti: ")

    replacement_class = {
        "course": course,
        "date": date,
        "time": time,
        "room": room
    }

    data["replacement_classes"].append(replacement_class)
    save_database(data)
    loading()
    print("\nKelas pengganti berhasil ditambahkan!")


# Admin = Dosen: Fitur membuat tugas 
def add_task():
    loading()
    data = load_database()
    new_id = len(data["tasks"]) + 1
    title = input("Masukkan judul tugas: ")
    description = input("Masukkan deskripsi tugas: ")
    deadline = input("Masukkan tenggat waktu (format YYYY-MM-DD): ")
    task = {"id": new_id, "title": title, "description": description, "deadline": deadline}
    data["tasks"].append(task)
    save_database(data)
    loading()
    print("\nTugas berhasil ditambahkan!")

# Admin = Dosen: Fitur mengupdate tugas
def update_task():
    data = load_database()
    loading()
    task_id = int(input("Masukkan ID tugas yang ingin diperbarui: "))
    task = next((t for t in data["tasks"] if t["id"] == task_id), None)
    if not task:
        loading()
        print("Tugas tidak ditemukan.")
        return
    print(f"Tugas saat ini: {task['title']} - {task['description']} (Tenggat: {task['deadline']})")
    title = input("Masukkan judul baru (kosongkan jika tidak ingin mengubah): ") or task["title"]
    description = input("Masukkan deskripsi baru (kosongkan jika tidak ingin mengubah): ") or task["description"]
    deadline = input("Masukkan tenggat waktu baru (format YYYY-MM-DD, kosongkan jika tidak ingin mengubah): ") or task["deadline"]
    task.update({"title": title, "description": description, "deadline": deadline})
    loading()
    save_database(data)
    print("\nTugas berhasil diperbarui!")

# Login page & Main Fitur Dosen dan Mahasiswa
def main():
    print("=== Simple E-Learning ===")
    while True: 
        nim = input("Masukkan NIM/CD(Code Dosen): ")
        password = getpass.getpass("Masukkan Password: ")
        
        user = login(nim, password)
        if user:
            print(f"\nSelamat datang, {user['name']}!")
            loading()
            while True: 
                if user["role"] == "student":
                    print("\nMenu:")
                    print("1. Cek Jadwal")
                    print("2. Absensi")
                    print("3. Lihat Tugas")
                    print("4. Kerjakan Tugas")
                    print("5. Kelas Pengganti")
                    print("6. Logout")
                    choice = input("Pilih menu: ")
                    if choice == "1":
                        view_schedule(nim)
                    elif choice == "2":
                        mark_attendance(nim)
                    elif choice == "3":
                        view_tasks(nim)
                    elif choice == "4":
                        upload_task(nim)
                    elif choice == "5":
                        view_replacement_classes()
                    elif choice == "6":
                        print("Anda telah logout.")
                        break 
                    else:
                        loading()
                        print("Pilihan tidak valid, coba lagi.")
                elif user["role"] == "admin":
                    print("\nMenu Dosen:")
                    print("1. Lihat Absensi ")
                    print("2. Kelas Pengganti")
                    print("3. Tambah Tugas")
                    print("4. Update Tugas")
                    print("5. Lihat Tugas")
                    print("6. Logout")
                    choice = input("Pilih menu: ")
                    if choice == "1":
                        view_attendance()
                    elif choice == "2":
                        add_replacement_class()
                    elif choice == "3":
                        add_task()
                    elif choice == "4":
                        update_task()
                    elif choice == "5":
                        view_submissions()
                    elif choice == "6":
                        loading()
                        print("Anda telah logout.")
                        break 
                    else:
                        loading()
                        print("Pilihan tidak valid, coba lagi.")
            
            # Validasi/Konfirmasi setelah logout
            while True:  
                loading()
                print("\nApakah Anda ingin kembali ke halaman login?")
                option = input("Ketik 'ya' untuk kembali atau 'tidak' untuk keluar: ").strip().lower()
                if option == "ya" or option == "y":
                    loading()
                    print("Kembali ke halaman login...\n")
                    break  
                elif option == "tidak" or option == "n":
                    loading()
                    print("Terima kasih telah menggunakan E-Learning ini. Sampai jumpa!")
                    return  
                else:
                    loading()
                    print("Pilihan tidak valid, coba lagi.")
        else:
            loading()
            print("NIM atau Password salah! Silakan coba lagi.")

# Menjalankan program
if __name__ == "__main__":
    main()
