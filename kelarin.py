from operator import add
import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

# File untuk menyimpan data tugas
FILE_NAME = "log.json"

# ukuran dan judul jendela
root = tk.Tk()  
root.title("KELARIN.")
root.state('zoomed')  # Maksimalkan window sesuai ukuran layar
root.configure(bg="#0B0E14")  #warna latar belakang

latar_belakang = "#1A1F2B"  # Warna latar belakang kotak input dan list tugas
warna_utama = "#00FFD1"  
warna_teks = "#FFFFFF"  # Warna teks putih 
background_color = "#0B0E14"  

# --- LOGIKA JSON (SIMPAN & MUAT DATA) ---
def save_data():
    """Mengambil semua isi listbox dan menyimpannya ke file JSON"""
    all_tasks = selector.get(0, tk.END)
    with open(FILE_NAME, "w") as f:
        json.dump(all_tasks, f)

def load_data():
    """Membaca file JSON saat aplikasi pertama kali dibuka"""
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as f:
                tasks = json.load(f)
                for task in tasks:
                    selector.insert(tk.END, task)
        except:
            # Jika file korup, buat file baru kosong
            pass

#pemilihan tier
rank_options = ["S-TIER", "A-TIER", "B-TIER", "CHILL"]
selected_rank = tk.StringVar(root)
selected_rank.set(rank_options[0])

#pemilihan hari
# Daftar hari untuk dipilih
hari_options = ["SENIN", "SELASA", "RABU", "KAMIS", "JUMAT", "SABTU", "MINGGU"]
selected_hari = tk.StringVar(root)
selected_hari.set(hari_options[0])

#kepala
header_label = tk.Label(root, text="KELARIN.", font=("Space Grotesk", 35, "bold"), bg="#0B0E14", fg="#00FFD1")
header_label.pack(pady=(40, 5))

#daftar tugas
task_viewer_label = tk.Label(root, text="I'M STUCK ON THESE", font=("ARIAL", 15, "bold"), bg="#0B0E14", fg="#FFFFFF")
task_viewer_label.pack(pady=15)

#ukuran list tugas
frame = tk.Frame(root, bg="#0B0E14")
frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=400)

#scrollbar untuk list tugas
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

#selector tugas dengan desain yang lebih menarik
selector = tk.Listbox(frame, font=("montserrat", 12, "bold"), bg=latar_belakang, fg=warna_teks, selectbackground=warna_utama, selectforeground="#30363D", highlightthickness=2, borderwidth=1, relief=tk.FLAT)
selector.pack(pady=10, fill=tk.BOTH, expand=True, side=tk.LEFT)
selector.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=selector.yview)
selector.config(borderwidth=3, highlightthickness=3, relief=tk.FLAT)

# --- BAGIAN INPUT USER (TIER, HARI, JAM) ---
judul_input = tk.Label(root, text="Setting Tugas (Tier, Hari, Jam, Deskripsi):", font=("inter", 10, "italic", "bold"), bg="#0B0E14", fg="#FFFFFF")
judul_input.pack(pady=5)

# Frame untuk input waktu agar berjejer rapi
input_custom_frame = tk.Frame(root, bg="#0B0E14")
input_custom_frame.pack(pady=5)


# desain AI 1. Pilih Tier
tier_menu = tk.OptionMenu(input_custom_frame, selected_rank, *rank_options)
tier_menu.config(font=("Space Grotesk", 10, "bold"), bg=latar_belakang, fg=warna_utama, width=8, borderwidth=0, highlightthickness=0)
tier_menu.grid(row=0, column=0, padx=5)

# Hari input dengan desain AI
hari_menu = tk.OptionMenu(input_custom_frame, selected_hari, *hari_options)
hari_menu.config(font=("Space Grotesk", 10, "bold"), bg=latar_belakang, fg=warna_utama, 
                  width=10, borderwidth=0, highlightthickness=0)
hari_menu["menu"].config(bg=latar_belakang, fg=warna_utama, font=("Space Grotesk", 10))
hari_menu.grid(row=0, column=1, padx=5)

# 3. Input Jam (Contoh: 19:00)
entry_jam = tk.Entry(input_custom_frame,  font=("montserrat", 10, "bold"), bg=latar_belakang, fg=warna_teks, insertbackground=warna_utama, width=8, borderwidth=0, highlightthickness=1, highlightbackground="#30363D")
entry_jam.insert(0, "Jam?") 
entry_jam.grid(row=0, column=2, padx=5)

#tempat pengingat input
judul_input_msg = tk.Label(root, text="Masukkan list tugas yang ingin kamu kerjakan", font=("inter", 10, "italic", "bold"), bg="#0B0E14", fg="#FFFFFF")
judul_input_msg.pack(pady=5)

#kotak input tugas dan desain nyala saat aktif
def add_task():
    task = task_entry.get()
    hari = selected_hari.get()
    jam = entry_jam.get()
    tier = selected_rank.get()

    if task and hari != "Hari?" and jam != "Jam?":
        full_entry = f"[{tier}] {hari.upper()} ==> {jam} - {task}"
        selector.insert(tk.END, full_entry)
        
        # --- MODIFIKASI: SIMPAN SETELAH TAMBAH ---
        save_data()
        
        task_entry.delete(0, tk.END)
        selected_hari.set(hari_options[0])
        entry_jam.delete(0, tk.END)
        entry_jam.insert(0, "Jam?")
    else:
        messagebox.showwarning("Input Error", "Lengkapi Tugas, Hari, dan Jam dulu!")

task_entry = tk.Entry(root, font=("montserrat", 12, "bold"), 
                      bg=latar_belakang, fg=warna_teks, 
                      insertbackground=warna_utama, 
                      highlightthickness=2, highlightbackground="#30363D", 
                      highlightcolor=warna_utama, 
                      width=40, borderwidth=0)
task_entry.pack(pady=10)

#tombol tambah, hapus, selesai
frame_buttons = tk.Frame(root, bg="#0B0E14")
frame_buttons.pack(pady=10, expand=True)

tbl_tambah = tk.Button(frame_buttons, text="TAMBAH TUGAS", font=("Space Grotesk", 12, "bold"), bg="#FF3333", fg="#FFFFFF", command=add_task, width=13, )
tbl_tambah.grid (row=0, column=0, padx=5)

def delete_task():
    if selector.curselection():
        if messagebox.askyesno("Konfirmasi", "Hapus tugas yang dipilih?"):
            selector.delete(selector.curselection())
            
            # --- MODIFIKASI: SIMPAN SETELAH HAPUS ---
            save_data()
            
            messagebox.showinfo("Tugas Dihapus", "Tugas telah dihapus!")
    else:
        messagebox.showwarning("Hapus Error", "Silakan pilih tugas untuk dihapus.")

def delete_all_tasks():
    if selector.size() > 0:
        if messagebox.askyesno("Konfirmasi", "Hapus semua tugas?"):
            selector.delete(0, tk.END)
            
            # --- MODIFIKASI: SIMPAN SETELAH HAPUS SEMUA ---
            save_data()
    else:
        messagebox.showinfo("Info", "List tugas kosong.")

#TOMBOL HAPUS BIASA
btn_delete = tk.Button(frame_buttons, text="HAPUS", font=("Space Grotesk", 12, "bold"), bg="#FFD700", fg="#0B0E14", command=delete_task, width=10)
btn_delete.grid(row=0, column=2, padx=5)

#TOMBOL HAPUS SEMUA
btn_delete_all = tk.Button(frame_buttons, text="HAPUS SEMUA", font=("Space Grotesk", 12, "bold"), bg="#FF0000", fg="#FFFFFF", command=delete_all_tasks, width=12)
btn_delete_all.grid(row=0, column=1, padx=5)

def complete_task():
    selected_task_index = selector.curselection()
    if selected_task_index:
        task = selector.get(selected_task_index)
        selector.delete(selected_task_index)
        
        # --- MODIFIKASI: SIMPAN SETELAH SELESAI ---
        save_data()
        
        messagebox.showinfo("Tugas Selesai", f"Tugas '{task}' telah diselesaikan!")
    else:
        messagebox.showwarning("Selesai Error", "Silakan pilih tugas untuk diselesaikan.")

#TOMBOL SELESAI
btn_complete = tk.Button(frame_buttons, text="SELESAI", font=("Space Grotesk", 12, "bold"), bg="#28A745", fg="#0B0E14", command=complete_task, width=10)
btn_complete.grid(row=0, column=3, padx=5)

# aplikasi berjalan
load_data()
root.mainloop()