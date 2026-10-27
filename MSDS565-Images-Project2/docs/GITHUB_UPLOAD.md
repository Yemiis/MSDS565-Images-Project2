# Organize and upload the repository

The prepared folder is `MSDS565-Images-Project2`. `Project2` is the shared filename token required by the prompt's `<TeamName>` convention. It is not Team 1 and does not contain a student's name.

## Before uploading

1. Keep `Images` and `Images.zip` outside this folder. The package already excludes raw photos, prepared arrays, checkpoints, caches and duplicate notebooks.
2. Export the actual notebook conda environment using the run guide. The included environment.yml is explicitly reconstructed and must be replaced for rubric compliance.
3. Run:

```powershell
python scripts/validate_project.py
python scripts/validate_project.py --submission
```

The first checks the source/model package. The second also reports unfinished human reviews, live-demo records, notebook execution gaps and the missing true environment export. A passing source check alone does not mean the entire assignment is complete.

4. Keep executed notebook outputs intact as the prompt requires. Do not run a blanket output-clearing command. Include no separate image files, arrays or image ZIPs.
5. Complete real meeting minutes. Keep individual peer evaluations private and submit them through the instructor's designated route rather than committing personal feedback to the team repository.

## Browser upload

1. Sign in to GitHub yourself.
2. Create a **new repository** named `MSDS565-Images-Project2`. Private is the default recommendation for this coursework; give the instructor access as required by the course.
3. Do not add another README or license during creation, because this package includes the README.
4. Choose **uploading an existing file**. Open the extracted project folder and drag its contents into the upload area, preserving the `app`, `data`, `models`, `notebooks`, `docs`, `scripts` and `tests` folders. Upload the contents, not the outer ZIP.
5. Browser uploads can miss hidden files. Check that `.gitignore` and `.streamlit/config.toml` are present. Git CLI is more reliable for this step.
6. Commit with a clear description. Check the four canonical notebook filenames and the app script. Do not enable GitHub Pages; it does not run a Python Streamlit server.

## Git CLI upload

Run from the extracted repository root. Copy the real remote URL from your new GitHub repository; do not push to an older project's remote.

```powershell
git init -b main
git add .
git status --short
git diff --cached --stat
git commit -m "Add Project 2 image classification notebooks and Streamlit app"
```

Then run `git remote add origin` followed by the exact URL GitHub gave you, and:

```powershell
git push -u origin main
```

Inspect the staged files before committing. All included probes are under 100 KB and need no Git LFS. Large pretrained backbones stay in your Keras cache; they are rebuilt/downloaded at app startup.

This delivery organizes files only. It does not connect to GitHub, grant account access, publish a repository or deploy a public website.
