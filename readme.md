# flyers-generator

Generates flyers with captions from a csv file and a collection of background images.

- `all_captions.py` - Reads the column from the csv file and generates flyers with the background pictures from the `images` directory. The generated flyer is saved in the `output` directory.

- `random_caption.py` - Generates a single flyer in the `output` directory.

- `ifttt_webhook.py` - Generates a single flyer, upload it to ImgBB using [ImgBB API](https://api.imgbb.com/), trigger the [IFTTT webhook](https://help.ifttt.com/hc/en-us/articles/115010230347-Webhooks-service-FAQ) with playloads containing the captions and imgbb URL, and finally delete all generated flyers from the `output` directory.

- `batch_image_resize.py` - Resizes all images in the `images` directory and saves the output in the `resized` directory.

## Dependencies

```
pip install python-dotenv
pip install Pillow
```

## Configuration

Create and edit the `.env` file based on the `.env.example` example file. Create directories `images` and `output`.

To run the `ifttt_webhook.py` script, you will need the API keys for [IFTTT](https://help.ifttt.com/hc/en-us/articles/115010230347-Webhooks-service-FAQ) and [ImgBB](https://api.imgbb.com/) and create an IFTTT Applet with a webhook trigger. In my script,  `{{Value1}}` given in the webhook is the caption and `{{Value2}}` is the URL of the image uploaded to ImgBB.

## Demo

![](https://raw.githubusercontent.com/groundcat/flyers-generator/main/output.example/1_Rememberyo.jpg)

![](https://raw.githubusercontent.com/groundcat/flyers-generator/main/output.example/2_YoumatterY.jpg)

![](https://raw.githubusercontent.com/groundcat/flyers-generator/main/output.example/3_WefallWebr.jpg)

![](https://raw.githubusercontent.com/groundcat/flyers-generator/main/output.example/4_Youaremore.jpg)

![](https://raw.githubusercontent.com/groundcat/flyers-generator/main/output.example/5_Allyouneed.jpg)

![](https://raw.githubusercontent.com/groundcat/flyers-generator/main/output.example/6_Takeitoned.jpg)

