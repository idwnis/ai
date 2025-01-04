import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier

# Download NLTK resources
nltk.download("stopwords")

# Text preprocessing
stop_words_set = set(stopwords.words("english"))
text_stemmer = PorterStemmer()

def preprocess_text(input_text):
    # Convert text to lowercase
    processed = input_text.lower()
    # Remove stopwords
    filtered_words = [word for word in processed.split() if word not in stop_words_set]
    # Apply stemming
    stemmed_words = [text_stemmer.stem(word) for word in filtered_words]
    return " ".join(stemmed_words)

# Sample data
sample_questions = ["What is your name?", "How are you?", "Tell me a joke."]
sample_answers = ["Denis Emadi", "25", "humor"]

# Preprocess training data
processed_questions = [preprocess_text(question) for question in sample_questions]

# Vectorize data
tfidf_vectorizer = TfidfVectorizer(max_features=500)
vectorized_questions = tfidf_vectorizer.fit_transform(processed_questions)

# Train the model
decision_tree_model = DecisionTreeClassifier()
decision_tree_model.fit(vectorized_questions, sample_answers)

# Predict response
def predict_response(user_question):
    # Preprocess the user question
    cleaned_question = preprocess_text(user_question)
    # Vectorize the question
    question_vector = tfidf_vectorizer.transform([cleaned_question])
    # Predict the answer
    predicted_answer = decision_tree_model.predict(question_vector)
    return predicted_answer[0]

# User interface
while True:
    user_input = input("Ask your question: ")
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Goodbye!")
        break
    predicted_answer = predict_response(user_input)
    print("Answer:", predicted_answer)
