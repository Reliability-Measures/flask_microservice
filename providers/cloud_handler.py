from dropbox import dropbox
import json


def get_config_file(cloud_config, file='cloud_config_file'):

    provider = cloud_config.get('cloud_host')
    filename = cloud_config.get(file)
    key = cloud_config.get('cloud_access_key')

    if provider == 'dropbox':
        dbx = dropbox.Dropbox(key)
        res = dbx.files_list_folder(path="")
        rv = {}
        for entry in res.entries:
            rv[entry.name] = entry
            # print(entry.name)

        md, res = dbx.files_download("/" + filename)
        data = res.content
        # print(len(data), 'bytes; md:', md, type(data))
        try:
            return json.loads(data.decode())
        except Exception as exc:
            #print(exc)
            return data


if __name__ == '__main__':
    from common.config import cloud_provider

    print(get_config_file(cloud_provider, "cloud_rm_file"))

    #print(json.dumps(get_config_file(cloud_provider), indent=4))