from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
    InputFile
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import os
import json

# ================================
# 🔑 Token & ID
# ================================
TOKEN = "8245780531:AAG0uzBXGVRJ1v_jBpYI9V7fInWnUHD-0vI"  # Ganti dengan token Anda
ADMIN_CHAT_ID = -4854413968     # ID grup admin tempat laporan pengaduan
ADMIN_IDS = [1419182308]         # Ganti dengan user_id admin

# ================================
# 📂 File & Data
# ================================
BEASISWA_IMAGE = "pamflet_beasiswa.jpg"
DATA_FILE = "data.json"

# --- Fungsi untuk memuat dan menyimpan data dari data.json ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"perkuliahan": [], "beasiswa": []}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# --- Muat data saat bot pertama kali dijalankan ---
app_data = load_data()

# ================================
# 📚 Data Informasi Organisasi (Tetap sama)
# ================================
ORGANISASI_DATA = {
    "komisi1": "📌 *Komisi I – Pemerintahan*\n\nProgram Unggulan: *Safari Legislatif* ...",
    "komisi2": "📌 *Komisi II – Kajian Sosial Ekonomi*\n\nProgram Unggulan: *Dialog Legislatif* ...",
    "komisi3": "📌 *Komisi III – Pengembangan & Pelatihan*\n\nProgram Unggulan: *Pelatihan Legislatif* ...",
    "komisi4": "📌 *Komisi IV – Kesejahteraan Mahasiswa*\n\nProgram Unggulan: *Dialog Interaktif* ...",
    "bkd": "📌 *Badan Kehormatan Dewan (BKD)*\n\nProgram Unggulan: *Staff Magang* ...",
    "baleg": "📌 *Badan Legislasi*\n\nFokus pada fungsi legislasi ...",
    "bawas": "📌 *Badan Pengawasan*\n\nMelakukan fungsi kontrol ...",
    "advokasi": "📌 *Badan Advokasi*\n\nMenampung aspirasi ...",
    "kominfo": "📌 *Badan Kominfo*\n\nMengelola informasi & publikasi ...",
}

# ================================
# 🧭 Menu Utama (Tetap sama)
# ================================
async def show_main_menu(update_or_query, context: ContextTypes.DEFAULT_TYPE, edited=False):
    keyboard = [
        [InlineKeyboardButton("📚 Informasi Perkuliahan", callback_data="perkuliahan_menu")],
        [InlineKeyboardButton("💰 Informasi Beasiswa", callback_data="beasiswa")],
        [InlineKeyboardButton("📝 Pengaduan", callback_data="pengaduan")],
        [InlineKeyboardButton("🏛 Informasi Organisasi", callback_data="organisasi")]
    ]
    if isinstance(update_or_query, Update):
        user_id = update_or_query.message.from_user.id
    else:
        user_id = update_or_query.from_user.id
    if user_id in ADMIN_IDS:
        keyboard.append([InlineKeyboardButton("⚙️ Admin Menu", callback_data="admin_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "👋 *Selamat datang!*\nSilakan pilih menu di bawah ini:"
    if isinstance(update_or_query, Update):
        await update_or_query.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        if edited:
            await update_or_query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")
        else:
            await update_or_query.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

# ================================
# 📚 Informasi Perkuliahan (DIUBAH TOTAL)
# ================================
async def show_perkuliahan_menu(query, context: ContextTypes.DEFAULT_TYPE):
    perkuliahan_items = app_data.get("perkuliahan", [])
    keyboard = []
    
    if not perkuliahan_items:
        text = "📚 *Informasi Perkuliahan*\n\nSaat ini belum ada informasi yang tersedia."
    else:
        text = "📚 *Informasi Perkuliahan*\n\nSilakan pilih dokumen yang ingin Anda lihat:"
        # Buat tombol untuk setiap item
        for index, item in enumerate(perkuliahan_items):
            button = InlineKeyboardButton(
                f"{index + 1}. {item['title']}", 
                callback_data=f"get_perkuliahan_{index}"
            )
            keyboard.append([button])

    # Tambahkan tombol kembali
    keyboard.append([InlineKeyboardButton("⬅️ Kembali ke Menu", callback_data="main_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

# ================================
# 💰 Informasi Beasiswa (Tetap sama)
# ================================
async def show_beasiswa(query, context: ContextTypes.DEFAULT_TYPE):
    beasiswa_list = app_data.get("beasiswa", ["Informasi belum tersedia."])
    info_text = "\n".join([f"• {item}" for item in beasiswa_list])

    text = (f"💰 *Informasi Beasiswa Terbaru*\n\n{info_text}")
    keyboard = [[InlineKeyboardButton("⬅️ Kembali ke Menu", callback_data="main_menu")]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    if os.path.exists(BEASISWA_IMAGE):
        await query.message.reply_photo(photo=InputFile(BEASISWA_IMAGE), caption="📢 Pamflet Beasiswa")
    else:
        await query.message.reply_text("⚠️ Pamflet beasiswa belum tersedia.")

# ================================
# 📝 Pengaduan & Handler (Tetap sama)
# ================================
async def show_pengaduan(query, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📝 *Layanan Pengaduan*\n\n"
        "Silakan kirimkan pengaduan Anda di chat ini.\n"
        "Contoh:\n`[Pengaduan] Nama - NIM - Isi pengaduan`\n\n"
        "Admin akan menindaklanjuti laporan Anda."
    )
    keyboard = [[InlineKeyboardButton("⬅️ Kembali ke Menu", callback_data="main_menu")]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def pengaduan_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text
    report = (
        f"📨 *Pengaduan Baru*\n\n"
        f"👤 Dari: {user.first_name} (@{user.username or 'tidak ada username'})\n"
        f"🆔 ID: {user.id}\n\n"
        f"📝 Isi Pengaduan:\n{text}"
    )
    try:
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=report, parse_mode="Markdown")
        await update.message.reply_text("✅ Pengaduan Anda telah dikirim ke admin. Terima kasih 🙏")
    except Exception as e:
        await update.message.reply_text("⚠️ Gagal mengirim pengaduan ke admin.")
        print("Error kirim ke admin:", e)

# ================================
# 🏛 Informasi Organisasi (Tetap sama)
# ================================
async def show_organisasi_menu(query, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Komisi I", callback_data="komisi1"), InlineKeyboardButton("Komisi II", callback_data="komisi2")],
        [InlineKeyboardButton("Komisi III", callback_data="komisi3"), InlineKeyboardButton("Komisi IV", callback_data="komisi4")],
        [InlineKeyboardButton("BKD", callback_data="bkd"), InlineKeyboardButton("Baleg", callback_data="baleg")],
        [InlineKeyboardButton("Bawas", callback_data="bawas"), InlineKeyboardButton("Advokasi", callback_data="advokasi")],
        [InlineKeyboardButton("Kominfo", callback_data="kominfo")],
        [InlineKeyboardButton("⬅️ Kembali ke Menu", callback_data="main_menu")]
    ]
    text = "🏛 *Informasi Organisasi*\n\nPilih Komisi atau Badan untuk melihat program unggulannya:"
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

# ================================
# ⚙️ Admin Menu & Handlers (Diperbarui)
# ================================
async def show_admin_menu(query, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("✏️ Ubah List Info Perkuliahan", callback_data="admin_edit_list_perkuliahan")],
        [InlineKeyboardButton("🖼 Update Pamflet Beasiswa (Gambar)", callback_data="admin_update_beasiswa")],
        [InlineKeyboardButton("✏️ Ubah List Info Beasiswa", callback_data="admin_edit_list_beasiswa")],
        [InlineKeyboardButton("⬅️ Kembali ke Menu Utama", callback_data="main_menu")]
    ]
    await query.edit_message_text("⚙️ *Admin Menu*\nPilih konten yang ingin diperbarui:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

admin_update_mode = {}

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id

    if data == "perkuliahan_menu":
        await show_perkuliahan_menu(query, context)
    elif data.startswith("get_perkuliahan_"):
        index = int(data.split('_')[-1])
        item = app_data['perkuliahan'][index]
        file_path = item['file']
        if os.path.exists(file_path):
            await query.message.reply_document(document=InputFile(file_path), caption=item['title'])
        else:
            await query.message.reply_text(f"⚠️ Maaf, file '{file_path}' tidak ditemukan.")
    elif data == "beasiswa":
        await show_beasiswa(query, context)
    elif data == "pengaduan":
        await show_pengaduan(query, context)
    elif data == "organisasi":
        await show_organisasi_menu(query, context)
    elif data in ORGANISASI_DATA:
        await query.message.reply_text(ORGANISASI_DATA[data], parse_mode="Markdown")
    elif data == "admin_menu":
        await show_admin_menu(query, context)
    elif data == "main_menu":
        await show_main_menu(query, context, edited=True)
    
    # --- Logika baru untuk admin ---
    elif data == "admin_update_beasiswa":
        admin_update_mode[user_id] = "beasiswa_image"
        await query.message.reply_text("📥 Kirimkan *gambar pamflet* untuk menggantikan pamflet beasiswa.")
    elif data == "admin_edit_list_perkuliahan":
        admin_update_mode[user_id] = "perkuliahan_list"
        current_list_str = []
        for item in app_data.get("perkuliahan", []):
            current_list_str.append(f"{item['title']};{item['file']}")
        
        await query.message.reply_text(
            "📝 Kirimkan list informasi perkuliahan yang baru.\n"
            "Format per baris: `Judul Dokumen;path/ke/file.pdf`\n"
            "Contoh:\n`Surat Edaran Akademik;dokumen/surat.pdf`\n\n"
            f"*List saat ini:*\n`{chr(10).join(current_list_str) if current_list_str else 'Kosong'}`",
            parse_mode="Markdown"
        )
    elif data == "admin_edit_list_beasiswa":
        admin_update_mode[user_id] = "beasiswa_list"
        current_list = "\n".join(app_data.get("beasiswa", []))
        await query.message.reply_text(
            "📝 Kirimkan list informasi beasiswa yang baru.\n"
            "Pisahkan setiap item dengan baris baru (Enter).\n\n"
            f"*List saat ini:*\n{current_list if current_list else 'Kosong'}",
            parse_mode="Markdown"
        )

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id in ADMIN_IDS and user_id in admin_update_mode:
        mode = admin_update_mode[user_id]
        
        if mode == "beasiswa_image" and update.message.photo:
            photo = update.message.photo[-1]
            await photo.get_file().download_to_drive(BEASISWA_IMAGE)
            await update.message.reply_text("✅ Pamflet beasiswa berhasil diperbarui.")
        
        elif mode == "perkuliahan_list" and update.message.text:
            new_list = []
            lines = update.message.text.split('\n')
            for line in lines:
                if ';' in line:
                    title, file_path = line.split(';', 1)
                    new_list.append({"title": title.strip(), "file": file_path.strip()})
            app_data["perkuliahan"] = new_list
            save_data(app_data)
            await update.message.reply_text("✅ List informasi perkuliahan berhasil diperbarui.")

        elif mode == "beasiswa_list" and update.message.text:
            new_list = [item.strip() for item in update.message.text.split('\n') if item.strip()]
            app_data["beasiswa"] = new_list
            save_data(app_data)
            await update.message.reply_text("✅ List informasi beasiswa berhasil diperbarui.")
        
        else:
            await update.message.reply_text("⚠️ Jenis input tidak sesuai. Silakan kirim file atau teks yang benar.")
        
        del admin_update_mode[user_id]
        return

    await pengaduan_handler(update, context)

# ================================
# 🚀 Main Program (Tetap sama)
# ================================
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", show_main_menu))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO | filters.Document.ALL & ~filters.COMMAND, message_handler))
    
    print("🤖 Bot berjalan... Tekan CTRL+C untuk berhenti.")
    app.run_polling()

if __name__ == "__main__":
    main()