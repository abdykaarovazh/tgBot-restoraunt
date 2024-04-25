feedback = []

def insert_feedback(user_name: str, text: str, score: float):
    user_feedback = feedback.insert(
        len(feedback),
        [user_name, text, score]
    )
    print(feedback)
    return user_feedback