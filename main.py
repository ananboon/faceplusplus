## d
import config

API = 'compare'
payload = {'api_key': config.API_KEY,
           'api_secret': config.API_SECRET,
           'image_url1': config.IMG_URL1,
           'image_url2': config.IMG_URL2
           }


# print (callout.callout_post_message(config.SERVER, payload))
# print (
#     callout.callout_post(
#         callout.create_request(config.SERVER, payload)
#     )
# )
#
# print (
#     callout.callout_post(
#         callout.create_request(config.SERVER, payload)
#     )
# )

def init():
    from faceapp import API
    return API(config.API_KEY, config.API_SECRET, config.SERVER)


api = init()


def _run():
    msg = 'Welcome to Test Face++ program'
    from IPython import embed
    embed(banner2=msg)


if __name__ == '__main__':
    _run()
