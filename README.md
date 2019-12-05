# nli_chatbot 
This chatbot implementation is the trial for understanding Natural Langauge Processing (NLP) and also including the interactive talking part. It is implemented based on the idea of BookBot which is able to recommend books to users by genre, title or author name. The simple greetings part are also implemented.

After runing the project, user can wake the BookBot up by saying 'hi' or 'hello' (See the list of wake up words in agent.py then the BookBot will be ready to talk. 

User can simply ask the bot to recommend the books by saying 'recommend me a book' and BookBot will ask if user want him to recommend by genre or author. User also can tell the bot to 'find the book /bookname/' then BookBot will find the book information for user.

Example conversation:

**User**: Hello

**BookBot**: Hi, would you like me to find any books for reading today? I can recommend books for your by genre, title, authors of find book for you.

**User**: Recommend me some books 

**BootBot**: Would you like me to recommend by genre or author?

**User**: The author name's JK Rowling

**BookBot**:  (It gives you a book information) Would you like me to find more information?

**User**: Yes, please

**BookBot**: I found /BookBot gives you more books' information/


# Features and Integrations

## How the chatbot can talk and listen
### Speech to Text (STT) and Text to Speech (TTS)
* The integration for STT has done by using speech_recognition package. See package stt.
* The integration for TTS has done by using pyttsx3 package. See package tts.


## How can it understand what users said

### Spacy: Text Parser, Part of Speech (POS), entity, doc
In order to understand human language, we need to analyse the sentence spoke by user and 'Spacy' is used for POS (part of speech) analysis.

### Dialogue Manager and Intents
To manage converstations between users and BookBot, dialog manager is implemented. Chatbot must be able to ask user when it needs information or reply greetings and so on. In this project the dialogue manager and intents are cutsomised part which can be improved.

## How the bot know that it is greeting or something else from the sentence

### Artificial Intelligence: Machine Learning for classification dialogue type
**NativeBayes** is used for classifying the sentence spoke by users whether it is greeting, whQuetion, yAnswer, Statement, Reject and so on. NativeBayes is used here due to the speed in training. It gives 68% of accuracy. 

#### Model building and dataset for dialogue
* nps_chat (See folder 'nps_chat') is the dataset used for training and testing with ratio 0.8: 0.2 
* The model is not saved and reloaded, it is trained once the application is started. (can be improved)

## How BookBot searches for information

### Sparql and Ontology learning
In this project, you can learn example queries of SPARQL to query information on Ontology (OWL) file.

### Google API for books' information integration
When the sentence spoke by users are analyzed for the intents, the BookBot will search for books according to the intent in Ontology first, incase the book is not found, Google API for searching books will be called.



##### Message from me
I hope this project would help you to understand how Natural Language Processing, SparQL, Ontology, Machine Learning, Speech to Text, Text to Speech work together. There are a lot of thing can be improved to make it works smoother. Feel free to clone and modify it to have your own chatbot version :D


