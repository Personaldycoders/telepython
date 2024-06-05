#SC INI 100% HASIL CODING DYCODERS RECODE? TIDAK BOLEH HAPUS TEXT INI

# SC USERBOT BY DYCODERS
from telethon.sync import TelegramClient, events
from telethon.tl.types import ChannelParticipantsAdmins, ChannelParticipantsBots, ChannelParticipantsKicked, ChannelParticipantsBanned, ChannelParticipantsSearch, InputChannel, InputChannelEmpty
from telethon.tl.types import MessageMediaDocument
from telegraph import upload_file, exceptions
from telethon.tl.functions.contacts import BlockRequest
from telethon import functions
import os
from googletrans import Translator
import time
import re
from telethon import types
import asyncio
import speedtest
from datetime import datetime
import requests
import json
import aiohttp
from subprocess import Popen
from googlesearch import search
from bs4 import BeautifulSoup
import subprocess 
import base64
from telethon.tl.types import InputPeerUser
from telethon.tl.types import PeerChannel, PeerChat
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.types import DocumentAttributeAudio
import yt_dlp as youtube_dl
from PIL import Image
import pytesseract
import io
import mimetypes
from telethon import Button






api_id = '26179013'
api_hash = '557709e4ba2e464c2fd69b45254c6f6d'

client = TelegramClient('dysession', api_id, api_hash)
target_chat_id = None
fake_typing_task = None
owner_id = '6721761178'
removebg_api_key = "KENZ-MD"
read_messages = {}
user_details = {}
CHECK_HOST_API_URL = "https://check-host.net/check-"
CHECK_HOST_RESULT_URL = "https://check-host.net/check-result/"
ocr_api_key = 'K88699237688957'
upload_directory = '/'
translator = Translator()


menu_items = [
    "uploads", "ocr", "encode", "decode", "readall",
    "bc", "generateemail", "getbox", "google", "cekhost",
    "ai", "subdomain", "cat", "ls", "run",
    "cekdomain", "block", "nik", "cekip", "groupinfo",
    "status", "restart", "top", "ping", "ig",
    "tiktok", "play", "speedtest", "getid", "startsimi",
    "stopsimi", "setid", "kick", "ssweb", "tourl",
    "hd", "cekid", "faketyping", "id", "menu"
]

menu_text = " | ".join(menu_items)
menu_text = menu_text.replace(" | ", "\n   • ")


menu_message = f"**Pilih menu:**\n\n   • {menu_text}"


image_url = "https://telegra.ph/file/6cb17d079041c6ae70cc5.jpg"  

@client.on(events.NewMessage(pattern='/menu'))
async def menu(event):
    if str(event.sender_id) != owner_id:
        return

    
    await event.respond(
        menu_message,
        parse_mode='markdown',
        file=image_url  
    )
    await event.delete()









@client.on(events.NewMessage(pattern='/lirik'))
async def search_lyrics(event):
    if str(event.sender_id) != owner_id:
        return
    
    query = event.message.text.split(' ', 1)[1]
    url = f"https://api.maher-zubair.tech/search/lyrics?q={query}"
    
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            artist = data['result']['artist']
            title = data['result']['title']
            lyrics = data['result']['lyrics']
            message = f"Lirik lagu {title} oleh {artist}:\n\n{lyrics}"
            await event.respond(message)
        else:
            await event.respond(f"Tidak dapat menemukan lirik untuk {query}")
        
        
        await event.delete()
        
    except Exception as e:
        await event.respond(f"Terjadi kesalahan: {str(e)}")



@client.on(events.NewMessage(pattern='/upload'))
async def upload_file(event):
    if str(event.sender_id) != owner_id:
        return

    if event.is_reply:
        replied_msg = await event.get_reply_message()
        if replied_msg.media:
            file = await replied_msg.download_media(file=upload_directory)
            file_extension = os.path.splitext(file)[1].lower()

            if file_extension in ['.txt', '.png', '.jpg', '.jpeg']:
                await event.respond(f"File {file} berhasil diunggah ke direktori {upload_directory}")
            else:
                os.remove(file)
                await event.respond("Jenis file tidak didukung. Harap unggah file TXT, PNG, atau JPG.")
        else:
            await event.respond("Balas pesan yang berisi file yang ingin diunggah.")
    else:
        await event.respond("Balas pesan yang berisi file dengan perintah /upload.")






@client.on(events.NewMessage(pattern='/ocr'))
async def handler(event):
    if str(event.sender_id) != owner_id:
        return

    
    if event.is_reply:
        reply_message = await event.get_reply_message()
        if reply_message.photo or reply_message.document:
            try:
               
                file_path = await reply_message.download_media()
                file_name = os.path.basename(file_path)
                file_extension = os.path.splitext(file_name)[1]

                
                if not file_extension:
                    mime_type, _ = mimetypes.guess_type(file_path)
                    if mime_type:
                        file_extension = mimetypes.guess_extension(mime_type)
                        new_file_path = file_path + file_extension
                        os.rename(file_path, new_file_path)
                        file_path = new_file_path
                    else:
                        await event.reply("Tidak dapat menentukan jenis file. Mohon pastikan file memiliki ekstensi yang benar.")
                        return

               
                with open(file_path, 'rb') as f:
                    response = requests.post(
                        'https://api.ocr.space/parse/image',
                        files={'filename': (file_name, f, 'application/octet-stream')},
                        data={'apikey': ocr_api_key}
                    )
                
                result = response.json()
                if result['IsErroredOnProcessing'] == False:
                    text = result['ParsedResults'][0]['ParsedText']
                    
                    await event.reply(f"`Hasil OCR:\n\n{text}`")
                else:
                    await event.reply(f"Terjadi kesalahan: {result['ErrorMessage']}")

               
                os.remove(file_path)

            except Exception as e:
                await event.reply(f"Terjadi kesalahan: {e}")
        else:
            await event.reply("Pesan yang dibalas harus berupa gambar atau dokumen.")
    else:
        await event.reply("Gunakan perintah ini sebagai balasan ke pesan yang berisi gambar atau dokumen.")





@client.on(events.NewMessage(pattern='/encode'))
async def encode(event):
    if str(event.sender_id) != owner_id:
        
        return

    try:
        message = event.message.message
        text_to_encode = message.split(' ', 1)[1]
        encoded_text = base64.b64encode(text_to_encode.encode()).decode()
        await event.reply(f"Encoded text: `{encoded_text}`")
    except IndexError:
        await event.reply("Please provide text to encode after the command. Example: /encode hello")



@client.on(events.NewMessage(pattern='/decode'))
async def decode(event):
    if str(event.sender_id) != owner_id:
       
        return

    try:
        message = event.message.message
        text_to_decode = message.split(' ', 1)[1]
        decoded_text = base64.b64decode(text_to_decode).decode()
        await event.edit(f"Decoded text: {decoded_text}")
    except (IndexError, base64.binascii.Error):
        await event.reply("Please provide valid Base64 text to decode after the command. Example: /decode aGVsbG8=")





@client.on(events.NewMessage(pattern='/readall'))
async def read_all_handler(event):
    if str(event.sender_id) != owner_id:
        return

    dialogs = await client.get_dialogs()
    for dialog in dialogs:
        if dialog.unread_count > 0:
            try:
                await client.send_read_acknowledge(dialog.entity)
                print(f"Marked all messages as read in {dialog.name}")
            except Exception as e:
                print(f"Failed to mark messages as read in {dialog.name}: {e}")

    await event.respond("DONE √.")







@client.on(events.NewMessage(pattern='/bc'))
async def broadcast_handler(event):
    if str(event.sender_id) != owner_id:
        return

    message_text = event.message.text.split(' ', 1)
    if len(message_text) < 2:
        await event.respond("Silakan berikan pesan untuk disiarkan. Contoh penggunaan: /bc [pesan Anda]")
        return

    message = message_text[1]

    async for dialog in client.iter_dialogs():
        if dialog.is_group or dialog.is_channel:
            try:
                await client.send_message(dialog.id, message)
            except Exception as e:
                print(f"Failed to send message to {dialog.name}: {e}")

    await event.respond("Pesan telah dikirim ke semua grup.")














async def get_temp_email():
    url = 'https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data[0]
    return None

@client.on(events.NewMessage(pattern='/generateemail'))
async def generate_email(event):
    if str(event.sender_id) != owner_id:
        return
    try:
        email = await get_temp_email()
        if email:
            await event.respond(f"Email sementara: {email}")
        else:
            await event.respond("Gagal mendapatkan email sementara.")
    except Exception as e:
        await event.respond(f"Terjadi kesalahan: {str(e)}")

async def get_inbox(email):
    try:
        domain = email.split('@')[1]
        username = email.split('@')[0]
        url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={username}&domain={domain}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

async def get_message_details(email, message_id):
    try:
        domain = email.split('@')[1]
        username = email.split('@')[0]
        url = f"https://www.1secmail.com/api/v1/?action=readMessage&login={username}&domain={domain}&id={message_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

async def get_message_text(email, message_id):
    details = await get_message_details(email, message_id)
    if details:
        return details.get('textBody', '') or details.get('htmlBody', '')
    return ''

def split_text(text, length):
    return [text[i:i+length] for i in range(0, len(text), length)]

@client.on(events.NewMessage(pattern='/getbox'))
async def get_box(event):
    if str(event.sender_id) != owner_id:
        return
    try:
        email = event.message.text.split(' ', 1)[1] if len(event.message.text.split()) > 1 else None
        if not email:
            await event.respond("Harap berikan email yang valid. Contoh penggunaan: /getbox example@1secmail.com")
            return
        
        inbox = await get_inbox(email)
        if inbox is not None:
            if len(inbox) == 0:
                await event.respond("Inbox kosong.")
            else:
                for msg in inbox:
                    details = await get_message_details(email, msg['id'])
                    message_text = await get_message_text(email, msg['id'])
                    full_message = f"Pengirim: {details['from']}\nSubjek: {details['subject']}\nTanggal: {details['date']}\nIsi: {message_text}"

                   
                    parts = split_text(full_message, 4000)
                    for part in parts:
                        
                        part = re.sub(r'(```(python|html|css|js|javascript|php)(.*?)```)', r'```\2\n\3\n```', part, flags=re.DOTALL)
                        
                        
                        part = re.sub(r'(<pre.*?>.*?</pre>)', r'```\n\1\n```', part, flags=re.DOTALL)
                        part = re.sub(r'(<code.*?>.*?</code>)', r'```\n\1\n```', part, flags=re.DOTALL)
                        part = re.sub(r'(<style.*?>.*?</style>)', r'```\n\1\n```', part, flags=re.DOTALL)
                        part = re.sub(r'(<script.*?>.*?</script>)', r'```\n\1\n```', part, flags=re.DOTALL)

                        await event.respond(part)
        else:
            await event.respond("Gagal mendapatkan inbox.")
    except Exception as e:
        await event.respond(f"Terjadi kesalahan: {str(e)}")










def google_dorking(query):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        search_url = f"https://www.google.com/search?q={query}"
        response = requests.get(search_url, headers=headers)
        if response.status_code != 200:
            return [f"Terjadi kesalahan: {response.status_code}"]

        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        for g in soup.find_all('div', class_='tF2Cxc'):
            anchors = g.find_all('a')
            if anchors:
                link = anchors[0]['href']
                title = g.find('h3').text
                results.append(f"{title}\n{link}")
        return results if results else ["Tidak ada hasil yang ditemukan."]
    except Exception as e:
        return [f"Terjadi kesalahan: {e}"]

@client.on(events.NewMessage(pattern='/google'))
async def handler(event):
    if str(event.sender_id) != owner_id:
        return  

    
    query = event.message.text.split('/google ', maxsplit=1)[1]
    if not query:
        await event.reply('Harap masukkan query untuk pencarian Google Dorking.')
        return

   
    response = await event.reply('Mohon tunggu, sedang mencari...')

   
    search_results = google_dorking(query)

    
    result_message = '\n\n'.join(search_results)

    
    await response.edit(result_message)









async def check_host(session, host, check_type='ping', max_nodes=3):
    url = f"{CHECK_HOST_API_URL}{check_type}?host={host}&max_nodes={max_nodes}"
    headers = {"Accept": "application/json"}
    
    async with session.get(url, headers=headers) as response:
        response_data = await response.json()
        if response_data.get('ok') == 1:
            request_id = response_data['request_id']
            permanent_link = response_data['permanent_link']
            return request_id, permanent_link
        else:
            return None, None

async def get_check_result(session, request_id):
    url = f"{CHECK_HOST_RESULT_URL}{request_id}"
    headers = {"Accept": "application/json"}
    
    async with session.get(url, headers=headers) as response:
        result_data = await response.json()
        return result_data



@client.on(events.NewMessage(pattern='/cekhost'))
async def handle_cekhost(event):
    message = event.message.text.strip()
    command, host = message.split(maxsplit=1)
    
    
    wait_message = await event.respond("Wait...")

    async with aiohttp.ClientSession() as session:
        
        request_id, permanent_link = await check_host(session, host)
        
        if not request_id:
            await wait_message.edit("Gagal melakukan pengecekan host.")
            return

       
        await asyncio.sleep(10)

       
        result_data = await get_check_result(session, request_id)
        
        if not result_data:
            await wait_message.edit("Gagal mendapatkan hasil pengecekan host.")
            return

        
        result_text = f"Hasil pengecekan host untuk {host}:\n\n{result_data}"
        await wait_message.edit(result_text)







@client.on(events.NewMessage(pattern='/ai'))
async def handle_ai_command(event):
    if str(event.sender_id) != owner_id:
        return

    text = event.text.split(' ', 1)[1] if len(event.text.split()) > 1 else None
    if text:
        ai_response = get_ai_response(text)
        if ai_response:
            await event.delete()
            
            # Format code blocks properly
            code_blocks = re.findall(r'```(python|html|css|js|javascript|php)(.*?)```', ai_response, re.DOTALL)
            if code_blocks:
                for lang, block in code_blocks:
                    formatted_block = f"```{lang}\n{block.strip()}\n```"
                    ai_response = ai_response.replace(f'```{lang}{block}```', formatted_block)
            await event.respond(ai_response)
        else:
            await event.respond("Gagal mendapatkan respons dari AI.")
    else:
        await event.respond("Tolong masukkan pertanyaan atau teks yang ingin Anda kirim ke AI.")

def get_ai_response(prompt):
    try:
        response = openai.Completion.create(
            engine="davinci-codex",  # or another engine suitable for your use case
            prompt=prompt,
            max_tokens=150,  # adjust as needed
            n=1,
            stop=None,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error getting AI response: {str(e)}")
        return None








def find_subdomains(domain):
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    response = requests.get(url)
    
    if response.status_code == 200:
        subdomains = set()
        try:
            results = response.json()
            for entry in results:
                common_name = entry['name_value']
                if domain in common_name:
                    subdomains.update(common_name.split('\n'))
        except ValueError:
            return None
        return list(subdomains)
    else:
        return None

@client.on(events.NewMessage(pattern='/subdomain'))
async def subdomain_finder(event):
    if str(event.sender_id) != owner_id:
        return
    
    message_text = event.message.text.split(' ')
    if len(message_text) < 2:
        await event.respond("Harap sertakan URL setelah perintah /subdomain.")
        return
    domain = message_text[1]

    wait_message = await event.respond("Wait...")

    subdomains = find_subdomains(domain)
    if subdomains is not None:
        response_text = f"Subdomain ditemukan untuk {domain}:\n"
        response_text += "\n".join(subdomains)
    else:
        response_text = f"Gagal menemukan subdomain untuk {domain}."

    await client.delete_messages(event.chat_id, wait_message)
    await event.respond(response_text)





# jangan pernah melihat fitur dari /start karna berbeda



@client.on(events.NewMessage(pattern='/cat'))
async def cat_file(event):
    if str(event.sender_id) != owner_id:
        return

    try:
        command = event.message.text.split(maxsplit=1)
        if len(command) < 2:
            await event.respond("Format perintah salah. Gunakan /cat <nama_file>")
            return
        
        file_path = command[1]
        if os.path.exists(file_path):
            file_extension = os.path.splitext(file_path)[1].lower()
            if file_extension == '.txt':
                
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    await event.respond(f'```\n{content}\n```', parse_mode='markdown')
            elif file_extension in ['.png', '.jpg', '.jpeg']:
                
                await client.send_file(event.chat_id, file_path, caption=f"done: {file_path}")
            else:
                await event.respond("Jenis file tidak didukung. Harap gunakan file TXT, PNG, atau JPG.")
        else:
            await event.respond(f"File {file_path} tidak ditemukan.")
    except Exception as e:
        await event.respond(f"Terjadi kesalahan: {str(e)}")








@client.on(events.NewMessage(pattern='/ls'))
async def list_directory(event):
    if str(event.sender_id) != owner_id:
        return
    
    try:
        command = event.message.text.split(maxsplit=1)
        directory = command[1] if len(command) > 1 else '.'
        result = subprocess.run(['ls', '-l', directory], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        await event.respond(f'```\n{result.stdout}\n{result.stderr}\n```', parse_mode='markdown')
    except Exception as e:
        await event.respond(f"Terjadi kesalahan: {str(e)}")



async def handle_run_command(event):
   
    message = event.message.text.strip()

    
    command, file_name = message.split(maxsplit=1)

    if command == '/run':
        
        result = os.system(f'python {file_name}')

        if result == 0:
            await event.respond("Skrip dijalankan dengan sukses!")
        else:
            await event.respond("Terjadi kesalahan saat menjalankan skrip.")


@client.on(events.NewMessage(pattern='/run'))
async def run_script(event):
    await handle_run_command(event)




async def check_domain(domain):
    url = f'https://dikaardnt.com/api/tool/domain?url={domain}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data
    return None


@client.on(events.NewMessage(pattern='/cekdomain'))
async def cekdomain(event):
    if str(event.sender_id) != owner_id:
        return
    try:
        
        domain = event.message.text.split(' ', 1)[1] if len(event.message.text.split()) > 1 else None
        if not domain:
            await event.respond("Harap berikan domain yang valid. Contoh penggunaan: /cekdomain example.com")
            return
        
        
        domain_data = await check_domain(domain)
        if not domain_data:
            await event.respond("Gagal memeriksa domain.")
            return
        
        
        result_message = "Hasil pemeriksaan domain:\n"
        for key, value in domain_data.items():
            result_message += f"{key}: {value}\n"

        
        parts = split_text(result_message, 4096)
        for part in parts:
            await event.respond(part)
    except Exception as e:
        await event.respond(f"Terjadi kesalahan: {str(e)}")


def split_text(text, length):
    return [text[i:i+length] for i in range(0, len(text), length)]







@client.on(events.NewMessage(pattern='/block'))
async def block_user(event):
    
    if str(event.sender_id) != owner_id:
        return
    
    try:
        if event.is_private:
            user_to_block = await event.get_reply_message()
            if user_to_block:
                user_id = user_to_block.sender_id
            else:
                await event.respond("Balas pesan pengguna yang ingin diblokir dengan perintah /block.")
                return

            await client(BlockRequest(id=user_id))
            await event.respond("Pengguna telah berhasil diblokir.")
        else:
            await event.respond("Perintah ini hanya dapat digunakan dalam obrolan pribadi.")
    except Exception as e:
        await event.respond(f"Terjadi kesalahan: {str(e)}")



@client.on(events.NewMessage(pattern='/nik'))
async def check_nik(event):
   
    if str(event.sender_id) != owner_id:
        return
    
    try:
        message_text = event.message.text.split(' ')
        if len(message_text) < 2:
            await event.respond("Harap sertakan nomor NIK setelah perintah /nik.")
            return

        nik = message_text[1]
        api_url = "https://skizo.tech/api/checknik"
        params = {"apikey": "xyydycoders", "nik": nik}
        response = requests.get(api_url, params=params)

        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 200:
                nik_info = data["message"]["data"]
                result = (
                    f"NIK: {nik_info['nik']}\n"
                    f"Jenis Kelamin: {nik_info['jk']}\n"
                    f"Tanggal Lahir: {nik_info['tgl']}\n"
                    f"Kecamatan: {nik_info['kec']}\n"
                    f"Kabupaten: {nik_info['kab']}\n"
                    f"Provinsi: {nik_info['prov']}\n"
                    f"Sumber: {nik_info['source']}\n"
                    f"Terakhir Diubah: {nik_info['modified_time']}"
                )
                await event.respond(result)
            else:
                await event.respond("NIK tidak ditemukan atau terjadi kesalahan.")
        else:
            await event.respond("Gagal memeriksa NIK.")
    except Exception as e:
        await event.respond(f"Terjadi kesalahan: {str(e)}")


        

async def get_ip_info(ip_address):
    try:
        url = f"https://dikaardnt.com/api/ip/{ip_address}"
        response = requests.get(url)
        if response.status_code == 200:
            ip_info = response.json()
            return ip_info
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None





@client.on(events.NewMessage(pattern=r'/groupinfo\s+(\S+)'))
async def group_info(event):
    if str(event.sender_id) != owner_id:
        return
    group_link = event.pattern_match.group(1)
    try:
        entity = await client.get_entity(group_link)
        if entity:
            info_text = f'Nama Grup: {entity.title}\n'
            info_text += f'Jumlah Member: {await get_total_members(entity)}\n'
            info_text += f'Jumlah member yang sedang online: {await get_online_members(entity)}\n'
            info_text += f'Jumlah admin grup: {await get_admin_count(entity)}\n'
            info_text += f'Jumlah pengguna telegram premium yang ada di grup: {await get_premium_users_count(entity)}\n'
            await event.respond(info_text)
        else:
            await event.respond('Grup tidak ditemukan.')
    except Exception as e:
        await event.respond(f'Error: {e}')

async def get_total_members(entity):
    try:
        participants = await client.get_participants(entity)
        return len(participants)
    except Exception as e:
        return "Error: " + str(e)

async def get_online_members(entity):
    try:
        participants = await client.get_participants(entity)
        online_count = sum(1 for user in participants if user.status == 'online')
        return online_count
    except Exception as e:
        return "Error: " + str(e)

async def get_admin_count(entity):
    try:
        admins = await client.get_participants(entity, filter=ChannelParticipantsAdmins)
        return len(admins)
    except Exception as e:
        return "Error: " + str(e)

async def get_premium_users_count(entity):
    try:
        participants = await client.get_participants(entity)
        premium_count = sum(1 for user in participants if user.premium)
        return premium_count
    except Exception as e:
        return "Error: " + str(e)

@client.on(events.NewMessage(pattern='/status'))
async def get_status(event):
    if str(event.sender_id) != owner_id:
        return
    global target_chat_id
    with open('zall.txt', 'r') as file:
        saved_chat_id = file.read()
    if saved_chat_id:
        response = f'ID Target: {saved_chat_id}\nRequest Date: {datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")}\nLast Chat Message: {await get_last_message(saved_chat_id)}'
    else:
        response = 'No target chat ID set.'
    await event.respond(response)

async def get_last_message(chat_id):
    try:
        async for message in client.iter_messages(int(chat_id), limit=1):
            return message.text if message.text else "Null"
    except Exception as e:
        return "Error: " + str(e)


@client.on(events.NewMessage(pattern='/restart'))
async def restart(event):
    if str(event.sender_id) != owner_id:
        return
    await event.respond('Restarting bot...')
    os.execv(__file__, [__file__])



@client.on(events.NewMessage(pattern='/top'))
async def top_groups(event):
    if str(event.sender_id) != owner_id:
        return
    await event.respond('Fetching top 20 groups...')
    global unread_messages
    unread_messages = {}
    async for dialog in client.iter_dialogs():
        if dialog.is_group:
            unread_count = dialog.unread_count
            if unread_count > 0:
                unread_messages[dialog.id] = unread_count
    sorted_groups = sorted(unread_messages.items(), key=lambda x: x[1], reverse=True)[:20]
    top_groups_text = 'Top 20 groups with most unread messages:\n'
    for group_id, count in sorted_groups:
        chat = await client.get_entity(group_id)
        top_groups_text += f'{chat.title}: {count} unread messages\n'
    await event.respond(top_groups_text)

with open('owner.txt', 'w') as file:
    file.write(owner_id)
    
@client.on(events.NewMessage(pattern='/ping'))
async def ping(event):
    if str(event.sender_id) != owner_id:
        return
    start_time = time.time()
    await event.respond('Wait!')
    end_time = time.time()
    response_time = end_time - start_time
    await event.respond(f'Bot response time: {response_time:.2f} seconds')
    
# DOWNLOADER MENU

@client.on(events.NewMessage(pattern=r'\?tiktok'))
async def download_tiktok(event):
    if str(event.sender_id) != owner_id:
        return

    message_text = event.message.text.split(' ')
    if len(message_text) < 2:
        await event.respond("Harap sertakan URL TikTok setelah perintah ?tiktok.")
        return
    
    url = message_text[1]
    wait_message = await event.respond("Wait...")

    api_url = "https://dikaardnt.com/api/download/tiktok"
    params = {"url": url}
    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        data = response.json()
        video_url = data["video"]["url"]["without_watermark"]
        video_file = requests.get(video_url)

        if video_file.status_code == 200:
            video_path = "tiktok_video.mp4"
            with open(video_path, "wb") as f:
                f.write(video_file.content)

            await client.delete_messages(event.chat_id, [wait_message])
            await event.respond(file=video_path)
            os.remove(video_path)
        else:
            await event.respond("Gagal mengunduh video TikTok.")
    else:
        await event.respond("Gagal mengunduh video TikTok.")





@client.on(events.NewMessage(pattern='/ig'))
async def download_instagram(event):
    try:
        if str(event.sender_id) != owner_id:
            return

        if event.is_reply:
            reply_message = await event.get_reply_message()
            if reply_message and reply_message.text:
                url = reply_message.text
            else:
                await event.respond("Pesan yang di-reply tidak berisi URL Instagram.")
                return
        else:
            message_text = event.message.text.split(' ')
            if len(message_text) < 2:
                await event.respond("Harap sertakan URL Instagram setelah perintah /ig.")
                return
            url = message_text[1]


        api_url = "https://dikaardnt.com/api/download/instagram"
        params = {"url": url}
        response = requests.get(api_url, params=params)

        if response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list):
                video_url = data[0]
                video_file = requests.get(video_url)

                if video_file.status_code == 200:
                    video_path = "instagram_video.mp4"
                    with open(video_path, "wb") as f:
                        f.write(video_file.content)
                    await event.respond(file=video_path)
                    os.remove(video_path)
                else:
                    await event.respond("Gagal mengunduh video Instagram.")
            else:
                await event.respond("Gagal mengunduh video Instagram.")
        else:
            await event.respond("Gagal mengunduh video Instagram.")
    except Exception as e:
        await event.respond(f"Terjadi kesalahan: {str(e)}")





async def search_and_download_soundcloud(query):
    url = f"https://api.maher-zubair.tech/search/soundcloud?q={query}"
    response = requests.get(url)
    if response.status_code == 200:
        result = response.json()["result"]["result"]
        if result:
            song = result[0]  
            download_url = f"https://api.maher-zubair.tech/download/soundcloud?url={song['url']}"
            download_response = requests.get(download_url)
            if download_response.status_code == 200:
                download_data = download_response.json()["result"]
                title = download_data["title"]
                mp3_link = download_data["link"]
                mp3_file = requests.get(mp3_link)
                if mp3_file.status_code == 200:
                    return title, mp3_file.content
    return None, None


@client.on(events.NewMessage(pattern='/play'))
async def play_soundcloud(event):
    if str(event.sender_id) != owner_id:
        return
    try:
        query = event.message.text.split(' ', 1)[1]
        title, mp3_content = await search_and_download_soundcloud(query)
        if title and mp3_content:
            file_name = f"{title}.mp3"
            with open(file_name, "wb") as f:
                f.write(mp3_content)
            await event.respond(f"Sedang memainkan: {title}")
            await event.respond(file=file_name) 
            os.remove(file_name) 
        else:
            await event.respond("Tidak ada hasil lagu yang ditemukan.")
    except Exception as e:
        await event.respond(f"Terjadi kesalahan: {str(e)}")


@client.on(events.NewMessage(pattern='/speedtest'))
async def speed_test(event):
    if str(event.sender_id) != owner_id:
        return
    await event.respond('Running speed test...')
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1_000_000 
    upload_speed = st.upload() / 1_000_000  
    ping = st.results.ping
    server_info = st.results.server
    client_info = st.results.client
    await event.respond(f'Download speed: {download_speed:.2f} Mbps\nUpload speed: {upload_speed:.2f} Mbps\nPing: {ping} ms')
    await event.respond(f'Server Info:\n{server_info}')
    await event.respond(f'Client Info:\n{client_info}')

async def get_id(event):
    user_id = event.sender_id
    await event.respond(f"Your ID is: {user_id}")

@client.on(events.NewMessage(pattern='/getid'))
async def get_id_wrapper(event):
    await get_id(event)




async def get_simi_response(text):
    api_key = "xyydycoders"
    level = 10
    url = f"https://skizo.tech/api/simi?apikey={api_key}&text={text}&level={level}"
    response = requests.get(url)
    if response.status_code == 200:
        result = response.json()["result"]
        return result
    return None


@client.on(events.NewMessage(pattern='/startsimi'))
async def startsimi(event):
    global target_chat_ids
    if target_chat_ids:
        await event.respond('Simi already started.')
    else:
        await event.respond('Please set target chat IDs using /setid command.')


@client.on(events.NewMessage(pattern='/stopsimi'))
async def stopsimi(event):
    global target_chat_ids
    sender_chat_id = event.chat_id
    for label, chat_ids in target_chat_ids.items():
        if sender_chat_id in chat_ids:
            target_chat_ids[label] = []
            await event.respond(f'Simi for label {label} stopped.')
            break
    else:
        await event.respond('You are not authorized to stop simi.')


@client.on(events.NewMessage())
async def simi_chat(event):
    global target_chat_ids
    for label, chat_ids in target_chat_ids.items():
        if event.chat_id in chat_ids:
            text = event.message.text
            response = await get_simi_response(text)
            if response:
                
                await event.reply(response)
            else:
                await event.respond("Failed to get response from simi API.")


@client.on(events.NewMessage(pattern=r'/setid\s+(\d+)\s+(\w+)'))
async def set_id(event):
    global target_chat_ids
    chat_id = int(event.pattern_match.group(1))
    label = event.pattern_match.group(2)
    if chat_id:
        if label in target_chat_ids:
            target_chat_ids[label].append(chat_id)
        else:
            target_chat_ids[label] = [chat_id]
        with open('simi.json', 'w') as file:
            json.dump(target_chat_ids, file)
        await event.respond(f'Target chat ID {chat_id} with label {label} set successfully.')
    else:
        await event.respond('Please provide a valid chat ID.')


target_chat_ids = {}
try:
    with open('simi.json', 'r') as file:
        target_chat_ids = json.load(file)
except FileNotFoundError:
    pass


    
@client.on(events.NewMessage(pattern='/kick'))
async def kick_user(event):
   
    if str(event.sender_id) != owner_id:
       
        return

   
    if event.is_group:
        
        if event.reply_to_msg_id is not None:
           
            reply_message = await event.get_reply_message()
            
            user_id = reply_message.sender_id
            
            await event.client.kick_participant(event.chat_id, user_id)
            await event.respond('User kicked successfully.')
        else:
            await event.respond('Reply to a message to tag a user to kick.')
    else:
        await event.respond('This command can only be used in groups.')


@client.on(events.NewMessage(pattern='/ssweb'))
async def screenshot_website(event):
    if str(event.sender_id) != owner_id:
        return

    try:
        if event.is_reply:
            reply_message = await event.get_reply_message()
            if reply_message and reply_message.text:
                url = reply_message.text
            else:
                await event.respond("Pesan yang di-reply tidak berisi URL.")
                return
        else:
            message_text = event.message.text.split(' ')
            if len(message_text) < 2:
                await event.respond("Harap sertakan URL setelah perintah /ssweb.")
                return
            url = message_text[1]

        wait_message = await event.respond("Wait...")

        api_url = "https://api.apiflash.com/v1/urltoimage"
        params = {
            "access_key": "e15f7f20a03c42d8ac93221a3bdd66d7",
            "url": url,
            "format": "png",
            "fresh": "true",
            "full_page": "true",
            "quality": "80",
            "scroll_page": "true",
            "response_type": "json",
            "no_cookie_banners": "true",
            "no_ads": "true",
            "no_tracking": "true",
            "wait_until": "network_idle"
        }
        response = requests.get(api_url, params=params)

        if response.status_code == 200:
            data = response.json()
            screenshot_url = data.get("url")
            if screenshot_url:
                screenshot_file = requests.get(screenshot_url)
                if screenshot_file.status_code == 200:
                    screenshot_path = "screenshot.png"
                    with open(screenshot_path, "wb") as f:
                        f.write(screenshot_file.content)
                    await client.delete_messages(event.chat_id, wait_message)
                    await event.respond(file=screenshot_path)
                    os.remove(screenshot_path)
                else:
                    await event.respond("Gagal mengunduh screenshot.")
            else:
                await event.respond("Gagal mengunduh screenshot.")
        else:
            await event.respond("Gagal mengunduh screenshot.")
    except Exception as e:
        await event.respond(f"Terjadi kesalahan: {str(e)}")




@client.on(events.NewMessage(pattern='/tourl'))
async def img_to_url(event):
    if str(event.sender_id) != owner_id:
        return

    try:
        if event.is_reply:
            reply_message = await event.get_reply_message()
            if reply_message and reply_message.media:
                wait_message = await event.respond("Wait...")
                file_path = await reply_message.download_media()
                with open(file_path, 'rb') as file:
                    response = requests.post('https://telegra.ph/upload', files={'file': ('file', file, 'image/jpeg')})
                os.remove(file_path)
                if response.status_code == 200:
                    file_info = response.json()[0]
                    url = f"https://telegra.ph{file_info['src']}"
                    await client.delete_messages(event.chat_id, wait_message)
                    await event.respond(f"URL: {url}")
                else:
                    await event.respond("Gagal mengunggah gambar ke Telegra.ph.")
            else:
                await event.respond("Pesan yang di-reply tidak berisi gambar.")
        else:
            await event.respond("Harap reply ke pesan yang berisi gambar dengan perintah /tourl.")
    except Exception as e:
        await event.respond(f"Terjadi kesalahan: {str(e)}")





@client.on(events.NewMessage(pattern='/hd'))
async def enhance_image(event):
    if str(event.sender_id) != owner_id:
        return

    try:
        if event.is_reply:
            reply_message = await event.get_reply_message()
            if reply_message and reply_message.media:
                wait_message = await event.respond("Wait...")
                file_path = await reply_message.download_media()
                with open(file_path, 'rb') as file:
                    response = requests.post('https://telegra.ph/upload', files={'file': ('file', file, 'image/jpeg')})
                if response.status_code == 200:
                    file_info = response.json()[0]
                    telegra_url = f"https://telegra.ph{file_info['src']}"

                    api_url = "https://api.betabotz.eu.org/api/tools/remini"
                    params = {"apikey": "KENZ-MD", "url": telegra_url}
                    remini_response = requests.get(api_url, params=params)

                    if remini_response.status_code == 200:
                        data = remini_response.json()
                        if data.get("status"):
                            enhanced_image_url = data["url"]
                            enhanced_image = requests.get(enhanced_image_url)
                            if enhanced_image.status_code == 200:
                                enhanced_image_path = "enhanced_image.jpg"
                                with open(enhanced_image_path, "wb") as f:
                                    f.write(enhanced_image.content)
                                await client.delete_messages(event.chat_id, [wait_message])
                                await event.respond(file=enhanced_image_path)
                                os.remove(enhanced_image_path)
                            else:
                                await event.respond("Gagal mengunduh gambar hasil.")
                        else:
                            await event.respond("Gagal memproses gambar dengan Remini API.")
                    else:
                        await event.respond("Gagal memproses gambar dengan Remini API.")
                else:
                    await event.respond("Gagal mengunggah gambar ke Telegra.ph.")
                os.remove(file_path)
            else:
                await event.respond("Pesan yang di-reply tidak berisi gambar.")
        else:
            await event.respond("Harap reply ke pesan yang berisi gambar dengan perintah /hd.")
    except Exception as e:
        await event.respond(f"Terjadi kesalahan: {str(e)}")





@client.on(events.NewMessage(pattern='/cekid'))
async def cekid(event):
    if str(event.sender_id) != owner_id:
        
        return

    try:
        command_text = event.message.message.split()
        
        if len(command_text) == 2:
            username = command_text[1]
            if username.startswith('@'):
                username = username[1:]  
            
            try:
                user = await client.get_entity(username)
                user_id = user.id
                await event.respond(f"ID untuk {username}: {user_id}")
            except Exception as e:
                await event.respond(f"Gagal mendapatkan ID untuk {username}: {str(e)}")
        elif event.is_private:
            user_id = event.sender_id
            await event.respond(f"ID Anda: {user_id}")
        else:
            await event.respond("Perintah ini hanya dapat digunakan dalam obrolan pribadi atau dengan menyebutkan username.")
    except Exception as e:
        await event.respond(f"Terjadi kesalahan: {str(e)}")

 
@client.on(events.NewMessage(pattern='/fake_typing'))
async def fake_typing(event):
    if str(event.sender_id) != owner_id:
        return
    global target_chat_id
    if target_chat_id:
        chat_id = target_chat_id
        await event.respond('Fake typing started.')
        await start_fake_typing(chat_id)
    else:
        await event.respond('Please set a target chat ID using /setid command.')

async def start_fake_typing(chat_id):
    global fake_typing_task
    while True:
        async with client.action(chat_id, 'typing'):
            await asyncio.sleep(5)

@client.on(events.NewMessage(pattern=r'/id\s+(\d+)'))
async def id(event):
    if str(event.sender_id) != owner_id:
        return
    global target_chat_id
    chat_id = event.pattern_match.group(1)
    if chat_id:
        target_chat_id = int(chat_id)
        with open('dy.txt', 'w') as file:
            file.write(str(target_chat_id))
        await event.respond('Target chat ID set successfully.')
    else:
        await event.respond('Please provide a valid chat ID.')


def translate_text(text, target_language):
    translated = translator.translate(text, dest=target_language)
    return translated.text
    
@client.on(events.NewMessage(pattern=r'/tr\s+(\w+)(?:\s+|$)(.*)'))
async def translate(event):

    if str(event.sender_id) != owner_id:
        return

    lang = event.pattern_match.group(1)
    text = event.pattern_match.group(2)

    if not text and event.is_reply:
        reply_message = await event.get_reply_message()
        text = reply_message.text

    if text:
        try:
            translated = translate_text(text, lang)
            await event.respond(translated)
        except Exception as e:
            await event.respond(f"Error during translation: {e}")
    else:
        await event.respond("Please provide the text to translate or reply to a message.")

    

async def get_ip_info(ip_address):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        data = response.json()
        if data['status'] == 'success':
            return data
        else:
            return None
    except Exception as e:
        print(f"Error fetching IP info: {e}")
        return None

@client.on(events.NewMessage(pattern='/cekip'))
async def check_ip(event):
    # Memastikan hanya pemilik bot yang dapat menggunakan perintah ini
    if str(event.sender_id) != owner_id:
        return

    text = event.message.text

    if len(text.split()) != 2:
        await event.respond("Format salah. Gunakan /cekip <IP_ADDRESS>")
        return
    
    _, ip_address = text.split(' ', 1)
    
    ip_info = await get_ip_info(ip_address)
    if ip_info:
        message = f"Informasi IP untuk {ip_address}:\n"
        message += f"Negara: {ip_info['country']}\n"
        message += f"Kode Negara: {ip_info['countryCode']}\n"
        message += f"Wilayah: {ip_info['regionName']}\n"
        message += f"Kota: {ip_info['city']}\n"
        message += f"Waktu: {ip_info['datetime']}\n"
        message += f"Koordinat: {ip_info['lat']}, {ip_info['lon']}\n"
        message += f"Zona Waktu: {ip_info['timezone']}\n"
        message += f"ISP: {ip_info['isp']}\n"
        message += f"AS: {ip_info['as']}\n"
        message += f"Alamat: {ip_info['query']}"
        
        sent_message = await event.respond(message)
        
        await asyncio.sleep(35)
        
        await sent_message.delete()
    else:
        await event.respond("Tidak dapat menemukan informasi untuk IP tersebut.")

async def main():
    await client.start()
    await client.run_until_disconnected()

client.loop.run_until_complete(main())





#Jangan di hpus itu agar fake online



async def keep_online_and_auto_read():
    while True:
        try:
           
            await client(functions.account.UpdateStatusRequest(offline=False))
            await client(functions.messages.SetTypingRequest(
                peer='me',
                action=types.SendMessageTypingAction()
            ))

          
            async for dialog in client.iter_dialogs():
                if dialog.is_user:
                    async for message in client.iter_messages(dialog.id, unread=True):
                        await client(functions.messages.ReadHistory(peer=message.peer_id, max_id=message.id))

        except Exception as e:
            print(f"Error: {e}")
        await asyncio.sleep(25)

async def main():
    await client.start()
    await asyncio.gather(
        keep_online_and_auto_read(),
        client.run_until_disconnected()
    )

asyncio.run(main())
