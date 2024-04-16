# CronusMainframe/utils/scoring_model.py

def calculate_score(user_data):
    """
    Calculate the score for a user based on their activity and behavior.
    """
    positive_score = 0
    negative_score = 0

    # Positive factors
    positive_score += user_data.get('messages_sent', 0) * 0.1
    positive_score += user_data.get('photos_sent', 0) * 0.2

    # Negative factors
    negative_score += user_data.get('timeouts', 0) * 1
    negative_score += user_data.get('force_disconnects', 0) * 0.5
    negative_score += user_data.get('forced_deletions', 0) * 0.5

    # Calculate the final score
    score = positive_score / (1 + negative_score)

    return score
