from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests
import os
import re
import threading

# -------------------------
# Global Variables
# -------------------------
current_chat = None       # Currently active allowed chat name
last_message_time = None  # Timestamp of the last message processed in the active chat
fetched_messages = set()  # Set to store processed messages

# -------------------------
# API Configuration
# -------------------------
MISTRAL_API_KEY = '********************************'
# You can choose the appropriate MODEL_URL; here we use the Meta Llama model endpoint.
# MODEL_URL = 'https://api.deepinfra.com/v1/inference/meta-llama/Llama-3.3-70B-Instruct-Turbo'
MODEL_URL = 'https://api.mistral.ai/v1/chat/completions'
HEADERS = {
    'Authorization': f'Bearer {MISTRAL_API_KEY}',
    'Content-Type': 'application/json',
}

# -------------------------
# Utility Functions
# -------------------------


def append_to_basicR(person_name, user_message, ai_response):
    """
    Append the conversation turn to the basicR file.
    """
    person_folder = os.path.join("People", person_name)
    basicR_path = os.path.join(person_folder, "basicR.txt")

    # Ensure directory exists
    if not os.path.exists(person_folder):
        os.makedirs(person_folder)

    # Append conversation turn
    conversation_entry = (f"<start_of_turn>user\n{user_message}\n<end_of_turn>\n"
                          f"<start_of_turn>model\n{ai_response}\n<end_of_turn>\n")

    with open(basicR_path, 'a', encoding='utf-8') as file:
        file.write(conversation_entry)



def update_submain_and_temp_reference(person_name):
    """
    Update the submain.txt and temp_reference.txt files with conversation context.
    Reads the entire conversation from main.txt, then extracts the beginning and
    end portions to create a summary for context.
    """
    main_file_path = f"People/{person_name}/main.txt"
    submain_file_path = f"People/{person_name}/submain.txt"
    temp_reference_path = f"People/{person_name}/temp_reference.txt"
    
    try:
        with open(main_file_path, 'r', encoding='utf-8') as main_file:
            main_content = main_file.read()
    except FileNotFoundError:
        main_content = ""
    
    # Extract first and last 1000 characters (or tokens)
    beginning_part = main_content[:1000]
    last_tokens = main_content[-1000:]
    submain_content = f"{beginning_part}{last_tokens}"
    
    with open(submain_file_path, "w", encoding='utf-8') as submain_file:
        submain_file.write(submain_content)
    
    with open(temp_reference_path, "w", encoding='utf-8') as temp_reference_file:
        temp_reference_file.write(submain_content)
    
    print(f"[INFO] Updated {submain_file_path} and {temp_reference_path} with context.")

def remove_emojis(text):
    """
    Remove emojis from a given text using regex.
    """
    emoji_pattern = re.compile(
        '['
        '\U0001F600-\U0001F64F'  # Emoticons
        '\U0001F300-\U0001F5FF'  # Misc Symbols and Pictographs
        '\U0001F680-\U0001F6FF'  # Transport and Map Symbols
        '\U0001F700-\U0001F77F'  # Alchemical Symbols
        '\U0001F780-\U0001F7FF'  # Geometric Shapes Extended
        '\U0001F800-\U0001F8FF'  # Supplemental Arrows-C
        '\U0001F900-\U0001F9FF'  # Supplemental Symbols and Pictographs
        '\U0001FA00-\U0001FA6F'  # Chess Symbols
        '\U0001FA70-\U0001FAFF'  # Symbols and Pictographs Extended-A
        '\U00002702-\U000027B0'  # Dingbats
        '\U000024C2-\U0001F251'  # Enclosed Characters
        ']+',
        flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)

def get_last_message_time():
    """
    Retrieve the timestamp of the last message in the current chat.
    """
    time_xpath = "//span[@class='x1rg5ohu x16dsc37']"
    message_times = driver.find_elements(By.XPATH, time_xpath)
    if message_times:
        return message_times[-1].text
    return None

def fetch_latest_messages():
    """
    Fetch the last 5 messages from the active chat.
    Returns a list of tuples (sender, message_text).
    """
    print("[INFO] Fetching the latest messages...")
    messages = driver.find_elements(By.XPATH, "//div[@role='row']")
    messages_data = []
    
    for i, message in enumerate(messages[-1:], 1):
        try:
            sender = message.find_element(By.XPATH, ".//div[contains(@class, '_amk6')]/span").get_attribute("aria-label")
            message_text = message.find_element(By.XPATH, ".//div[contains(@class, '_akbu')]").text
            messages_data.append((sender, message_text))
        except Exception as e:
            print(f"[WARN] Error fetching a message: {e}")
    
    return messages_data

def send_message_to_whatsapp(message):
    """
    Send the provided message to the active WhatsApp chat.
    """
    message_input_xpath = "//div[@role='textbox' and contains(@aria-placeholder, 'Type a message')]"
    try:
        message_input = driver.find_element(By.XPATH, message_input_xpath)
        message_input.send_keys(message)
        message_input.send_keys(Keys.ENTER)
        print(f"[INFO] Message sent: {message}")
    except Exception as e:
        print(f"[ERROR] Failed to send message: {e}")

def get_ai_response(user_message):
    """
    Call the AI model API with the conversation history and the new user message,
    and return the model's response.
    """
    global current_chat
    person_name = current_chat
    # File paths for conversation history
    main_file_path = f"People/{person_name}/main.txt"
    submain_file_path = f"People/{person_name}/submain.txt"
    temp_reference_path = f"People/{person_name}/temp_reference.txt"
    
    update_submain_and_temp_reference(person_name)
    
    conversation_history = "<start_of_turn>user\n <start_of_turn>model\n"
    try:
        with open(submain_file_path, "r", encoding='utf-8') as sub_main_file:
            conversation_history += sub_main_file.read()
    except FileNotFoundError:
        pass  # No history yet
    
    conversation_history += f"<start_of_turn>user\n{user_message}<end_of_turn>\n<start_of_turn>model\n"
    
    content = "You are an AI that talks to people instead of me. You talk as a natural human being. You reply in medium length. You about Robotic replies and you also posses knowledge of using slangs just like humans do."
    
    data = {
        "model": "mistral-large-2411",
        "messages": [
        {"role": "system", "content": content},
        {"role": "user", "content": conversation_history}],
        "temperature" : 0.8
    }
    
    print(f"[INFO] Sending message to AI model: {user_message}")
    try:
        response = requests.post(MODEL_URL, json=data, headers=HEADERS)
        if response.status_code == 200:
            res = response.json()
            model_response = res['choices'][0]['message']["content"]
            model_response = model_response.replace("\n", " ")
            model_response = remove_emojis(model_response)
            print(f"[INFO] AI Model Response: {model_response}")
            return model_response
        else:
            print(f"[ERROR] Request failed with status code {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"[ERROR] Exception when calling AI API: {e}")
        return None

def append_to_submain(person_name, user_message, ai_response):
    """
    Append the current conversation turn to the submain.txt file.
    """
    person_folder = os.path.join("People", person_name)
    if not os.path.exists(person_folder):
        os.makedirs(person_folder)
    person_file_path = os.path.join(person_folder, "submain.txt")
    
    conversation_entry = (f"<start_of_turn>user\n{user_message}\n<end_of_turn>\n"
                          f"<start_of_turn>model\n{ai_response}\n<end_of_turn>\n")
    
    with open(person_file_path, 'a', encoding='utf-8') as file:
        file.write(conversation_entry)

def append_to_conversation_history(person_name, user_message, ai_response):
    """
    Append the conversation turn to the main.txt file for long-term history.
    """
    person_folder = os.path.join("People", person_name)
    if not os.path.exists(person_folder):
        os.makedirs(person_folder)
    person_file_path = os.path.join(person_folder, "main.txt")
    
    conversation_entry = (f"<start_of_turn>user\n{user_message}\n<end_of_turn>\n"
                          f"<start_of_turn>model\n{ai_response}\n<end_of_turn>\n")
    
    with open(person_file_path, 'a', encoding='utf-8') as file:
        file.write(conversation_entry)

# -------------------------
# Chat Monitoring & Processing Loops
# -------------------------
def monitor_top_chat():
    """
    Continuously monitor the WhatsApp chat list to detect the top chat.
    If a new top chat is detected and its name exists in the People folder,
    switch to that chat.
    """
    global current_chat, last_message_time, fetched_messages
    while True:
        try:
            # Locate the top chat using the translateY(0px) style attribute
            top_chat_xpath = ("//div[contains(@class, 'x10l6tqk') and contains(@class, 'xh8yej3') "
                              "and contains(@class, 'x1g42fcv') and contains(@style, 'translateY(0px)')]")
            top_chat_element = driver.find_element(By.XPATH, top_chat_xpath)
            # Extract the chat name from the child span element
            chat_name_element = top_chat_element.find_element(By.XPATH, ".//span[contains(@class, 'x1iyjqo2')]")
            chat_name = chat_name_element.text.strip()
            
            # If a new chat appears at the top, check if it is allowed
            if chat_name != current_chat:
                if os.path.exists(os.path.join("People", chat_name)):
                    print(f"[INFO] Switching to allowed chat: {chat_name}")
                    top_chat_element.click()
                    current_chat = chat_name
                    last_message_time = get_last_message_time()
                    fetched_messages = set()
                else:
                    print(f"[INFO] Chat '{chat_name}' not in allowed profiles. Skipping response.")
            time.sleep(2)  # Polling interval can be adjusted
        except Exception as e:
            print(f"[ERROR] Exception in monitor_top_chat: {e}")
            time.sleep(2)

def process_messages():
    """
    Continuously fetch and process new messages from the active chat.
    Only processes messages if the current chat is allowed (exists in People directory).
    """
    global current_chat, last_message_time, fetched_messages
    while True:
        try:
            # Only process if we have an allowed active chat
            if current_chat and os.path.exists(os.path.join("People", current_chat)):
                current_message_time = get_last_message_time()
                if current_message_time and (last_message_time is None or current_message_time >= last_message_time):
                    latest_messages = fetch_latest_messages()
                    new_messages = []
                    for sender, message_text in latest_messages:
                        if sender and (sender, message_text) not in fetched_messages:
                            new_messages.append((sender, message_text))
                            fetched_messages.add((sender, message_text))
                    
                    if new_messages:
                        print(f"[INFO] New messages in chat '{current_chat}':")
                        for sender, user_message in new_messages:
                            print(f"  From {sender}: {user_message}")
                            # Optional: Check if the sender is the contact (e.g., if sender includes current_chat)
                            if current_chat in sender:
                                ai_response = get_ai_response(user_message)
                                if ai_response:
                                    send_message_to_whatsapp(ai_response)
                                    append_to_conversation_history(current_chat, user_message, ai_response)
                                    append_to_basicR(current_chat, user_message, ai_response)
                                    append_to_submain(current_chat, user_message, ai_response)
                    last_message_time = current_message_time
            time.sleep(5)  # Adjust as necessary for responsiveness
        except Exception as e:
            print(f"[ERROR] Exception in process_messages: {e}")
            time.sleep(5)

# -------------------------
# WebDriver & Main Execution
# -------------------------
# Set up Edge WebDriver paths and options
edge_driver_path = r"C:\Users\ADMIN\OneDrive\Desktop\edgedriver_win64\msedgedriver.exe" # Use your LOCATIONS
user_data_dir = r"C:\Users\ADMIN\AppData\Local\Microsoft\Edge\User Data" # Use your LOCATIONS
profile_name = "Default"

options = Options()
options.add_argument(f"--user-data-dir={user_data_dir}")
options.add_argument(f"--profile-directory={profile_name}")
options.add_argument("--remote-debugging-port=9222")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

service = Service(edge_driver_path)

print("[INFO] Starting Edge WebDriver...")
driver = webdriver.Edge(service=service, options=options)

try:
    print("[INFO] Navigating to WhatsApp Web...")
    driver.get("https://web.whatsapp.com")
    print("[INFO] Please log in to WhatsApp Web if not already logged in.")
    time.sleep(15)  # Wait for manual login
    
    # Start threads for monitoring chat changes and processing messages
    chat_monitor_thread = threading.Thread(target=monitor_top_chat, daemon=True)
    message_processor_thread = threading.Thread(target=process_messages, daemon=True)
    
    chat_monitor_thread.start()
    message_processor_thread.start()
    
    # Keep the main thread alive so the daemon threads continue running
    input("Press Enter to exit the script manually...")
except Exception as e:
    print(f"[ERROR] Exception in main execution: {e}")
finally:
    driver.quit()
