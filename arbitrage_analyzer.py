def analyze_arbitrage(options_data, ticker, current_price):
    """
    Analyze options data for arbitrage opportunities.
    
    Args:
        options_data (list): List of option contracts with their prices and details
        ticker (str): The stock ticker symbol
        current_price (float): Current price of the underlying stock
    """
    print(f"\n{'='*80}")
    print(f"ARBITRAGE ANALYSIS FOR {ticker} (Current Price: ${current_price:.2f})")
    print(f"{'='*80}")
    
    # Group options by expiry date
    options_by_expiry = {}
    for option in options_data:
        expiry = option['expiry_date']
        if expiry not in options_by_expiry:
            options_by_expiry[expiry] = {'calls': [], 'puts': []}
        
        if option['type'] == 'call':
            options_by_expiry[expiry]['calls'].append(option)
        else:
            options_by_expiry[expiry]['puts'].append(option)
    
    # Track opportunity numbers
    opportunity_count = 1
    
    # Analyze each expiry date
    for expiry, options in options_by_expiry.items():
        print(f"\n{'-'*80}")
        print(f"EXPIRY DATE: {expiry}")
        print(f"{'-'*80}")
        
        # Sort options by strike price
        calls = sorted(options['calls'], key=lambda x: x['strike'])
        puts = sorted(options['puts'], key=lambda x: x['strike'])
        
        # Check for put-call parity violations
        print("\nPUT-CALL PARITY VIOLATIONS:")
        print("-" * 40)
        for call in calls:
            # Find corresponding put with same strike
            matching_put = next((put for put in puts if put['strike'] == call['strike']), None)
            if matching_put and call['lastPrice'] > 0 and matching_put['lastPrice'] > 0:
                # Put-call parity: C - P = S - K*e^(-rT)
                # For simplicity, we'll use a basic check: C - P ≈ S - K
                theoretical_diff = current_price - call['strike']
                actual_diff = call['lastPrice'] - matching_put['lastPrice']
                
                # If the difference is significant (more than 5% of the stock price)
                if abs(theoretical_diff - actual_diff) > current_price * 0.05:
                    print(f"\nOpportunity #{opportunity_count}")
                    print(f"Type: Put-Call Parity Violation")
                    print(f"Strike: ${call['strike']:.2f}")
                    print(f"Call price: ${call['lastPrice']:.2f}")
                    print(f"Put price: ${matching_put['lastPrice']:.2f}")
                    print(f"Theoretical difference: ${theoretical_diff:.2f}")
                    print(f"Actual difference: ${actual_diff:.2f}")
                    print(f"Potential profit: ${abs(theoretical_diff - actual_diff):.2f}")
                    opportunity_count += 1
        
        # Check for box spreads
        print("\nBOX SPREAD OPPORTUNITIES:")
        print("-" * 40)
        for i in range(len(calls) - 1):
            for j in range(i + 1, len(calls)):
                lower_call = calls[i]
                higher_call = calls[j]
                
                # Find corresponding puts
                lower_put = next((put for put in puts if put['strike'] == lower_call['strike']), None)
                higher_put = next((put for put in puts if put['strike'] == higher_call['strike']), None)
                
                # Only proceed if all options have non-zero prices
                if (lower_put and higher_put and 
                    lower_call['lastPrice'] > 0 and higher_call['lastPrice'] > 0 and
                    lower_put['lastPrice'] > 0 and higher_put['lastPrice'] > 0):
                    
                    # Box spread: Buy lower call, sell higher call, buy higher put, sell lower put
                    cost = (lower_call['lastPrice'] + higher_put['lastPrice']) - (higher_call['lastPrice'] + lower_put['lastPrice'])
                    profit = higher_call['strike'] - lower_call['strike']
                    
                    # Only show opportunities with significant profit potential (>1% of the spread)
                    min_profit_threshold = profit * 0.01
                    if cost < profit and (profit - cost) > min_profit_threshold:
                        print(f"\nOpportunity #{opportunity_count}")
                        print(f"Type: Box Spread")
                        print(f"Lower strike: ${lower_call['strike']:.2f}")
                        print(f"Higher strike: ${higher_call['strike']:.2f}")
                        print(f"Cost: ${cost:.2f}")
                        print(f"Guaranteed profit: ${profit:.2f}")
                        print(f"Net profit: ${(profit - cost):.2f}")
                        if cost != 0:
                            print(f"Return on investment: {((profit - cost) / abs(cost) * 100):.2f}%")
                        opportunity_count += 1
        
        # Check for butterfly spreads
        print("\nBUTTERFLY SPREAD OPPORTUNITIES:")
        print("-" * 40)
        for i in range(len(calls) - 2):
            lower_call = calls[i]
            middle_call = calls[i + 1]
            higher_call = calls[i + 2]
            
            # Only proceed if all options have non-zero prices
            if (lower_call['lastPrice'] > 0 and 
                middle_call['lastPrice'] > 0 and 
                higher_call['lastPrice'] > 0):
                
                # Butterfly spread: Buy lower call, sell 2 middle calls, buy higher call
                cost = (lower_call['lastPrice'] - 2 * middle_call['lastPrice'] + higher_call['lastPrice'])
                
                # Only show opportunities with significant profit potential (>1% of the spread)
                spread_width = higher_call['strike'] - lower_call['strike']
                min_profit_threshold = spread_width * 0.01
                
                if cost < 0 and abs(cost) > min_profit_threshold:
                    print(f"\nOpportunity #{opportunity_count}")
                    print(f"Type: Butterfly Spread")
                    print(f"Lower strike: ${lower_call['strike']:.2f}")
                    print(f"Middle strike: ${middle_call['strike']:.2f}")
                    print(f"Higher strike: ${higher_call['strike']:.2f}")
                    print(f"Cost: ${cost:.2f}")
                    print(f"Maximum profit: ${abs(cost):.2f}")
                    initial_cost = lower_call['lastPrice'] + higher_call['lastPrice']
                    if initial_cost > 0:
                        print(f"Return on investment: {(abs(cost) / initial_cost * 100):.2f}%")
                    opportunity_count += 1
    
    print(f"\n{'-'*80}")
    print(f"ANALYSIS COMPLETE - Found {opportunity_count-1} potential opportunities")
    print(f"{'-'*80}\n") 