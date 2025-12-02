from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import re

# Sentiment word dictionaries
POSITIVE_WORDS = {
    'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love',
    'best', 'perfect', 'beautiful', 'awesome', 'brilliant', 'outstanding',
    'superb', 'magnificent', 'marvelous', 'terrific', 'fabulous', 'nice',
    'happy', 'pleased', 'delighted', 'satisfied', 'enjoyable', 'impressive',
    'exceptional', 'incredible', 'superior', 'valuable', 'positive', 'better',
    'like', 'thanks', 'thank', 'appreciate', 'helpful', 'recommend', 'excited'
}

NEGATIVE_WORDS = {
    'bad', 'terrible', 'awful', 'horrible', 'poor', 'worst', 'hate', 'dislike',
    'disappointing', 'disappointed', 'worthless', 'useless', 'garbage', 'trash',
    'pathetic', 'disgusting', 'annoying', 'frustrating', 'angry', 'sad', 'upset',
    'unhappy', 'dissatisfied', 'regret', 'waste', 'inferior', 'mediocre',
    'unacceptable', 'difficult', 'problem', 'issue', 'fail', 'failed', 'broken',
    'wrong', 'defective', 'damaged', 'never', 'nothing', 'nobody', 'boring'
}

NEGATIONS = {'not', 'no', 'never', 'neither', 'nobody', 'nothing', 'none', "don't", "doesn't", "didn't", "won't", "wouldn't", "can't", "couldn't"}
INTENSIFIERS = {'very', 'really', 'extremely', 'absolutely', 'totally', 'completely', 'utterly', 'highly', 'so', 'too'}


def preprocess_text(text):
    """Clean and tokenize text"""
    text = text.lower()
    text = re.sub(r'[^a-z\s\'\-]', ' ', text)
    words = text.split()
    return words


def calculate_sentiment_score(words):
    """Calculate sentiment score with context awareness"""
    positive_count = 0
    negative_count = 0
    
    for i, word in enumerate(words):
        is_negated = False
        if i > 0 and words[i-1] in NEGATIONS:
            is_negated = True
        elif i > 1 and words[i-2] in NEGATIONS:
            is_negated = True
        
        intensity = 1.0
        if i > 0 and words[i-1] in INTENSIFIERS:
            intensity = 1.5
        
        if word in POSITIVE_WORDS:
            if is_negated:
                negative_count += intensity
            else:
                positive_count += intensity
        elif word in NEGATIVE_WORDS:
            if is_negated:
                positive_count += intensity
            else:
                negative_count += intensity
    
    return positive_count, negative_count


def analyze_sentiment(text):
    """Main sentiment analysis function"""
    if not text or not text.strip():
        return "Neutral", 0.0
    
    words = preprocess_text(text)
    
    if not words:
        return "Neutral", 0.0
    
    positive_score, negative_score = calculate_sentiment_score(words)
    total_score = positive_score + negative_score
    
    if total_score == 0:
        return "Neutral", 0.5000
    
    if positive_score > negative_score:
        sentiment = "Positive"
        confidence = positive_score / total_score
    elif negative_score > positive_score:
        sentiment = "Negative"
        confidence = negative_score / total_score
    else:
        sentiment = "Neutral"
        confidence = 0.5000
    
    return sentiment, round(confidence, 4)


class SentimentHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        if self.path == '/analyze':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                text = data.get('text', '')
                
                if not text:
                    self.send_error_response(400, "No text provided")
                    return
                
                sentiment, score = analyze_sentiment(text)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {
                    'sentiment': sentiment,
                    'score': score
                }
                
                self.wfile.write(json.dumps(response).encode('utf-8'))
                
            except json.JSONDecodeError:
                self.send_error_response(400, "Invalid JSON")
            except Exception as e:
                self.send_error_response(500, str(e))
        else:
            self.send_error_response(404, "Not Found")
    
    def send_error_response(self, code, message):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = {'error': message}
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def log_message(self, format, *args):
        print(f"[{self.date_time_string()}] {format % args}")


def run_server(host='0.0.0.0', port=5000):
    server_address = (host, port)
    httpd = HTTPServer(server_address, SentimentHandler)
    print(f"✅ Sentiment Analyzer Server Started")
    print(f"🌐 Server running on http://{host}:{port}")
    print(f"📍 Accessible at http://10.10.31.109:{port}")
    print("🛑 Press Ctrl+C to stop the server\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped")
        httpd.shutdown()


if __name__ == '__main__':
    run_server()
