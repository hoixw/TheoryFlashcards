import mimetypes
import os
import random
from pathlib import Path

import genanki
import requests
from bs4 import BeautifulSoup
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


def __parse_html_question(id):
    """Parse the HTML response from the question (POST) request."""
    url = f"https://mocktheorytest.com/checkquestion/car/all/0/{id}/"
    response = requests.post(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the question
        question = soup.find('span', class_='question-text').text

        # Extract the answer options
        options = soup.find_all('li', id=lambda x: x and x.startswith('li_'))
        option_texts = [option.find('p').text for option in options]

        # Extract image URLs within the 'minheight' div
        minheight_div = soup.find('div', class_='minheight')
        image_tags = minheight_div.find_all('img')
        image_urls = [tag['src'] for tag in image_tags]

        return question, option_texts, image_urls
    else:
        raise TypeError(f"""
        Failed to fetch question data.\n
        Response: {response}\n
        Status code: {response.status_code}
        """)


def __parse_html_answer(id):
    """Parse the HTML response from the answer (GET) request."""
    base_url = "https://mocktheorytest.com/highway-code/post.php"
    answers = ['a', 'b', 'c', 'd']

    for answer in answers:
        params = {
            "answer_a": answer,
            "id": id,
            "amount_correct": "",
            "incorrect_ids": "",
            "rx": ""
        }
        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            if soup.find('span', class_='correct'):
                result_text = soup.find('span', class_='result-normal').text
                return f"Correct: {answer.upper()}<br>\n<br>\n{result_text}"
        else:
            raise TypeError(f"""
            Failed to fetch answer data.\n
            Response: {response}\n
            Status code: {response.status_code}
            """)

    raise TypeError("No correct answer found.")


def __download_image(subdir, output_dir):
    """Download an image and save it to the specified directory."""
    subdir = subdir.replace(" ", "")    
    url = f"https://mocktheorytest.com{subdir}"
    
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    response.raise_for_status()

    img_mime_type = mimetypes.guess_type(url.split("?")[0], strict=True)
    img_extension = mimetypes.guess_extension(img_mime_type[0], strict=True)
    img_name = f"{slugify(url.split('/')[-1].split('.')[0])}{img_extension}"
    img_path = os.path.join(output_dir, img_name)

    with open(img_path, 'wb') as f:
        f.write(response.content)

    return img_name


def __build_package(name, IDs, test):
    """Build an Anki package from the given IDs."""
    media_files = []
    my_deck = genanki.Deck(random.randrange(1 << 30, 1 << 31), name)
    
    for id in IDs:
        # Parse the POST request HTML
        question, option_texts, image_urls = __parse_html_question(id)
    
        # Parse the GET request HTML
        correct_answer = __parse_html_answer(id)
    
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
        print(f"Flashcard {id} created on deck {name} for {test}")
    

    package = genanki.Package(my_deck)
    package.media_files = media_files
    package.write_to_file(f'../Flashcards/{test}/{name}.apkg')
    
    print(f"\n\nAnki package for {name} in {test} created successfully!\n\n")

def build_flashcards(ID_DICT, test):
    """Takes ID_DICT: Dictionary of flashcard IDs, test: string corresponding to test"""

    ## make folder for media and flashcards
    Path("temp/").mkdir(exist_ok=True)
    Path("../flashcards/").mkdir(exist_ok=True)
    Path(f"../flashcards/{test}/").mkdir(exist_ok=True)

    for name, IDs in ID_DICT.items():
        __build_package(name, IDs, test)