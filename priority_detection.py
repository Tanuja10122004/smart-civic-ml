
def calculate_priority(complaint_data):
    score = 0
    reasons = []

    category = complaint_data.get("category", "").lower()
    severity = complaint_data.get("severity", 1)

    blocks_traffic = complaint_data.get("blocks_traffic", False)
    injury_risk = complaint_data.get("injury_risk", False)
    near_school_hospital = complaint_data.get(
        "near_school_hospital", False
    )

    # Rule 1: Damage severity
    if severity >= 4:
        score += 3
        reasons.append("Severe damage reported")
    elif severity >= 3:
        score += 2
        reasons.append("Moderate damage reported")
    else:
        score += 1
        reasons.append("Low damage severity")

    # Rule 2: Type of road damage
    if category == "open_manhole":
        score += 3
        reasons.append("Open manhole may cause accidents")
    elif category == "waterlogged_road":
        score += 2
        reasons.append("Waterlogging may affect road safety")
    elif category == "pothole":
        score += 2
        reasons.append("Pothole may affect road users")
    elif category == "broken_edges":
        score += 2
        reasons.append("Broken road edges reported")
    elif category == "crack":
        score += 1
        reasons.append("Road crack reported")
    elif category == "construction_zone":
        score += 1
        reasons.append("Construction zone reported")

    # Rule 3: Traffic impact
    if blocks_traffic:
        score += 2
        reasons.append("Traffic is blocked")

    # Rule 4: Risk of injury
    if injury_risk:
        score += 3
        reasons.append("Possible injury risk reported")

    # Rule 5: Sensitive public locations
    if near_school_hospital:
        score += 1
        reasons.append("Near a school or hospital")

    # Assign priority
    if injury_risk or (
        category == "open_manhole" and severity >= 4
    ):
        priority = "Critical"
    elif near_school_hospital and score >= 4:
        priority = "High"
    elif score >= 7:
        priority = "High"
    elif score >= 4:
        priority = "Medium"
    else:
        priority = "Low"

    return {
        "priority": priority,
        "score": score,
        "reasons": reasons
    }


# Test example
if __name__ == "__main__":
    complaint = {
        "category": "open_manhole",
        "severity": 5,
        "blocks_traffic": True,
        "injury_risk": True,
        "near_school_hospital": False
    }

    result = calculate_priority(complaint)

    print("Priority:", result["priority"])
    print("Score:", result["score"])
    print("Reasons:")

    for reason in result["reasons"]:
        print("-", reason)
