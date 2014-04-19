import json
import sys
import base64
from Crypto import Random
from Crypto.Cipher import AES
from core.models import geoip
from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


reload(sys)
sys.setdefaultencoding("utf-8")

GENDER_CHOICES = (
    ('M', _(u'Male')),
    ('F', _(u'Female'))
)

USER_TYPE_PARTICIPANT = 'participant'
USER_TYPE_SCIENTIST = 'scientist'
USER_TYPE_DEPARTMENT = 'department'

USER_TYPE_CHOICES = (
    (USER_TYPE_PARTICIPANT, _(u'Participant')),
    (USER_TYPE_SCIENTIST, _(u'Scientist')),
    (USER_TYPE_DEPARTMENT, _(u'Department'))
)

UNIVERSITY_RESEARCH_CHOICES = (
    ('psychological', _(u'psychological (info/pics/egs of what this is below)')),
    ('neuroscience', _(u'neuroscience (as above)')),
)

BUSINESS_RESEARCH_CHOICES = (
    ('online research', _(u'online research')),
)

USER_TYPE = [USER_TYPE_PARTICIPANT, USER_TYPE_SCIENTIST, USER_TYPE_DEPARTMENT]


def json_result(request, data):
    response_data = json.dumps(data)
    if 'application/json' in request.META.get('HTTP_ACCEPT_ENCODING', None):
        mimetype = 'application/json'
    else:
        mimetype = 'text/plain'
    return HttpResponse(response_data, mimetype=mimetype)


def get_page(request, items, count_per_page):
    paginator = Paginator(items, count_per_page)
    page = request.GET.get('page')
    try:
        paginator.object_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paginator.object_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paginator.object_list = paginator.page(paginator.num_pages)
    return paginator


def get_client_ip(request):
    """
    Returns the IP of the request, accounting for the possibility of being
    behind a proxy.
    """
    ip = request.META.get('HTTP_X_FORWARDED_FOR', None)
    if ip:
        #X_FORWARDED_FOR returns client1, proxy1, proxy2,...
        ip = ip.split(', ')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', '')
    return ip


def get_location_by_ip(request):
    try:
        client_ip = get_client_ip(request)
        location = geoip.ipaddress_to_location(client_ip)
    except Exception as e:
        location = {
            'lng': 0,
            'lat': 0
        }
    return location


def get_location(request):
    """
    Returns longitude(lng) and latitude(lat)
    """
    try:
        is_location_by_ip = True
        if request.user.is_authenticated():
            basic_info = request.user.userprofile.basic_info.get(request.session.get('user_type'), None)
            lng = float(basic_info.get('lng', 0)) if basic_info else 0
            lat = float(basic_info.get('lat', 0)) if basic_info else 0
            if lng != 0 or lat != 0:
                is_location_by_ip = False
                location = {
                    'lng': lng,
                    'lat': lat
                }
        if is_location_by_ip:
            location = get_location_by_ip(request)
    except Exception as e:
        location = {
            'lng': 0,
            'lat': 0
        }
    return location


pad = lambda s: s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size)
unPad = lambda s: s[0:-ord(s[-1])]


def encrypt(val):
    """
    Return by AES and basic64 encrypt string
    """
    try:
        if isinstance(val, unicode):
            val = str(val)
        key = pad(settings.ENCRYPT_KEY)
        raw = pad(val)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))
    except Exception as e:
        return val


def decrypt(val):
    """
    Return by decrypt ciphertext raw string
    """
    try:
        key = pad(settings.ENCRYPT_KEY)
        enc = base64.b64decode(val)
        iv = enc[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        d_str = unPad(cipher.decrypt(enc[AES.block_size:]))
        if not isinstance(d_str, unicode):
            d_str = unicode(d_str, 'utf-8')
        return d_str
    except Exception as e:
        return val


def is_integer(val, positive=None):
    try:
        num = int(val)
        if positive is True:
            if num > 0:
                return num
            else:
                return 0
        elif positive is False:
            if num < 0:
                return num
            else:
                return 0
        else:
            return num
    except ValueError:
        return 0


def is_float(val, positive=None):
    try:
        num = float(val)
        if positive is True:
            if num > 0:
                return num
            else:
                return 0
        elif positive is False:
            if num < 0:
                return num
            else:
                return 0
        else:
            return num
    except ValueError:
        return 0


def errors_to_json(errors):
    """
    Convert a Form error list to JSON::

        >>> f = SomeForm(...)
        >>> errors_to_json(f.errors)
        {'field': ['This field is required']}
    """
    # Force error strings to be un-lazied.
    return json.dumps(
        dict(error=
        dict(
            (k, map(unicode, v))
            for (k, v) in errors.iteritems()
        ))
    )