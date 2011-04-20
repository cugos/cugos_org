from django.http import HttpResponse, HttpResponseServerError

# graphviz stuff
# Use python's ability to run a command as if from the shell
from subprocess import Popen,PIPE

# import the app script to actually generate the image
from modelviz.graph import generate_dot

# model graph generator
def graph(request, app=None):
  if app:
    if app == "all":
      content = generate_dot(all_applications=True)
    else:
      app_labels = [app]
      content = generate_dot(app_labels)
  else:
    content = generate_dot(app_labels=['flaws','auth','gis',])

  response = HttpResponse(mimetype='image/png')
  try:
      dot = Popen(['dot','-Tpng'],stdin=PIPE,stdout=PIPE)
      dot.stdin.write(content)
      dot.stdin.close()
      response.write(dot.stdout.read())
      dot.stdout.close()
  except Exception, E:
      return HttpResponseServerError('Sorry a problem occured when generating the graphviz image (is the "dot" command installed on your system?). System error: %s' % E)
  return response

# wrap the main graph function to add a view to catch and render a specific model or 'all'
def graph_app(request, app):
  return graph(request,app)