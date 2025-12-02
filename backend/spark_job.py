import os
import sys

# Print to confirm script is starting
print("="*60)
print("SCRIPT STARTING...")
print("="*60)
sys.stdout.flush()

# IMPORTANT: Set these BEFORE importing pyspark
os.environ['PYSPARK_PYTHON'] = 'python'
os.environ['PYSPARK_DRIVER_PYTHON'] = 'python'

print("Importing PySpark...")
sys.stdout.flush()

from pyspark import SparkConf, SparkContext

print("PySpark imported successfully!")
sys.stdout.flush()


# ---------------------------
#  ENHANCED SENTIMENT ANALYSIS
# ---------------------------
def run_sentiment(sc, text_list):
    """
    Improved sentiment analysis with:
    - Word weighting (intensity modifiers)
    - Negation handling
    - Punctuation consideration
    - Normalized scoring
    """
    
    # Extended sentiment dictionaries with weights
    positive_words = {
        "good": 1, "great": 2, "awesome": 3, "excellent": 3, "happy": 2,
        "love": 3, "wonderful": 3, "fantastic": 3, "amazing": 3, "perfect": 3,
        "beautiful": 2, "best": 3, "brilliant": 3, "outstanding": 3,
        "delightful": 2, "enjoy": 2, "pleased": 2, "satisfied": 2,
        "like": 1, "nice": 1, "fine": 1, "well": 1, "positive": 2
    }
    
    negative_words = {
        "bad": 1, "sad": 2, "terrible": 3, "worst": 3, "awful": 3,
        "hate": 3, "horrible": 3, "poor": 2, "disappointing": 2,
        "disappointed": 2, "useless": 2, "waste": 2, "regret": 2,
        "pathetic": 3, "disgusting": 3, "annoying": 2, "boring": 2,
        "dislike": 2, "unfortunate": 1, "negative": 2, "problem": 1
    }
    
    # Intensifiers and negations
    intensifiers = ["very", "really", "extremely", "absolutely", "totally", "completely"]
    negations = ["not", "no", "never", "nothing", "nowhere", "neither", "nobody", "none"]

    rdd = sc.parallelize(text_list)

    def analyze_sentence(sentence):
        """Analyze sentiment with context awareness"""
        text = sentence.lower()
        words = text.split()
        
        if not words:
            return 0.0
        
        score = 0.0
        total_weight = 0
        
        for i, word in enumerate(words):
            # Clean word from punctuation
            clean_word = word.strip(".,!?;:'\"")
            
            # Check if previous word is a negation
            is_negated = i > 0 and words[i-1].strip(".,!?;:'\"") in negations
            
            # Check if previous word is an intensifier
            intensifier_multiplier = 1.5 if i > 0 and words[i-1].strip(".,!?;:'\"") in intensifiers else 1.0
            
            # Calculate sentiment contribution
            if clean_word in positive_words:
                word_score = positive_words[clean_word] * intensifier_multiplier
                score += -word_score if is_negated else word_score
                total_weight += 1
                
            elif clean_word in negative_words:
                word_score = negative_words[clean_word] * intensifier_multiplier
                score += word_score if is_negated else -word_score
                total_weight += 1
        
        # Exclamation marks add emphasis
        exclamation_count = sentence.count("!")
        if exclamation_count > 0 and score != 0:
            score *= (1 + exclamation_count * 0.2)
        
        # Normalize score to -1 to 1 range
        if total_weight > 0:
            normalized_score = max(-1.0, min(1.0, score / (total_weight * 3)))
        else:
            normalized_score = 0.0
            
        return normalized_score

    def classify_sentiment(score):
        """Convert score to sentiment label and confidence"""
        if score > 0.1:
            sentiment = "Positive"
        elif score < -0.1:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
            
        confidence = abs(score)
        return sentiment, confidence

    # Process all texts
    scores = rdd.map(analyze_sentence).collect()
    classifications = [classify_sentiment(s) for s in scores]
    
    return scores, classifications


# ---------------------------
#  COMPREHENSIVE SPARK TESTS
# ---------------------------
def test_spark_cluster():
    """Enhanced cluster testing with multiple operations"""
    
    print("\nConfiguring Spark...")
    sys.stdout.flush()
    
    # Configure Spark with explicit settings
    conf = (SparkConf()
            .setAppName("SparkClusterTest")
            .set("spark.driver.memory", "1g")
            .set("spark.executor.memory", "1g")
            .set("spark.python.worker.reuse", "true"))
    
    print("Creating SparkContext...")
    sys.stdout.flush()
    
    # Create SparkContext
    sc = SparkContext(conf=conf)
    
    print("SparkContext created successfully!")
    sys.stdout.flush()
    
    try:
        print("\n" + "="*60)
        print("           SPARK CLUSTER COMPREHENSIVE TEST")
        print("="*60 + "\n")
        sys.stdout.flush()

        # Test 1: Basic Transformations
        print("TEST 1: Basic Transformations")
        print("-" * 40)
        sys.stdout.flush()
        
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        rdd = sc.parallelize(data, numSlices=4)
        
        squares = rdd.map(lambda x: x * x).collect()
        print(f"Original: {data}")
        print(f"Squares:  {squares}")
        print(f"Sum of squares: {sum(squares)}")
        print()
        sys.stdout.flush()

        # Test 2: Filtering Operations
        print("TEST 2: Filtering Operations")
        print("-" * 40)
        sys.stdout.flush()
        
        evens = rdd.filter(lambda x: x % 2 == 0).collect()
        odds = rdd.filter(lambda x: x % 2 != 0).collect()
        print(f"Even numbers: {evens}")
        print(f"Odd numbers:  {odds}")
        print()
        sys.stdout.flush()

        # Test 3: Reduce Operations
        print("TEST 3: Reduce Operations")
        print("-" * 40)
        sys.stdout.flush()
        
        total = rdd.reduce(lambda a, b: a + b)
        product = rdd.reduce(lambda a, b: a * b)
        maximum = rdd.reduce(lambda a, b: a if a > b else b)
        print(f"Sum:     {total}")
        print(f"Product: {product}")
        print(f"Maximum: {maximum}")
        print()
        sys.stdout.flush()

        # Test 4: Word Count (MapReduce Pattern)
        print("TEST 4: Word Count (MapReduce Pattern)")
        print("-" * 40)
        sys.stdout.flush()
        
        text_data = [
            "spark is great",
            "spark is fast",
            "spark is powerful",
            "distributed computing is great"
        ]
        text_rdd = sc.parallelize(text_data, numSlices=2)
        
        word_counts = (text_rdd
                       .flatMap(lambda line: line.split())
                       .map(lambda word: (word, 1))
                       .reduceByKey(lambda a, b: a + b)
                       .sortBy(lambda x: x[1], ascending=False)
                       .collect())
        
        print("Word frequencies:")
        for word, count in word_counts:
            print(f"  {word}: {count}")
        print()
        sys.stdout.flush()

        # Test 5: Cluster Information
        print("TEST 5: Cluster Information")
        print("-" * 40)
        sys.stdout.flush()
        
        num_partitions = rdd.getNumPartitions()
        print(f"Number of partitions: {num_partitions}")
        print(f"Spark version: {sc.version}")
        print(f"Application name: {sc.appName}")
        print(f"Master URL: {sc.master}")
        print()
        sys.stdout.flush()

        # Test 6: Advanced Transformations
        print("TEST 6: Advanced Transformations")
        print("-" * 40)
        sys.stdout.flush()
        
        pairs = rdd.map(lambda x: (x, x * x))
        grouped = pairs.groupByKey().mapValues(list).collect()
        print("Key-Value pairs (number, square):")
        for key, values in grouped[:5]:
            print(f"  {key}: {values}")
        print()
        sys.stdout.flush()

        # Test 7: Statistics
        print("TEST 7: Statistical Analysis")
        print("-" * 40)
        sys.stdout.flush()
        
        stats = rdd.stats()
        print(f"Count:    {stats.count()}")
        print(f"Mean:     {stats.mean():.2f}")
        print(f"Stdev:    {stats.stdev():.2f}")
        print(f"Max:      {stats.max()}")
        print(f"Min:      {stats.min()}")
        print()
        sys.stdout.flush()

        # Test 8: Sentiment Analysis Demo
        print("TEST 8: Sentiment Analysis Demo")
        print("-" * 40)
        sys.stdout.flush()
        
        test_sentences = [
            "This is absolutely great and wonderful!",
            "I hate this terrible product",
            "Not bad, but not good either",
            "This is okay"
        ]
        
        scores, classifications = run_sentiment(sc, test_sentences)
        for i, sentence in enumerate(test_sentences):
            sentiment, confidence = classifications[i]
            print(f"Text: '{sentence}'")
            print(f"  -> {sentiment} (score: {scores[i]:.3f}, confidence: {confidence:.3f})")
            print()
        sys.stdout.flush()

        # Test 9: Parallel Processing Demo
        print("TEST 9: Parallel Processing Verification")
        print("-" * 40)
        sys.stdout.flush()
        
        large_data = list(range(1, 101))
        large_rdd = sc.parallelize(large_data, numSlices=10)
        
        # Get partition info
        def show_partition_info(index, iterator):
            items = list(iterator)
            return [(index, len(items), items[:3] if len(items) > 0 else [])]
        
        partition_info = large_rdd.mapPartitionsWithIndex(show_partition_info).collect()
        print(f"Processing {len(large_data)} items across {large_rdd.getNumPartitions()} partitions:")
        for part_id, count, sample in partition_info[:5]:
            print(f"  Partition {part_id}: {count} items (sample: {sample}...)")
        print()
        sys.stdout.flush()

        print("="*60)
        print("           ALL TESTS COMPLETED SUCCESSFULLY")
        print("="*60 + "\n")
        sys.stdout.flush()
        
    except Exception as e:
        print(f"\n*** ERROR during testing: {e}")
        sys.stdout.flush()
        import traceback
        traceback.print_exc()
    finally:
        # Properly stop SparkContext
        print("\nStopping SparkContext...")
        sys.stdout.flush()
        sc.stop()
        print("SparkContext stopped successfully.\n")
        sys.stdout.flush()


# ---------------------------
#  MAIN ENTRY POINT
# ---------------------------
if __name__ == "__main__":
    print("\n" + "="*60)
    print("MAIN EXECUTION STARTING")
    print("="*60)
    sys.stdout.flush()
    
    try:
        test_spark_cluster()
        print("\n" + "="*60)
        print("PROGRAM COMPLETED SUCCESSFULLY")
        print("="*60 + "\n")
        sys.stdout.flush()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.stdout.flush()
        sys.exit(0)
    except Exception as e:
        print(f"\n\n*** FATAL ERROR: {e}")
        sys.stdout.flush()
        import traceback
        traceback.print_exc()
        sys.exit(1)
