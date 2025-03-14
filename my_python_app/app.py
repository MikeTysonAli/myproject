from flask import Flask, render_template, request
from textblob import TextBlob

app = Flask(__name__)

# Define the route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

# Define the route for handling form submission
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Get the answers from the form
        answer1 = request.form['answer1']
        answer2 = request.form['answer2']
        answer3 = request.form['answer3']
        answer4 = request.form['answer4']

        # Perform sentiment analysis on each answer
        sentiment1 = analyze_sentiment(answer1)
        sentiment2 = analyze_sentiment(answer2)
        sentiment3 = analyze_sentiment(answer3)
        sentiment4 = analyze_sentiment(answer4)

        # Calculate overall mood score
        overall_score = calculate_overall_score([sentiment1, sentiment2, sentiment3, sentiment4])

        # Create a mood summary based on the sentiment analysis
        mood_summary = {
            "Answer 1": sentiment1,
            "Answer 2": sentiment2,
            "Answer 3": sentiment3,
            "Answer 4": sentiment4,
            "Overall Mood Score": overall_score
        }

        # Render the result page with the mood summary
        return render_template('result.html', mood_summary=mood_summary)

# Function to analyze sentiment using TextBlob
def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity  # -1 (negative) to 1 (positive)
    
    # Classify sentiment as positive, neutral, or negative
    if sentiment > 0:
        mood = "Positive"
    elif sentiment == 0:
        mood = "Neutral"
    else:
        mood = "Negative"
    
    return mood

# Function to calculate overall mood score (average)
def calculate_overall_score(moods):
    # Map moods to numeric values
    mood_map = {"Positive": 1, "Neutral": 0, "Negative": -1}
    scores = [mood_map[mood] for mood in moods]
    overall_score = sum(scores) / len(scores)  # Average score
    return overall_score

# Route to handle feedback submission
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    # Get the user's rating of the sentiment analysis
    feedback_rating = request.form['feedback_rating']
    
    # Here you would typically store the rating in a database or use it for model retraining
    # For now, we'll just print it out for demonstration purposes
    print(f"Feedback rating received: {feedback_rating}")
    
    return "Thank you for your feedback!"

if __name__ == "__main__":
    app.run(debug=True)
