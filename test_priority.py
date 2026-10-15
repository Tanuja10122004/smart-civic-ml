
from priority_detection import calculate_priority

test_cases = [
    {
        "name": "Low",
        "data": {
            "category": "crack",
            "severity": 1,
            "blocks_traffic": False,
            "injury_risk": False,
            "near_school_hospital": False
        }
    },
    {
        "name": "Medium",
        "data": {
            "category": "pothole",
            "severity": 3,
            "blocks_traffic": False,
            "injury_risk": False,
            "near_school_hospital": False
        }
    },
    {
        "name": "High",
        "data": {
            "category": "pothole",
            "severity": 4,
            "blocks_traffic": True,
            "injury_risk": False,
            "near_school_hospital": False
        }
    },
    {
        "name": "Critical - Injury Risk",
        "data": {
            "category": "crack",
            "severity": 1,
            "blocks_traffic": False,
            "injury_risk": True,
            "near_school_hospital": False
        }
    },
    {
        "name": "Critical - Open Manhole",
        "data": {
            "category": "open_manhole",
            "severity": 4,
            "blocks_traffic": False,
            "injury_risk": False,
            "near_school_hospital": False
        }
    },
    {
        "name": "High - Near School",
        "data": {
            "category": "pothole",
            "severity": 3,
            "blocks_traffic": False,
            "injury_risk": False,
            "near_school_hospital": True
        }
    }
]

for test in test_cases:
    result = calculate_priority(test["data"])

    print("\nTest:", test["name"])
    print("Priority:", result["priority"])
    print("Score:", result["score"])
    print("Reasons:", ", ".join(result["reasons"]))
