import cv2

def get_templates():
    candy_colors = ['blue', 'green', 'orange', 'purple', 'red', 'yellow']

    template_images = {}
    for color in candy_colors:
        template_images[color] = cv2.imread(f'candies/{color}/{color}.png', cv2.IMREAD_UNCHANGED)
        template_images[color+'_sh'] = cv2.imread(f'candies/{color}/{color}_sh.png', cv2.IMREAD_UNCHANGED)
        template_images[color+'_sv'] = cv2.imread(f'candies/{color}/{color}_sv.png', cv2.IMREAD_UNCHANGED)
        template_images[color+'_p'] = cv2.imread(f'candies/{color}/{color}_p.png', cv2.IMREAD_UNCHANGED)

    template_images['Ñ'] = cv2.imread(f'candies/Special/special.png', cv2.IMREAD_UNCHANGED)
    return template_images

def classify_candy(image_path, template_images):
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    best_match = None
    best_score = 0.0
    
    for variant, template in template_images.items():
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val > best_score:
            best_score = max_val
            best_match = variant
    
    return best_match