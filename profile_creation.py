import os

def create_profile():
    print("Welcome to the Profile Creation Wizard!")
    
    # Gather input from the user
    name = input("Name of the person: ").strip()
    relationship = input("Relationship with user: ").strip()
    talk_style = input("How should I talk to them: ").strip()
    
    # Additional personalization (optional)
    preferred_language = input("Preferred language (leave blank for default): ").strip() or "Default"
    avoid_topics = input("Any specific topics to avoid (comma-separated, leave blank for none): ").strip()
    
    # Define folder path and file paths
    people_folder = "People"
    person_folder = os.path.join(people_folder, name)
    main_file_path = os.path.join(person_folder, "main.txt")
    submain_file_path = os.path.join(person_folder, "submain.txt")
    temp_reference_file_path = os.path.join(person_folder, "temp_reference.txt")
    
    # Create the folder for the person
    os.makedirs(person_folder, exist_ok=True)
    
    # Content for main.txt
    main_content = (
        f"<start_of_turn>user\n"
        f"Hello! My name is Dev Jadhav, and I created you! " # Use your name
        f"I'm using this service to communicate on WhatsApp with people while I'm busy. "
        f"You are gonna talk to my '{relationship}'. {talk_style} "
        f"Talk to him in {preferred_language}"
        f"Now you will talk to them. Goodbye<end_of_turn>\n"
    )
    
    # Write to main.txt
    with open(main_file_path, "w", encoding="utf-8") as main_file:
        main_file.write(main_content)
    
    # Create empty submain.txt and temp_reference.txt
    for path in [submain_file_path, temp_reference_file_path]:
        with open(path, "w", encoding="utf-8") as file:
            file.write("")  # Initialize with empty content
    
    # Success message
    print(f"Profile for '{name}' has been created successfully!")
    print(f"Files created: \n- {main_file_path}\n- {submain_file_path}\n- {temp_reference_file_path}")

# Call the function
create_profile()
