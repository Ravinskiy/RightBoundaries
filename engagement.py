import csv
from datetime import datetime
from operator import itemgetter

INPUT_FILE_PATH = 'engagements/eng.csv'
OUTPUT_FILE_PATH = 'engagement_rate.csv'
HEADERS = ['Date', 'campaign_id', 'engagement_rate']


if __name__ == '__main__':
    engagements = list()
    csv_reader = csv.DictReader(open(INPUT_FILE_PATH))
    for record in csv_reader:
        record['timestamp_int'] = int(datetime.strptime(
            record['timestamp'], '%Y-%m-%d %H:%M:%S'
        ).timestamp())
        engagements.append(record)
    ordered_engagements = sorted(engagements, key=itemgetter('timestamp_int'))
    campaigns = {
        'campaign_id': {
            'date_time': 0,
            'delivered': 0,
            'engagements': 0,
            'engagement_rate': 0.0
        }
    }
    campaigns = dict()
    for event_log in ordered_engagements:
        campaign_id = event_log['campaign_id']
        if campaign_id not in campaigns:
            date_time = event_log['timestamp']
            campaigns[campaign_id] = {
                'date_time': date_time,
                'delivered': 0,
                'engagements': 0
            }
        event = event_log['event']
        if event == 'delivered':
            campaigns[campaign_id]['delivered'] += 1
        elif event in ['open', 'click', 'reply', 'survey completed']:
            campaigns[campaign_id]['engagements'] += 1
    campaigns_report = list()
    for campaign_id, campaign in campaigns.items():
        engagement_rate = 0.0
        if campaign['delivered'] > 0:
            engagement_rate = campaign['engagements'] / campaign['delivered']
        report = {
            'Date': campaign['date_time'],
            'campaign_id': campaign_id,
            'engagement_rate': engagement_rate
        }
        campaigns_report.append(report)
    # for report in campaigns_report:
    #     print(
    #         report['Date'],
    #         report['campaign_id'],
    #         report['engagement_rate'],
    #         campaigns[report['campaign_id']]['delivered'],
    #         campaigns[report['campaign_id']]['engagements']
    #     )
    csv_writer = csv.DictWriter(
        open(OUTPUT_FILE_PATH, 'w'),
        fieldnames=HEADERS
    )
    csv_writer.writeheader()
    csv_writer.writerows(campaigns_report)
