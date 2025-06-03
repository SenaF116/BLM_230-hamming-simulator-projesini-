import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import math

class HammingSECDed:
    def __init__(self, data_bits):
        """
        Initialize Hamming SEC-DED encoder/decoder
        :param data_bits: Number of data bits (8, 16, or 32)
        """
        if data_bits not in [8, 16, 32]:
            raise ValueError("Veri bit sayısı 8, 16 veya 32 olmalı")
        self.data_bits = data_bits
        self.total_bits = self.calculate_total_bits()
        self.parity_positions = self.calculate_parity_positions()

    def calculate_total_bits(self):
        """Toplam bit sayısını hesapla (veri + düzeltme bitleri)"""
        m = 0
        while (2 ** m) < (self.data_bits + m + 1):
            m += 1
        return self.data_bits + m

    def calculate_parity_positions(self):
        """Düzeltme bitlerinin pozisyonlarını hesapla"""
        return [2**i for i in range(self.total_bits - self.data_bits)]

    def encode(self, data):
        """
        Veriyi Hamming koduna dönüştür
        :param data: Binary string of data bits
        :return: Encoded Hamming code
        """
        if len(data) != self.data_bits:
            raise ValueError(f"Veri {self.data_bits} bit uzunluğunda olmalı")

        encoded = ['0'] * self.total_bits
        data_index = 0
        for i in range(1, self.total_bits + 1):
            if i not in self.parity_positions:
                encoded[i-1] = data[data_index]
                data_index += 1

        for p in self.parity_positions:
            parity_sum = 0
            for i in range(1, self.total_bits + 1):
                if i & p == p:
                    parity_sum += int(encoded[i-1])
            encoded[p-1] = str(parity_sum % 2)

        return ''.join(encoded)

    def decode(self, encoded_data):
        """
        Hamming kodunu çöz ve hataları tespit et/düzelt
        :param encoded_data: Encoded Hamming code
        :return: Tuple (decoded data, error position if any)
        """
        if len(encoded_data) != self.total_bits:
            raise ValueError(f"Kodlanmış veri {self.total_bits} bit uzunluğunda olmalı")

        syndrome = []
        for p in self.parity_positions:
            parity_sum = 0
            for i in range(1, self.total_bits + 1):
                if i & p == p:
                    parity_sum += int(encoded_data[i-1])
            syndrome.append(str(parity_sum % 2))

        syndrome_str = ''.join(syndrome)
        error_position = int(syndrome_str, 2)

        if error_position == 0:
            return self.extract_data(encoded_data), None

        if 1 <= error_position <= self.total_bits:
            corrected = list(encoded_data)
            corrected[error_position-1] = str(1 - int(corrected[error_position-1]))
            return self.extract_data(corrected), error_position

        return None, "Çift hata tespit edildi"

    def extract_data(self, encoded_data):
        """Kodlanmış veriden orijinal veriyi çıkar"""
        data = []
        for i in range(1, self.total_bits + 1):
            if i not in self.parity_positions:
                data.append(encoded_data[i-1])
        return ''.join(data)

    def inject_random_error(self):
        """Rastgele hata ekle"""
        try:
            encoded = self.encoded_output.get()
            if not encoded:
                raise ValueError("İlk olarak veri kodlanmalı")
            
            error_type = self.error_type_var.get()
            error_positions = []
            
            # Rastgele pozisyonlar seç
            while len(error_positions) < (1 if error_type == "Tek Hata" else 
                                        2 if error_type == "Çift Hata" else 3):
                pos = random.randint(1, self.hamming.total_bits)
                if pos not in error_positions:
                    error_positions.append(pos)
            
            # Hataları ekle
            current_data = encoded
            for pos in error_positions:
                current_data = self.hamming.inject_error(current_data, pos)
            
            self.error_output.config(state="normal")
            self.error_output.delete(0, tk.END)
            self.error_output.insert(0, current_data)
            self.error_output.config(state="readonly")
            
            self.draw_bits(current_data)
            
            # Hata pozisyonlarını göster
            error_str = ", ".join(map(str, sorted(error_positions)))
            self.status_var.set(f"Rastgele hatalar eklendi: Pozisyon(lar): {error_str}")
            
        except ValueError as e:
            messagebox.showerror("Hata", str(e))
            self.status_var.set(str(e))

    def inject_random_error(self):
        """Rastgele hata ekle"""
        try:
            encoded = self.encoded_output.get()
            if not encoded:
                raise ValueError("İlk olarak veri kodlanmalı")
            
            error_type = self.error_type_var.get()
            error_positions = []
            
            # Rastgele pozisyonlar seç
            while len(error_positions) < (1 if error_type == "Tek Hata" else 
                                        2 if error_type == "Çift Hata" else 3):
                pos = random.randint(1, self.hamming.total_bits)
                if pos not in error_positions:
                    error_positions.append(pos)
            
            # Hataları ekle
            current_data = encoded
            for pos in error_positions:
                current_data = self.hamming.inject_error(current_data, pos)
            
            self.error_output.config(state="normal")
            self.error_output.delete(0, tk.END)
            self.error_output.insert(0, current_data)
            self.error_output.config(state="readonly")
            
            self.draw_bits(current_data)
            
            # Hata pozisyonlarını göster
            error_str = ", ".join(map(str, sorted(error_positions)))
            self.status_var.set(f"Rastgele hatalar eklendi: Pozisyon(lar): {error_str}")
            
        except ValueError as e:
            messagebox.showerror("Hata", str(e))
            self.status_var.set(str(e))

    def inject_error(self, encoded_data, position):
        """
        Belirli pozisyona hata ekle
        :param encoded_data: Encoded Hamming code
        :param position: Hata eklenecek pozisyon (1-based index)
        :return: Data with error injected
        """
        if position < 1 or position > self.total_bits:
            raise ValueError("Hata pozisyonu geçersiz")
        
        data_list = list(encoded_data)
        data_list[position-1] = str(1 - int(data_list[position-1]))
        return ''.join(data_list)

class HammingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hamming SEC-DED Simülatörü")
        self.root.geometry("1000x800")
        
        # Hamming encoder başlat
        self.hamming = HammingSECDed(8)
        
        # Ana frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Veri boyutu seçimi
        ttk.Label(self.main_frame, text="Veri Boyutu:").grid(row=0, column=0, sticky=tk.W)
        self.data_size_var = tk.StringVar(value="8")
        self.data_size_combo = ttk.Combobox(self.main_frame, 
                                           textvariable=self.data_size_var,
                                           values=["8", "16", "32"],
                                           width=5)
        self.data_size_combo.grid(row=0, column=1, sticky=tk.W)
        
        # Hata tipi seçimi
        ttk.Label(self.main_frame, text="Hata Tipi:").grid(row=1, column=0, sticky=tk.W)
        self.error_type_var = tk.StringVar(value="Tek Hata")
        self.error_type_combo = ttk.Combobox(self.main_frame,
                                           textvariable=self.error_type_var,
                                           values=["Tek Hata", "Çift Hata", "Üçlü Hata"],
                                           width=10)
        self.error_type_combo.grid(row=1, column=1, sticky=tk.W)
        
        # Hata ekleme butonu
        self.inject_auto_btn = ttk.Button(self.main_frame, text="Rastgele Hata Ekle", 
                                        command=self.inject_random_error_gui)
        self.inject_auto_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Açıklama metni
        ttk.Label(self.main_frame, text="""
        Hamming SEC-DED (Tek Hata Düzeltme, Çift Hata Tespit) kodu, 
        veri iletiminde hataları tespit etme ve düzeltme için kullanılır.
        Bu simülatör, veri boyutuna göre Hamming kodunu oluşturur,
        hataları simüle eder ve düzeltir.
        """).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Veri girişi
        ttk.Label(self.main_frame, text="Orijinal Veri (0 ve 1):").grid(row=4, column=0, sticky=tk.W)
        self.data_entry = ttk.Entry(self.main_frame, width=40)
        self.data_entry.grid(row=4, column=1, sticky=tk.W)
        
        # Encode butonu
        self.encode_btn = ttk.Button(self.main_frame, text="Kodu Oluştur", command=self.encode_data)
        self.encode_btn.grid(row=5, column=0, columnspan=2, pady=10)
        
        # Visual bit gösterimi
        self.bit_canvas = tk.Canvas(self.main_frame, width=800, height=100, bg='white')
        self.bit_canvas.grid(row=6, column=0, columnspan=2, pady=10)
        
        # Kodlanmış veri
        ttk.Label(self.main_frame, text="Kodlanmış Veri:").grid(row=7, column=0, sticky=tk.W)
        self.encoded_output = ttk.Entry(self.main_frame, width=40, state="readonly")
        self.encoded_output.grid(row=7, column=1, sticky=tk.W)
        
        # Hata eklenecek veri
        ttk.Label(self.main_frame, text="Hatalı Veri:").grid(row=10, column=0, sticky=tk.W)
        self.error_output = ttk.Entry(self.main_frame, width=40, state="readonly")
        self.error_output.grid(row=10, column=1, sticky=tk.W)
        
        # Decode butonu
        self.decode_btn = ttk.Button(self.main_frame, text="Kodu Çöz", command=self.decode_data)
        self.decode_btn.grid(row=11, column=0, columnspan=2, pady=10)
        
        # Çözülen veri
        ttk.Label(self.main_frame, text="Çözülen Veri:").grid(row=12, column=0, sticky=tk.W)
        self.decoded_output = ttk.Entry(self.main_frame, width=40, state="readonly")
        self.decoded_output.grid(row=12, column=1, sticky=tk.W)
        
        # Hata pozisyonu
        ttk.Label(self.main_frame, text="Tespit Edilen Hata Pozisyonu:").grid(row=13, column=0, sticky=tk.W)
        self.error_pos_output = ttk.Entry(self.main_frame, width=40, state="readonly")
        self.error_pos_output.grid(row=13, column=1, sticky=tk.W)
        
        # Durum mesajı
        self.status_var = tk.StringVar()
        self.status_label = ttk.Label(self.main_frame, textvariable=self.status_var)
        self.status_label.grid(row=14, column=0, columnspan=2, pady=10)
        
        # Hamming kodu açıklaması
        ttk.Label(self.main_frame, text="""
        Hamming Kodu Açıklaması:
        - Düzeltme bitleri (P) veri bitlerini korur
        - Her düzeltme biti, belirli pozisyonlardaki bitleri kontrol eder
        - Tek hatalar otomatik olarak düzeltilebilir
        - Çift hatalar tespit edilebilir
        """).grid(row=15, column=0, columnspan=2, pady=10)

        # Console output
        ttk.Label(self.main_frame, text="Konsol Çıktısı:").grid(row=16, column=0, sticky=tk.W)
        self.console_text = tk.Text(self.main_frame, height=10, width=50)
        self.console_text.grid(row=17, column=0, columnspan=2, pady=10)
        self.console_text.insert(tk.END, "Program başlatıldı\n")
        self.console_text.configure(state='disabled')  # Prevent editing
        
    def draw_bits(self, bits):
        """Bitleri görsel olarak göster"""
        if not bits:
            return
            
        bit_width = 50
        bit_height = 50
        x_offset = 50
        y_offset = 25
        
        self.bit_canvas.delete("all")
        
        for i, bit in enumerate(bits):
            x = x_offset + (i * (bit_width + 10))
            
            # Bit kutusu
            self.bit_canvas.create_rectangle(x, y_offset, 
                                           x + bit_width, y_offset + bit_height,
                                           fill='white', outline='black')
            
            # Bit değeri
            self.bit_canvas.create_text(x + bit_width/2, y_offset + bit_height/2,
                                       text=bit, font=('Arial', 16))
            
            # Düzeltme bitlerini farklı renkle göster
            if i + 1 in self.hamming.parity_positions:
                self.bit_canvas.create_rectangle(x, y_offset, 
                                               x + bit_width, y_offset + bit_height,
                                               fill='lightblue', outline='black')
            
            # Bit pozisyonu
            self.bit_canvas.create_text(x + bit_width/2, y_offset + bit_height + 20,
                                       text=str(i + 1), font=('Arial', 10))
    
    def encode_data(self):
        try:
            data_size = int(self.data_size_var.get())
            self.hamming = HammingSECDed(data_size)
            
            data = self.data_entry.get()
            if len(data) != data_size:
                raise ValueError(f"Veri {data_size} bit uzunluğunda olmalı")
            if not all(bit in '01' for bit in data):
                raise ValueError("Veri sadece 0 ve 1 içerebilir")
            
            encoded = self.hamming.encode(data)
            self.encoded_output.config(state="normal")
            self.encoded_output.delete(0, tk.END)
            self.encoded_output.insert(0, encoded)
            self.encoded_output.config(state="readonly")
            
            self.draw_bits(encoded)
            self.status_var.set("Veri başarıyla kodlandı")
            self.console_text.configure(state='normal')
            self.console_text.insert(tk.END, f"Veri kodlandı: {encoded}\n")
            self.console_text.configure(state='disabled')
            self.console_text.see(tk.END)
        except ValueError as e:
            messagebox.showerror("Hata", str(e))
            self.status_var.set(str(e))
    
    def inject_random_error_gui(self):
        try:
            encoded = self.encoded_output.get()
            if not encoded:
                raise ValueError("İlk olarak veri kodlanmalı")
            
            error_type = self.error_type_var.get()
            error_positions = []
            
            # Rastgele pozisyonlar seç
            while len(error_positions) < (1 if error_type == "Tek Hata" else 
                                        2 if error_type == "Çift Hata" else 3):
                pos = random.randint(1, self.hamming.total_bits)
                if pos not in error_positions:
                    error_positions.append(pos)
            
            # Hataları ekle
            current_data = encoded
            for pos in error_positions:
                current_data = self.hamming.inject_error(current_data, pos)
            
            self.error_output.config(state="normal")
            self.error_output.delete(0, tk.END)
            self.error_output.insert(0, current_data)
            self.error_output.config(state="readonly")
            
            self.draw_bits(current_data)
            self.status_var.set(f"{len(error_positions)} hata rastgele pozisyona eklendi")
            self.console_text.configure(state='normal')
            self.console_text.insert(tk.END, f"{len(error_positions)} hata eklendi: Pozisyonlar {error_positions}\n")
            self.console_text.configure(state='disabled')
            self.console_text.see(tk.END)
            
        except ValueError as e:
            messagebox.showerror("Hata", str(e))
            self.status_var.set(str(e))

    def decode_data(self):
        try:
            data = self.error_output.get()
            if not data:
                raise ValueError("Hatalı veri bulunamadı")
            
            decoded, error_pos = self.hamming.decode(data)
            
            self.decoded_output.config(state="normal")
            self.decoded_output.delete(0, tk.END)
            self.decoded_output.insert(0, decoded if decoded else "")
            self.decoded_output.config(state="readonly")
            
            self.error_pos_output.config(state="normal")
            self.error_pos_output.delete(0, tk.END)
            self.error_pos_output.insert(0, str(error_pos) if error_pos else "")
            self.error_pos_output.config(state="readonly")
            
            if error_pos is None:
                self.status_var.set("Herhangi bir hata bulunamadı")
                self.console_text.configure(state='normal')
                self.console_text.insert(tk.END, "Herhangi bir hata bulunamadı\n")
                self.console_text.configure(state='disabled')
                self.console_text.see(tk.END)
            elif error_pos == "Çift hata tespit edildi":
                self.status_var.set("Çift hata tespit edildi! Düzeltilemez.")
                self.console_text.configure(state='normal')
                self.console_text.insert(tk.END, "Çift hata tespit edildi! Düzeltilemez.\n")
                self.console_text.configure(state='disabled')
                self.console_text.see(tk.END)
            else:
                # Show which type of bit is faulty
                if error_pos in self.hamming.parity_positions:
                    self.status_var.set(f"{error_pos}. pozisyondaki düzeltme bitinde hata tespit edildi")
                else:
                    self.status_var.set(f"Tek hata {error_pos}. pozisyonda tespit edildi")
                self.console_text.configure(state='normal')
                self.console_text.insert(tk.END, f"Tek hata tespit edildi: Pozisyon {error_pos}\n")
                self.console_text.configure(state='disabled')
                self.console_text.see(tk.END)
                # Show the bit positions clearly
                self.status_var.set(self.status_var.get() + 
                                  f"\n(Parity bits: {', '.join(map(str, self.hamming.parity_positions))})")
                
        except ValueError as e:
            messagebox.showerror("Hata", str(e))
            self.status_var.set(str(e))

def main():
    root = tk.Tk()
    app = HammingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
