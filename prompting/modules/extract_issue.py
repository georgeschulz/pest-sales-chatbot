from Generator import Generator
from Extractor import Extractor
from GenExtract import GenExtract

extract_issue = GenExtract(
    Generator('prompts/customer_issues_extractor/map_summarize_location_size.json'),
    Extractor(type="natural_language_to_dict", keys=["pest_id", "special_instructions", "location", "square_footage", 'property_type', 'acres']),
    print_intermediate=False
)

def extract_issue_analyzer(content):
    issues = extract_issue(content)
    mappings = {
        '0': 'none',
        '1': 'ants',
        '2': 'spiders',
        '3': 'termites',
        '4': 'rats',
        '5': 'mice',
        '6': 'roaches',
        '7': 'fleas',
        '8': 'ticks',
        '9': 'bed bugs',
        '10': 'bees',
        '11': 'wasps',
        '12': 'millipedes',
        '13': 'centipedes',
        '14': 'crickets',
        '15': 'earwigs',
        '16': 'mosquitoes'
    }

    issue_string = []
    if issues['pest_id'] != 'none':
        issues_ids = issues['pest_id'].split(',')
        #trim whitespace
        issues_ids = [issue.strip() for issue in issues_ids]
        for issue in issues_ids:
            issue_string.append(mappings[issue])
    
    target_pests = ', '.join(issue_string)
    issues['target_pests'] = target_pests
    return issues