# 🛠️ Git High-Yield Cheatsheet

```bash
# Inspection & Staging
git status -sb                              # Short status with branch info
git diff --staged                           # View changes staged for commit
git log --oneline --graph --decorate -n 20  # Pretty visual commit graph

# Branching & Worktrees
git checkout -b feature/new-branch          # Create and switch to new branch
git worktree add ../feature-worktree main   # Add isolated worktree branch
git worktree list                           # View active worktrees

# Advanced History Manipulation
git rebase -i HEAD~4                        # Interactive rebase last 4 commits
git commit --amend --no-edit                # Amend staged changes to last commit
git reflog                                  # Emergency log of all HEAD movements
git cherry-pick <commit-sha>                # Apply specific commit to current branch

# Recovery & Undo
git restore <file>                          # Discard unstaged changes in file
git restore --staged <file>                 # Unstage file without losing modifications
git reset --soft HEAD~1                     # Undo last commit, keep changes staged
```
