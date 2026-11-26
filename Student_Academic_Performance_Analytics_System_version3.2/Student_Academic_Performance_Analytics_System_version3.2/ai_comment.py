import requests

# =========================
# Ollama AI Integration
# =========================
# Integrates with a locally running Ollama server (default: localhost:11434)
# to generate an AI-written comment on a student's performance.
# If Ollama isn't running or the call fails, it silently falls back to a
# rule-based analysis (_fallback_analysis).

class OllamaAI:

    def __init__(self, model="gemma4:e4b"):
        self.model = model  # Name of the model to use
        self.api_url = "http://localhost:11434/api/generate"  # Local Ollama API endpoint
        
    def check_ollama_running(self):
        """Check if Ollama is running"""
        # Ping the /api/tags endpoint to see if the local Ollama service is up
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            return response.status_code == 200
        except:
            # Any network error / service not running is treated as "not available"
            return False
    
    def generate_performance_analysis(self, student_data, factors):
        """Generate AI-powered performance analysis using Ollama"""
        
        # Skip straight to the fallback if Ollama isn't running - no point trying
        if not self.check_ollama_running():
            return self._fallback_analysis(student_data, factors)
        
        # Prepare prompt for Ollama
        # Build the prompt text from the student's data and the factor analysis
        prompt = self._create_analysis_prompt(student_data, factors)
        
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,       # Get the full response at once instead of streaming
                "temperature": 0.7     # Controls how random/creative the generated text is
            }
            
            response = requests.post(self.api_url, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                # Pull the 'response' field out of the JSON; fall back if missing
                return result.get('response', self._fallback_analysis(student_data, factors))
            else:
                # Non-200 status code also falls back to the rule-based analysis
                return self._fallback_analysis(student_data, factors)
                
        except Exception as e:
            # Any exception during the request (timeout, connection error, etc.) falls back too
            print(f"AI generation error: {e}")
            return self._fallback_analysis(student_data, factors)
    
    def _create_analysis_prompt(self, student_data, factors):
        """Create a detailed prompt for AI analysis"""
        # Start with the student's basic info
        prompt = f"""You are an educational AI assistant analyzing student performance.

Student Information:
- Student ID: {student_data['student_id']}
- Final Grade: {student_data['G3']}
- Previous Failures: {student_data['failures']}
- Weekly Study Time: {student_data['studytime']} (scale 1-4)
- Absences: {student_data['absences']}
- Health Status: {student_data['health']} (scale 1-5)

Performance Factors Analysis:
"""
        # Append each factor's analysis and recommendation to the prompt
        for factor in factors:
            prompt += f"\n{factor['factor']} (Importance: {factor['importance']}%)\n"
            prompt += f"- {factor['analysis']}\n"
            prompt += f"- Recommendation: {factor['recommendation']}\n"
        
        # Ask the model to respond in a fixed format (level/comment/recommendation)
        # so it's easy to display consistently
        prompt += """

Based on this information, provide:
1. A performance level classification (Excellent/Good/Average/Needs Improvement/Poor)
2. A detailed comment about the student's performance (2-3 sentences)
3. Specific recommendations for improvement

Format your response as:
Performance Level: [level]
Comment: [your comment]
Recommendation: [your recommendation]
"""
        return prompt
    
    def _fallback_analysis(self, student_data, factors):
        """Fallback analysis if Ollama is not available"""
        # Generates a "pretend AI" comment using simple rules and string templates
        
        # Determine performance level
        # Classify the student into a performance tier based on grade range
        grade = student_data['G3']
        if grade >= 18:
            level = "Excellent"
            comment = "This student demonstrates excellent academic performance."
        elif grade >= 15:
            level = "Good"
            comment = "This student shows good academic performance with room for improvement."
        elif grade >= 12:
            level = "Average"
            comment = "This student performs at an average level."
        elif grade >= 10:
            level = "Needs Improvement"
            comment = "This student needs improvement to achieve better grades."
        else:
            level = "Poor"
            comment = "This student is struggling academically and needs immediate support."
        
        # Add specific observations
        # Add personalized notes based on the raw data (failures / low study time / high absences)
        observations = []
        if student_data['failures'] > 0:
            observations.append("has previous failures")
        if student_data['studytime'] < 2:
            observations.append("has low study time")
        if student_data['absences'] > 10:
            observations.append("has high absences")
        
        if observations:
            comment += f" The student {' and '.join(observations)}."
        
        # Generate recommendation
        # Build up a list of recommendations based on which conditions were triggered
        recommendations = []
        for factor in factors:
            if factor['factor'] == 'Failures' and student_data['failures'] > 0:
                recommendations.append("Provide additional academic support")
            if factor['factor'] == 'Study Time' and student_data['studytime'] < 3:
                recommendations.append("Increase weekly study hours")
            if factor['factor'] == 'Absences' and student_data['absences'] > 10:
                recommendations.append("Improve attendance")
        
        recommendation = ", ".join(recommendations) if recommendations else "Continue current study habits"
        
        # Match the same format as the real AI response, so callers don't need
        # to know whether this was AI-generated or rule-based
        return f"""Performance Level: {level}

Comment: {comment}

Recommendation: {recommendation} to achieve consistent academic success.
"""