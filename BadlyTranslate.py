import os
import random
import re
from html import escape, unescape
from google.cloud import translate_v2 as translate

# Set Google Cloud credentials file path and initialize Google Translate API client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "YOUR KEYS HERE"
translate_client = translate.Client()

# Function to translate text to a specific language
def translate_text(text, target_language):
	return translate_client.translate(text, target_language=target_language)["translatedText"]

# Function to translate text through multiple random languages and back to English
def translate_multilanguage(text, iterations=15):
	# List of language codes to translate through
	languages = ['am', 'mg', 'my', 'ne', 'si', 'su', 'tg', 'uz', 'yi', 'zu', 'haw', 'xh', 'fil', 'ceb', 'hmn']
	for _ in range(iterations):
		text = translate_text(text, random.choice(languages))
	# Translate the text back to English
	return translate_text(text, 'en')

# Function to translate text files in a folder
def translate_files(input_folder, output_folder, batch_size=10):
	# Iterate through the folder structure
	for root, dirs, files in os.walk(input_folder):
		# Create corresponding output directories if they don't exist
		for dirname in dirs:
			os.makedirs(os.path.join(output_folder, dirname), exist_ok=True)
		# Iterate through each file in the folder
		for filename in files:
			# Check if the file is a text file
			if filename.endswith(".txt"):
				# Define input and output file paths
				input_file_path = os.path.join(root, filename)
				output_file_path = os.path.join(output_folder, input_file_path[len(input_folder)+1:])
				# Read lines from the input file
				with open(input_file_path, "r", encoding="utf-8") as input_file:
					lines = input_file.readlines()
				# Open the output file for writing
				with open(output_file_path, "w", encoding="utf-8") as output_file:
					# Iterate through lines in batches
					for i in range(0, len(lines), batch_size):
						# Get a batch of lines
						batch_lines = lines[i:i+batch_size]
						translated_lines = []
						# Iterate through lines in the batch
						for line in batch_lines:
							# Split line into segments based on quotation marks
							segments = re.split(r'(".*?")', line)
							translated_segments = ['"' + translate_multilanguage(segment.strip('"')).replace('"', r'\"') + '"' if segment.startswith('"') and segment.endswith('"') else segment for segment in segments]
							translated_line = ''.join(translated_segments)
							translated_lines.append(translated_line)
						# Write translated lines to the output file
						output_file.writelines(translated_lines)

# Define input and output folder paths
input_folder = "YOUR INPUT FOLDER HERE"
output_folder = "YOUR OUTPUT FOLDER HERE"
# Translate files from the input folder to the output folder
translate_files(input_folder, output_folder)