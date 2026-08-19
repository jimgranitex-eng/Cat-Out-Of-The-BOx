#!/usr/bin/env python
"""Cat-Out-Of-The-BOx Diagram Skill - integrates worker.py with diagram design."""

import sys
import os
import json
import time
from pathlib import Path

# Add tools to path
sys.path.insert(0, os.path.dirname(__file__))

from worker import ContinuousWorker, ChatHistory, TransformersBackend


class DiagramSkill:
    """Skill that combines Cat-Out-Of-The-BOx continuous worker with diagram design."""
    
    def __init__(self, tester_folder=None):
        self.tester_folder = tester_folder or self._get_tester_folder()
        self.history = ChatHistory()
        self.worker = ContinuousWorker(backend="transformers", model_name="gpt2")
        self.running = True
        self.iteration = 0
        
    def _get_tester_folder(self):
        """Get tester folder path - tries common locations."""
        # Try relative to opencode config
        config_dir = Path("C:/Users/Natalie/.config/opencode")
        tester_path = config_dir / "AI-Model" / "Patent" / "tester"
        if tester_path.exists():
            return str(tester_path)
        
        # Try common locations
        for path in [
            Path("F:/AI-Model/Patent/tester"),
            Path("C:/AI-Model/Patent/tester"),
            Path("./tester"),
            Path("../tester"),
        ]:
            if path.exists():
                return str(path)
        
        # Return None - skill will work with concept diagrams
        return None
    
    def run_diagram_analysis(self, diagram_file, checklist=None):
        """Run diagram analysis using continuous worker."""
        if checklist is None:
            checklist = {
                "f.1": "spacing-and-margins",
                "f.2": "flow-correction", 
                "f.3": "significant-improvements",
                "f.4": "review-other-files",
                "f.5": "leave-as-is"
            }
        
        # Add task to history
        self.history.add("user", f"Analyze diagram: {diagram_file} with checklist: {checklist}")
        
        # If tester folder exists, list files
        if self.tester_folder and os.path.exists(self.tester_folder):
            files = os.listdir(self.tester_folder)
            self.history.add("assistant", f"Found {len(files)} files in tester folder: {files}")
        
        # Run continuous task
        self.iteration = 0
        while self.running and self.iteration < 50:
            self.iteration += 1
            
            # Get recent history
            recent = self.history.get_recent(20)
            
            # Get AI response
            response, success = self.worker.backend.get_response(recent)
            
            if not success:
                self.history.add("assistant", f"Error: {response}")
                break
            
            # Check for completion
            resp_lower = response.lower()
            if any(kw in resp_lower for kw in ["complete", "finished", "done", "analysis complete"]):
                self.history.add("assistant", response)
                self.history.save()
                return {"completed": True, "result": response, "iteration": self.iteration}
            
            # Check for control commands
            if "/stop" in resp_lower:
                self.running = False
                self.history.add("assistant", response)
                break
            
            # Add to history
            self.history.add("assistant", response)
            
            # Brief pause
            time.sleep(0.1)
        
        self.history.save()
        return {"completed": self.running, "iteration": self.iteration, "result": response if 'response' in dir() else "completed"}
    
    def fix_diagram_issues(self, diagram_path, issues=None):
        """Fix specific diagram issues based on checklist."""
        if issues is None:
            issues = {
                "spacing": "adjust spacing between elements",
                "margins": "ensure proper margins",
                "flow": "rework flow to be intuitive",
                "overlapping": "prevent overlapping of text and boxes"
            }
        
        self.history.add("user", f"Fix diagram issues for {diagram_path}: {issues}")
        
        # Run analysis and fixing
        result = self.run_diagram_analysis(diagram_path, issues)
        
        # Generate fix report
        report = {
            "diagram": diagram_path,
            "issues_addressed": issues,
            "iteration": self.iteration,
            "status": "completed" if result.get("completed") else "interrupted",
            "history_file": ".chat_history.json"
        }
        
        self.history.save()
        return report


# Entry point for opencode integration
def run_skill(diagram_file=None, issues=None, tester_folder=None):
    """Run the diagram skill from opencode."""
    skill = DiagramSkill(tester_folder=tester_folder)
    
    if diagram_file:
        result = skill.fix_diagram_issues(diagram_file, issues)
    else:
        # Default: analyze common diagram patterns
        result = skill.run_diagram_analysis(
            "tester_diagrams", 
            {"f.1": "spacing", "f.2": "flow", "f.3": "improvements", "f.5": "leave-as-is"}
        )
    
    return result


if __name__ == "__main__":
    # Allow running from command line
    diagram = sys.argv[1] if len(sys.argv) > 1 else None
    result = run_skill(diagram_file=diagram)
    print(json.dumps(result, indent=2))