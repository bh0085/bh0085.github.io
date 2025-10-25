#!/usr/bin/env python3
"""
Fetch Gantt Chart data from Notion and export to JSON

Called by .github/workflows/update-gantt.yml daily at midnight UTC.
Reads NOTION_API_KEY from environment variable (GitHub secret).
Outputs gantt_data.json which is used by gantt.html and index.html.
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path

# Configuration
NOTION_API_KEY = os.getenv('NOTION_API_KEY')
DATABASE_ID = '291cdd12fc5e81ceafeadc78e6c03258'
OUTPUT_FILE = 'gantt_data.json'

def fetch_notion_database(database_id, api_key):
    """Fetch all pages from a Notion database"""
    url = f'https://api.notion.com/v1/databases/{database_id}/query'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json'
    }
    
    all_results = []
    has_more = True
    start_cursor = None
    
    while has_more:
        payload = {}
        if start_cursor:
            payload['start_cursor'] = start_cursor
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        
        all_results.extend(data['results'])
        has_more = data.get('has_more', False)
        start_cursor = data.get('next_cursor')
    
    return all_results

def extract_property_value(prop):
    """Extract value from Notion property based on type"""
    if not prop or 'type' not in prop:
        return None
    
    prop_type = prop['type']
    
    if prop_type == 'title':
        return ''.join([t['plain_text'] for t in prop['title']])
    elif prop_type == 'rich_text':
        return ''.join([t['plain_text'] for t in prop['rich_text']])
    elif prop_type == 'select' and prop['select']:
        return prop['select']['name']
    elif prop_type == 'multi_select':
        return [item['name'] for item in prop['multi_select']]
    elif prop_type == 'date' and prop['date']:
        return {
            'start': prop['date']['start'],
            'end': prop['date'].get('end')
        }
    elif prop_type == 'number':
        return prop['number']
    elif prop_type == 'status' and prop['status']:
        return prop['status']['name']
    elif prop_type == 'relation':
        return [rel['id'] for rel in prop['relation']]
    else:
        return None

def transform_to_gantt_format(notion_pages):
    """Transform Notion database pages to simplified Gantt format"""
    tasks = []
    
    for page in notion_pages:
        props = page['properties']
        
        task = {
            'id': page['id'],
            'name': extract_property_value(props.get('Task/Project Name', {})),
            'category': extract_property_value(props.get('Category', {})),
            'start_date': extract_property_value(props.get('Start Date', {})),
            'end_date': extract_property_value(props.get('End Date', {})),
            'status': extract_property_value(props.get('Status', {})),
            'priority': extract_property_value(props.get('Priority', {})),
            'assigned_to': extract_property_value(props.get('Assigned To', {})),
            'progress': extract_property_value(props.get('Progress', {})),
            'dependencies': extract_property_value(props.get('Dependencies', {})),
            'tags': extract_property_value(props.get('Tags', {})),
            'budget_cost': extract_property_value(props.get('Budget/Cost', {})),
            'one_time_cost': extract_property_value(props.get('One-Time Cost', {})),
            'monthly_cost': extract_property_value(props.get('Monthly Cost', {})),
            'blocked_by': extract_property_value(props.get('Blocked by', {})),
            'blocking': extract_property_value(props.get('Blocking', {})),
        }
        
        if task['start_date']:
            task['start_date'] = task['start_date']['start']
        if task['end_date']:
            task['end_date'] = task['end_date']['start']
        
        tasks.append(task)
    
    return tasks

def main():
    if not NOTION_API_KEY:
        print("ERROR: NOTION_API_KEY environment variable not set")
        print("\nTo set it up:")
        print("1. Go to https://www.notion.so/my-integrations")
        print("2. Create a new integration")
        print("3. Copy the 'Internal Integration Token'")
        print("4. Share your Gantt Chart database with the integration")
        print("5. Export the key: export NOTION_API_KEY='your-key-here'")
        return
    
    print(f"Fetching Gantt Chart data from Notion database {DATABASE_ID}...")
    pages = fetch_notion_database(DATABASE_ID, NOTION_API_KEY)
    print(f"Found {len(pages)} tasks")
    
    print("Transforming to Gantt format...")
    tasks = transform_to_gantt_format(pages)
    
    output_data = {
        'exported_at': datetime.now().isoformat(),
        'database_id': DATABASE_ID,
        'task_count': len(tasks),
        'tasks': tasks
    }
    
    print(f"Writing to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"✓ Successfully exported {len(tasks)} tasks to {OUTPUT_FILE}")
    
    stats_by_category = {}
    for task in tasks:
        cat = task.get('category') or 'Uncategorized'
        stats_by_category[cat] = stats_by_category.get(cat, 0) + 1
    
    print("\nTasks by category:")
    for cat, count in sorted(stats_by_category.items()):
        print(f"  {cat}: {count}")

if __name__ == '__main__':
    main()

