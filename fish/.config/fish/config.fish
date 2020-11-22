fish_vi_key_bindings

# Disable the greeting
set fish_greeting

# Set vim as default editor
set -gx EDITOR vim

# Set the cursors to be a line
set fish_cursor_default line
set fish_cursor_insert line
set fish_cursor_visual line

if status is-interactive
  abbr --add  vnceee "x11vnc -display :0 -geometry 1024x600"

  abbr --add  uoftsshY "ssh -Y nolancal@teach.cs.utoronto.ca"
  abbr --add  uoftssh "ssh -Y nolancal@teach.cs.utoronto.ca"
  abbr --add  swap "setxkbmap -option caps:swapescape"
  abbr --add  q "exit"
  abbr --add  monitor "xrandr --output VGA-0 --mode 1280x1024 --rate 75.02"
  abbr --add  vnceee "x11vnc -display :0 -geometry 1024x600"
  abbr --add  h "cd ~/"
  abbr --add  m "cd ~/Nextcloud"

  # Program
  abbr --add  ydlm "youtube-dl -x --audio-format mp3 "
  abbr --add  scrrec "ffmpeg -video_size 1280x1024 -framerate 25 -f x11grab -i :0.0 rec.mp4"
  abbr --add  webcam "mpv av://v4l2:/dev/video0 --profile=low-latency --untimed"
  abbr --add  mail "mailsync && neomutt"


   
  # Files
  abbr --add  v "vim"
  abbr --add  frc "vim ~/.config/fish/config.fish"
  abbr --add  frld "source ~/.config/fish/config.fish"
  abbr --add  vrc "vim ~/.vimrc"
  abbr --add  brc "vim ~/.bashrc"
  abbr --add  trc "vim ~/.tmux.conf"
  abbr --add  irc "vim ~/.config/i3/config"
  abbr --add  krc "vim ~/.config/kitty/kitty.conf"
  abbr --add  bal "vim ~/.bash_aliases"
  abbr --add  brld "source ~/.bashrc"
  abbr --add  trld "tmux source-file ~/.tmux.conf"


  #  linux Aliases
  abbr --add  pi "yay -S"
  abbr --add  pr "sudo pacman -R"
  abbr --add  as "apt-cache search"

  # Locations
  abbr --add  bs "cd ~/basic-system"

  # Open ranger quickly
  abbr --add  r "ranger"

  #-------------------------------------------------------------
  # Git Alias Commands
  #-------------------------------------------------------------
  abbr --add  g "git status"
  abbr --add  ga "git add"
  abbr --add  gaa "git add ."
  #abbr --add  gau "git add -u"
  abbr --add  gc "git commit"
  #abbr --add  gca "git commit -am"
  #abbr --add  gb "git branch"
  #abbr --add  gbd "git branch -d"
  #abbr --add  gco "git checkout"
  #abbr --add  gcob "git checkout -b"
  #abbr --add  gt "git stash"
  #abbr --add  gta "git stash apply"
  #abbr --add  gm "git merge"
  #abbr --add  gr "git rebase"
  #abbr --add  gl "git log --oneline --decorate --graph"
  #abbr --add  glog "git log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --"
  #abbr --add  glga "git log --graph --oneline --all --decorate"
  #abbr --add  gb "git branch"
  #abbr --add  gs "git show"
  abbr --add  gd "git difftool"
  # abbr --add  gdc "git diff --cached"
  # abbr --add  gbl "git blame"
  abbr --add  gps "git push"
  abbr --add  gpl "git pull"
  abbr --add  gpl "git pull"
  # abbr --add  gb "git branch"
  abbr --add  gcl "git clone"
  # abbr --add  gd "git diff"
  # abbr --add  go "git checkout "
  # abbr --add  gk "gitk --all&"
  # abbr --add  gx "gitx --all"
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
# function viman 
#   man "$argv" | vim -R +":set ft=man" - ;
# end

# search for word in pdf's
function pfind
  pdfgrep -n -i -e "$argv" *.pdf
end

# search the running processes for a given word
function psgrep
  ps aux | grep "$argv" 
end

#function thread_compile
#  gcc -g "$argv.c" -o "$argv" -lpthread 
#end

# generate and open a temporary pdf
function ptemp
  pandoc "$argv" -o ~/temp/temp.pdf
  zathura --fork ~/temp/temp.pdf
end

function ix
   "$argv" |  curl -F 'f:1=<-' ix.io
end
