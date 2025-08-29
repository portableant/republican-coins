# Roman Republican Coins from the Portable Antiquities Scheme

This repository holds data and scripts for working with Roman Republican coins from the Portable Antiquities Scheme and 
mapping them onto an instance of Peripleo. The Portable Antiquities Scheme (PAS) is a project in England and Wales to encourage the reporting of archaeological finds by the public. I built the database from 2006 - 2016, and my code is still in use now in 2025. There
are plans to replace what I built, but for now, it continues to serve its purpose. This demonstration shows how linked open data drawn from the database can be used to produce interesting visualizations and insights. 

The process to do this has been made considerably harder than when I was in post and I no longer have access to the same resources I did then. The British Museum IT team have removed lots of features making it harder to access data, assign recorders and finders and produce any insight into who recorded what, when or how their knowledge grew. They have also blocked search indexing and are using Cloudflare to try and prevent robots and programmatic access to data - or at least that is what they probably think. 

## Obtaining data to play with

I wanted images and data from the system and geographical context, so I wrote a series of scripts to extract and process the information I needed. These are all in Python and do the following:

- Scrape JSON data from the PAS website
- Geocode known as places to allows them to be mapped (badly)
- Download images of the coins
- Compress the images to a smaller size for use in Peripleo
- Create Linked Pasts geojson for use in Peripleo
- Split the images into obverse and reverse
- Create a ML model for coin identification
- Provide an example of running the scripts

## Installation

To run the python code I recommend using a virtual environment and then run the code snippets in the appropriate sections.

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## Scrape JSON to CSV

**To get round Cloudflare, use the `cloudscraper` library.** 
To scrape the JSON data from the PAS website and convert it to CSV format, run the following command:
```python
cd scrapers
python records.py
```
## To geocode the csv for missing grids
```python
cd ../scripts
python geocode.py
```

### Generate LinkedPasts geojson

To generate LinkedPasts geojson files, run the following command:

```python
cd ../scripts
python createLPgeoJson.py
``` 
This dataset is well structured and I didn't need to go off and find additional data. The IDs for linked open data already exist - this is a product of LAWDI and NOMISMA - and we have access to pleiadesID, dbPediaID, VIAF and Nomisma IDs (and WOEID and OS IDs, but hey, they went...) The LinkedPasts project provides a framework for publishing and connecting this data and these data features have links and types. 

## Download images
To download images of the coins, run the following command, some will fail as they are either missing or inaccessible (how that happened...) Some can be got from wikicommons. 

```python
python images.py
```
## Compress images 

To compress downloaded images assume you are in the scrapers folder, change directory and use the following script:

```python
cd ../scripts
python compress.py
```
Compressing keeps the size down so you actually run your peripleo instance off GH pages build. I don't trust the PAS images to remain accessible easily, so they are used under CC-BY license here (I changed the BM stance on using this in 2006)

## Mapping the coins 



## Split images

To split the images into obverse and reverse, run the following command:

```python
python splitImages.py   
```

# Proof of concept Machine Learning for RRC ID

The below scripts demonstrate a proof of concept for using machine learning to classify coin images based on their RRC IDs. The images are processed and used to train a model that can predict the RRC ID of new coin images. However, there's not many of each type on PAS. So, this would work far better taking images from CRRO and then using the data there to try and predict the PAS coin and RRC ID. I didn't have time to do it that way, so try this for now. 

## Classification

The classification script takes the images and uses obverse and reverse images for training, aligned to their respective rrcIDs. 

```python
python classification.py    
```

## Make predictions for images

This script takes the trained model and makes predictions on new images, which are stored in a folder. The first will give you the top choice, but that might be too specific.

```python
python scripts/classifier_single.py
```
This script will give you a set of predictions with their probabilities.

```python
python scripts/classifier_multiple.py
```


