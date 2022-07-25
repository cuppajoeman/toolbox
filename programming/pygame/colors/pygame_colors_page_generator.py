import pygame

f = open('pygame_colors.html','w')

table_row = '<tr><td>{0}:</td><td style="background:rgb{1}">{1}</td></tr>'

content = '<div class="center-screen"><table>{}</table></div>'.format(''.join(table_row.format(k, v) for k, v in pygame.color.THECOLORS.items()))

styles = """
.center-screen {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  min-height: 100vh;
}
body {
    font-size: 4vw;
}
"""


skeleton = """
 <!DOCTYPE html>
<html>
<head>
<style>
{styles}
</style>
</head>
<body>
{content}
</body>
</html> 
"""

html = skeleton.format(styles=styles, content=content)

f.write(html)
