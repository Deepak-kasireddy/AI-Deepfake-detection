def calculate_reality(image, text, source):
    try:
        # Extract confidence values and results
        image_conf = float(image.get("confidence", 0)) if image else 0
        image_result = image.get("result", "") if image else ""
        
        # NaN check for image_conf
        if image_conf != image_conf:
            image_conf = 0.5
            
        text_conf = float(text.get("confidence", 0)) if text else 0
        text_result = text.get("result", "") if text else ""
        
        # NaN check for text_conf
        if text_conf != text_conf:
            text_conf = 0.5
            
        source_score = float(source.get("score", 50)) if source else 50
        if source_score != source_score:
            source_score = 50
        
        # Calculate individual authenticity scores (0 = Fake, 1 = Real)
        # For image: "Real" is authentic, "AI-Generated" is not
        if image_result == "Real":
            image_auth = image_conf
        elif image_result == "AI-Generated":
            image_auth = 1 - image_conf
        else:
            image_auth = 0.5 # Default for error/unknown
            
        # For text: "Real" is authentic, "Fake" is not
        if text_result == "Real":
            text_auth = text_conf
        elif text_result == "Fake":
            text_auth = 1 - text_conf
        else:
            text_auth = 0.5 # Default for error/unknown
            
        # Calculate weighted authenticity score (0-100)
        score = (
            image_auth * 30 +
            text_auth * 30 +
            (source_score / 100) * 40
        )

        # Final safety checks
        if score != score: # NaN check
            score = 50.0
            
        score = max(0, min(100, round(float(score), 2)))

        if score > 70:
            label = "Authentic"
        elif score > 40:
            label = "Suspicious"
        else:
            label = "Likely Fake"

        return score, label
    except Exception as e:
        print(f"Error calculating reality score: {e}")
        return 50.0, "Unable to determine"