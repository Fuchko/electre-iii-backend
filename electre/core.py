def run_electre(data):
    alternatives = data.get('alternatives', [])
    criteria = data.get('criteria', [])
    evaluations = data.get('evaluations', [])

    num_alt = len(alternatives)
    num_crit = len(criteria)

    weights = [c['weight'] for c in criteria]

    concordance_matrix = [[0 for _ in range(num_alt)] for _ in range(num_alt)]
    discordance_matrix = [[0 for _ in range(num_alt)] for _ in range(num_alt)]
    outranking_matrix = [[0 for _ in range(num_alt)] for _ in range(num_alt)]

    for i in range(num_alt):
        for j in range(num_alt):
            if i == j:
                concordance_matrix[i][j] = None
                discordance_matrix[i][j] = None
                outranking_matrix[i][j] = None
                continue

            sum_weights = 0
            total_weight = sum(weights)
            max_discordance = 0

            for k in range(num_crit):
                diff = evaluations[i][k] - evaluations[j][k]
                q = criteria[k]['q']
                p = criteria[k]['p']
                v = criteria[k]['v']

                # Concordance
                if diff >= -q:
                    sum_weights += weights[k]
                elif -p < diff < -q:
                    partial = (diff + p) / (p - q)
                    sum_weights += weights[k] * partial

                # Discordance
                if diff < -p:
                    disc = min(1, (abs(diff) - p) / (v - p)) if abs(diff) <= v else 1
                    max_discordance = max(max_discordance, disc)

            concordance_index = sum_weights / total_weight
            concordance_matrix[i][j] = round(concordance_index, 3)
            discordance_matrix[i][j] = round(max_discordance, 3)

            # Outranking decision
            threshold_C = 0.6
            threshold_D = 0.4

            if concordance_index >= threshold_C and max_discordance <= threshold_D:
                outranking_matrix[i][j] = 1
            else:
                outranking_matrix[i][j] = 0

    # Генеруємо текстовий висновок
    dominance_scores = [sum(1 if outranking_matrix[i][j] == 1 else 0 for j in range(num_alt) if i != j) for i in range(num_alt)]
    max_score = max(dominance_scores)
    best_alternatives = [alternatives[i] for i, score in enumerate(dominance_scores) if score == max_score]

    if len(best_alternatives) == 1:
        conclusion = f"Альтернатива '{best_alternatives[0]}' є домінуючою, оскільки переважає інших."
    else:
        alt_list = ", ".join(best_alternatives)
        conclusion = f"Альтернативи {alt_list} входять до множини Парето (жодна не переважається іншою явно)."

    return {
        'status': 'success',
        'alternatives': alternatives,
        'concordance_matrix': concordance_matrix,
        'discordance_matrix': discordance_matrix,
        'outranking_matrix': outranking_matrix,
        'conclusion': conclusion
    }
