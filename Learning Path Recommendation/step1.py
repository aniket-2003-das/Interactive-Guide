# Step 1: Calculate concept error rates F
def calculate_error_rates(R, QC):
    concept_error_rates = {}  # Stores concept error rates
    # Calculate error rates for each concept
    for concept, concept_questions in QC.items():
        total = 0
        correct = 0
        for question in concept_questions:
            if R[question] == 1:
                correct += 1  # Increment if the answer is correct
            total += 1  # Increment total questions
        error_rate = 1 - correct / total if total != 0 else 1  # Calculate error rate
        concept_error_rates[concept] = error_rate
    return concept_error_rates

