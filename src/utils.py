import mimetypes
import os
import random
from pathlib import Path

import genanki
import requests
from slugify import slugify

# Create Question Models
__ONE_IMAGE_MODEL = genanki.Model(
    1607392388,
    'One Image Model',
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
        {'name': 'Options'},
        {'name': 'MyMedia'}
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Question}}<br><br>{{MyMedia}}<br><br>{{Options}}',
            'afmt': '{{Answer}}',
        },
    ]
)

__NO_IMAGE_MODEL = genanki.Model(
    1607392389,
    'No Image Model',
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
        {'name': 'Options'}
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Question}}<br><br>{{Options}}',
            'afmt': '{{Answer}}',
        },
    ]
)

__FOUR_IMAGE_MODEL = genanki.Model(
    1607392390,
    'Four Image Model',
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
        {'name': 'MyMedia1'},
        {'name': 'MyMedia2'},
        {'name': 'MyMedia3'},
        {'name': 'MyMedia4'}                   
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Question}}<br><br>A.<br>{{MyMedia1}}<br>B.<br>{{MyMedia2}}<br>C.<br>{{MyMedia3}}<br>D.<br>{{MyMedia4}}',
            'afmt': '{{Answer}}',
        },
    ]
)

__FIVE_IMAGE_MODEL = genanki.Model(
    1607392391,
    'Five Image Model',
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
        {'name': 'MyMedia'},
        {'name': 'MyMedia1'},
        {'name': 'MyMedia2'},
        {'name': 'MyMedia3'},
        {'name': 'MyMedia4'}                   
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Question}}<br><br>{{MyMedia}}<br><br>A.<br>{{MyMedia1}}<br>B.<br>{{MyMedia2}}<br>C.<br>{{MyMedia3}}<br>D.<br>{{MyMedia4}}',
            'afmt': '{{Answer}}',
        },
    ]
)

def __parse_questions(url):
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        results = []

        for question_data in data['questions']:
            question = question_data['text']

            # Initialize the option_texts and image_urls arrays
            option_texts = []
            image_urls = []

            # Add the question's image_url if it's not null
            if question_data['image_url']:
                image_urls.append(question_data['image_url'])

            for idx, option in enumerate(question_data['options']):
                prefix = chr(65 + idx) + ". "  # 'A. ', 'B. ', 'C. ', 'D. '
                
                # Get the option text, or an empty string if it's null
                option_text = option['text'] if option['text'] is not None else ""
                
                # Add the prefix to the option text if it's non-null
                if option_text:
                    option_text = prefix + option_text
                
                option_texts.append(option_text)
                
                # Add the image_url to the image_urls array if it's not null
                if option['image_url']:
                    image_urls.append(option['image_url'])

            correct_answer = ""
            for idx, option in enumerate(question_data['options']):
                if option['is_correct']:
                    answer_letter = chr(65 + idx)  # Convert index to letter (A, B, C, D)
                    correct_answer = f"Correct: {answer_letter}<br>\n<br>\n{question_data['explanation']}"
                    break

            # Append the result to the results list
            results.append([question, option_texts, image_urls, correct_answer])
    
    else:
        raise TypeError(f"""
        Failed to fetch question data.\n
        Response: {response}\n
        Status code: {response.status_code}
        """)
    
    return results


def __download_image(url, output_dir):
    """Download an image and save it to the specified directory."""
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    response.raise_for_status()

    img_mime_type = mimetypes.guess_type(url.split("?")[0], strict=True)
    img_extension = mimetypes.guess_extension(img_mime_type[0], strict=True)
    img_name = f"{slugify(url.split('/')[-1].split('.')[0])}{img_extension}"
    img_path = os.path.join(output_dir, img_name)

    with open(img_path, 'wb') as f:
        f.write(response.content)

    return img_name


def __build_package(name, url, test):
    """Build an Anki package from the given IDs."""
    media_files = []
    my_deck = genanki.Deck(random.randrange(1 << 30, 1 << 31), name)

    results = __parse_questions(url)
    count = 1
    
    for question, option_texts, image_urls, correct_answer in results:
    
        # There will either be 0, 1 or 4 images, pick model off this
        # Apparently there are also 5
        if len(image_urls) == 0:
            model = __NO_IMAGE_MODEL
            fields = [question, correct_answer, '\n<br>\n'.join(option_texts)]
            
        elif len(image_urls) == 1:
            model = __ONE_IMAGE_MODEL
            output_dir = Path('./temp').absolute()
            image_path = __download_image(image_urls[0], output_dir)
            media_files.append("temp/" + str(image_path))
            fields = [question, correct_answer, '\n<br>\n'.join(option_texts), f'<img src="{image_path}">']
        
        elif len(image_urls) == 4:
            model = __FOUR_IMAGE_MODEL
            output_dir = Path('./temp').absolute()
            image_paths = [__download_image(url, output_dir) for url in image_urls]
            media_files.extend(["temp/" + str(image_path) for image_path in image_paths])
            fields = [question, correct_answer] + [f'<img src="{image_path}">' for image_path in image_paths]

        elif len(image_urls) == 5:
            model = __FIVE_IMAGE_MODEL
            output_dir = Path('./temp').absolute()
            image_paths = [__download_image(url, output_dir) for url in image_urls]
            media_files.extend(["temp/" + str(image_path) for image_path in image_paths])
            fields = [question, correct_answer] + [f'<img src="{image_path}">' for image_path in image_paths]
        
        else:
            raise ValueError("Unsupported number of images")
    
        # Create a Note instance and add it to a Deck
        my_note = genanki.Note(
            model=model,
            fields=fields
        )
        my_deck.add_note(my_note)
        print(f"Flashcard {count} created on deck {name} for {test}")
        count += 1
    

    package = genanki.Package(my_deck)
    package.media_files = media_files
    package.write_to_file(f'../Flashcards/{test}/{name}.apkg')
    
    print(f"\n\nAnki package for {name} in {test} created successfully!\n\n")

def build_flashcards(URL_DICT, test):
    """Takes URL_DICT: Dictionary of flashcard URLs, test: string corresponding to test"""

    ## make folder for media and flashcards
    Path("temp/").mkdir(exist_ok=True)
    Path("../flashcards/").mkdir(exist_ok=True)
    Path(f"../flashcards/{test}/").mkdir(exist_ok=True)

    for name, url in URL_DICT.items():
        __build_package(name, url, test)