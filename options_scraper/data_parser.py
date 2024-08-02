def parse_options_table(table):
    rows = table.find_all('tr')[1:]  # Skip the header row
    options = []
    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 9:
            continue
        options.append({
            'contract_name': cols[0].text.strip(),
            'strike': float(cols[2].text.strip().replace(',', '')),
            'last_price': float(cols[3].text.strip().replace(',', '')),
            'bid': float(cols[4].text.strip().replace(',', '')),
            'ask': float(cols[5].text.strip().replace(',', '')),
            'volume': int(cols[6].text.strip().replace(',', '').replace('-', '0')),
            'open_interest': int(cols[7].text.strip().replace(',', '').replace('-', '0')),
            'implied_volatility': float(cols[8].text.strip().replace('%', '').replace(',', ''))
        })
    return options
