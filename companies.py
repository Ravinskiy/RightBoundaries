import csv
import json
from collections import defaultdict

INPUT_FILE_PATH = 'Webpages_LinkedInPages_Fortune100_normalized.csv'
COMPANIES_OUTPUT_FILE_PATH = 'companies.json'
LN_PAGES_OUTPUT_FILE_PATH = 'linkedin_pages.json'
DOMAINS_OUTPUT_FILE_PATH = 'domains.json'


if __name__ == '__main__':
    csv_reader = csv.DictReader(
        open(INPUT_FILE_PATH),
        fieldnames=['company_name', 'domain', 'linkedin']
    )
    company_names = defaultdict(lambda: defaultdict(list))
    ln_pages = defaultdict(dict)
    domains = defaultdict(dict)
    for record in csv_reader:
        company_name = record['company_name']
        domain = record['domain']
        ln_page = record['linkedin']
        if company_name and ln_page:
            company_names[company_name]['ln_pages'].append(ln_page)
        if company_name and domain:
            company_names[company_name]['domains'].append(domain)
    for company, data in company_names.items():
        company_ln_pages = data['ln_pages']
        company_domains = data['domains']
        for ln_page in company_ln_pages:
            ln_pages[ln_page]['ln_pages'] = company_ln_pages
            ln_pages[ln_page]['domains'] = company_domains
        for domain in company_domains:
            domains[domain]['ln_pages'] = company_ln_pages
            domains[domain]['domains'] = company_domains

    json.dump(
        company_names,
        open(COMPANIES_OUTPUT_FILE_PATH, 'w'),
        indent=2
    )
    json.dump(
        ln_pages,
        open(LN_PAGES_OUTPUT_FILE_PATH, 'w'),
        indent=2
    )
    json.dump(
        domains,
        open(DOMAINS_OUTPUT_FILE_PATH, 'w'),
        indent=2
    )

