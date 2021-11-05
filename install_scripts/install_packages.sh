yay -S $(grep -vE "^\s*#" $1  | tr "\n" " ") --needed --noconfirm
