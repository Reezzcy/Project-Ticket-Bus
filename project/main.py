from tabulate import tabulate
import datetime as dt
import random
import os

tickets = []
admins = []
orders = []

fileadmins = "./data/admins_db.txt"
filetickets = "./data/tickets_db.txt"
fileorders = "./data/orders_db.txt"

'''
DI BAWAH INI ADALAH FUNGSI UNTUK MEMPERMUDAH MAIN PROGRAM (LOGIKA UTAMA DI DALAM PROGRAM)
'''
#buat nambahin user, pw
def add_user(username, password):
    admins.append({
        "username":username,
        "password":password
    })

#buat tambahin isi jadwal bis
def add_ticket(kode_bis, tahun, bulan, hari, keberangkatan, tujuan, plat_nomor, jumlah_penumpang, jam_berangkat, jam_sampai, harga):
    tickets.append({
        "kode_bis": kode_bis,
        "tahun": int(tahun),
        "bulan": int(bulan),
        "tanggal": int(hari),
        "keberangkatan":keberangkatan,
        "tujuan":tujuan,
        "plat": plat_nomor,
        "jmlh_penumpang": int(jumlah_penumpang),
        "jam_berangkat":  jam_berangkat,
        "jam_sampai": jam_sampai,
        "harga": int(harga),
        "date": format_tanggal(int(tahun), int(bulan), int(hari))
    })

def add_order(kode_order, nama_pembeli, jumlah_tiket, tanggal_pembelian, kode_bis, total_harga):
    orders.append({
        "kode_order": kode_order,
        "nama_pembeli": nama_pembeli,
        "jumlah_tiket": jumlah_tiket,
        "tanggal_pembelian": tanggal_pembelian,
        "kode_bis": kode_bis,
        "total_harga": total_harga

    })

def load_user():
    lines =  ""
    with open(fileadmins, "r") as file:
        lines = file.readlines()

        if lines != "":

            for line in lines:
                line = line[:-1]
                line = line.split(";")

                if lines != "":
                    add_user(line[0], (line[1]))

#txt ke array tiket
def load_tickets():
    lines =  ""
    with open(filetickets, "r") as file:
        lines = file.readlines()
        if lines != "":

            for line in lines:
                line = line[:-1]
                line = line.split(";")

                if lines != "":
                    add_ticket(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10])

def load_orders():
    lines =  ""
    with open(fileorders, "r") as file:
        lines = file.readlines()

        if lines != "":
            for line in lines:
                line = line[:-1]
                line = line.split(";")

                if lines != "":
                    add_order(line[0],line[1],line[2],line[3],line[4],line[5])

def cek_id_unik(id_order):
    for order in orders:

        if id_order == order["kode_order"]:
            return False

    return True

#cek akun admin
def is_admin(username, password):
    for index in range (len(admins)):

        if username == admins[index]["username"]:

            if password == admins[index]["password"]:
                return True
    return False

#buat nambahin tiket
def save_ticket():
    lines = ""
    with open(filetickets, "w") as file:
        for ticket in tickets:
            line = f"{ticket['kode_bis']};{ticket['tahun']};{ticket['bulan']};{ticket['tanggal']};{ticket['keberangkatan']};{ticket['tujuan']};{ticket['plat']};{ticket['jmlh_penumpang']};{ticket['jam_berangkat']};{ticket['jam_sampai']};{ticket['harga']};\n"
            lines += line

        file.write(lines)

def save_orders():
    lines = ""
    with open(fileorders, "w") as file:

        for order in orders:
            line = f"{order['kode_order']};{order['nama_pembeli']};{order['jumlah_tiket']};{order['tanggal_pembelian']};{order['kode_bis']};{order['total_harga']}\n"
            lines += line

        file.write(lines)
        
def auto_generate_id_order():
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numeric = "0123456789"
    unique_id = ""

    for char in range(3):
        char = alphabet[random.randint(0, len(alphabet)-1)]
        unique_id += char

    for char in range(3):
        char = numeric[random.randint(0, len(numeric)-1)]
        unique_id += char

    if cek_id_unik(unique_id) == True:
        return unique_id
    else:
        return auto_generate_id_order()

#buat nyari index tiket 
def search_ticket_index(kode_bis):
    count = 0
    for ticket in tickets:

        if kode_bis == ticket["kode_bis"]:
            return count
        count += 1

    return -1

def mengurutkan_tiket_berdasarkan_key(key_dictionary):
    list_tiket = []
    copy_ticket = tickets.copy()

    for i in range (len(copy_ticket)):
        min_idx = i

        for j in range (i+1, len(copy_ticket)):
            if copy_ticket[min_idx][key_dictionary] > copy_ticket[j][key_dictionary]:
                min_idx = j

        copy_ticket[i], copy_ticket[min_idx] = copy_ticket[min_idx], copy_ticket[i]

    for dict_ticket in copy_ticket:
        list_tiket.append(mengubah_dict_tiket_ke_list(dict_ticket))
    print("="*120)
    print("\t\t\t\t\t\t\tJADWAL TIKET")
    print("="*120)
    menampilkan_list_tiket(list_tiket)

#buat masang harga tiket
def format_rupiah(value):
    rupiah = str(value)

    if len(rupiah) <= 3:
        rupiah = f"Rp {rupiah}"
        return rupiah

    else:
        tail= rupiah[-3:]
        head = rupiah[:-3]
        return format_rupiah(head) + "." + tail

#buat masang tanggal tiket
def format_tanggal(tahun, bulan, tanggal):
    tanggal = dt.date(tahun,bulan,tanggal)
    return tanggal

def mengubah_dict_tiket_ke_list(dict_tiket):
    return [dict_tiket["kode_bis"], dict_tiket["keberangkatan"], dict_tiket["tujuan"], dict_tiket["jam_berangkat"], dict_tiket["jam_sampai"], format_rupiah(dict_tiket["harga"]),dt.date(dict_tiket["tahun"],dict_tiket["bulan"],dict_tiket["tanggal"])]

def menampilkan_list_tiket(list_tiket):
    header = ["KODE_BIS","Keberangkatan","Tujuan","Jam Keberangkatan","Jam Sampai", "Harga","Tanggal(year-month-date)"]
    print(tabulate(list_tiket, headers= header, tablefmt="fancy_grid"))

def menu_urutkan():
    print("PILIH MENU UNTUK MENAMPILKAN TIKET BIS\n\n1. Tampilkan jadwal tiket secara normal\n2. Tampilkan jadwal tiket dari harga tiket termurah\n3. Tampilkan jadwal tiket berdasarkan tanggal terdekat\n4. Kembali ke menu awal")

#ui menu admin
def menu_admin():
    print("Selamat datang di menu Admin!\n\n1. Masukan Jadwal Tiket\n2. Delete Jadwal Tiket\n3. Munculkan Jadwal Tiket\n4. Kembali ke Halaman utama ")

#ui menu pembeli
def menu_pembeli():
    print("Selamat datang di menu Pembeli\n\n1. Cek Seluruh Jadwal Bis\n2. Beli Tiket Bis\n3. Menunjukan Info Tiket Yang Sudah Dibeli\n4. Kembali ke Halaman utama")

#ui menu awal
def menu_main():
    print("SELAMAT DATANG DI TRAVELEKO!\n\n1. Masuk Sebagai Admin\n2. Masuk Sebagai Pembeli\n3. Keluar Dari Aplikasi")

'''
DI BAWAH INI DALAH MAIN PROGRAM / LOGIKA DARI ALUR PROGRAM
'''

'''
PROGRAM ADMIN!
'''
#Admin memasukan detail dari tiket bis
def admin_insert_ticket():
    print("="*50)
    print("\t\tMENU INSERT TIKET")
    print("="*50)
    print("\nSILAKAN MASUKAN DATA TIKET!")

    kode_bis = input("\nMasukan kode bis\t\t: ")
    tahun = int(input("Masukan Tahun (yyyy)\t\t: "))
    bulan = int(input("Masukan bulan (1-12)\t\t: "))
    tanggal =int(input("Masukan Tanggal (1-13)\t\t: "))
    keberangkatan = input("Masukan Terminal Keberangkatan\t: ")
    tujuan = input("Masukan Terminal tujuan\t\t: ")
    plat_nomor = input("Masukan plat nomor\t\t: ")
    jumlah_penumpang = int(input("Masukan Jumlah Penumpang\t: "))
    jam_berngkat = input("Masukan jam keberangkatan (format = jam:menit): ")
    jam_sampai = input("Masukan jam kedatangan (format = jam:menit): ")
    harga = int(input("Masukan Harga (format = 50000)\t: "))

    add_ticket(kode_bis,tahun,bulan,tanggal, keberangkatan, tujuan, plat_nomor, jumlah_penumpang, jam_berngkat, jam_sampai, harga)

    save_ticket()

    print(f"\nTicket dengan kode bis {kode_bis} telah dimasukan!\n")

# Admin mendelete tiket berdasarkan kode_bis
def admin_delete_ticket():
    print("="*50)
    print("\t\tMENU DELETE TIKET")
    print("="*50)
    input_kode_ticket = input("Masukan Kode bis yang ingin di-delete:")
    index_ticket = search_ticket_index(input_kode_ticket)

    if index_ticket != -1:
        tickets.pop(index_ticket)
        print(f"Jadwal tiket bis {input_kode_ticket} berhasil dihapus!")
    else:
        print("KODE BIS YANG ANDA MASUKAN KOSONG! ")

    save_ticket()

#Liat jadwal bis
def show_tickets():
    print("="*120)
    print("\t\t\t\t\t\t\tJADWAL TIKET")
    print("="*120)
    data_set = []
    for ticket in tickets:
        data_set.append(mengubah_dict_tiket_ke_list(ticket))
    menampilkan_list_tiket(data_set)
    
def show_specific_ticket(kode_bis):
    index_tiket = search_ticket_index(kode_bis)

    if index_tiket != -1:
        data_set = []
        ticket = tickets[index_tiket]
        data_set.append(mengubah_dict_tiket_ke_list(ticket))
        menampilkan_list_tiket(data_set)
    else:
        print("Tiket tidak ditemukan!")

#filter tujuan
def buy_ticket():
    passenger_count = 0
    filterz = []
    print("="*50)
    print("\tMENU PEMBELIAN TIKET TRAVELIO!")
    print("="*50)
    print("\nPilih Terminal Keberangkatan & Tujuan anda")
    Keberangkatan = input("Masukan Terminal Keberangkatan\t:")
    Tujuan = input("Masukan Terminal Tujuan\t\t:")
    for ticket in tickets:
        if str(ticket["keberangkatan"]).lower() == Keberangkatan.lower() and str(ticket["tujuan"]).lower() == Tujuan.lower():
            filterz.append(mengubah_dict_tiket_ke_list(ticket))
    if filterz != []:
        os.system("cls")
        menampilkan_list_tiket(filterz)

        kode_bis = input("Masukan kode bis yang ingin anda beli\t\t: ")
        tiket_index = search_ticket_index(kode_bis)

        if tiket_index != -1:
            print("\nSILAHKAN MASUKAN DATA PEMBELi!")
            print(f"Remaining Seat\t\t\t: {tickets[tiket_index]['jmlh_penumpang']}")
            kode_order = auto_generate_id_order()
            jumlah_tiket = int(input("Masukan Jumlah tiket\t\t:"))
            total_harga = jumlah_tiket* tickets[tiket_index]["harga"]
            tanggal_pembelian = dt.date.today()
            
            while passenger_count < jumlah_tiket:
                nama_pembeli = input(f"Masukan Nama Penumpang ke {passenger_count+1}\t: ")
                add_order(kode_order, nama_pembeli, jumlah_tiket, tanggal_pembelian, kode_bis, total_harga)
                passenger_count += 1
                
            print(f"total pembayaran anda\t\t: {format_rupiah(total_harga)}")

            save_orders()
            print("\nSCREENSHOT BUKTI STRUK DI BAWAH INI!\n")

            cetak_struk(kode_order)
            print("Pembayaran Telah berhasil, Saldo di rekening anda sudah otomatis terpotong!")
            print("Terima kasih telah membeli tiket di Travelio, Semoga harimu menyenangkan!")
            tickets[tiket_index]['jmlh_penumpang'] -= jumlah_tiket

            save_ticket()
    else:
        print("TIKET TUJUAN TIDAK DITEMUKAN!")

def cetak_struk(kode_order):
    order_list = []
    for order in orders:
        if kode_order == order["kode_order"]:
            order_list.append([order["kode_order"], order["nama_pembeli"], order["jumlah_tiket"], order["tanggal_pembelian"], order["kode_bis"], format_rupiah(order["total_harga"])])
    
    if order_list != []:
        print(tabulate(order_list, headers=["KODE ORDER", "Nama Pembeli", "Jumlah Tiket", "Tanggal Pembelian", "Kode Bis", "Total Harga"], tablefmt="fancy_grid"))

def info_detail_order():
    order_list = []
    order_kode_bis = int
    print("="*50)
    print("\tINFO KODE ORDER TIKET TRAVELIO!")
    print("="*50)
    kode_order = input("Masukan Kode order anda\t:")
    for order in orders:
        if kode_order == order["kode_order"]:
            order_list.append([order["kode_order"], order["nama_pembeli"], order["tanggal_pembelian"], order["kode_bis"], format_rupiah(order["total_harga"])])
            order_kode_bis = order["kode_bis"]

    if order_list != []:
        os.system("cls")
        print("="*83)
        print("\t\t\t\tDETAIL ORDER")
        print("="*83)
        print(tabulate(order_list, headers=["KODE ORDER", "Nama Pembeli", "Tanggal Pembelian", "Kode Bis", "Total Harga"], tablefmt="fancy_grid"))
        print("="*120)
        print("\t\t\t\t\t\t\tJADWAL TIKET")
        print("="*120)
        show_specific_ticket(order_kode_bis)
    else:
        print("KODE TIKET ANDA TIDAK DITEMUKAN!")
            


#masukin username& pw admin, pilih menu admin
def program_admin():
    print("="*30)
    print("\tLOGIN ADMIN")
    print("="*30)
    count = 1
    username = input("Masukan username admin\t: ")
    password = input("Masukan Password\t: ")
    admin = is_admin(username, password)

    while (admin == False and count < 3):
        os.system("cls")
        print("="*30)
        print("\tLOGIN ADMIN")
        print("="*30)
        print(f"Akun admin tidak terdaftar, silakan coba lagi ({3-count})")
        username = input("Masukan username admin: ")
        password = input("Masukan Password\t: ")
        admin = is_admin(username, password)
        count += 1
    choose = 0

    if count < 3:
        os.system("cls")
        menu_admin()
        choose = int(input("\nPilih Menu di atas: "))

        while choose >= 1 and choose <= 3:
            if choose == 1:
                os.system("cls")
                admin_insert_ticket()
            elif choose == 2:
                os.system("cls")
                admin_delete_ticket()
            elif choose == 3:
                os.system("cls")
                show_tickets()

            menu_admin()
            choose = int(input("\nPilih Menu di atas: "))
        os.system("cls")

#pilih menu pembeli
def program_pembeli():
    menu_pembeli()
    choose = int(input("\nPilih Menu di atas: "))
    choose_tampilan = int

    while choose >= 1 and choose <= 3:
        if choose == 1:
            os.system("cls")
            menu_urutkan()
            choose_tampilan = int(input("\nMasukan Pilihan:"))

            while choose_tampilan >= 1 and choose_tampilan <= 3:
                os.system("cls")
                if choose_tampilan == 1:
                    show_tickets()
                elif choose_tampilan == 2:
                    mengurutkan_tiket_berdasarkan_key("harga")
                elif choose_tampilan == 3:
                    mengurutkan_tiket_berdasarkan_key("date")

                menu_urutkan()
                choose_tampilan = int(input("\nMasukan Pilihan: "))
            os.system("cls")
        elif choose == 2:
            os.system("cls")
            buy_ticket()
        elif choose == 3:
            os.system("cls")
            info_detail_order()

        menu_pembeli()
        choose = int(input("\nPilih Menu di atas: "))
    os.system("cls")

'''
HANDLING EROR JIKA FILE TIDAK DITEMUKAN
'''
try:
    load_orders()
except FileNotFoundError:
    print("FILE ORDERS TIDAK DITEMUKAN")

try:
    load_user()
except FileNotFoundError:
    print("FILE USER TIDAK DITEMUKAN")

try:
    load_tickets()
except FileNotFoundError:
    print("FILE TICKET TIDAK DITEMUKAN")

'''
MENU UTAMAAA
'''

#menu utama
def main():
    os.system("cls")
    menu_main()
    option = int(input("\nPilih menu di atas: "))

    while option >= 1 and option <= 2:
        if option == 1:
            os.system("cls")
            program_admin()
        elif option == 2:
            os.system("cls")
            program_pembeli()
        menu_main()
        option = int(input("\nPilih menu di atas: "))

main()