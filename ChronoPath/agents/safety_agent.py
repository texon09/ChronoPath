import re
import logging

logger = logging.getLogger("chronopath.agents.safety_agent")

class SafetyAgent:
    REQUIRED_FIELDS = {"story", "facts", "language"}
    BLOCKED_PATTERNS = ["ignore previous instructions", "system prompt", "api key"]
    
    # Regex Patterns
    EMAIL_REGEX = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
    PHONE_REGEX = re.compile(r"\+?\d{1,4}[-.\s]?\(?\d{1,3}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}")
    HTML_UNSAFE_REGEX = re.compile(r"<script|<iframe|<object|<embed|javascript:|on\w+\s*=", re.IGNORECASE)

    async def execute(self, state):
        narrative = state.get("story")
        safety = self.run(narrative)
        state.set("safety", safety)
        return state

    def run(self, narrative):
        issues = []
        confidence = 1.0
        
        # 1. Schema Validation
        if not isinstance(narrative, dict):
            issues.append("Narrative input is not a dictionary")
            return self._build_result(approved=False, confidence=0.0, issues=issues, schema=False, pii=False, prompt_inj=False, grounding=False, length=False, html=False, utf=False)

        has_schema = self.REQUIRED_FIELDS.issubset(narrative.keys())
        if not has_schema:
            issues.append("Missing required fields: story, facts, or language")
            confidence = 0.0

        story = narrative.get("story", "")
        facts = narrative.get("facts", [])
        language = narrative.get("language", "")

        # 2. Schema Parameter Type Verification
        if has_schema:
            if not isinstance(story, str):
                issues.append("Story is not a string type")
                confidence = 0.0
            if not isinstance(facts, list):
                issues.append("Facts is not a list type")
                confidence = 0.0
            if not isinstance(language, str):
                issues.append("Language is not a string type")
                confidence = 0.0

        # Stop early if schema is broken
        if confidence == 0.0:
            return self._build_result(approved=False, confidence=0.0, issues=issues, schema=False, pii=False, prompt_inj=False, grounding=False, length=False, html=False, utf=False)

        # 3. Empty & Length Validation
        story_len = len(story)
        length_ok = True
        if story_len == 0:
            issues.append("Story content is empty")
            confidence = 0.0
            length_ok = False
        elif story_len < 10:
            issues.append(f"Story length ({story_len}) is below minimum limit (10)")
            confidence = min(confidence, 0.5)
            length_ok = False
        elif story_len > 10000:
            issues.append(f"Story length ({story_len}) exceeds maximum limit (10000)")
            confidence = min(confidence, 0.5)
            length_ok = False

        # 4. Prompt Injection Validation
        has_blocked_text = any(pattern in story.lower() for pattern in self.BLOCKED_PATTERNS)
        if has_blocked_text:
            issues.append("Prompt injection keywords detected")
            confidence = 0.0

        # 5. PII (Email & Phone) Detection
        pii_safe = True
        if self.EMAIL_REGEX.search(story):
            issues.append("Email address detected in story")
            pii_safe = False
            confidence = min(confidence, 0.4)
        if self.PHONE_REGEX.search(story):
            issues.append("Phone number detected in story")
            pii_safe = False
            confidence = min(confidence, 0.4)

        # 6. Unsafe HTML Validation
        html_safe = True
        if self.HTML_UNSAFE_REGEX.search(story):
            issues.append("Unsafe HTML or Javascript detected in story")
            html_safe = False
            confidence = 0.0

        # 7. Invalid UTF-8 Validation
        utf8_ok = True
        try:
            story.encode("utf-8")
        except UnicodeEncodeError:
            issues.append("Invalid UTF-8 characters detected in story")
            utf8_ok = False
            confidence = 0.0

        # 8. Grounding Check
        has_grounding = bool(facts)
        if not has_grounding:
            issues.append("No historical facts provided for grounding validation")
            confidence = min(confidence, 0.8)

        approved = len(issues) == 0 and confidence == 1.0

        return self._build_result(
            approved=approved,
            confidence=confidence,
            issues=issues,
            schema=has_schema,
            pii=pii_safe,
            prompt_inj=not has_blocked_text,
            grounding=has_grounding,
            length=length_ok,
            html=html_safe,
            utf=utf8_ok
        )

    def _build_result(self, approved, confidence, issues, schema, pii, prompt_inj, grounding, length, html, utf):
        return {
            "approved": approved,
            "confidence": confidence,
            "issues": issues,
            "checks": {
                "schema": schema,
                "pii": pii,
                "prompt_injection": prompt_inj,
                "grounding": grounding,
                "length": length,
                "html": html,
                "utf8": utf
            }
        }
