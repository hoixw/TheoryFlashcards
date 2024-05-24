# Driving Theory Flashcards

This project scrapes flashcards off [https://mocktheorytest.com/](https://mocktheorytest.com/), a website which contains a direct copy of all the flashcards in the '4 in 1' app, the most popular paid app for driving theory. It then exports the scraped cards as Anki flashcards.

This project contains the flashcards outputted by the code in `/Flashcards`. In that folder are flashcards the for the car, motorbike, lorry, bus, and ADI tests, all of which are for GB (not NI).

## Setup
To reconstruct all the flashcards, go to `./src/` and run `setup.py`. This will install all the necessary dependencies. Run all the commands below in `./src/` also.

1. If you would like to reconstruct ALL flashcards, run `main.py`.
2. If you would like to reconstruct certain types of flashcards, these can be provided as command line options. For example, to reconstruct car and motorbike, run `main.py car motorbike`. These can be provided in any order. 
3. Downwloaded image files are stored in `/src/temp/`. These can be safely deleted after running, or deleted by running `main.py --clean`. 

## Dependencies
```
beautifulsoup4==4.12.3
genanki==0.13.1
python-slugify==8.0.4
Requests==2.32.2
```

## License

Apache.