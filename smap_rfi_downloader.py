import requests
import subprocess
import os
import datetime

download_dir = 'downloads'
os.makedirs(download_dir, exist_ok=True)  # Ensure the download directory exists

current_year = datetime.datetime.now().year
current_month = datetime.datetime.now().month

start_year = 2015
start_month = 4

years = range(start_year, current_year + 1)

for year in years:
    for month in range(1, 13):
        if year == start_year and month < start_month:
            continue  # Skip months before April 2015

        if year == current_year and month > current_month:
            break  # Skip months beyond the current month in the current year

        month_str = f'{month:02d}'
        url = f'https://salinity.oceansciences.org/images/maps/SMAP_RFI_percent_{year}_{month_str}.png'
        filename = f'{download_dir}/SMAP_RFI_percent_{year}_{month_str}.png'

        if os.path.exists(filename):
            print(f'Skipping download, file already exists: {filename}')
            continue

        response = requests.get(url)
        try:
            response.raise_for_status()
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f'Downloaded {url} to {filename}')
        except requests.exceptions.HTTPError as e:
            print(f'Error downloading {url}: {e}')
            continue

ffmpeg_command = [
    'ffmpeg',
    '-framerate', '6',
    '-pattern_type', 'glob',
    '-i', f'{download_dir}/*.png',
    '-c:v', 'libvpx',
    '-b:v', '1M',
    '-crf', '10',
    '-vf', 'scale=1920:-1',
    '-y', 'output/output.webm'
]

subprocess.run(ffmpeg_command, check=True)
