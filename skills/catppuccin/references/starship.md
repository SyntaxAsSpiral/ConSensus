# Starship

Mocha. Directory is blue, the branch is green, status is red, a clean prompt is mauve, an error is red.

```toml
format = """$directory$git_branch$git_status$character"""

[directory]
format = "[$path]($style) "
style = "bold #89b4fa"
truncation_length = 3
fish_style_pwd_dir_length = 1

[git_branch]
format = "[$symbol$branch]($style) "
symbol = " "
style = "bold #a6e3a1"

[git_status]
format = "[$all_status$ahead_behind]($style) "
style = "bold #f38ba8"
conflicted = "󰞇"
ahead = "⇡"
behind = "⇣"
diverged = "⇕"
up_to_date = ""
untracked = "?"
stashed = "$"
modified = "!"
staged = "+"
renamed = "»"
deleted = "✘"

[character]
success_symbol = "[╲)](#cba6f7)"
error_symbol = "[╲)](#f38ba8)"
vimcmd_symbol = "[╲)](#89b4fa)"
```
