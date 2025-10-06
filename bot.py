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
# --- GANTI DENGAN TOKEN DAN ID ANDA ---
TOKEN = "8245780531:AAG0uzBXGVRJ1v_jBpYI9V7fInWnUHD-0vI"
ADMIN_CHAT_ID = -4854413968
ADMIN_IDS = [1419182308] # Contoh: [12345, 67890] untuk banyak admin

# ================================
# 📂 Path & Data
# ================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.json")

def get_absolute_path(relative_path: str) -> str:
    """Ubah path relatif dari data.json menjadi absolut terhadap BASE_DIR."""
    if os.path.isabs(relative_path):
        return relative_path
    return os.path.join(BASE_DIR, relative_path)

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"perkuliahan": [], "beasiswa": []}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

app_data = load_data()

# ================================
# 📂 File & Data
# ================================
DATA_FILE = "data.json"

# --- Fungsi untuk memuat dan menyimpan data dari data.json ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    # Jika file tidak ada, buat struktur data default
    return {"perkuliahan": [], "beasiswa": []}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# --- Muat data saat bot pertama kali dijalankan ---
app_data = load_data()

# ================================
# 📚 Data Informasi Organisasi
# ================================
ORGANISASI_DATA = {
    "komisi1": "📌 *Komisi I – Pemerintahan*\n\nProgram Unggulan: *Safari Legislatif*",
    "komisi2": "📌 *Komisi II – Kajian Sosial Ekonomi*\n\nProgram Unggulan: *Dialog Legislatif*",
    "komisi3": "📌 *Komisi III – Pengembangan & Pelatihan*\n\nProgram Unggulan: *Pelatihan Legislatif*",
    "komisi4": "📌 *Komisi IV – Kesejahteraan Mahasiswa*\n\nProgram Unggulan: *Dialog Interaktif*",
    "bkd": "📌 *Badan Kehormatan Dewan (BKD)*\n\nProgram Unggulan: *Staff Magang*",
    "baleg": "📌 *Badan Legislasi*\n\nFokus pada fungsi legislasi",
    "bawas": "📌 *Badan Pengawasan*\n\nMelakukan fungsi kontrol",
    "advokasi": "📌 *Badan Advokasi*\n\nMenampung aspirasi",
    "kominfo": "📌 *Badan Kominfo*\n\nMengelola informasi & publikasi",
}

# ================================
# 🧭 Menu Utama (SUDAH DIPERBAIKI)
# ================================
async def show_main_menu(update_or_query, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📚 Informasi Perkuliahan", callback_data="perkuliahan_menu")],
        [InlineKeyboardButton("💰 Informasi Beasiswa", callback_data="beasiswa_menu")],
        [InlineKeyboardButton("📝 Pengaduan", callback_data="pengaduan")],
        [InlineKeyboardButton("🏛 Informasi Organisasi", callback_data="organisasi")]
    ]

    # Logika yang diperbaiki untuk mendapatkan user_id dengan benar
    if isinstance(update_or_query, Update):
        user_id = update_or_query.message.from_user.id
        action = update_or_query.message.reply_text
    else: # Ini adalah CallbackQuery
        user_id = update_or_query.from_user.id
        action = update_or_query.edit_message_text

    if user_id in ADMIN_IDS:
        keyboard.append([InlineKeyboardButton("⚙️ Admin Menu", callback_data="admin_menu")])
        
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "👋 *Selamat datang!*\nSilakan pilih menu di bawah ini:"

    await action(text, reply_markup=reply_markup, parse_mode="Markdown")

# ================================
# 📚 Informasi Perkuliahan
# ================================
async def show_perkuliahan_menu(query, context: ContextTypes.DEFAULT_TYPE):
    items = app_data.get("perkuliahan", [])
    keyboard = []
    text = "📚 *Informasi Perkuliahan*\n\n"
    if not items:
        text += "Saat ini belum ada informasi yang tersedia."
    else:
        text += "Silakan pilih dokumen yang ingin Anda lihat:"
        for index, item in enumerate(items):
            keyboard.append([InlineKeyboardButton(f"{index + 1}. {item['title']}", callback_data=f"get_perkuliahan_{index}")])
    keyboard.append([InlineKeyboardButton("⬅️ Kembali ke Menu", callback_data="main_menu_from_button")])
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

# ================================
# 💰 Informasi Beasiswa
# ================================
async def show_beasiswa_menu(query, context: ContextTypes.DEFAULT_TYPE):
    items = app_data.get("beasiswa", [])
    keyboard = []
    text = "💰 *Informasi Beasiswa*\n\n"
    if not items:
        text += "Saat ini belum ada informasi beasiswa yang tersedia."
    else:
        text += "Silakan pilih pamflet beasiswa yang ingin Anda lihat:"
        for index, item in enumerate(items):
            keyboard.append([InlineKeyboardButton(f"{index + 1}. {item['title']}", callback_data=f"get_beasiswa_{index}")])
    keyboard.append([InlineKeyboardButton("⬅️ Kembali ke Menu", callback_data="main_menu_from_button")])
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

# ================================
# 📝 Pengaduan & Organisasi
# ================================
async def show_pengaduan(query, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📝 *Layanan Pengaduan*\n\n"
        "Silakan kirimkan pengaduan Anda di chat ini.\n"
        "Contoh:\n`[Pengaduan] Nama - NIM - Isi pengaduan`\n\n"
        "Admin akan menindaklanjuti laporan Anda."
    )
    keyboard = [[InlineKeyboardButton("⬅️ Kembali ke Menu", callback_data="main_menu_from_button")]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def show_organisasi_menu(query, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Komisi I", callback_data="komisi1"), InlineKeyboardButton("Komisi II", callback_data="komisi2")],
        [InlineKeyboardButton("Komisi III", callback_data="komisi3"), InlineKeyboardButton("Komisi IV", callback_data="komisi4")],
        [InlineKeyboardButton("BKD", callback_data="bkd"), InlineKeyboardButton("Baleg", callback_data="baleg")],
        [InlineKeyboardButton("Bawas", callback_data="bawas"), InlineKeyboardButton("Advokasi", callback_data="advokasi")],
        [InlineKeyboardButton("Kominfo", callback_data="kominfo")],
        [InlineKeyboardButton("⬅️ Kembali ke Menu", callback_data="main_menu_from_button")]
    ]
    text = "🏛 *Informasi Organisasi*\n\nPilih Komisi atau Badan untuk melihat program unggulannya:"
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
        print(f"Error mengirim pengaduan ke admin: {e}")

# ================================
# ⚙️ Admin Menu & Handlers
# ================================
async def show_admin_menu(query, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("✏️ Ubah List Info Perkuliahan", callback_data="admin_edit_list_perkuliahan")],
        [InlineKeyboardButton("✏️ Ubah List Info Beasiswa", callback_data="admin_edit_list_beasiswa")],
        [InlineKeyboardButton("⬅️ Kembali ke Menu Utama", callback_data="main_menu_from_button")]
    ]
    await query.edit_message_text("⚙️ *Admin Menu*\nPilih konten yang ingin diperbarui:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

admin_update_mode = {}

# GANTI FUNGSI LAMA DENGAN VERSI BARU INI
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id

    if data == "main_menu_from_button":
        await show_main_menu(query, context)
    elif data == "perkuliahan_menu":
        await show_perkuliahan_menu(query, context)
    elif data == "beasiswa_menu":
        await show_beasiswa_menu(query, context)
    elif data == "pengaduan":
        await show_pengaduan(query, context)
    elif data == "organisasi":
        await show_organisasi_menu(query, context)
    elif data in ORGANISASI_DATA:
        await query.message.reply_text(ORGANISASI_DATA[data], parse_mode="Markdown")
    
    elif data.startswith("get_perkuliahan_") or data.startswith("get_beasiswa_"):
        # Logika Canggih untuk Mengirim File
        is_perkuliahan = data.startswith("get_perkuliahan_")
        index = int(data.split('_')[-1])
        
        item_list = app_data['perkuliahan'] if is_perkuliahan else app_data['beasiswa']
        item = item_list[index]
        file_path = item['file']

        if os.path.exists(file_path):
            # Cek ukuran file. Jika 0, beri peringatan.
            if os.path.getsize(file_path) > 0:
                if is_perkuliahan:
                    await query.message.reply_document(document=InputFile(file_path), caption=item['title'])
                else:
                    await query.message.reply_photo(photo=InputFile(file_path), caption=item['title'])
            else:
                await query.message.reply_text(f"⚠️ Maaf, file '{file_path}' ditemukan tapi isinya kosong (0 KB). Mohon hubungi admin.")
        else:
            await query.message.reply_text(f"⚠️ Maaf, file '{file_path}' tidak ditemukan di server. Mohon hubungi admin.")

    elif data == "admin_menu":
        await show_admin_menu(query, context)
        
    elif data == "admin_edit_list_perkuliahan":
        admin_update_mode[user_id] = "perkuliahan_list"
        current_list_str = [f"{item['title']};{item['file']}" for item in app_data.get("perkuliahan", [])]
        await query.message.reply_text(
            "📝 Kirimkan list info perkuliahan baru.\n"
            "Format per baris: `Judul;path/ke/file.pdf`\n\n"
            f"*List saat ini:*\n`{chr(10).join(current_list_str) if current_list_str else 'Kosong'}`",
            parse_mode="Markdown"
        )

    elif data == "admin_edit_list_beasiswa":
        admin_update_mode[user_id] = "beasiswa_list"
        current_list_str = [f"{item['title']};{item['file']}" for item in app_data.get("beasiswa", [])]
        await query.message.reply_text(
            "📝 Kirimkan list info beasiswa baru.\n"
            "Format per baris: `Judul;path/ke/gambar.jpg`\n\n"
            f"*List saat ini:*\n`{chr(10).join(current_list_str) if current_list_str else 'Kosong'}`",
            parse_mode="Markdown"
        )

async def text_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in ADMIN_IDS and user_id in admin_update_mode:
        mode = admin_update_mode.pop(user_id)
        text = update.message.text
        
        new_list = []
        try:
            for line in text.split('\n'):
                if ';' in line:
                    title, file_path = [x.strip() for x in line.split(';', 1)]
                    new_list.append({"title": title, "file": file_path})

            if mode == "perkuliahan_list":
                app_data["perkuliahan"] = new_list
                save_data(app_data)
                await update.message.reply_text("✅ List informasi perkuliahan berhasil diperbarui.")
            elif mode == "beasiswa_list":
                app_data["beasiswa"] = new_list
                save_data(app_data)
                await update.message.reply_text("✅ List informasi beasiswa berhasil diperbarui.")
        except ValueError:
            await update.message.reply_text("⚠️ Format salah. Pastikan menggunakan format `Judul;path/ke/file`.")
        return

    await pengaduan_handler(update, context)

admin_update_mode = {}

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id

    if data == "main_menu_from_button":
        await show_main_menu(query, context)
    elif data == "perkuliahan_menu":
        await show_perkuliahan_menu(query, context)
    elif data == "beasiswa_menu":
        await show_beasiswa_menu(query, context)
    elif data == "pengaduan":
        await show_pengaduan(query, context)
    elif data == "organisasi":
        await show_organisasi_menu(query, context)
    elif data in ORGANISASI_DATA:
        await query.message.reply_text(ORGANISASI_DATA[data], parse_mode="Markdown")
    
    elif data.startswith("get_perkuliahan_") or data.startswith("get_beasiswa_"):
        is_perkuliahan = data.startswith("get_perkuliahan_")
        index = int(data.split('_')[-1])
        item_list = app_data['perkuliahan'] if is_perkuliahan else app_data['beasiswa']
        item = item_list[index]

        file_path = get_absolute_path(item['file'])  # ✅ PENTING: konversi ke absolut

        if os.path.exists(file_path):
            if os.path.getsize(file_path) > 0:
                if is_perkuliahan:
                    await query.message.reply_document(document=InputFile(file_path), caption=item['title'])
                else:
                    await query.message.reply_photo(photo=InputFile(file_path), caption=item['title'])
            else:
                await query.message.reply_text(f"⚠️ File ditemukan tapi kosong (0 KB):\n`{file_path}`", parse_mode="Markdown")
        else:
            await query.message.reply_text(f"⚠️ File tidak ditemukan:\n`{file_path}`", parse_mode="Markdown")

# ================================
# 🚀 Main Program
# ================================
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Handlers
    app.add_handler(CommandHandler("start", show_main_menu))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message_handler))
    
    print("🤖 Bot berjalan... Tekan CTRL+C untuk berhenti.")
    app.run_polling()

if __name__ == "__main__":
    main()