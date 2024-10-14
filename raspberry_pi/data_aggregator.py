import json

def format_header(title):
    return f"{'=' * 40}\n{title.center(40)}\n{'=' * 40}\n"

def format_footer(footer):
    return f"\n{'=' * 40}\n{footer.center(40)}\n{'=' * 40}\n"

def format_section(title, content):
    return f"\n{title}\n{'-' * len(title)}\n{content}\n"

def format_table(data):
    headers = data[0].keys()
    rows = [list(item.values()) for item in data]
    table = ' | '.join(headers) + '\n' + '-' * (len(headers) * 3 + len(headers) - 1) + '\n'
    for row in rows:
        table += ' | '.join(map(str, row)) + '\n'
    return table

def format_bullet_points(points):
    return '\n'.join([f"- {point}" for point in points])

def format_json_to_ascii(json_data):
    formatted_output = ""
    
    if 'header' in json_data:
        formatted_output += format_header(json_data['header'])
    
    if 'sections' in json_data:
        for section in json_data['sections']:
            formatted_output += format_section(section['title'], section['content'])
    
    if 'table' in json_data:
        formatted_output += format_section("Table", format_table(json_data['table']))
    
    if 'bullet_points' in json_data:
        formatted_output += format_section("Bullet Points", format_bullet_points(json_data['bullet_points']))
    
    if 'footer' in json_data:
        formatted_output += format_footer(json_data['footer'])
    
    return formatted_output

if __name__ == "__main__":
    example_json = '''
    {
        "header": "Intelligence Briefing",
        "sections": [
            {"title": "Introduction", "content": "This is the introduction section."},
            {"title": "Summary", "content": "This is the summary section."}
        ],
        "table": [
            {"Name": "Alice", "Age": 30, "Occupation": "Engineer"},
            {"Name": "Bob", "Age": 25, "Occupation": "Designer"}
        ],
        "bullet_points": ["Point 1", "Point 2", "Point 3"],
        "footer": "End of Briefing"
    }
    '''
    
    json_data = json.loads(example_json)
    print(format_json_to_ascii(json_data))