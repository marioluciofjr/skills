import random
import textwrap
import listas

def gerar_prompt():
    who = random.choice(listas.who)
    age = random.randint(18, 99)
    skintone = random.choice(listas.skintones)
    outfit = "white t-shirt, jeans and casual sneakers"
    hairstyle = random.choice(listas.hairstyles)
    background = "gray wall studio"
    camera_angle = "full body"
    pose = random.choice(listas.poses)
    aspect_ratio = "9:16"

    prompt = textwrap.dedent(f"""
        who: {who}
        age: {age}
        skintone: {skintone}
        outfit: {outfit}
        hairstyle: {hairstyle}
        background: {background}
        camera angle: {camera_angle}
        pose: {pose}
        aspect ratio: {aspect_ratio}
    """).strip()

    return prompt
