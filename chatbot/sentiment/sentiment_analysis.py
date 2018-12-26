# from textblob import TextBlob
# from PIL import Image
# 
# from tkinter import *
# 
# class Window(Frame):
# 
#     def __init__(self, master = None):
#         Frame.__init__(self, master)
#         self.master = master
# 
#         self.init_window()
# 
#     def init_window(self):
#         self.master.title("GUI")
#         self.pack(fill=BOTH, expand=1)
# 
# 
# statement = "Today I went to Barbeque Nation and the Food was awesome"
# sentiment = TextBlob(statement)
# print("Sentiment Score: ", sentiment.sentiment.polarity)  # Result = 1.0
# 
# statement2 = "Today I went to Barbeque Nation and the Food was normal"
# sentiment2 = TextBlob(statement2)
# print("Sentiment Score: ", sentiment2.sentiment.polarity)  # Result = 0.15