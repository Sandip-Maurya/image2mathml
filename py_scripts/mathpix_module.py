
def img2lat_by_mathpix(file_name):
    import requests, json, os
    from dotenv import load_dotenv
    load_dotenv()

    app_id = os.environ.get('mathpix_app_id')
    app_key = os.environ.get('mathpix_app_key')
    # print(app_id, app_key)
  
    r = requests.post("https://api.mathpix.com/v3/text",
        files={"file": open(f"{file_name}","rb")},
        data={
          "options_json": json.dumps({
            "math_inline_delimiters": ["$", "$"],
            "math_display_delimiters": ["$$", "$$"],
            "rm_spaces": True
          })
        },
        headers={
            "app_id": app_id,
            "app_key": app_key
        }
    )
    return r.json()['text']

