    #if time_value == '1mo':
    period = 60
    
    data_ts, meta_data_ts = ts.get_intraday(symbol=ticker, interval='1min', outputsize='full')
    data_ti, meta_data_ti = ti.get_rsi(symbol=ticker, interval='1min', time_period=period)
    df = data_ts[0]

    df.index = pd.Index(map(lambda x: str(x)[:-3], df.index))

    df2 = data_ti

    total_df = pd.concat([df, df2], axis=1, sort=True)

    cols = total_df.columns.drop("Date")
    total_df[cols] = total_df[cols].apply(pd.to_numeric)

    #Break down dataframes
    openList = []
    for o in total_df['1. open']:
        openList.append(float (o))
    highList = []
    for h in total_df['2. high']:
        highList.append(float (h))
    lowList = []
    for l in total_df['3. low']:
        lowList.append(float (l))
    closeList = []
    for c in total_df['4. close']:
        closeList.append(float (c))
    
    rsi_offset = []
    
    #zip two lists together ('RSI' column from ti and 'low' column)
    # for each value 'r' from RSI and 'l' from low, append to new list
    for r, l in zip(total_df['RSI'], lowList):
        rsi_offset.append(l - (l / r))
    
    #scatter plot for buy / sell / color coding part.
    scatter = pgo.Scatter(

    )
    #actual fig
    mainGraph = pgo.Candlestick(
        x = total_df.index,
        open = openList,
        high = highList,
        low = lowList,
        close = closeList,
        increasing={'line': {'color': '#00CC94'}},
        decreasing={'line': {'color': '#F50030'}},            
        name = 'candlestick'
    )
    data = [mainGraph]

    layout = pgo.Layout(
        paper_bgcolor='#27293d',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        xaxis = dict(type='category'),
        yaxis = dict(range=[min(rsi_offset), max(highList)]),
        font = dict(color='white'),
    )

    return {'data': data, 'layout': layout}