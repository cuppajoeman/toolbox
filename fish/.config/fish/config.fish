fish_vi_key_bindings

# Disable the greeting
set fish_greeting

# Set the cursors to be a line
set fish_cursor_default line
set fish_cursor_insert line
set fish_cursor_visual line

if status is-interactive
  abbr --add --global vnceee "x11vnc -display :0 -geometry 1024x600"

  abbr --add --global uoftsshY "ssh -Y nolancal@teach.cs.utoronto.ca"
  abbr --add --global uoftssh "ssh -Y nolancal@teach.cs.utoronto.ca"
  abbr --add --global swap "setxkbmap -option caps:swapescape"
  abbr --add --global q "exit"
  abbr --add --global monitor "xrandr --output VGA-0 --mode 1280x1024 --rate 75.02"
  abbr --add --global vnceee "x11vnc -display :0 -geometry 1024x600"
  abbr --add --global h "cd ~/"
  abbr --add --global m "cd ~/Nextcloud"

  # Program
  abbr --add --global ydlm "youtube-dl -x --audio-format mp3 "
  abbr --add --global scrrec "ffmpeg -video_size 1280x1024 -framerate 25 -f x11grab -i :0.0 rec.mp4"
  abbr --add --global webcam "mplayer tv:// -tv driver=v4l2:width=640:height=480:device=/dev/video2 -fps 60 -vf screenshot"
  abbr --add --global mail "mailsync && neomutt"


   
  # Files
  abbr --add --global v "vim"
  abbr --add --global frc "vim ~/.config/fish/config.fish"
  abbr --add --global frld "source ~/.config/fish/config.fish"
  abbr --add --global vrc "vim ~/.vimrc"
  abbr --add --global brc "vim ~/.bashrc"
  abbr --add --global trc "vim ~/.tmux.conf"
  abbr --add --global irc "vim ~/.config/i3/config"
  abbr --add --global krc "vim ~/.config/kitty/kitty.conf"
  abbr --add --global bal "vim ~/.bash_aliases"
  abbr --add --global brld "source ~/.bashrc"
  abbr --add --global trld "tmux source-file ~/.tmux.conf"


  #  linux Aliases
  abbr --add --global pi "sudo pacman -S"
  abbr --add --global pr "sudo pacman -R"
  abbr --add --global as "apt-cache search"

  # Locations
  abbr --add --global bs "cd ~/basic-system"

  # Open ranger quickly
  abbr --add --global r "ranger"

  #-------------------------------------------------------------
  # Git Alias Commands
  #-------------------------------------------------------------
  abbr --add --global g "git status"
  abbr --add --global ga "git add"
  abbr --add --global gaa "git add ."
  #abbr --add --global gau "git add -u"
  abbr --add --global gc "git commit"
  #abbr --add --global gca "git commit -am"
  #abbr --add --global gb "git branch"
  #abbr --add --global gbd "git branch -d"
  #abbr --add --global gco "git checkout"
  #abbr --add --global gcob "git checkout -b"
  #abbr --add --global gt "git stash"
  #abbr --add --global gta "git stash apply"
  #abbr --add --global gm "git merge"
  #abbr --add --global gr "git rebase"
  #abbr --add --global gl "git log --oneline --decorate --graph"
  #abbr --add --global glog "git log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --"
  #abbr --add --global glga "git log --graph --oneline --all --decorate"
  #abbr --add --global gb "git branch"
  #abbr --add --global gs "git show"
  abbr --add --global gd "git difftool"
  # abbr --add --global gdc "git diff --cached"
  # abbr --add --global gbl "git blame"
  abbr --add --global gps "git push"
  abbr --add --global gpl "git pull"
  abbr --add --global gpl "git pull"
  # abbr --add --global gb "git branch"
  abbr --add --global gcl "git clone"
  # abbr --add --global gd "git diff"
  # abbr --add --global go "git checkout "
  # abbr --add --global gk "gitk --all&"
  # abbr --add --global gx "gitx --all"
end

# =================
# === FUNCTIONS ===
# =================

# Preventing nested ranger instances

function ranger
  if test -z "$RANGER_LEVEL"
    /usr/bin/ranger $argv
  else
    exit
  end
end

# open manpages in vim
function viman 
  man "$argv" | vim -R +":set ft=man" - ;
end

# search for word in pdf's
function pfind
  pdfgrep -n -i -e "$argv" *.pdf
end

function thread_compile
  gcc -g "$argv.c" -o "$argv" -lpthread 
end

# generate and open a temporary pdf
function ptemp
  pandoc "$argv" -o ~/temp/temp.pdf
  zathura --fork ~/temp/temp.pdf
end

