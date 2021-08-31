import csv
import json
import os
import youtube_transcript_api

# open last dataset downloaded and extract id column
bold_dfs = os.listdir('data/csv-files')
last_bold = bold_dfs[len(bold_dfs) - 1]

# get video ids from last csv file
csv_path = "data/csv-files/{}".format(last_bold)


with open(csv_path) as f:
    reader_obj = csv.reader(f)
    bold_data = list(reader_obj)

id_index = bold_data[0].index('id')
all_id = [row[id_index] for row in bold_data[1:len(bold_data)]]

# find videos not downloaded yet
with open('data/transcripts/transcripts.json', 'r') as f:
    old_transcripts = json.load(f)

try:
    old_id = list(old_transcripts.keys())
except AttributeError:


new_id = list(set(all_id) - set(old_id))

print(old_transcripts)

# get new video transcripts
new_transcripts = dict()  # [[{},{},{}], [{},{},{}], [{},{},{}]]
for id in new_id:
    try:
        txt = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(
            id, languages=['it', 'en', 'es']
        )

    except youtube_transcript_api._errors.TranscriptsDisabled as e1:
        print('Subtitles are disabled for this video: {} {}'.format(id, e1))

    except youtube_transcript_api._errors.NoTranscriptFound as e2:
        print('Subtitles not found for this video: {} {}'.format(id, e2))

    except KeyError as e3:
        print('Cannot parse JSON: {} {}'.format(id, e3))

    new_transcripts[id] = ''
    for dct in txt:
        new_transcripts[id] = new_transcripts[id] + dct.get('text') + ' '

# add new key values to old transcripts
updated_transcrips = old_transcripts.update(new_transcripts)

# save transcripts to disk
json_string = json.dumps(updated_transcrips, ensure_ascii=False)
with open('data/transcripts/transcripts.json', 'w') as f:
    f.write(json_string)
