import xmlrpc.client

server = xmlrpc.client.ServerProxy('http://localhost:8000/', allow_none=True)

def main():
    while True:
        print("\nOptions:")
        print("1. Add a note")
        print("2. Get notes for a topic")
        print("3. Search Wikipedia and append info to a topic")
        print("4. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            topic_name = input("Enter topic name: ")
            note_text = input("Enter note text: ")
            print(server.add_note(topic_name, note_text))
        elif choice == "2":
            topic_name = input("Enter topic name: ")
            notes = server.get_notes(topic_name)
            if notes:
                for note in notes:
                    print(note)
            else:
                print("No notes found for this topic.")
        elif choice == "3":
            topic_name = input("Enter topic name for Wikipedia search: ")
            wikipedia_url = server.query_wikipedia(topic_name)
            if wikipedia_url != "No Wikipedia article found.":
                print("Wikipedia URL found:", wikipedia_url)
                result = server.add_wikipedia_info_to_topic(topic_name, wikipedia_url)
                print(result)
            else:
                print("No Wikipedia article found for this topic.")
        elif choice == "4":
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
