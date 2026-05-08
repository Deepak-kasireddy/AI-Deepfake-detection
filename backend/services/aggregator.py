def calculate_reality(image, text, source):
    try:
        # Default components
        components = []
        
        # 1. Handle Image
        image_res = image.get("result", "") if image else ""
        image_conf = float(image.get("confidence", 0)) if image else 0
        if image_res in ["Real", "AI-Generated"]:
            auth = image_conf if image_res == "Real" else (1 - image_conf)
            components.append({"auth": auth, "weight": 30})
            
        # 2. Handle Text
        text_res = text.get("result", "") if text else ""
        text_conf = float(text.get("confidence", 0)) if text else 0
        if text_res in ["Real", "Fake"]:
            auth = text_conf if text_res == "Real" else (1 - text_conf)
            components.append({"auth": auth, "weight": 30})
            
        # 3. Handle Source
        source_status = source.get("status", "") if source else ""
        source_score = float(source.get("score", 50)) if source else 50
        if source_status in ["Trusted", "Unreliable"]:
            components.append({"auth": source_score / 100, "weight": 40})

        # Calculate final score based on available components
        if not components:
            # Fallback if nothing is valid
            score = 50.0
            label = "Inconclusive"
            summary = "No definitive data could be extracted to verify this content."
            insights = ["Upload more context (text or URLs) for a better analysis."]
        else:
            total_weight = sum(c["weight"] for c in components)
            weighted_sum = sum(c["auth"] * c["weight"] for c in components)
            final_auth = weighted_sum / total_weight
            score = round(final_auth * 100, 2)
            
            # Labeling logic
            if score > 70:
                label = "Authentic"
                summary = "The content shows high indicators of authenticity."
                insights = ["Natural patterns detected in available data.", "Alignment with credible signatures."]
            elif score > 40:
                label = "Suspicious"
                summary = "The content has mixed signals. Some elements appear inconsistent."
                insights = ["Potential digital artifacts or phrasing issues.", "Further verification recommended."]
            else:
                label = "Likely Fake"
                summary = "Warning: Multiple indicators suggest this content is manipulated or AI-generated."
                insights = ["Artificial patterns detected.", "Lacks verifiable human characteristics."]

        return float(score), label, summary, insights
    except Exception as e:
        import traceback
        print(f"Error calculating reality score: {e}")
        traceback.print_exc()
        return 50.0, "Error", "An error occurred during analysis.", [str(e)]