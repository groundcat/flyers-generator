# flyers-generator

Generates flyers with captions from a csv file and a collection of background images.

- `all_captions.py` - Reads the column from the csv file and generates flyers with the background pictures from the `images` directory. The generated flyer is saved in the `output` directory.

- `random_caption.py` - Generates a single flyer in the `output` directory.

- `ifttt_webhook.py` - Generates a single flyer, upload it to imgbb using [imgbb API](https://api.imgbb.com/), trigger the [IFTTT webhook](https://help.ifttt.com/hc/en-us/articles/115010230347-Webhooks-service-FAQ) with playloads containing the captions and imgbb URL, and finally delete all generated flyers from the `output` directory.


## Dependencies

```
pip install python-dotenv
php install PIL
```

