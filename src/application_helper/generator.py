import json
import os

class AnswerGenerator:
    def __init__(self, profile_path='config/user_profile.json'):
        self.profile = self._load_profile(profile_path)

    def _load_profile(self, path):
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except:
            return {}

    def generate_answers(self, job):
        """
        Generates answers for common internship questions based on the job and user profile.
        """
        company = job.get('company', 'the company')
        role = job.get('role', 'Intern')
        
        skills_str = ", ".join(self.profile.get('skills', []))
        projects_str = ", ".join(self.profile.get('projects', []))
        
        # Template 1: Why should we hire you?
        why_hire_me = (
            f"I have a strong foundation in {skills_str}, which directly aligns with the {role} requirements at {company}. "
            f"I have practically applied these skills in projects like {projects_str}. "
            f"My hands-on experience ensures I can contribute effectively from day one."
        )

        # Template 2: Why do you want to join? (Cover Letter snippet)
        why_join = (
            f"I have been following {company}'s work and I am excited about the opportunity to work as a {role}. "
            f"I am eager to learn from the team and contribute my skills in {skills_str} to build impactful solutions. "
            f"I am available to start {self.profile.get('availability', 'immediately')}."
        )

        return {
            "why_hire_me": why_hire_me,
            "why_join": why_join
        }
