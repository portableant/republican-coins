import csv
import json

def convert_csv_to_geojson(csv_file, geojson_file):
    """
    Converts a CSV file with lat/lon coordinates into a GeoJSON file.
    """
    geojson = {
        "type": "FeatureCollection",
        "indexing": {
            "@context": "https://schema.org/",
            "@type": "Dataset",
            "name": "Roman Republican Coins from the Portable Antiquities Scheme",
            "description": "An enriched dataset of Roman Republican coins from the Portable Antiquities Scheme",
            "license": "https://creativecommons.org/licenses/by/4.0/",
            "identifier": "https://finds.org.uk/database/search/results/broadperiod/ROMAN/reeceID/1/"
        },
        "features": []
    }

    try:
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # Clean up and validate coordinates
                    lat_str = row.get('fourFigureLat', '').strip()
                    lon_str = row.get('fourFigureLon', '').strip()

                    # Skip records with empty or invalid coordinates
                    if not lat_str or not lon_str:
                        print(f"Skipping row with findIdentifier '{row.get('findIdentifier', 'N/A')}' due to missing coordinates.")
                        continue

                    lat = float(lat_str)
                    lon = float(lon_str)

                    # Create a GeoJSON Feature
                    # Format 'created' date to YYYY
                    created_raw = row.get('created')
                    created_year = None
                    if created_raw:
                        try:
                            created_year = str(created_raw).strip()[:4]
                            if not created_year.isdigit():
                                created_year = None
                        except Exception:
                            created_year = None
                    
                    feature = {
                        "@id": f"https://finds.org.uk/database/artefacts/record/id/{row.get('id')}",
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [lon, lat]
                        },
                        "properties": {
                            "findIdentifier": row.get('findIdentifier'),
                            "oldFindID": row.get('old_findID'),
                            "objecttype": row.get('objecttype'),
                            "broadperiod": row.get('broadperiod'),
                            "description": row.get('description'),
                            "county": row.get('county'),
                            "district": row.get('district'),
                            "parish": row.get('parish'),
                            "knownas": row.get('knownas'),
                            "ruler": row.get('rulerName'),
                            "moneyer": row.get('moneyerName'),
                            "denomination": row.get('denominationName'),
                            "mint": row.get('mintName'),
                            "manufacture": row.get('manufactureTerm'),
                            "rrcType": row.get('rrcType'),
                            "rrcID": row.get('rrcID'),
                            "reeceID": row.get('reeceID').
                            "nomismaIssuer": row.get('rulerNomisma'),
                            "nomismaMint": row.get('nomismaMintID'),
                            "pleiadesID": row.get('pleiadesID'),
                            "issuerDbPedia": row.get('rulerDbpedia'),
                            "metal": row.get('metal'),
                            "materialTerm": row.get('materialTerm'),
                            "weight": row.get('weight'),
                            "date_from": row.get('fromdate'),
                            "date_to": row.get('todate'),
                            "institution": row.get('institution'),
                            "created": created_year,
                        }
                    }
                    filename = row.get('filename', '').strip()
                    if filename:
                        baseurl = 'https://republican-coins.museologi.st/images/'
                        depiction_url = baseurl + filename
                        oldfindID = row.get('old_findID', '').strip()
                        feature['depictions'] = [
                            {
                                "@id": depiction_url,
                                "thumbnail": depiction_url,
                                "label": f"A depiction of {oldfindID}"
                            }
                        ]
                    description = row.get('description', '').strip()
                    if description:
                        feature['descriptions'] = [
                            {
                                "value": description
                            }
                        ]
                    rrc_id = row.get('rrcID', '').strip()
                    if rrc_id:
                        feature['types'] = [
                            {
                                "identifier": f"https://nomisma.org/id/{rrc_id.lower()}",
                                "label": f"Nomisma type: {rrc_id.lower()}"
                            }
                        ]
                    # Add 'when' key only if 'fromDate' is present
                    from_date = row.get('fromdate', '').strip().split('.')[0]
                    if from_date:
                        to_date = row.get('todate', '').strip().split('.')[0]
                        if to_date:
                            feature['when'] = {
                                "timespans": [
                                    {
                                        "start": {
                                            "in": f"{from_date}" if from_date else ""
                                        },
                                        "end": {
                                            "in": f"{to_date}" if to_date else "",
                                        }
                                    }
                                ],
                                "periods": [
                                    {
                                        "name": "Roman Republican 510 BC - 27 BC",
                                        "uri": "http://n2t.net/ark:/99152/p08m57h65c8"
                                    }
                                ],
                                "label": "for a century during the Roman period",
                                "certainty": "certain",
                                "duration": "P100Y"
                            }

                    links = []
                    pleiades_id = row.get('pleiadesID', '').strip()
                    if pleiades_id and pleiades_id.replace('.', '', 1).isdigit():
                        pleiades_id = str(int(float(pleiades_id)))
                    nomisma_mint_id = row.get('nomismaMintID', '').strip()
                    moneyer_id = row.get('moneyerID', '').strip()
                    dbpedia_issuer = row.get('rulerDbpedia', '').strip()    
                    nomisma_issuer = row.get('rulerNomisma', '').strip()
                    nomisma_reece_period = row.get('reeceID', '').strip()
                    if nomisma_issuer:
                        links.append({
                            "identifier": f"https://nomisma.org/id/{nomisma_issuer}",
                            "type": "seeAlso",
                            "label": f"Nomisma ruler {nomisma_issuer}"
                        })
                    if pleiades_id:
                        links.append({
                            "identifier": f"https://pleiades.stoa.org/places/{pleiades_id}",
                            "type": "seeAlso",
                            "label": f"Pleiades place {pleiades_id}"
                        })
                    if nomisma_mint_id:
                        links.append({
                            "identifier": f"https://nomisma.org/id/{nomisma_mint_id}",
                            "type": "seeAlso",
                            "label": f"Nomisma mint {nomisma_mint_id}"
                        })
                    if(nomisma_reece_id):
                        links.append({
                            "identifier": f"https://nomisma.org/id/{nomisma_reece_id}",
                            "type": "seeAlso",
                            "label": "Nomisma Reece Period 1"
                        })
                    if moneyer_id:
                        links.append({
                            "identifier": f"https://nomisma.org/id/{moneyer_id}",
                            "type": "seeAlso",
                            "label": f"Nomisma moneyer {moneyer_id}"
                        })
                    if dbpedia_issuer:
                        links.append({
                            "identifier": f"https://dbpedia.org/resource/{dbpedia_issuer}",
                            "type": "seeAlso",
                            "label": f"DBpedia resource for  {dbpedia_issuer}"
                        })
                    if links:
                        feature['links'] = links

                    geojson['features'].append(feature)
                except (ValueError, TypeError) as e:
                    print(f"Skipping row with findIdentifier '{row.get('findIdentifier', 'N/A')}' due to invalid coordinate data: {e}")
                    continue

        with open(geojson_file, 'w', encoding='utf-8') as f:
            json.dump(geojson, f, indent=2, ensure_ascii=False)
                        
        print(f"\nSuccessfully converted {len(geojson['features'])} valid records to {geojson_file}")
                            
    except FileNotFoundError:
        print(f"Error: The file '{csv_file}' was not found.")
    except Exception as e:  
        print(f"An unexpected error occurred: {e}")
                            
if __name__ == "__main__":  
    input_csv = "../data/geocoded.csv"
    output_geojson = "../data/republican.geojson"
    convert_csv_to_geojson(input_csv, output_geojson)
                            
                            
