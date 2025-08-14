import requests
import json
from datetime import datetime

def search_osdr_studies(organism):
    """Searches OSDR studies for a specific organism."""
    base_url = "https://osdr.nasa.gov/osdr/data/search"
    params = {
        "term": organism,
        "ffield": "organism",
        "fvalue": organism,
        "type": "cgene",
        "size": 1000,  # Fetch up to 1000 studies
        "sort_field": "_score",
        "sort_order": "desc"
    }
    try:
        response = requests.get(base_url, params=params, timeout=120) # increased timeout
        response.raise_for_status()
        return response.json()
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        print(f"Error searching for studies with organism {organism}: {e}")
        return None

def main():
    """Fetches and processes plant data from the GeneLab API."""
    plant_organisms = ["Arabidopsis thaliana", "Oryza sativa"]
    all_studies_data = []

    for organism in plant_organisms:
        print(f"Searching for studies with organism: {organism}")
        search_results = search_osdr_studies(organism)
        if search_results:
            total_hits = search_results.get("hits", {}).get("total", {})
            if isinstance(total_hits, dict):
                total_hits_value = total_hits.get("value", 0)
            else:
                total_hits_value = total_hits

            if total_hits_value > 0:
                hits = search_results.get("hits", {}).get("hits", [])
                for hit in hits:
                    study_data = hit.get("_source", {})
                    if study_data:
                        all_studies_data.append(study_data)

    print(f"Found a total of {len(all_studies_data)} studies for the specified organisms.")

    with open("data/genelab_osd.txt", "w") as f:
        f.write("OSD-id\thits\tpublicReleaseDate\tpublicReleaseDateYear\ttechnologyPlatform\ttechnologyType\tmeasurementType\tOrganismCount\tOrganism\tFactors\n")

        for study_data in all_studies_data:
            study_id = study_data.get('Study Identifier') or study_data.get('Accession')
            if not study_id:
                continue

            public_release_timestamp = study_data.get('Study Public Release Date')
            public_release_date = ''
            public_release_date_year = ''
            if public_release_timestamp:
                try:
                    # Convert to float first to handle string representations of numbers
                    timestamp = float(public_release_timestamp)
                    # It seems the timestamp is in seconds, not milliseconds
                    if timestamp > 10**12:
                         timestamp /= 1000
                    dt_object = datetime.fromtimestamp(timestamp)
                    public_release_date = dt_object.strftime('%Y-%m-%d')
                    public_release_date_year = dt_object.year
                except (ValueError, TypeError, OSError) as e:
                    print(f"Could not parse date: {public_release_timestamp} for study {study_id}. Error: {e}")

            technology_platform = study_data.get('Study Assay Technology Platform', '')
            technology_type = study_data.get('Study Assay Technology Type', '')
            measurement_type = study_data.get('Study Assay Measurement Type', '')

            factors = study_data.get('Study Factor Name', '')
            if isinstance(factors, list):
                collapsed_factors = ";".join(map(str, factors))
            else:
                collapsed_factors = str(factors)

            organism_name = study_data.get('organism', '')
            organism_count = len(organism_name.split(';')) if organism_name else 0

            def to_str(val):
                return str(val) if val is not None else ''

            f.write(f"{to_str(study_id)}\t1\t{to_str(public_release_date)}\t{to_str(public_release_date_year)}\t{to_str(technology_platform)}\t{to_str(technology_type)}\t{to_str(measurement_type)}\t{organism_count}\t{to_str(organism_name)}\t{to_str(collapsed_factors)}\n")

    print("Successfully wrote data to data/genelab_osd.txt")


if __name__ == "__main__":
    main()
