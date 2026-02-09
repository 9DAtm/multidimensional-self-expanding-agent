class Continuity:
    def assess(self, history):
        count = len(history)
        if count == 0:
            return {
                "length": 0,
                "continuous": False,
                "average_coherence": 0.0,
                "coherence_trend": "none",
                "drift_events": 0,
            }

        coherences = [s.coherence for s in history]
        avg_coherence = sum(coherences) / len(coherences)
        drift_events = 0

        for i in range(1, len(history)):
            drift = history[i].field.get("drift", 0.0)
            if drift > 0.2:
                drift_events += 1

        if len(coherences) >= 2:
            if coherences[-1] > coherences[0]:
                trend = "improving"
            elif coherences[-1] < coherences[0]:
                trend = "degrading"
            else:
                trend = "stable"
        else:
            trend = "insufficient_data"

        return {
            "length": count,
            "continuous": drift_events == 0,
            "average_coherence": round(avg_coherence, 4),
            "coherence_trend": trend,
            "drift_events": drift_events,
        }