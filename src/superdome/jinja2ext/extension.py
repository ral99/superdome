import jinja2

from whodat.extension import Extension

class Jinja2Renderer:
    """Renderer for Jinja2 templates."""

    def __init__(self, template_dir):
        """Load and compile templates."""
        self._env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
        self._env.compile_templates('%s_compiled.py' % template_dir, ignore_errors=False)

    def render(self, filename, context=None):
        """Render the specified template file with context."""
        return self._env.get_template(filename).render(context or {})

class Jinja2Extension(Extension):
    """Extension that adds a Jinja2Renderer instance to request."""

    def __init__(self, template_dir, attr_name):
        """Initialize a Jinja2Renderer instance."""
        self._attr_name = attr_name
        self._jinja2_renderer = Jinja2Renderer(template_dir)

    def process_request(self, request):
        """Set the Jinja2Renderer instance attribute in request."""
        setattr(request, self._attr_name, self._jinja2_renderer)

    def process_response(self, request, response):
        """Do nothing."""
        pass
