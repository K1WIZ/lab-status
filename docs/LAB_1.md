# Lab 1: source control and repeatable tests

## Goal

Create a repository, establish a passing baseline, make a change on a branch,
observe a failing test, fix it, and merge a pull request. Allow about 60–90
minutes, with extra time for first-time GitHub authentication.

## 1. Run the baseline

In the extracted `lab-status` directory:

```bash
python3 -m unittest discover -s tests -v
```

Expect 9 tests and OK. These tests call the application directly: a running
server is not required. Start `python3 app.py` separately and visit the three
endpoints to see the same behavior over HTTP. Stop it when done.

Read `app.py`, then `tests/test_app.py`. Identify which assertions verify the
health response, default message, and supplied commit ID.

## 2. Create local history

```bash
git init -b main
```

If Git does not already have your author identity, configure it for this repo.
Replace the email placeholder with your actual or GitHub-provided no-reply email:

```bash
git config user.name "John Rogers"
git config user.email "YOUR_COMMIT_EMAIL"
git status
git add .
git diff --cached
git commit -m "Add Lab Status app and baseline tests"
git log --oneline
```

`git add` stages a snapshot; `git commit` records that snapshot locally. Review
the staged diff before committing. The `.gitignore` should exclude Python cache
files. Never commit passwords, API tokens, or private keys.

## 3. Create an empty repository on GitHub and push

In GitHub, create a repository named `lab-status`. A private repository is fine.
Leave README, .gitignore, and license initialization unchecked because you
already have local content. Copy its SSH or HTTPS clone URL.

Replace the sample URL below with your repository URL:

```bash
git remote add origin https://github.com/YOUR_USERNAME/lab-status.git
git remote -v
git push -u origin main
```

Use your configured SSH key or HTTPS credential manager/token. A GitHub account
password is not a Git push credential. Do not embed a token in the URL. If push
fails, check the remote URL, authentication, and repository access before retrying.

Refresh GitHub and verify the files are present. You now have a local repository
and a remote copy. `push` transfers your local commits to that remote.

## 4. Make a small change on a branch

```bash
git switch -c feature/personalize-message
```

In `app.py`, change only `DEFAULT_MESSAGE` to:

```python
DEFAULT_MESSAGE = "Welcome to John's DevOps lab!"
```

Run the tests again:

```bash
python3 -m unittest discover -s tests -v
```

Expect **one failure**, in `test_home_shows_default_message`. Read the assertion
output: the application changed, but the test still expects the old greeting.
This is an intentional contract change, so updating that expectation is valid.
For an unintended regression, fix the application instead of weakening the test.

In that test, replace its `assertIn` line with:

```python
self.assertIn(b"Welcome to John&#x27;s DevOps lab!", response["body"])
```

The apostrophe is escaped in HTML. A browser displays it normally; our test
checks the response bytes. Also update the default-message entry in README's
configuration table to match the new text.

Run the tests again: all 9 should pass. Start the app and verify the homepage.
If an old server is still running, restart it to load your source change.

## 5. Review and publish your change

```bash
git diff
git status
git add app.py tests/test_app.py README.md
git diff --cached
git commit -m "Personalize the homepage greeting"
git push -u origin feature/personalize-message
```

On GitHub, open a pull request from `feature/personalize-message` into `main`.
Suggested title: **Personalize the homepage greeting**.

In the description, explain the change and record your validation:

> Updates the default greeting for my home lab and adjusts the test and README.
> Validation: all 9 unit tests pass; checked the homepage in a browser.

Review the Files changed tab. In a team, a colleague would review this; for this
solo exercise, review and merge it yourself. There will be no CI check yet.
Merge using GitHub's normal merge option, then return to the terminal:

```bash
git switch main
git pull --ff-only origin main
python3 -m unittest discover -s tests -v
git log --oneline --graph --all -10
```

Keep the feature branch for now so you can inspect the history.

## 6. Practice a safe undo

On `main`, temporarily edit the greeting again, but do not stage or commit it.
Inspect the change with `git diff`. To discard ONLY that intentional practice
edit, run:

```bash
git restore app.py
git status
```

`git restore` discards uncommitted changes in the named file. Use it only after
checking the diff and confirming you do not need those changes. Your working
tree should now be clean.

## Done when you can explain

- Working tree vs. staging area vs. commit.
- Local branch vs. remote branch; commit vs. push.
- What a pull request contributes beyond simply pushing code.
- Why the test failed and why this particular expectation changed.
- Why passing local tests is different from an enforced CI check.
- How to see a diff before committing and synchronize after a remote merge.

Record your observations in `LEARNING_NOTES.md`. Your next lab packages this
same application into a container; keep this repository for the full sequence.
