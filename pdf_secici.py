import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PyPDF2 import PdfReader, PdfWriter
import os

def pdf_sayfa_secici():
    # Tkinter penceresini gizle
    root = tk.Tk()
    root.withdraw()

    # PDF klasörünü seçtir
    klasor_yolu = filedialog.askdirectory(title="PDF'lerin Bulunduğu Klasörü Seç")
    if not klasor_yolu:
        messagebox.showinfo("Bilgi", "Klasör seçilmedi.")
        return

    # Klasördeki PDF'leri bul
    pdf_yollari = [
        os.path.join(klasor_yolu, f)
        for f in os.listdir(klasor_yolu)
        if f.lower().endswith(".pdf")
    ]

    if not pdf_yollari:
        messagebox.showinfo("Bilgi", "Seçilen klasörde PDF bulunamadı.")
        return

    # Hangi sayfalar kalsın?
    sayfalar_str = simpledialog.askstring(
        "Sayfa Seçimi",
        "Hangi sayfalar kalsın? (Örn: 1,2,5)"
    )
    if not sayfalar_str:
        messagebox.showinfo("Bilgi", "Sayfa belirtilmedi.")
        return

    try:
        sayfalar = [int(s.strip()) - 1 for s in sayfalar_str.split(",")]
    except ValueError:
        messagebox.showerror("Hata", "Geçersiz sayı formatı.")
        return

    # Kaydedilecek klasörü seçtir
    kayit_klasoru = filedialog.askdirectory(title="Kaydedilecek Klasörü Seç")
    if not kayit_klasoru:
        messagebox.showinfo("Bilgi", "Kaydedilecek klasör seçilmedi.")
        return

    # PDF’leri işle
    olusan_dosyalar = []
    for pdf_yolu in pdf_yollari:
        try:
            reader = PdfReader(pdf_yolu)
            writer = PdfWriter()

            for i in sayfalar:
                if 0 <= i < len(reader.pages):
                    writer.add_page(reader.pages[i])

            dosya_adi = os.path.basename(os.path.splitext(pdf_yolu)[0]) + "_secili_sayfalar.pdf"
            kayit_yolu = os.path.join(kayit_klasoru, dosya_adi)

            with open(kayit_yolu, "wb") as f:
                writer.write(f)

            olusan_dosyalar.append(dosya_adi)

        except Exception as e:
            messagebox.showerror("Hata", f"{os.path.basename(pdf_yolu)} işlenirken hata: {e}")

    if olusan_dosyalar:
        messagebox.showinfo("Tamamlandı", f"İşlem tamamlandı!\n\nOluşturulan dosyalar:\n" + "\n".join(olusan_dosyalar))
    else:
        messagebox.showinfo("Bilgi", "Hiç dosya oluşturulamadı.")

if __name__ == "__main__":
    pdf_sayfa_secici()
