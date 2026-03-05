import os

repo_root = r"g:\Programas\My Projects\agency-agents"
source_base_dir = os.path.join(repo_root, "claude")
target_base_dir = os.path.join(repo_root, "gemini")
source_dirs = ['design', 'engineering', 'marketing', 'product', 'project-management', 'spatial-computing', 'specialized', 'strategy']
skills_dir = os.path.join(target_base_dir, ".agent", "skills")

os.makedirs(skills_dir, exist_ok=True)

# To avoid converting non-agent files, we will match files in these dirs
for d in source_dirs:
    dir_path = os.path.join(source_base_dir, d)
    if not os.path.exists(dir_path):
        continue
    
    # Recursively find md files
    for root, _, files in os.walk(dir_path):
        for f in files:
            if not f.endswith('.md'):
                continue
            
            # Skip uppercase files like README.md, EXECUTIVE-BRIEF.md, QUICKSTART.md
            if f.isupper() and len(f) > 5:
                continue

            file_path = os.path.join(root, f)
            print(f"Processing {file_path}")
            
            try:
                with open(file_path, "r", encoding="utf-8") as rf:
                    content = rf.read()
            except Exception as e:
                print(f"Failed to read {file_path}: {e}")
                continue

            # Check if it has a frontmatter with 'name:'
            if not content.startswith("---") or "name:" not in content.split("---")[1]:
                print(f"Skipping {file_path} - not an agent file.")
                continue
                
            # Determine new folder name
            basename = f[:-3]
            # Strip prefix if it exists (e.g., engineering-frontend-developer -> frontend-developer)
            if d != "specialized" and basename.startswith(d + "-"):
                folder_name = basename[len(d)+1:]
            elif d == "project-management" and basename.startswith("project-manager-"):
                folder_name = basename[len("project-manager-"):]
            else:
                folder_name = basename
                
            skill_folder = os.path.join(skills_dir, folder_name)
            os.makedirs(skill_folder, exist_ok=True)
            
            new_file_path = os.path.join(skill_folder, "SKILL.md")
            
            try:
                with open(new_file_path, "w", encoding="utf-8") as wf:
                    wf.write(content)
            except Exception as e:
                print(f"Failed to write {new_file_path}: {e}")
                continue

print("Conversion complete. Original .md files were not deleted.")
