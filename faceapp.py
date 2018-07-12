# standard import
import itertools
import mimetools
import mimetypes
import os.path
# local application/library specific imports
import callout
from utilities.log import Log

class File(object):

    """an object representing a local file"""
    path = None
    content = None

    def __init__(self, path):
        self.path = path
        self._get_content()

    def _get_content(self):
        """read image content"""

        if os.path.getsize(self.path) > 2 * 1024 * 1024:
            Log.fatal('image file size too large')
        else:
            with open(self.path, 'rb') as f:
                self.content = f.read()

    def get_filename(self):
        return os.path.basename(self.path)

class API(object):
    key = None
    secret = None
    server = None

    def __init__(self, key, secret, server):
        self.key = key
        self.secret = secret
        self.server = server
        Log.debug('API called')
        _setup_apiobj(self, self, [])

    def __str__(self):
        return 'API'


class _APIProxy(object):

    _api = None
    _urlbase = None

    def __init__(self, api, path):
        Log.debug('_APIProxy called')
        _setup_apiobj(self, api, path)

    def __call__(self, *args, **kargs):
        kargs['api_key'] = self._api.key
        kargs['api_secret'] = self._api.secret
        req = callout.create_request(self._urlbase, **kargs)
        content = callout.callout_post(req)
        form = _MultiPartForm()
        for (k,v) in kargs.iteritems():
            if isinstance(v, File):
                form.add_file(k, v.get_filename(), v.content)
            pass
        print(content)

    def __str__(self):
        return '_APIProxy / _api : %s / _urlbase : %s' % (self._api, self._urlbase)


def _setup_apiobj(self, api, path):
    if self is not api:
        Log.debug('self is not api')
        self._api = api
        self._urlbase = api.server + '/'.join(path)

    lvl = len(path)
    done = set()
    for i in _APIS:
        if len(i) <= lvl:
            continue
        cur = i[lvl]
        if i[:lvl] == path and cur not in done:
            done.add(cur)
            setattr(self, cur, _APIProxy(api, i[:lvl + 1]))


class _MultiPartForm(object):

    """Accumulate the data to be used when posting a form."""

    def __init__(self):
        self.form_fields = []
        self.files = []
        self.boundary = mimetools.choose_boundary()
        return

    def get_content_type(self):
        return 'multipart/form-data; boundary=%s' % self.boundary

    def add_field(self, name, value):
        """Add a simple field to the form data."""
        self.form_fields.append((name, value))
        return

    def add_file(self, fieldname, filename, content, mimetype=None):
        """Add a file to be uploaded."""
        if mimetype is None:
            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        self.files.append((fieldname, filename, mimetype, content))
        return

    def __str__(self):
        """Return a string representing the form data, including attached files."""
        # Build a list of lists, each containing "lines" of the
        # request.  Each part is separated by a boundary string.
        # Once the list is built, return a string where each
        # line is separated by '\r\n'.
        parts = []
        part_boundary = '--' + self.boundary

        # Add the form fields
        parts.extend(
            [part_boundary,
             'Content-Disposition: form-data; name="%s"' % name,'',value, ]
            for name, value in self.form_fields
        )

        # Add the files to upload
        parts.extend(
            [part_boundary,
             'Content-Disposition: file; name="%s"; filename="%s"' %
             (field_name, filename),
             'Content-Type: %s' % content_type,
             '',
             body,
             ]
            for field_name, filename, content_type, body in self.files
        )

        # Flatten the list and add closing boundary marker,
        # then return CR+LF separated data
        flattened = list(itertools.chain(*parts))
        flattened.append('--' + self.boundary + '--')
        flattened.append('')
        return '\r\n'.join(flattened)

_APIS = [
    '/detect',
    '/compare',
    '/search',
    '/faceset/create',
    '/faceset/addface',
    '/faceset/removeface',
    '/faceset/update',
    '/faceset/getdetail',
    '/faceset/delete',
    '/faceset/getfacesets',
    '/face/analyze',
    '/face/getdetail',
    '/face/setuserid'
]

_APIS = [i.split('/')[1:] for i in _APIS]


