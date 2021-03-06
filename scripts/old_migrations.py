import os
import json
import codecs

from dateutil.parser import parse

from scrapi.util import make_dir
from scrapi.util import safe_filename


def migrate_from_old_scrapi():
    for dirname, dirs, filenames in os.walk('archive'):
        for filename in filenames:
            oldpath = os.path.join(dirname, filename)
            source, sid, dt = dirname.split('/')[1:]

            if parse(dt).isoformat() != dt:
                dt = parse(dt).isoformat()
                sid = safe_filename(sid)
                newpath = os.path.join('archive', source, sid, dt, filename)

                make_dir(os.path.dirname(newpath))

                if filename == 'manifest.json':
                    with open(oldpath) as old:
                        old_json = json.load(old)
                    new_json = {
                        'harvesterVersion': old_json['harvester_version'],
                        'normalizeVersion': old_json['harvester_version'],
                        'timestamp': dt,
                        'source': source,
                        'id': sid
                    }
                    new_json = json.dumps(new_json, indent=4, sort_keys=True)
                    with open(newpath, 'w') as new:
                        new.write(new_json)
                    os.remove(oldpath)
                else:
                    os.rename(oldpath, newpath)

                print '{} -> {}'.format(oldpath, newpath)


def migrate_plos_to_xml():
    import xmltodict
    for dirname, dirs, filenames in os.walk('archive/plos'):
        for filename in filenames:
            if filename == 'raw.json':
                jsonp = os.path.join(dirname, filename)
                xmlp = os.path.join(dirname, 'raw.xml')
                raw = json.load(open(jsonp))

                print '{} -> {}'.format(jsonp, xmlp)

                with codecs.open(xmlp, 'w', encoding='utf-8') as xml:
                    xml.write(xmltodict.unparse({'doc': raw}))
