# Load the trained classifier
import pickle
from scipy.sparse import hstack
from customtkinter import * 
rf_classifier= pickle.load(open('my_classifier.pkl', 'rb'))
subject_vectorizer= pickle.load(open('subject_vectorizer.pkl', 'rb'))
body_vectorizer= pickle.load(open('body_vectorizer.pkl', 'rb'))
from spellchecker import SpellChecker
spell = SpellChecker()



def create_popup(text):
    popup = CTkToplevel()
    popup.title(text)
    popup.geometry("300x100")
    
    label = CTkLabel(popup, text=text)
    label.pack(pady=20)
    popup.lift()
    popup.attributes("-topmost", True)

def clasify():

    # Prediction example with new emails
    email_subjects = []
    email_subjects.append(subjectText.get('1.0',END))
    email_bodies = []
    email_bodies.append(bodyText.get('1.0',END))

    # Transform the text
    new_subject = subject_vectorizer.transform(email_subjects)
    new_body = body_vectorizer.transform(email_bodies)
    # Combine the features
    new_combined_features = hstack([new_subject, new_body])
    # Predict
    new_predictions = rf_classifier.predict(new_combined_features)
    for i in new_predictions:
        text = ""
        if i==0:
            text = "SAFE"
        else:
            text = 'PHISHING'
        create_popup(text)
        

#####################################################################################################


# GUI
mainWindow = CTk()
mainWindow.geometry("600x450")
mainWindow.title("PHISHING EMAIL DETECTOR")

mainFrame = CTkFrame(mainWindow)
mainFrame.pack(pady=20, padx=20)

####################################################################################################

# Subject Label
subjectLabel = CTkLabel(mainFrame, text="Subject")
subjectLabel.grid(row=0, column=0, sticky=W, padx=10, pady=10)

# Subject Text Box
subjectText = CTkTextbox(mainFrame, height=100)
subjectText.grid(row=1, column=0, columnspan=3, padx=10)

####################################################################################################


# Body Label
bodyLabel = CTkLabel(mainFrame, text="Body")
bodyLabel.grid(row=3, column=0, sticky=W, padx=10, pady=10)

# Body Text Box
bodyText = CTkTextbox(mainFrame,height=100)
bodyText.grid(row=4, column=0, columnspan=3, padx=10)

####################################################################################################

# run Button
button = CTkButton(mainFrame, text="Submit",width = 10,hover_color='green',command=clasify)
button.grid(row=5, column=2, columnspan=2, pady=10, padx=10)

# Main loop
mainWindow.mainloop()