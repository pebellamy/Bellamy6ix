from dotenv import load_dotenv
from time import sleep
import os
import io
import warnings
from PIL import Image
from flask import Blueprint, jsonify, current_app, request, url_for
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

generate_image = Blueprint('generate_image', __name__)

load_dotenv()


# Set up the client
stability_api = client.StabilityInference(
    key=os.getenv("STABILITY_KEY"),
    verbose=True, # Set this to False to disable logging
    engine="stable-diffusion-xl-1024-v1-0"
)

def stability_ai_request(prompt):
    # Detemine seed by hashing the prompt
    seed = abs(hash(prompt))

    # For more information on the generate function, see the documentation: https://platform.stability.ai/docs/features/text-to-image#Python
    answers = stability_api.generate(
        prompt=prompt,
        seed=0,         # If a seed is provided, the resulting generated image will be deterministic.
                        # What this means is that as long as all generation parameters remain the same, you can always recall the same image simply by generating it again.
                        # Note: This isn't quite the case for Clip Guided generations, which we'll tackle in a future example notebook.
        steps=30,       # Amount of inference steps performed on image generation. Defaults to 30.
        cfg_scale=10.0,  # Influences how strongly your generation is guided to match your prompt.
                        # Setting this value higher increases the strength in which it tries to match your prompt.
                        # Defaults to 7.0 if not specified.
        width=1024,     # Width of the generated image. Defaults to 512 if not included.
        height=1024,    # Height of the generated image. Defaults to 512 if not included.
        samples=1,      # Number of images to generate. Defaults to 1 if not included.
        sampler=generation.SAMPLER_K_DPMPP_2M    # Choose which sampler we want to denoise our generation with.
                                                 # Defaults to k_dpmpp_2m if not specified. Clip Guidance only supports ancestral samplers.
                                                 # (Available Samplers: ddim, plms, k_euler, k_euler_ancestral, k_heun, k_dpm_2, k_dpm_2_ancestral, k_dpmpp_2s_ancestral, k_lms, k_dpmpp_2m, k_dpmpp_sde)
    )

    # Generate the image then save it to a file
    img_urls = []
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn(
                    "Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again.")
            if artifact.type == generation.ARTIFACT_IMAGE:

                img = Image.open(io.BytesIO(artifact.binary))
                # Save our generated images with their seed number as the filename. should go in static/stability_ai_output/
                img.save(f"static/stability_ai_output/{seed}.png")
                image_url = url_for('serve_generated_image', filename=f"{seed}.png")
                img_urls += image_url
        return img_urls
                

@generate_image.route("/generate-image", methods=["POST"])
def generate_image_route():
    user_prompt = request.form.get('prompt')
    full_prompt = f"""
     Illustrate in the style of a New Yorker cartoon: '{user_prompt}'.
    """
    if current_app.config['DEBUG']:
        # Mock a delay
        sleep(3)
        # Mock API response from Open AI API (https://platform.openai.com/docs/guides/images/usage)
        image_urls = []
        for seed in ['1409325373574066945', '2440169983116909559', '6170566389842304918', '8090517238952629365']
            image_url = url_for('serve_generated_image', filename=f"{seed}.png")
            image_urls += image_url
    else:
        image_urls = stability_ai_request(full_prompt)
        
    return jsonify({'image_urls': image_urls})
