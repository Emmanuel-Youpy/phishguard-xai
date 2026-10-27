# Publishing the artefact as a repository

**Important:** Choose repository privacy/access based on UWE marker requirements and the dataset/code rights review. This package includes a processed dataset; its redistribution rights have **not** been verified.

## Option A: GitHub via Git (recommended for dozens of files)

1. Make a separate working copy of `PhishGuard_XAI_Repository_v37` and open that folder in VS Code.
2. In GitHub (or your university-approved Git host), create an empty repository named `phishguard-xai` — private by default pending the rights review. Do not initialise with extra files if you will push this directory as-is.
3. From the repository folder terminal, **after checking the files contain no credentials and that you can share them**, run:

```powershell
git init
git add .
git commit -m "PhishGuard XAI research artefact for MSc review"
git branch -M main
git remote add origin <REMOTE_REPOSITORY_URL>
git push -u origin main
```

Replace `<REMOTE_REPOSITORY_URL>` with the address shown by your chosen host. GitHub may request its supported sign-in/authentication method.

4. Open the repository in a fresh browser to verify files and README show correctly.
5. For a private repository, explicitly grant access to your supervisor/markers *if permitted*. If marker identities/access are unclear, ask the module team whether they require a public link, UWE GitLab, or another approved artefact-hosting arrangement.
6. Put the accessible repository URL in Blackboard **Comments** on the report submission.

## Option B: Upload through GitHub's browser

Create the repository, open its file-upload option and add the package's **contents** (not the top-level ZIP file). Large or numerous uploads are more reliably handled with Git. Verify nested folders remain structured.

**Only one version of `app/app.py` is intended for markers**. Do not accidentally include local `app2`, virtual environments, old models, raw URLs, unreviewed notes or backups.
