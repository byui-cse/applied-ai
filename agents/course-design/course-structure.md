I'm teaching a course on applied AI for software engineering. This is a 2 credit (twice a week) 14 week course taught to juniors and seniors. The goal is we don't write a single line of code. We have to use AI for the entire process.

The first 7 weeks will be brownfield development and the last 7 weeks will be greenfield development.

Here's an example layout: 

Phase,Module,Primary Topics & Focus
Phase 1: Brownfield (Legacy Systems),1. Context & Efficiency,"Markdown systems, staying under 20% context, and token optimization for large existing codebases."
,2. Architectural State,"Memory management, caching strategies, and managing technical debt with AI assistance."
,3. Extended Tools,"Using Model Context Protocol (MCP) and Worktrees to navigate and refactor complex, multi-repo legacy systems."
Phase 2: Greenfield (New Systems),4. Foundations & Skills,"Core AI software engineering skills and setting up clean, AI-ready project architectures from scratch."
,5. Extensibility,Developing and integrating Plugins to extend LLM capabilities within a new application.
,6. Autonomous Agents,Designing and deploying single and multi-agent systems to handle specialized development tasks.
Final Integration,7. Advanced Workflows,"Orchestrating multiple agents and complex MCP integrations to finalize a production-ready ""Greenfield"" MVP."


You are given the task of structuring this course. Create a content folder and place all the markdown files inside of this content folder. The structure should go as follows:

content -> phase-<phase_number> -> week-<week_number> 
  - day-1.md
  - labs/

Finally create a syllabus at the top level of the content folder

Make sure you add a day 2 for each week

For each week, create a week-overview.md file, which serves as the week overview (links to days and labs, plus learning outcomes for the week).

The brownfield project that the students will do and add features/fix bugs for is this one:

https://github.com/instructure/canvas-lms 

Update all the markdown files relevant to brownfield for this