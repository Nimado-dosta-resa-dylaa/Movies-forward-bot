from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from collections import defaultdict
import asyncio

# Aapka API ID aur API Hash
api_id = '25105744'
api_hash = '0ca4154111e7b0f99e9929710faa3f25'

# Aapka string session yahan dalein
string_session = "1BJWap1sBu6omS2_iVngaPxEQRgCyWmukbK8mQ-WTSSSjbJPX31mPLEI1XZjX7n7ceVZfD7WknjhrXSs7UWSCpx2vUkzvWb9N-QJ_aeCjsLFDfeF0xFMzeItpS64sbAJpLVtsxS3z_115ky-ag_HqnnxMcCqqXGm-LilTu6PG4s1NOF39VeXxoK5nGQdass_UqSOgsGRlXvubEuvI89QyNTm6Euu-VmrWXspWlsR6fBY0LTgW5OuXG_5avqZTuY79qRaUaAT2s7deOunpF1yuU0We08m5CMFt0QEYZMW-qA7Zc2B9dzxZ5kPkDufJzZQRpPOMr3UwJglsa87xybaq8Pm0KzJzi9U="
channel_username = -1001972766787
admin_id = '@PrivateMoviesOwner' # Telegram Admin ID
batch_size = 100  # Batch size
delay_between_batches = 3  # Delay between batches in seconds

# String session se client ko initialize karein
client = TelegramClient(StringSession(string_session), api_id, api_hash)
    
async def delete_duplicate_videos():
    video_messages = defaultdict(list)

    async for message in client.iter_messages(channel_username):
        if message.video:
            file_id = message.video.id
            video_messages[file_id].append(message)
    
    for file_id, msgs in video_messages.items():
        if len(msgs) > 1:
            # Process in batches
            for i in range(1, len(msgs), batch_size):
                batch = msgs[i:i + batch_size]
                for msg in batch:
                    await client.delete_messages(channel_username, msg.id)
                    
                    # Log ko admin ID par bhejein
                    log_message = f"Deleted duplicate video: File ID: {file_id}, Message ID: {msg.id}"
                    await client.send_message(admin_id, log_message)
                
                # Wait between batches
                await asyncio.sleep(delay_between_batches)

with client:
    client.loop.run_until_complete(delete_duplicate_videos())
