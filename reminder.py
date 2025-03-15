import os
import re
import requests
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# AI Model Configuration
MISTRAL_API_KEY = '********************************'
MODEL_URL = 'https://api.mistral.ai/v1/chat/completions'
HEADERS = {
    'Authorization': f'Bearer {MISTRAL_API_KEY}',
    'Content-Type': 'application/json',
}

def extract_reminders(file_path, person_name):
    reminders = []
    
    # Define keywords to look for
    reminder_keywords = [
        "remind", "remember", "don't forget", "make sure to", "note to", "set a reminder for"
    ]
    reminder_pattern = re.compile(r'|'.join(reminder_keywords), re.IGNORECASE)
    
    # Read the main.txt file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Split content into individual lines or messages
    messages = content.split("<end_of_turn>")
    
    for message in messages:
        # Check for reminder keywords
        if reminder_pattern.search(message):
            # Process message with NLP
            doc = nlp(message)
            
            # Extract dates/times using named entities
            time_info = []
            for ent in doc.ents:
                if ent.label_ in ("DATE", "TIME"):
                    time_info.append(ent.text)
            
            # Save the reminder with person information
            reminders.append({
                "person": person_name,
                "text": message.strip(),
                "time": time_info
            })
    
    return reminders

def send_to_ai(reminders):
    # Format the reminders into a structured prompt
    formatted_messages = []
    for reminder in reminders:
        formatted_messages.append(
            f'"{reminder["text"]} (From: {reminder["person"]})"'
        )
        
    print(formatted_messages)
    prompt = "Here are the text messages I received from whatsapp. Please identify if there are any reminders and tell me who gave that:\n" + "\n".join(formatted_messages)

    print (prompt)
    # Send the prompt to the AI model
    data = {
        "model": "mistral-large-2411",
        "messages": [{"role": "user", "content": prompt}],
        "temperature" : 0.7
    }
    
   # print("\n--- Sending Prompt to AI ---")
   # print(prompt)
    
    response = requests.post(MODEL_URL, json=data, headers=HEADERS)
    
    if response.status_code == 200:
        try:
            result = response.json()
            generated_text = result["choices"][0]["message"]["content"]
            print("\n--- AI Response ---")
            print(generated_text)
            return generated_text
        except (KeyError, IndexError):
            print("Unexpected response format from the AI model.")
            print(response.json())
            return None
    else:
        print(f"AI request failed with status code {response.status_code}: {response.text}")
        return None

# Main Function
if __name__ == "__main__":
    # Directory containing main.txt files
    people_folder = "People"
    
    all_reminders = []
    
    # Iterate over all people folders
    for person_name in os.listdir(people_folder):
        main_file_path = os.path.join(people_folder, person_name, "basicR.txt")
        if os.path.exists(main_file_path):
         #   print(f"\nProcessing reminders for: {person_name}")
            reminders = extract_reminders(main_file_path, person_name)
            all_reminders.extend(reminders)
    
    # Send all reminders to AI for analysis
    if all_reminders:
        send_to_ai(all_reminders)
        ai_response = send_to_ai(all_reminders)
        with open("reminder.txt", "a", encoding="utf-8") as reminder_file:
           reminder_file.write(ai_response + "\n")
        
    else:
        print("No reminders detected.")
    
    
    
    # Clear all text from each basicR.txt file
    for person_name in os.listdir(people_folder):
        basicR_path = os.path.join(people_folder, person_name, "basicR.txt")
        if os.path.exists(basicR_path):
            with open(basicR_path, "w", encoding="utf-8") as file:
                file.truncate(0)  # Clear file contents

            
